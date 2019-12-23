import time
import logging
from functools import wraps


def logThis(filename=None, timed=True):
    """Decorator logging the method called, the arguments it was called with
    as well as the time it took it to execute in log file.

    Args:
        filename (string): Name of the log file.
        timed (bool, optional): If True measures execution time and logs it.

    Returns:
        func: The wrapped function.

    """

    def decorate(function):

        logname = filename if filename else 'logfile.log'
        log = logging.getLogger(logname)
        logging.basicConfig(filename=logname, level=logging.INFO)

        if timed is True:

            @wraps(function)
            def wrapper(*args, **kwargs):

                start = time.time()
                result = function(*args, **kwargs)
                end = time.time()
                duration = end - start

                log.log(logging.INFO, '{0} ran in {1:.4f} seconds with args: {2}, and kwargs: {3}'.format(
                    function.__name__, duration, args, kwargs))

                return result
        else:

            @wraps(function)
            def wrapper(*args, **kwargs):

                result = function(*args, **kwargs)

                log.log(logging.INFO,
                        '{0} ran with args: {1}, and kwargs: {2}'
                        .format(function.__name__, args, kwargs))

                return result

        return wrapper

    return decorate
