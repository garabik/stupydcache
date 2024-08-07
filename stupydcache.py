#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os, sys, zlib, pickle, base64, string, hashlib, random, functools

# for 2/3 compatibility
try:
    unicode
except NameError:
    # this happens in python3
    unicode = ()

def debug(*x):
    print(*x, file=sys.stderr)

def smart_str(obj):
    "smart version of str(), works in both python2/3, regardless of whether obj is an unicode or a string or bytes"
    if isinstance(obj, unicode): # for python3, it gives False, because unicode==()
        s = obj.encode('utf-8')  # but for python2, we have to use a string, not unicode string
    elif not isinstance(obj, str):
        s = str(obj)
    else: # obj is already a string
        s = obj
    return s

class Cache:
    "general on-disk cache"
    def __init__(self, cachedir='cache', name=''):
        if os.path.exists(cachedir) and not os.path.isdir(cachedir):
            raise IOError('File {} exists but is not a directory'.format(cachedir))
        if not os.path.exists(cachedir):
            os.makedirs(cachedir)
        self.cachedir = cachedir
        # name is used to distinguish between several caches using the same directory
        self.name = name

    def _to_safe(self, s):
        "helper function to extract only filesystem-safe character from a string"
        s = smart_str(s)
        return ''.join(x for x in s if x in string.ascii_letters+string.digits)

    def _fname(self, key):
        # asckey is used as a human readable prefix of the on-disk files, to aid in debugging
        asckey = self._to_safe(key)
        key = repr(key)
        fname1 = asckey[:10]
        h = hashlib.md5((repr(self.name)+key).encode('utf-8', errors='replace'))
        hd = h.digest()
        fname2 = base64.urlsafe_b64encode(hd)
        fname2 = fname2.decode('ascii')
        fname = fname1 + fname2
        fname = os.path.join(self.cachedir, fname)
        return fname

    def __getitem__(self, key):
        fname = self._fname(key)
        if os.path.exists(fname):
            value = pickle.loads(zlib.decompress(open(fname, 'rb').read()))
            return value
        else:
            raise KeyError(key)

    def __setitem__(self, key, val):
        fname = self._fname(key)
        p = pickle.dumps(val)
        # trying to get some atomicity
        fname_tmp = fname+'.'+str(random.random())+'.tmp'
        open(fname_tmp, 'wb').write(zlib.compress(p, 9))
        os.rename(fname_tmp, fname)

    def __contains__(self, key):
        fname = self._fname(key)
        return os.path.exists(fname)

    def get(self, key, default=None):
        return self[key] if key in self else default

def memoize(func=None, cachedir='cache', cachename=None):
    "simple memoizing decorator, works on functions, methods, or classes"
    "inspired by https://wiki.python.org/moin/PythonDecoratorLibrary"


    def memoizer_decorator(obj):
        # try to minimize conflicts between different caches by constructing more or less unique name
        if cachename is None:
            if '__name__' in dir(obj):
                localcachename = obj.__name__
            else:
                localcachename = ''
            localcachename += str(type(obj))
        else:
            localcachename = cachename
 
        if isinstance(cachedir, dict):
            cache = cachedir
        elif isinstance(cachedir, str):
            cache = Cache(cachedir, localcachename)
        else:
            raise ValueError('Expecting directory path or dictionary')

        @functools.wraps(obj)
        def memoizer(*args, **kwargs):
            # kwargs keys are guaranteed to be strings, so we can sort the items to get deterministic order
            kwargs_hash = sorted(kwargs.items()) if kwargs else None
            key = (args, kwargs_hash)
            if key in cache:
                #print('cached', args, kwargs)
                val = cache[key]
            else:
                #print('unchached', args, kwargs)
                val = obj(*args, **kwargs)
                cache[key] = val
            return val
        return memoizer

    # if this is used as a decorator without arguments
    if func is not None and callable(func):
        return memoizer_decorator(func)

    return memoizer_decorator


if __name__=='__main__':
    pass

