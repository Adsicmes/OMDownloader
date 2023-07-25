import functools
import itertools
import time

from loguru import logger


def retry(delays=(3, 3, 3), exceptions=(Exception,), except_exceptions=(None,)):
    def wrapper(function):
        @functools.wraps(function)
        def wrapped(*args, **kwargs):
            problems = []
            for delay in itertools.chain(delays, [None]):
                try:
                    return function(*args, **kwargs)
                except exceptions as problem:
                    if isinstance(problem, except_exceptions):
                        raise problem

                    problems.append(problem)
                    if delay is None:
                        logger.error(f"Function {function.__name__} failed after {len(delays)} retries. "
                                     f"Exceptions: {problems}")
                        raise
                    else:
                        logger.warning(f"Function {function.__name__} fails of {type(problem).__name__}({problem}). "
                                       f"Will retry in {delay} second(s).")
                        time.sleep(delay)

        return wrapped

    return wrapper
