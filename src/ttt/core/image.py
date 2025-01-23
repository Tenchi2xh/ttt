from PIL import Image
from .blocks import to_blocks_pil


def load(file: str):
    image = Image.open(file).convert("1", dither=Image.NONE)
    width, height = image.size
    return image, width, height


def load_image(file: str, invert: bool):
    image, width, height = load(file)
    return to_blocks_pil(image, x0=0, y0=0, width=width, height=height, invert=invert)
