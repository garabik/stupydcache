This is a simple on-disk cache for Python objects mimicking dict interface.

Sample usage:

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

