import sys
import click

from .ttt import ttt
from .util import inject_blitter

from ..core.text import Font, Text
from ..resources import all_fonts, font_names


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


@ttt.command()
@click.argument("text", required=False)
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
@inject_blitter
def write(text, font, list_fonts, blit):
    """
    Renders TEXT with a specified font or list available fonts.

    Input can also be provided through a pipe.
    """

    if not text and not sys.stdin.isatty():
        text = sys.stdin.read().strip()

    def blit_text(text: str, font: Font):
        text_renderer = Text(font)
        blit(text_renderer(text=text))

    if list_fonts:
        for i, f in enumerate(all_fonts):
            print(f"{i + 1}. {f.id} '{f.name}' ({f.size}px) by {f.author}: {f.url}")
            print()
            if text:
                blit_text(text, font=f)
            else:
                blit_text(f.name, font=f)
                blit_text(" ".join(samples[cs] for cs in f.charsets), font=f)
            print()

    else:
        if not text:
            raise click.UsageError("Missing argument 'TEXT'.")
        blit_text(text, font=next(f for f in all_fonts if f.id == font))
