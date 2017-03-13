from src.core.utils import Vector2
from random import random


def randscalar():
    # between -5 and 5
    return -5 + 10 * random()


def randtuple():
    return (randscalar(), randscalar())


def randvec():
    return Vector2(randscalar(), randscalar())


def repeat(times=10):
    def decorate(test_func):
        def new_test_func(*args, **kwargs):
            for _ in range(times):
                test_func(*args, **kwargs)
        return new_test_func
    return decorate
