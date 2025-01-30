import time
from typing import Callable
from contextlib import contextmanager


@contextmanager
def callback_timer(callback: Callable, *args):
    start = time.time()
    try:
        yield
    finally:
        callback(1000 * (time.time() - start), *args)
