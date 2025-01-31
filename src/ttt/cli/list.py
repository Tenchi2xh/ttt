import click

from ..core.bits import Column, Grid, Image, Text
from ..core.engine import RawBit
from ..resources import all_fonts, all_frames, all_patterns, get_frame, get_pattern
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

    targets = [
        Column([RawBit(f"#{i}\nby PiiiXL"), Image(get_frame(i))])
        for i in range(len(all_frames))
    ]
    blit(Grid(targets=targets))


@list.command()
@inject_blitter
def patterns(blit):
    """
    Lists all available pattern designs.
    """

    print("Pattern authors and licenses:")
    print("- lettercore: (CC BY 4.0) https://creativecommons.org/licenses/by/4.0/")
    print()

    targets = [
        Column([RawBit(f"#{i}\nby lettercore"), Image(get_pattern(i))])
        for i in range(len(all_patterns))
    ]
    blit(Grid(targets=targets))


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
        if text:
            blit(Text(text=text, font=f))
        else:
            blit(Text(text=f.name, font=f))
            blit(Text(text=" ".join(samples[cs] for cs in f.charsets), font=f))
        print()
