import atexit
import shutil
import sys
from contextlib import contextmanager


CSI = "\033["

FULL_SCREEN_ON = CSI + "?1049h"
FULL_SCREEN_OFF = CSI + "?1049l"
HIDE_CURSOR = CSI + "?25l"
SHOW_CURSOR = CSI + "?25h"
CLEAR_SCREEN = CSI + "2J"
INVERT = CSI + "7m"
RESET = CSI + "0m"


def clear_screen():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()


def move_cursor(x, y):
    sys.stdout.write(f"{CSI}{y + 1};{x + 1}H")
    sys.stdout.flush()


def move_cursor_up(amount):
    sys.stdout.write(f"{CSI}{amount}A")
    sys.stdout.flush()


def move_cursor_down(amount):
    sys.stdout.write(f"{CSI}{amount}B")
    sys.stdout.flush()


def move_cursor_right(amount):
    sys.stdout.write(f"{CSI}{amount}C")
    sys.stdout.flush()


def move_cursor_right_raw(amount):
    return f"{CSI}{amount}C"


def color_fg_raw(fg: int):
    return f"{CSI}38;5;{fg}m"


def color_bg_raw(bg: int):
    return f"{CSI}48;5;{bg}m"


def colors_raw(colors: tuple[int, int]):
    return f"{CSI}38;5;{colors[0]};48;5;{colors[1]}m"


def get_size():
    return shutil.get_terminal_size()


@contextmanager
def full_screen():
    sys.stdout.write(FULL_SCREEN_ON)
    sys.stdout.flush()
    try:
        yield
    finally:
        sys.stdout.write(FULL_SCREEN_OFF)
        sys.stdout.flush()


@contextmanager
def hide_cursor():
    atexit.register(lambda: sys.stdout.write(SHOW_CURSOR) or sys.stdout.flush())
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()
    try:
        yield
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()
