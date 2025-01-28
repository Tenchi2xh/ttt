from typing import override

import PIL

from ..engine import Renderable


class Atlas(Renderable):
    def __init__(self, file: str, sprite_width: int, sprite_height: int, offset_x: int, offset_y: int, gap_x: int, gap_y: int):
        self.image = PIL.Image.open(file).convert("1", dither=PIL.Image.NONE)
        self.image_width, self.image_height = self.image.size

        self.sprite_width, self.sprite_height = sprite_width, sprite_height
        self.offset_x, self.offset_y = offset_x, offset_y
        self.gap_x, self.gap_y = gap_x, gap_y

        self.sprites_per_row = (self.gap_x + self.image_width - 2 * self.offset_x) // (self.sprite_width + self.gap_x)
        self.sprites_per_col = (self.gap_y + self.image_height - 2 * self.offset_y) // (self.sprite_height + self.gap_y)
        self.total_sprites = self.sprites_per_row * self.sprites_per_col

    def coordinates(self, index: int):
        row = index // self.sprites_per_row
        column = index % self.sprites_per_row

        x0 = self.offset_x + column * (self.sprite_width + self.gap_x)
        y0 = self.offset_y + row * (self.sprite_height + self.gap_y)

        return x0, y0

    @override
    def to_image(self, available_width: int, index: int=0):
        x0, y0 = self.coordinates(index)
        return self.image.crop((x0, y0, x0 + self.sprite_width, y0 + self.sprite_height))
