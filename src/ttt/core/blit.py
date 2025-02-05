import numpy as np

from ..core import term
from ..core.colors import unsort_indices
from .blocks import int_to_block, int_to_braille


def blit(
    blocks: np.ndarray,
    offset: int = 0,
    end: str = "\n",
    do_print: bool = True,
    braille: bool = False,
):
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)
    mapping = int_to_braille if braille else int_to_block

    buffer: list[str] = []
    for line in blocks:
        buffer.append(padding + "".join(mapping[b] for b in line))

    if do_print:
        print("\n".join(buffer), end=end)

    return buffer


def blit_colors(
    blocks: np.ndarray,
    colors: np.ndarray,
    offset: int = 0,
    end: str = "\n",
    braille: bool = False,
):
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)
    mapping = int_to_braille if braille else int_to_block

    height, width = blocks.shape
    buffer = []
    for j in range(height):
        line = padding
        prev_fg = prev_bg = None

        for i in range(width):
            fg, bg = fix_colors(colors[j, i])

            # The biggest bottlneck for printing fast is not
            # the amount of logic but the number of printed characters.
            # ANSI escape sequences add a lot of characters,
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

            line += color + mapping[blocks[j, i]]

        buffer.append(line + term.RESET)

    print("\n".join(buffer), end=end)


def fix_colors(colors: tuple[int, int]):
    return unsort_indices[colors[0]], unsort_indices[colors[1]]
