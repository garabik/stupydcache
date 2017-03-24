This is a simple on-disk cache for Python objects mimicking dict interface.

Sample usage:

# Cache

If you have a program that takes some input data (let's say from data files), makes computationally or I/O intense
operations on them and then continues:

    r = read_and_process_data(datafile)
    #... do stuff with r

and the data changes infrequently, you can use the stupydcache module to cache the result:

    from stupydcache import Cache
    cache = Cache()
    if datafile in cache:
        r = cache[datafile]
    else:
        r = read_and_process_data(datafile)
        cache[datafile] = r

cache is persistent on disk, the next invocation of the program will use the cached values.


# memoize

The module provides one decorator, `memoize`. You can use it to decorate a
function, each call to the function will go through the cache, the key will be
constructed from the arguments and function name. Each subsequent call with the same arguments will use the cached value.

You can provide a cache directory and/or a cache name:

    from stupydcache import memoize

    @memoize(cachedir='/tmp/cachedir', cachename='mycache')
    def fun(*args):
        ...
        return result

Or as a shorcut, use it without arguments (as a decorator, `@memoize` is equivalent to `@memoize()`):

    from stupydcache import memoize

    @memoize
    def fun(*args):
        ...
        return result


