import click

from ..core.bits import Atlas, Banner, Image
from .ttt import ttt
from .util import design_option, inject_blitter


@ttt.group()
def draw():
    pass


@draw.command()
@inject_blitter
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
def image(file: str, blit):
    """
    Draw a picture provided by the given FILE.
    """
    image = Image(file)
    blit(image)


@draw.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-w",
    "--width",
    type=int,
    required=True,
    help="Width of each sprite in the atlas (in pixels).",
)
@click.option(
    "-h",
    "--height",
    type=int,
    required=True,
    help="Height of each sprite in the atlas (in pixels).",
)
@click.option(
    "-ox",
    "--offset-x",
    type=int,
    default=0,
    help=(
        "Horizontal offset from the top-left corner of the atlas "
        "to the first sprite (in pixels). Default is 0."
    ),
)
@click.option(
    "-oy",
    "--offset-y",
    type=int,
    default=0,
    help=(
        "Vertical offset from the top-left corner of the atlas "
        "to the first sprite (in pixels). Default is 0."
    ),
)
@click.option(
    "-gx",
    "--gap-x",
    type=int,
    default=0,
    help="Horizontal gap between sprites in the atlas (in pixels). Default is 0.",
)
@click.option(
    "-gy",
    "--gap-y",
    type=int,
    default=0,
    help="Vertical gap between sprites in the atlas (in pixels). Default is 0.",
)
@click.option(
    "-i",
    "--index",
    type=int,
    default=0,
    help=(
        "Index of the sprite to draw (0-based). "
        "If not provided, all sprites are drawn consecutively."
    ),
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
        gap_y=gap_y,
        index=index,
    )

    blit(atlas)


@draw.command()
@click.option(
    "-l",
    "--lines",
    type=int,
    default=None,
    help="Number of text lines to fill (overriden by '-repeat').",
)
@click.option(
    "-r",
    "--repeat",
    metavar="INTEGER",
    type=click.IntRange(min=1),
    default=None,
    help="Repeat the full pattern x times.",
)
@design_option("flo1", "pattern")
@inject_blitter
def banner(design, lines, repeat, blit):
    """
    Draw a full-width banner using repeating patterns.

    Patterns by Lettercore (https://lettercore.itch.io/).
    """

    banner = Banner(design, lines=lines, repeat=repeat)
    blit(banner)
