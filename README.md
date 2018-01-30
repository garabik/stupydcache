This is a simple on-disk compressed cache for Python objects mimicking dict interface.

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
constructed from the arguments and the function name. Each subsequent call with
the same arguments will use the cached value.  Since each cache entry is a
separate file, do not use it when you call the functions with many (as in,
many thousands) different combinations of their arguments.

You can provide a cache directory and/or a cache name:

    from stupydcache import memoize

    @memoize(cachedir='/tmp/cachedir', cachename='mycache')
    def fun(*args):
        ...
        return result

Or as a shortcut, use it without arguments (as a decorator, `@memoize` is equivalent to `@memoize()`):

    from stupydcache import memoize

    @memoize
    def fun(*args):
        ...
        return result

## Caching into RAM

If you use a dictionary as a cachedir, the caching will be done in RAM, using
that dictionary, using function arguments as the dictionary keys. However, you
run into issues - if the function arguments are unhashable, the decorator will
raise an exception. Use with care.

Do not reuse the same dictionary for different functions - only the arguments are used as the keys, not the function name.

Example:
    from stupydcache import memoize

    cache_dict = {}
    @memoize(cache_dict)
    def fun(*args):
        ...
        return result


