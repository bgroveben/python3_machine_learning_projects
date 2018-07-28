import functools
import gc
import itertools
import sys
from timeit import default_timer as _timer


def timeit(_func=None, *, repeat=3, number=1000, file=sys.stdout):
    """
    Decorator that prints time from the best of the `repeat` trials.
    Mimics `timeit.repeat()` and then prints out the average time.
    Returns the function result and prints time.
    Like Python's @dataclass decorator, this will work with or without parentheses.
    Any kwargs are passed to `print()`.

    ...
    >>>
    @timeit
    def f():
        return "-".join(str(n) for n in range(100))
    >>>
    >>>
    @timeit(number=100000)
    def g():
        return "-".join(str(n) for n in range(10))
    >>>
    ...
    """

_repeat = functools.partial(itertools.repeat, None)

def wrap(func):
    pass
