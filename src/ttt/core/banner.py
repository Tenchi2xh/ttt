from typing import Optional, override

import PIL

from .engine import Renderable
from ..resources import get_pattern


class Banner(Renderable):
    def __init__(self, pattern_name: str):
        self.pattern = get_pattern(pattern_name)

    @override
    def to_image(self, available_width: int, lines: Optional[int], repeat: Optional[int]):
        width = available_width

        if lines is None:
            height = self.pattern.height
        else:
            height = lines * 4

        if repeat is not None:
            height = self.pattern.height * repeat

        image = PIL.Image.new("1", (width, height), 0)

        pattern_width, pattern_height = self.pattern.size

        for x in range(0, width, pattern_width):
            for y in range(0, height, pattern_height):
                image.paste(self.pattern, (x, y))

        return image
