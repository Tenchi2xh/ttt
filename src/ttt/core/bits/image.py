from typing import override

from PIL import Image as PILImage

from .util import load_image
from ..engine import RasterBit, Canvas


class Image(RasterBit):
    def __init__(self, file: str | PILImage.Image):
        if isinstance(file, str):
            self.image = load_image(file)
        else:
            self.image = file

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        return Canvas(self.image)
