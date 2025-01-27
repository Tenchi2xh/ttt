from typing import Tuple
import numpy as np

from .blocks import int_to_block
from ..core import term
from ..core.colors import unsort_indices


def blit(blocks: np.ndarray, offset: int=0, end: str="\n"):
    buffer = []
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)
    for line in blocks:
        buffer.append(padding + "".join(int_to_block[b] for b in line))
    print("\n".join(buffer), end=end)


def blit_colors(blocks: np.ndarray, colors: np.ndarray, offset: int=0, end: str="\n"):
    height, width = blocks.shape
    buffer = []
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)
    for j in range(height):
        buffer.append(
            padding
            + "".join(
                term.colors_raw(fix_colors(colors[j, i])) + int_to_block[blocks[j, i]]
                for i in range(width)
            )
            + term.RESET
        )
    print("\n".join(buffer), end=end)


def fix_colors(colors: Tuple[int, int]):
    return unsort_indices[colors[0]], unsort_indices[colors[1]]
