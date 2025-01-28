import click


from .ttt import ttt
from .util import invert_option, outline_option

from ..core.blit import blit
from ..core.image import Image
from ..core.atlas import Atlas
from ..core.banner import Banner
from ..core.engine import render
from ..core.effects import Outline, OutlineMode, outline


@ttt.group()
def draw():
    pass


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@invert_option
@outline_option
def image(file, invert, outline_modes):
    """
    Draw a picture provided by the given FILE.
    """
    image = Image(file)
    blit(render(outline(outline_modes, image()), invert=invert))


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@invert_option
@outline_option
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
def atlas(file, invert, outline_modes, width, height, offset_x, offset_y, gap_x, gap_y, index):
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
        blit(render(outline(outline_modes, atlas(index=index)), invert=invert))
    else:
        for i in range(atlas.total_sprites):
            blit(render(outline(outline_modes, atlas(index=i)), invert=invert))


@draw.command()
@invert_option
@outline_option
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
def banner(invert, outline_modes, pattern_name, lines, repeat):
    """
    Draw a full-width banner using repeating patterns.

    Patterns by Lettercore (https://lettercore.itch.io/).
    """
    try:
        pattern_name = int(pattern_name)
    finally:
        pass

    banner = Banner(pattern_name)
    blit(render(outline(outline_modes, banner(lines=lines, repeat=repeat)) , invert=invert))
