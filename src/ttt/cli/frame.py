import sys
import click

from .ttt import ttt
from .util import inject_blitter, font_option

from ..core import term
from ..core.renderables import Frame, Text, Blank
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
    help="Frame number."
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

    font = next(f for f in all_fonts if f.id == font)
    text_renderer = Text(font)
    blank = Blank()

    if verbatim:
        lines = text.splitlines()
        width = max(len(l) for l in lines) * 2
        height = len(lines) * 4
        render_target = blank(width=width, height=height)
    else:
        render_target = text_renderer(text=text)

    frame = Frame(index)
    blit(
        frame(
            target=render_target,
            frame_perfect=frame_perfect,
            full_width=full_width,
            padding=padding,
        )
    )

    if verbatim:
        d = frame.verbatim_data
        # TODO: Fix wrong invert when --invert is used or some effects
        invert = term.INVERT if d["invert"] else ""
        term.move_cursor_up(d["total_rows"] - d["row"])
        for line in lines:
            term.move_cursor_right(d["col"])
            print(invert + line + term.RESET)
        term.move_cursor_down(d["total_rows"] - d["row"] - len(lines))
