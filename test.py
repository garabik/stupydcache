#!/usr/bin/python3
# -*- coding: utf-8 -*-

from stupydcache import memoize, Cache

print('testing cache:')
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
try:
    print(cache['kľúč2']) # should fail with KeyError
except KeyError:
    pass

print('OK')

print('testing memoize:')

@memoize
def fib(n):
    print('Calculating fib({})'.format(n))
    if n<0:
        raise ValueError
    elif n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

for i in range(10):
    print(i, fib(i))



