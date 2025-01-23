from dataclasses import dataclass
from typing import List, Optional
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from .blocks import to_blocks_pil
from .effects import OutlineMode, draw_with_outline


def get_width(text: str, font: ImageFont.FreeTypeFont):
    left, _, right, _ = font.getbbox(text)
    return right - left


@dataclass
class Font:
    id: str
    name: str
    author: str
    url: str
    size: int
    offset_y: Optional[int]
    line_height: Optional[int]
    transform: List[str]
    charsets: List[str]
    binary: bytes


def render_text(
    text: str,
    max_width: int,
    font: Font,
    invert: bool=False,
    outline: OutlineMode=OutlineMode.none
):
    text = transform_text(text, font)
    pil_font = ImageFont.truetype(BytesIO(font.binary), size=font.size)
    lines, total_width, total_height, line_height = break_and_measure(text, max_width, font, pil_font)

    x = 0
    y = font.offset_y if font.offset_y is not None else 0

    if outline != OutlineMode.none:
        x += 1
        y += 1
        total_width += 2
        total_height += 2

    image = Image.new("1", (total_width, total_height), 0)
    draw = ImageDraw.Draw(image)

    for line in lines:
        draw_with_outline(
            outline, x, y,
            lambda x, y, fill: draw.text((x, y), line, font=pil_font, fill=fill)
        )
        y += line_height

    return to_blocks_pil(image, x0=0, y0=0, width=total_width, height=total_height, invert=invert)


def transform_text(text: str, font: Font):
    for transform in font.transform:
        match transform:
            case "upper":
                text = text.upper()
            case "lower":
                text = text.lower()
    return text


def break_and_measure(text: str, max_width: int, font: Font, pil_font: ImageFont.FreeTypeFont):
    lines = []
    raw_lines = text.splitlines()
    total_width = 0

    for raw_line in raw_lines:
        words = raw_line.split(" ")
        current_line = words[0]
        total_width = max(total_width, get_width(current_line, pil_font))

        for word in words[1:]:
            test_line = f"{current_line} {word}"
            width = get_width(test_line, pil_font)
            if width <= max_width:
                current_line = test_line
                total_width = max(total_width, width)
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

    ascent, descent = pil_font.getmetrics()
    line_height = descent + ascent

    if font.line_height is not None:
        line_height = font.line_height

    total_height = line_height * len(lines)

    return lines, total_width, total_height, line_height
