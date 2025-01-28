from typing import override

import PIL

from .engine import Renderable


class Image(Renderable):
    def __init__(self, file: str):
        self.image = PIL.Image.open(file).convert("1", dither=PIL.Image.NONE)

    @override
    def to_image(self, available_width: int):
        return self.image
