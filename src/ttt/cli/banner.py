import shutil
import click


from .ttt import ttt
from ..core.text import render_text
from ..core.blit import blit
from ..resources import all_fonts


@ttt.command()
@click.argument("text")
def banner(text):
    blocks = render_text(
        text=text,
        max_width=2 * shutil.get_terminal_size()[0],
        font=all_fonts[1]
    )

    blit(blocks)
