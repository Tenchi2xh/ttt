import sys
import click

from .ttt import ttt
from .util import inject_blitter, font_option

from ..core.renderables import Text
from ..resources import all_fonts


@ttt.command()
@click.argument("text", required=False)
@font_option
@inject_blitter
def write(text, font, list_fonts, blit):
    """
    Renders TEXT with a specified font or list available fonts.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if not text:
        raise click.UsageError("Missing argument 'TEXT'.")

    font = next(f for f in all_fonts if f.id == font)
    text_renderer = Text(font)
    blit(text_renderer(text=text))
