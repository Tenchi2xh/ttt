import sys
from typing import List
import click



from .ttt import ttt
from .util import invert_option, outline_option

from ..core import term
from ..core.blit import blit
from ..core.text import Font, Text
from ..core.engine import render
from ..core.effects import OutlineMode, outline
from ..resources import all_fonts, font_names

# TODO: Alignments

samples = {
    "Latin":           "AaBbCc",
    "Latin+":          "ĐđĒēĞğ",
    "Greek":           "ΑαΒβΓγ",
    "Cyrillic":        "АаБбВв",
    "Hebrew":          "אבגד",
    "Arabic":          "جميل ج م ي ل",
    "Runic":           "ᚦᚢᚱᛁᛉᚨᛉ",
    "Hiragana":        "あいうえお",
    "Katakana":        "アイウエオ",
    "CJK Simplified":  "爱发叶艺",
    "CJK Traditional": "愛發葉藝",
    "Korean":          "가너미도루배",
}


def blit_text(text: str, font: Font, invert: bool, outline_modes: List[OutlineMode]):
    text_renderer = Text(font)
    blit(render(outline(outline_modes, text_renderer(text=text)), invert=invert))


@ttt.command()
@click.argument("text", required=False)
@invert_option
@outline_option
@click.option(
    "-f", "--font",
    type=click.Choice(font_names),
    metavar="FONT",
    default="monogram",
    help="Specify the font to use for rendering the text. Default is 'monogram'."
)
@click.option(
    "-l", "--list-fonts", is_flag=True,
    help="List all available fonts with details and examples.",
)
def write(text, invert, outline_modes, font, list_fonts):
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
                blit_text(text, font=f, invert=invert, outline_modes=outline_modes)
            else:
                blit_text(f.name, font=f, invert=invert, outline_modes=outline_modes)
                blit_text(" ".join(samples[cs] for cs in f.charsets), font=f, invert=invert, outline_modes=outline_modes)
            print()

    else:
        if not text:
            raise click.UsageError("Missing argument 'TEXT'.")
        blit_text(text, font=next(f for f in all_fonts if f.id == font), invert=invert, outline_modes=outline_modes)

