import shutil
import sys
import click

from .ttt import ttt
from .util import invert_option

from ..core.text import render_text
from ..core.blit import blit
from ..resources import all_fonts, Font, font_names


samples = {
    "Latin":          "AaBbCc",
    "Latin+":         "ĐđĒēĞğ",
    "Greek":          "ΑαΒβΓγ",
    "Cyrillic":       "АаБбВв",
    "Hebrew":         "אבגד",
    "Arabic":         "جميل ﺝﻡﻱﻝ",
    "Runic":          "ᚦᚢᚱᛁᛉᚨᛉ",
    "Hiragana":       "あいうえお",
    "Katakana":       "アイウエオ",
    "CJK Ideographs": "發藝 发艺",
    "Korean":         "가너미도루배",
}


def blit_text(text: str, font: Font, invert: bool):
    blocks = render_text(
        text=text,
        max_width=2 * shutil.get_terminal_size()[0],
        font=font
    )
    blit(blocks, invert=invert)


@ttt.command()
@click.argument("text", required=False)
@invert_option
@click.option(
    "-f", "--font",
    type=click.Choice(font_names),
    default="monogram",
    help="Specify the font to use for rendering the text. Defaults to 'monogram'."
)
@click.option(
    "-L", "--list-fonts", is_flag=True,
    help="List all available fonts with details and examples.",
)
def write(text, invert, font, list_fonts):
    """
    Renders TEXT with a specified font or list available fonts.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    if list_fonts:
        for i, f in enumerate(all_fonts):
            print(f"{i + 1}. {f.id} '{f.name}' ({f.size}px) by {f.author}: {f.url}")
            print()
            if text:
                blit_text(text, font=f, invert=invert)
            else:
                blit_text(f.name, font=f, invert=invert)
                blit_text(" ".join(samples[cs] for cs in f.charsets), font=f, invert=invert)
            print()

    else:
        if not text:
            raise click.UsageError("Missing argument 'TEXT'.")
        blit_text(text, font=next(f for f in all_fonts if f.id == font), invert=invert)
