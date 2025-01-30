import sys
import click

from .ttt import ttt
from .util import inject_blitter, font_option

from ..core.bits import Frame, Text
from ..core.engine import RawBit
from ..resources import all_fonts


@ttt.command()
@click.argument("text", required=False)
@click.option(
    "-V", "--verbatim",
    is_flag=True,
    help="Don't format input and display it verbatim inside the frame."
)
@click.option(
    "-P", "--frame-perfect",
    is_flag=True,
    help="Force the frame width to be at a multiple of 8 to align with the original pixel art."
)
@click.option(
    "-F", "--full-width",
    is_flag=True,
    help="Use as much width as possible."
)
@click.option(
    "-p", "--padding",
    type=int, default=0,
    help="Padding (in pixels) between the frame and the contents."
)
@click.option(
    "-i", "--index",
    type=int, default=27,
    help="Frame number. Use command 'list frames' to see all frames."
)
@font_option
@inject_blitter
def frame(text, verbatim, frame_perfect, full_width, padding, index, font, blit):
    """
    Renders TEXT with a specified font inside a frame.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if not text:
        raise click.UsageError("Missing argument 'TEXT'.")

    if verbatim:
        target = RawBit(text)
    else:
        font = next(f for f in all_fonts if f.id == font)
        target = Text(text=text, font=font)

    frame = Frame(
        index=index,
        target=target,
        frame_perfect=frame_perfect,
        full_width=full_width,
        padding=padding
    )

    blit(frame)
