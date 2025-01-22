from typing import Sequence
from .blocks import int_to_block, int_to_block_inverse


def blit(blocks: Sequence[Sequence[int]], offset: int=0, end: str="\n"):
    buffer = []
    padding = " " * offset
    for line in blocks:
        buffer.append(padding + "".join(int_to_block[b] for b in line))
    print("\n".join(buffer), end=end)
