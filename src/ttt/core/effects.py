from enum import StrEnum, auto
from typing import Callable


class OutlineMode(StrEnum):
    none = auto()
    soft = auto()
    hard = auto()


def draw_with_outline(mode: OutlineMode, x: int, y: int, draw: Callable[[int, int, int], None]):
    fill = 255 if mode == OutlineMode.none else 0

    if mode in (OutlineMode.soft, OutlineMode.hard):
        draw(x - 1, y, 255)
        draw(x + 1, y, 255)
        draw(x, y - 1, 255)
        draw(x, y + 1, 255)

    if mode == OutlineMode.hard:
        draw(x - 1, y - 1, 255)
        draw(x + 1, y - 1, 255)
        draw(x - 1, y + 1, 255)
        draw(x + 1, y + 1, 255)

    draw(x, y, fill)
