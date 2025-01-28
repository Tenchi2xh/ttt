from dataclasses import dataclass
from typing import List, Optional, override
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from .engine import Renderable


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


class Text(Renderable):
    def __init__(self, font: Font):
        self.font = font
        self.pil_font = ImageFont.truetype(BytesIO(font.binary), size=font.size)

    @override
    def to_image(self, available_width: int, text: str):
        text = transform_text(text, self.font)

        lines, total_width, total_height, line_height = break_and_measure(text, available_width, self.font, self.pil_font)

        y = self.font.offset_y if self.font.offset_y is not None else 0

        image = Image.new("1", (total_width, total_height), 0)
        draw = ImageDraw.Draw(image)

        for line in lines:
            draw.text((0, y), line, font=self.pil_font, fill=255)
            y += line_height

        return image


def transform_text(text: str, font: Font):
    for transform in font.transform:
        match transform:
            case "upper":
                text = text.upper()
            case "lower":
                text = text.lower()
    return text


def get_width(text: str, font: ImageFont.FreeTypeFont):
    left, _, right, _ = font.getbbox(text)
    return right - left


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
