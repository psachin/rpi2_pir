import logging

from functools import wraps, partial
from os import environ



fh = logging.FileHandler('debug.log')
fh.setLevel(logging.DEBUG)


def debug(func=None, prefix=''):
    if func is None:
        # if func wasn't passed
        return partial(debug5, prefix=prefix)
    if 'DEBUG' not in environ:
        return func
    logger = logging.getLogger(func.__module__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    msg = prefix + func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        logger.debug("{}{}={}".format(msg,
                                      args,
                                      func(*args, **kwargs)))
        return func(*args, **kwargs)
    return wrapper


def debugmethods(cls):
    '''cls is class

    class decorators does not work with classmethods and static
    methods?

    '''
    for key, value in vars(cls).items():
        if callable(value):     # True if value is a function
            setattr(cls, key, debug(value))
    return cls


class DebugMeta(type):
    '''
    Usage:
    import DebugMeta


    class Example(metaclass=DebugMeta):
        def yoda(self):
            ...
    '''
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname,
                                 bases, clsdict)
        clsobj = debugmethods(clsobj)
        return clsobj
