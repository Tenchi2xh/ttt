from .blocks import to_block_pil
from .io import load


def load_image(file: str, invert: bool):
    image, width, height = load(file)
    return to_block_pil(image, x0=0, y0=0, width=width, height=height, invert=invert)
