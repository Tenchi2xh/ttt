from .blocks import to_block
from .io import load


def load_image(file: str, invert: bool):
    pixels, width, height = load(file)
    return to_block(pixels, x0=0, y0=0, width=width, height=height, invert=invert)
