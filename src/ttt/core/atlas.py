from dataclasses import dataclass
from typing import Optional

from .blocks import to_block
from .io import load


@dataclass
class AtlasMetadata:
    width: int
    height: int
    sprite_width: int
    sprite_height: int
    offset_x: int
    offset_y: int
    gap_x: int
    gap_y: int


def load_atlas(
    file: str,

    sprite_width: int, sprite_height: int,
    offset_x: int,     offset_y: int,
    gap_x: int,        gap_y: int,

    index: Optional[int] = None
):
    pixels, width, height = load(file)

    md = AtlasMetadata(
        width=width,               height=height,
        sprite_width=sprite_width, sprite_height=sprite_height,
        offset_x=offset_x,         offset_y=offset_y,
        gap_x=gap_x,               gap_y=gap_y
    )

    sprites_per_row, _, total_sprites = atlas_metrics(md)

    if index is not None:
        assert index < total_sprites
        return atlas_render_sprite(pixels, md=md, index=index, sprites_per_row=sprites_per_row)
    else:
        for i in range(total_sprites):
            x0, y0 = atlas_coordinates(md, i, sprites_per_row)
            return (
                atlas_render_sprite(pixels, md=md, index=i, sprites_per_row=sprites_per_row)
                for i in range(total_sprites)
            )


def atlas_metrics(md: AtlasMetadata):
    sprites_per_row = (md.gap_x + md.width - 2 * md.offset_x) // (md.sprite_width + md.gap_x)
    sprites_per_col = (md.gap_y + md.height - 2 * md.offset_y) // (md.sprite_height + md.gap_y)

    total_sprites = sprites_per_row * sprites_per_col

    return sprites_per_row, sprites_per_col, total_sprites


def atlas_coordinates(
    md: AtlasMetadata,
    index: int,
    sprites_per_row: int
):
    row = index // sprites_per_row
    column = index % sprites_per_row

    x0 = md.offset_x + column * (md.sprite_width + md.gap_x)
    y0 = md.offset_y + row * (md.sprite_height + md.gap_y)

    return x0, y0



def atlas_render_sprite(
    pixels,
    md: AtlasMetadata,
    index: int,
    sprites_per_row: int
):
    x0, y0 = atlas_coordinates(md, index, sprites_per_row)
    return to_block(pixels, x0=x0, y0=y0, width=md.sprite_width, height=md.sprite_height)
