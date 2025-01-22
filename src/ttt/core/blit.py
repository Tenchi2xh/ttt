from typing import Sequence

from .blocks import int_to_block
from ..core import term


def blit(blocks: Sequence[Sequence[int]], offset: int=0, end: str="\n"):
    buffer = []
    padding = "" if offset == 0 else term.move_cursor_right_raw(offset)
    for line in blocks:
        buffer.append(padding + "".join(int_to_block[b] for b in line))
    print("\n".join(buffer), end=end)
