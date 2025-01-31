import time
from contextlib import contextmanager
from typing import Callable


@contextmanager
def callback_timer(callback: Callable, *args):
    start = time.time()
    try:
        yield
    finally:
        callback(1000 * (time.time() - start), *args)
