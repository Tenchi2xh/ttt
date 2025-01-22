from contextlib import contextmanager
import time
from typing import Callable


@contextmanager
def callback_timer(callback: Callable, *args):
    start = time.time()
    try:
        yield
    finally:
        callback(1000 * (time.time() - start), *args)


@contextmanager
def noop(_, __):
    yield


def get_callback_timer(enable: bool=True):
    if enable:
        return callback_timer
    return noop
