from typing import override
from ..engine import Renderable

from PIL import Image


class Blank(Renderable):
    @override
    def to_image(self, available_width: int, width: int, height: int):
        return Image.new("1", (width, height), 0)
