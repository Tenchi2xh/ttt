import sys

import click

from ..core.bits import Text
from ..resources import all_fonts
from .ttt import ttt
from .util import font_option, inject_blitter


@ttt.command()
@click.argument("text", required=False)
@font_option
@inject_blitter
def write(text, font, blit):
    """
    Renders TEXT with a specified font or list available fonts.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if not text:
        raise click.UsageError("Missing argument 'TEXT'.")

    font = next(f for f in all_fonts if f.id == font)
    blit(Text(text=text, font=font))
