import sys
import click

from .ttt import ttt
from .util import invert_option

from ..core import term
from ..core.types import Font, OutlineMode
from ..core.text import render_text
from ..core.blit import blit
from ..resources import all_fonts, font_names

# TODO: Stroke modes: soft (vertical horizontal) and hard (all 8 directions)

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


def blit_text(text: str, font: Font, invert: bool, outline: OutlineMode):
    blocks = render_text(
        text=text,
        max_width=2 * term.get_size()[0],
        font=font,
        invert=invert,
        outline=outline
    )
    blit(blocks)


@ttt.command()
@click.argument("text", required=False)
@invert_option
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
@click.option(
    "-o", "--outline",
    type=click.Choice(OutlineMode),
    default=OutlineMode.none,
    help="Draw the text with an outline. Default is 'none'."
)
def write(text, invert, font, list_fonts, outline):
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
                blit_text(text, font=f, invert=invert, outline=outline)
            else:
                blit_text(f.name, font=f, invert=invert, outline=outline)
                blit_text(" ".join(samples[cs] for cs in f.charsets), font=f, invert=invert, outline=outline)
            print()

    else:
        if not text:
            raise click.UsageError("Missing argument 'TEXT'.")
        blit_text(text, font=next(f for f in all_fonts if f.id == font), invert=invert, outline=outline)
