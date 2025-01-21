from typing import Sequence
from .blocks import int_to_block, int_to_block_inverse


def blit(blocks: Sequence[Sequence[int]], invert: bool):
    map = int_to_block_inverse if invert else int_to_block
    buffer = ""
    for line in blocks:
        buffer += "".join(map[b] for b in line) + "\n"
    print(buffer)
