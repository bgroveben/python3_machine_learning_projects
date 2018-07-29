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
        @functools.wraps(func)

    def _timeit(*args, **kwargs):
        # Suspend garbage collection so that times can be compared.
        gcold = gc.isenabled()
        gc.disable()

        try:
            trials = []
            for _ in _repeat(number):
                start = _timer()
                result = func(*args, **kwargs)
                end = _timer()
                total += end - start
            trials.append(total)

            # Now we are looking for the average time from the best trial according to Pythons timeit module.
            best = min(trials) / number
            print('Best of {} trials with {} function'
                  ' calls per trial: '.format(repeat, number))
            print('Function `{}` ran in average'
                  ' of {:0.3f} seconds.'.format(func.__name__, best),
                  end='\n\n', file=file)

        finally:
            if gcold:
                gc.enable()
        # Result is returned only once
        return result
    return _timeit
# Syntax trick from Python's @dataclass
if _func is None:
    return wrap
else:
    return wrap(_func)
