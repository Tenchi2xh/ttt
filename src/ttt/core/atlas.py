from dataclasses import dataclass
from typing import Optional

from .blocks import to_blocks_pil
from .image import load


@dataclass
class Atlas:
    file: str
    sprite_width: int
    sprite_height: int
    offset_x: int
    offset_y: int
    gap_x: int
    gap_y: int

    def __post_init__(self):
        self.image, width, height = load(self.file)
        self.width, self.height = width, height
        self.sprites_per_row = (self.gap_x + width - 2 * self.offset_x) // (self.sprite_width + self.gap_x)
        self.sprites_per_col = (self.gap_y + height - 2 * self.offset_y) // (self.sprite_height + self.gap_y)
        self.total_sprites = self.sprites_per_row * self.sprites_per_col

    def coordinates(self, index: int):
        row = index // self.sprites_per_row
        column = index % self.sprites_per_row

        x0 = self.offset_x + column * (self.sprite_width + self.gap_x)
        y0 = self.offset_y + row * (self.sprite_height + self.gap_y)
        return x0, y0

    def render_sprite(self, index: int, invert: bool):
        x0, y0 = self.coordinates(index)

        return to_blocks_pil(
            self.image, x0=x0, y0=y0,
            width=self.sprite_width, height=self.sprite_height,
            invert=invert
        )


def load_atlas(
    file: str,

    sprite_width: int, sprite_height: int,
    offset_x: int,     offset_y: int,
    gap_x: int,        gap_y: int,

    invert: bool = False,
    index: Optional[int] = None
):
    atlas = Atlas(
        file=file,
        sprite_width=sprite_width,
        sprite_height=sprite_height,
        offset_x=offset_x,
        offset_y=offset_y,
        gap_x=gap_x,
        gap_y=gap_y
    )

    if index is not None:
        assert index < atlas.total_sprites
        return atlas.render_sprite(index=index, invert=invert)
    else:
        return (
            atlas.render_sprite(index=i, invert=invert)
            for i in range(atlas.total_sprites)
        )
