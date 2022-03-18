import logging
from functools import wraps
import time

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def watch(func):
    # Good idea is to launch time calculation only if the service is in debug mode
    @wraps(func)
    def wrapper():
        t0 = time.time()
        result = func()
        LOGGER.debug(f'The function  takes {time.time() - t0}')
        return result
    return wrapper


@watch
def slow_function() -> None:
    time.sleep(3)


@watch
def fast_function() -> None:
    time.sleep(1)


if __name__ == '__main__':
    slow_function()
    fast_function()
