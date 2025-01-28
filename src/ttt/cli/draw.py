import click

from .ttt import ttt
from .util import inject_blitter

from ..core.renderables import Image, Atlas, Banner


@ttt.group()
def draw():
    pass


@draw.command()
@inject_blitter
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
def image(file, blit):
    """
    Draw a picture provided by the given FILE.
    """
    image = Image(file)
    blit(image())


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-w", "--width",
    type=int, required=True,
    help="Width of each sprite in the atlas (in pixels)."
)
@click.option(
    "-h", "--height",
    type=int, required=True,
    help="Height of each sprite in the atlas (in pixels)."
)
@click.option(
    "-ox", "--offset-x",
    type=int, default=0,
    help="Horizontal offset from the top-left corner of the atlas to the first sprite (in pixels). Default is 0."
)
@click.option(
    "-oy", "--offset-y",
    type=int, default=0,
    help="Vertical offset from the top-left corner of the atlas to the first sprite (in pixels). Default is 0."
)
@click.option(
    "-gx", "--gap-x",
    type=int, default=0,
    help="Horizontal gap between sprites in the atlas (in pixels). Default is 0."
)
@click.option(
    "-gy", "--gap-y",
    type=int, default=0,
    help="Vertical gap between sprites in the atlas (in pixels). Default is 0."
)
@click.option(
    "-i", "--index",
    type=int, default=None,
    help="Index of the sprite to draw (0-based). If not provided, all sprites are drawn consecutively."
)
@inject_blitter
def atlas(file, width, height, offset_x, offset_y, gap_x, gap_y, index, blit):
    """
    Draw a sprite from the sprite atlas provided by the given FILE.

    Options for width, height, offsets, and gaps are used to define the sprite layout,
    and the index option specifies a particular sprite to draw. If no index is provided,
    all sprites are drawn consecutively.
    """

    atlas = Atlas(
        file=file,
        sprite_width=width,
        sprite_height=height,
        offset_x=offset_x,
        offset_y=offset_y,
        gap_x=gap_x,
        gap_y=gap_y
    )

    if index is not None:
        blit(atlas(index=index))
    else:
        for i in range(atlas.total_sprites):
            blit(atlas(index=i))


@draw.command()
@click.option(
    "-p", "--pattern", "pattern_name",
    metavar="INTEGER",
    required=True, type=click.IntRange(min=0, max=299),
    help="Pattern number."
)
@click.option(
    "-l", "--lines",
    type=int, default=None,
    help="Number of text lines to fill (overriden by '-repeat')."
)
@click.option(
    "-r", "--repeat",
    metavar="INTEGER",
    type=click.IntRange(min=1), default=None,
    help="Repeat the full pattern x times.",
)
@inject_blitter
def banner(pattern_name, lines, repeat, blit):
    """
    Draw a full-width banner using repeating patterns.

    Patterns by Lettercore (https://lettercore.itch.io/).
    """
    try:
        pattern_name = int(pattern_name)
    finally:
        pass

    banner = Banner(pattern_name)
    blit(banner(lines=lines, repeat=repeat))
