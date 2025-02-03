import sys

import click

from ..core.bits import Frame, Image, Row, Text
from ..core.engine import RawBit
from ..resources import find_font, get_icon
from .ttt import ttt
from .util import design_option, font_option, inject_blitter


@ttt.command()
@click.argument("text", required=False)
@click.option(
    "-V",
    "--verbatim",
    is_flag=True,
    help="Don't format input and display it verbatim inside the frame.",
)
@click.option(
    "-P",
    "--frame-perfect",
    is_flag=True,
    help=(
        "Force the frame width to be at a multiple of 8 "
        "to align with the original pixel art."
    ),
)
@click.option("-F", "--full-width", is_flag=True, help="Use as much width as possible.")
@click.option(
    "-p",
    "--padding",
    type=int,
    default=0,
    help="Padding (in pixels) between the frame and the contents.",
)
@click.option(
    "-L",
    "--left-icon",
    type=str,
    default=None,
    help="Icon to display on the left. Use command 'list icons' to see all icons.",
)
@click.option(
    "-R",
    "--right-icon",
    type=str,
    default=None,
    help="Icon to display on the right. Use command 'list icons' to see all icons.",
)
@design_option("27", "frame")
@font_option
@inject_blitter
def frame(
    text,
    verbatim,
    frame_perfect,
    full_width,
    padding,
    left_icon,
    right_icon,
    design,
    font,
    blit,
):
    """
    Renders TEXT with a specified font inside a frame.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if not text:
        raise click.UsageError("Missing argument 'TEXT'.")

    if verbatim:
        text_bit = RawBit(text)
    else:
        font = find_font(font)
        text_bit = Text(text=text, font=font)

    targets = []

    if left_icon:
        targets.append(Image(get_icon(left_icon)))

    targets.append(text_bit)
    target = Row(targets, gap=2)

    if right_icon:
        targets.append(Image(get_icon(right_icon)))

    frame = Frame(
        index=design,
        target=target,
        frame_perfect=frame_perfect,
        full_width=full_width,
        padding=padding,
    )

    blit(frame)
