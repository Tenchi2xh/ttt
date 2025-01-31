from io import BytesIO
from typing import override

from PIL import ImageFont

from ..engine import Canvas, RasterBit
from ..font import Font


class Text(RasterBit):
    def __init__(self, text: str, font: Font):
        self.text = text
        self.font = font
        self.pil_font = ImageFont.truetype(BytesIO(font.binary()), size=font.size)

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        lines, total_width, total_height, line_height = break_and_measure(
            text=transform_text(self.text, self.font),
            max_width=available_width,
            font=self.font,
            pil_font=self.pil_font,
        )

        y = self.font.offset_y if self.font.offset_y is not None else 0

        result = Canvas.new(total_width, total_height, color=0)

        for line in lines:
            result.draw_text(0, y, line, font=self.pil_font, fill=255)
            y += line_height

        return result


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
    return int(right - left)


def break_and_measure(
    text: str, max_width: int, font: Font, pil_font: ImageFont.FreeTypeFont
):
    lines: list[str] = []
    raw_lines = text.splitlines()
    total_width: int = 0

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
