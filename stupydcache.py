#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os, zlib, pickle, base64, string, hashlib

# for 2/3 compatibility
try:
    unicode
except NameError:
    unicode = ()


def memoize(obj):
    "simple memoizing decorator, works on functions, methods, or classes"
    "inspired by https://wiki.python.org/moin/PythonDecoratorLibrary"

    cache = obj.cache = {}
    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
           cache[key] = obj(*args, **kwargs)
           return cache[key]
    return memoizer

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
        if isinstance(s, unicode): # for python3, it gives False, because unicode==()
            s = s.encode('utf-8')  # but for python2, we have to use string, not unicode string
        elif not isinstance(s, str):
            s = str(s)
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
        open(fname, 'wb').write(zlib.compress(p, 9))

    def __contains__(self, key):
        fname = self._fname(key)
        return os.path.exists(fname)

    def get(self, key, default=None):
        return self[key] if key in self else default

if __name__=='__main__':
    # test
    cache = Cache(cachedir='/tmp/testcache', name='TESTČ')
    k1 = u'kľúč1'
    v1 = [1,2,3,4,5, 'šesť', b'sedem', {1,2,3}]
    cache[k1] = v1
    assert k1 in cache
    assert cache[k1] == v1
    k2 = 123.45
    v2 = 10
    cache[k2] = v2
    assert k2 in cache
    assert cache[k2] == v2

    print(cache.get(k1,'ble'))
    print ('k2' in cache)
    print(cache['kľúč2']) # should fail with KeyError

