from PIL import Image

from .blocks import to_blocks_pil


def render_pattern(pattern: Image, width: int, height: int, invert: bool=False):
    image = Image.new("1", (width, height), 0)
    pattern_width, pattern_height = pattern.size

    for x in range(0, width, pattern_width):
        for y in range(0, height, pattern_height):
            image.paste(pattern, (x, y))

    return to_blocks_pil(image, x0=0, y0=0, width=width, height=height, invert=invert)