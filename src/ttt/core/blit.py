from typing import Sequence
from .blocks import int_to_block, int_to_block_inverse


def blit(blocks: Sequence[Sequence[int]]):
    buffer = ""
    for line in blocks:
        buffer += "".join(int_to_block[b] for b in line) + "\n"
    print(buffer)
