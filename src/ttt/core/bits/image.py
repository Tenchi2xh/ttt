from typing import override

from PIL import Image as PILImage

from ..engine import Canvas, RasterBit
from .util import load_image


class Image(RasterBit):
    def __init__(self, file: str | PILImage.Image):
        if isinstance(file, str):
            self.image = load_image(file)
        else:
            self.image = file

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        return Canvas(self.image)
