from dataclasses import dataclass
from typing import Optional
from PIL import Image


def load(file: str):
    img = Image.open(file).convert("1", dither=Image.NONE)
    width, height = img.size
    pixels = img.load()
    return pixels, width, height


def load_image(file: str):
    pixels, width, height = load(file)
    return to_block(pixels, x0=0, y0=0, width=width, height=height)


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


def load_atlas(
    file: str,
    sprite_width: int,
    sprite_height: int,
    offset_x: int,
    offset_y: int,
    gap_x: int,
    gap_y: int,
    index: Optional[int] = None
):
    pixels, width, height = load(file)

    md = AtlasMetadata(
        width=width,
        height=height,
        sprite_width=sprite_width,
        sprite_height=sprite_height,
        offset_x=offset_x,
        offset_y=offset_y,
        gap_x=gap_x,
        gap_y=gap_y
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


def atlas_render_sprite(
    pixels,
    md: AtlasMetadata,
    index: int,
    sprites_per_row: int
):
    x0, y0 = atlas_coordinates(md, index, sprites_per_row)
    return to_block(pixels, x0=x0, y0=y0, width=md.sprite_width, height=md.sprite_height)


def to_block(pixels, x0: int, y0: int, width: int, height: int):
    for y in range(y0, y0 + height, 4):
        line = []
        for x in range(x0, x0 + width, 2):
            block_value = 0
            for i in range(8):
                pixel_x = x + (i % 2)
                pixel_y = y + (i // 2)
                block_value |= (pixels[pixel_x, pixel_y] == 255) << i
            line.append(block_value)
        yield line
