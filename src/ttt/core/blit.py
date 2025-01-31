import numpy as np

from ..core import term
from ..core.colors import unsort_indices
from .blocks import int_to_block


def blit(blocks: np.ndarray, offset: int = 0, end: str = "\n", do_print: bool = True):
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)

    buffer: list[str] = []
    for line in blocks:
        buffer.append(padding + "".join(int_to_block[b] for b in line))

    if do_print:
        print("\n".join(buffer), end=end)

    return buffer


def blit_colors(
    blocks: np.ndarray, colors: np.ndarray, offset: int = 0, end: str = "\n"
):
    height, width = blocks.shape

    buffer = []
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)

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

            line += color + int_to_block[blocks[j, i]]

        buffer.append(line + term.RESET)

    print("\n".join(buffer), end=end)


def fix_colors(colors: tuple[int, int]):
    return unsort_indices[colors[0]], unsort_indices[colors[1]]
