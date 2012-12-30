__author__ = 'Aaron Kaufman'

import functools


#re-implements modulo operator such that it always returns a positive remainder(used for wrapping)
def modu(num, divby):
    return (num % divby + abs(divby))%divby

#Stolen shamelessly from some other python library
def memo(func):
    cache = {}
    @ functools.wraps(func)
    def wrap(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrap
