from collections.abc import Sequence
from typing import Callable

import click

from ..core.bits import Column, Grid, Image, Text
from ..core.engine import RawBit
from ..resources import (
    Resource,
    all_fonts,
    all_frames,
    all_icons,
    all_patterns,
    credits,
    get_frame,
    get_icon,
    get_pattern,
)
from .ttt import ttt
from .util import inject_blitter


samples = {
    "Latin": "AaBbCc",
    "Latin+": "ĐđĒēĞğ",
    "Greek": "ΑαΒβΓγ",
    "Cyrillic": "АаБбВв",
    "Hebrew": "אבגד",
    "Arabic": "جميل ج م ي ل",
    "Runic": "ᚦᚢᚱᛁᛉᚨᛉ",
    "Hiragana": "あいうえお",
    "Katakana": "アイウエオ",
    "CJK Simplified": "爱发叶艺",
    "CJK Traditional": "愛發葉藝",
    "Korean": "가너미도루배",
}


@ttt.group(help="Commands for listing built-in resources.")
def list():
    pass


named_option = click.option(
    "-N", "--named", is_flag=True, help="Only show designs that have an alias name."
)


@list.command()
@named_option
@inject_blitter
def icons(blit, named: bool):
    """
    Lists all available icons.
    """

    print("Frame authors and licenses:")
    print("- PiiiXL: (CC BY-ND 4.0) https://creativecommons.org/licenses/by-nd/4.0/")
    print()

    blit_list(blit, all_icons, get_icon, named)


@list.command()
@named_option
@inject_blitter
def frames(blit, named: bool):
    """
    Lists all available frame designs.
    """

    print("Frame authors and licenses:")
    print("- PiiiXL: (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/")
    print()

    blit_list(blit, all_frames, get_frame, named)


@list.command()
@named_option
@inject_blitter
def patterns(blit, named):
    """
    Lists all available pattern designs.
    """

    print("Pattern authors and licenses:")
    print("- lettercore: (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/")
    print()

    blit_list(blit, all_patterns, get_pattern, named)


@list.command()
@click.argument("text", required=False)
@inject_blitter
def fonts(text, blit):
    """
    List all available fonts with details and examples.

    Preview text configurable using optional argument TEXT.
    """

    for i, f in enumerate(all_fonts):
        credit = next(c for c in credits if c.name == f.name and c.author == f.author)
        number = f"#{i + 1}: "

        print(f"{number}{f.id} '{f.name}' ({f.size}px) by {f.author}: {f.url}")
        print(
            f"{' ' * len(number)}License: {credit.license_name} ({credit.license_url})"
        )
        print()
        if text:
            blit(Text(text=text, font=f))
        else:
            blit(Text(text=f.name, font=f))
            blit(Text(text=" ".join(samples[cs] for cs in f.charsets), font=f))
        print()


def blit_list(blit, resources: Sequence[Resource], getter: Callable, named: bool):
    targets = [
        Column([RawBit(make_label(i, resources)), Image(getter(i))])
        for i in range(len(resources))
        if named and resources[i]["name"] or not named
    ]
    blit(Grid(targets=targets))


def make_label(i: int, resources: Sequence[Resource]):
    resource = resources[i]
    lines = [(f"#{i}", "")]

    author = resource["author"]
    name = resource["name"]

    right_width = len(author)

    if name is not None:
        lines.append(("Alias: ", name))
        right_width = max(len(s) for s in (author, name))
    else:
        lines.append(("", ""))

    lines.append(("Author:", author))

    right_width = max(right_width, resource["width"] // 2 - 8)

    return "\n".join(line[0] + " " + line[1].rjust(right_width) for line in lines)
