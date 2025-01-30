from typing import override

from PIL import Image as PILImage

from ..engine import Renderable


class Image(Renderable):
    def __init__(self, file: str | PILImage.Image):
        if isinstance(file, str):
            self.image = PILImage.open(file).convert("1", dither=PILImage.Dither.NONE)
        else:
            self.image = file

    @override
    def to_image(self, available_width: int): # type: ignore
        return self.image
