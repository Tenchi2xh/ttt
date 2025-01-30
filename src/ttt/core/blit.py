from typing import List, Tuple
import numpy as np

from .blocks import int_to_block
from ..core import term
from ..core.colors import unsort_indices


def blit(blocks: np.ndarray, offset: int = 0, end: str = "\n", do_print: bool = True):
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)

    buffer: List[str] = []
    for line in blocks:
        buffer.append(padding + "".join(int_to_block[b] for b in line))

    if do_print:
        print("\n".join(buffer), end=end)

    return buffer


def blit_multiple(blocks_list: List[np.ndarray], gap: int=1):
    max_height = max(blocks.shape[0] for blocks in blocks_list)
    filler = 0

    def pad_bottom(blocks):
        return np.pad(blocks, ((0, max_height - blocks.shape[0]), (0, 0)), mode="constant", constant_values=filler)

    padded_blocks = [pad_bottom(block) for block in blocks_list]
    gap_array = np.full((max_height, gap), filler)

    result = []
    for i, block in enumerate(padded_blocks):
        result.append(block)
        if i < len(padded_blocks) - 1:
            result.append(gap_array)

    flat = np.concatenate(result, axis=1)
    blit(flat)


def blit_colors(blocks: np.ndarray, colors: np.ndarray, offset: int=0, end: str="\n"):
    height, width = blocks.shape

    buffer = []
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)

    for j in range(height):
        line = padding
        prev_fg = prev_bg = None

        for i in range(width):
            fg, bg = fix_colors(colors[j, i])

            # The biggest bottlneck for printing fast is not the amount of logic but
            # the number of printed characters. ANSI escape sequences add a lot of characters,
            # so let's only add them when necessary.
            color = ""
            if (fg, bg) != (prev_fg, prev_bg):
                if fg == prev_fg:
                    color = term.color_bg_raw(bg)
                elif bg == prev_bg:
                    color = term.color_fg_raw(fg)
                else:
                    color = term.colors_raw((fg, bg))
                prev_fg, prev_bg = fg, bg

            line += color + int_to_block[blocks[j, i]]

        buffer.append(line + term.RESET)

    print("\n".join(buffer), end=end)


def fix_colors(colors: Tuple[int, int]):
    return unsort_indices[colors[0]], unsort_indices[colors[1]]
