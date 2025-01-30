import click
import numpy as np

from ..core import term
from ..resources import all_fonts, all_frames, all_patterns, get_frame, get_pattern
from ..core.renderables import Text, Image

from .ttt import ttt
from .util import inject_blitter


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


@ttt.group()
def list():
    pass


@list.command()
@inject_blitter
def frames(blit):
    """
    Lists all available frame designs.
    """

    print("Frame authors and licenses:")
    print("- PiiiXL: (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/")
    print()

    display_grid(blit, all_frames, get_frame)



@list.command()
@inject_blitter
def patterns(blit):
    """
    Lists all available pattern designs.
    """

    print("Pattern authors and licenses:")
    print("- lettercore: (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/")
    print()

    display_grid(blit, all_patterns, get_pattern)


@list.command()
@click.argument("text", required=False)
@inject_blitter
def fonts(text, blit):
    """
    List all available fonts with details and examples.

    Preview text configurable using optional argument TEXT.
    """

    for i, f in enumerate(all_fonts):
        print(f"#{i + 1}: {f.id} '{f.name}' ({f.size}px) by {f.author}: {f.url}")
        print()
        text_renderer = Text(font=f)
        if text:
            blit(text_renderer(text=text))
        else:
            blit(text_renderer(text=f.name))
            blit(text_renderer(text=" ".join(samples[cs] for cs in f.charsets)))
        print()


def display_grid(blit, all_images, getter):
    term_cols = term.get_size()[0]
    gap = 2

    cols = 0
    items = []

    def display():
        top_line = ""
        bottom_line = ""
        targets = []

        for i, item in enumerate(items):
            if i != 0:
                top_line += " " * gap
                bottom_line += " " * gap

            top_line += item["top_line"].ljust(item["cols"])
            bottom_line += item["bottom_line"].rjust(item["cols"])
            targets.append(item["target"])

        print(top_line)
        print(bottom_line)
        blit(targets, gap=gap)

    for i in range(len(all_images)):
        image = getter(i)
        render_target = Image(image)()
        image_cols = (image.width + 1) // 2

        if cols + gap + image_cols > term_cols:
            display()
            print()
            cols = 0
            items = []

        if cols > 0:
            cols += 2
        cols += image_cols

        items.append({
            "target": render_target,
            "top_line": f"#{i}",
            "bottom_line": "",
            "cols": image_cols,
        })

    display()