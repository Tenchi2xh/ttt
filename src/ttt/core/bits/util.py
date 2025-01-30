from functools import cache

from PIL import Image


@cache
def load_image(file: str):
    return Image.open(file).convert("1", dither=Image.Dither.NONE)
