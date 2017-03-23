#!/usr/bin/python3


import os, zlib, pickle, base64, string, hashlib


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
        return ''.join(x for x in s if x in string.ascii_letters+string.digits)

    def _fname(self, key):
        # asckey is used as a human readable prefix of the on-disk files, to aid in debugging
        asckey = self._to_safe(str(key))
        key = repr(key)
        fname1 = asckey[:10]
        h = hashlib.md5((self.name+key).encode('utf-8', errors='replace'))
        hd = h.digest()
        fname2 = base64.urlsafe_b64encode(hd)
        fname2 = str(fname2, 'ascii')
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
    cache = Cache(cachedir='/tmp/testcache', name='TEST')
    k1 = 'kľúč1'
    v1 = [1,2,3,4,5, 'šesť', b'sedem', {1,2,3}]
    cache[k1] = v1
    assert k1 in cache
    assert cache[k1] == v1
    print(cache.get(k1,'ble'))
    print ('k2' in cache)
    print(cache['kľúč2']) # should fail with KeyError

