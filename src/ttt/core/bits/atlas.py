from typing import override

from .util import load_image

from ..engine import RasterBit, Canvas


class Atlas(RasterBit):
    def __init__(
        self,
        file: str,
        sprite_width: int,
        sprite_height: int,
        offset_x: int,
        offset_y: int,
        gap_x: int,
        gap_y: int,
        index: int
    ):
        image = load_image(file)

        width, height = image.size

        sprites_per_row = (gap_x + width  - 2 * offset_x) // (sprite_width  + gap_x)
        sprites_per_col = (gap_y + height - 2 * offset_y) // (sprite_height + gap_y)

        self.total_sprites = sprites_per_row * sprites_per_col

        row = index // sprites_per_row
        column = index % sprites_per_row

        x0 = offset_x + column * (sprite_width  + gap_x)
        y0 = offset_y + row    * (sprite_height + gap_y)

        self.image = image.crop((x0, y0, x0 + sprite_width, y0 + sprite_height))

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        return Canvas(self.image)
