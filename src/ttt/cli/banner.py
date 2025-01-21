import shutil
import sys
import click

from .ttt import ttt
from ..core.text import render_text
from ..core.blit import blit
from ..resources import all_fonts, Font, font_names

def do_blit(text: str, font: Font):
    blocks = render_text(
        text=text,
        max_width=2 * shutil.get_terminal_size()[0],
        font=font
    )

    blit(blocks)


@ttt.command()
@click.option("-f", "--font", type=click.Choice(font_names), default="monogram")
@click.option("-L", "--list-fonts", is_flag=True)
@click.argument("text", required=False)
def banner(text, font, list_fonts):
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if list_fonts:
        for i, f in enumerate(all_fonts):
            print(f"{i + 1}. {f.id} '{f.name}' ({f.size}px) by {f.author}: {f.url}")
            do_blit(text if text else f.name, f)
            print()

    else:
        if not text:
            raise click.UsageError("Missing argument 'TEXT'.")
        do_blit(text, next(f for f in all_fonts if f.id == font))
