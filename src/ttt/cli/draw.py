import click



from .ttt import ttt
from .util import invert_option

from ..core import term
from ..core.blit import blit
from ..core.image import load_image
from ..core.atlas import load_atlas
from ..core.banner import render_pattern

from ..resources.patterns.patterns import get_pattern


@ttt.group()
def draw():
    pass


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@invert_option
def image(file, invert):
    """
    Draw a picture provided by the given FILE.
    """
    blocks = load_image(file, invert=invert)
    blit(blocks)


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@invert_option
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
def atlas(file, invert, width, height, offset_x, offset_y, gap_x, gap_y, index):
    """
    Draw a sprite from the sprite atlas provided by the given FILE.

    Options for width, height, offsets, and gaps are used to define the sprite layout,
    and the index option specifies a particular sprite to draw. If no index is provided,
    all sprites are drawn consecutively.
    """

    blocks = load_atlas(
        file,
        sprite_width=width,
        sprite_height=height,
        offset_x=offset_x,
        offset_y=offset_y,
        gap_x=gap_x,
        gap_y=gap_y,
        index=index,
        invert=invert
    )
    if index is not None:
        blit(blocks)
    else:
        for b in blocks:
            blit(b)


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
@invert_option
def banner(pattern_name, lines, repeat, invert):
    """
    Draw a full-width banner using repeating patterns.

    Patterns by Lettercore (https://lettercore.itch.io/).
    """
    try:
        pattern_name = int(pattern_name)
    finally:
        pass

    pattern = get_pattern(pattern_name)
    width = term.get_size()[0] * 2

    if lines is None:
        height = pattern.size[1]
    else:
        height = lines * 4

    if repeat is not None:
        height = pattern.size[1] * repeat

    blocks = render_pattern(pattern, width, height, invert=invert)
    blit(blocks)
