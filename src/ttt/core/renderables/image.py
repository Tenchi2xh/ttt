from typing import override

import PIL
from PIL.Image import Image as PILImage

from ..engine import Renderable


class Image(Renderable):
    def __init__(self, file: str | PILImage):
        if isinstance(file, str):
            self.image = PIL.Image.open(file).convert("1", dither=PIL.Image.NONE)
        else:
            self.image = file

    @override
    def to_image(self, available_width: int):
        return self.image
