from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from .blocks import to_block
from ..resources import Font


def get_width(text: str, font: ImageFont.FreeTypeFont):
    left, _, right, _ = font.getbbox(text)
    return right - left



def render_text(text: str, max_width: int, font: Font):
    font = ImageFont.truetype(BytesIO(font.binary), size=font.size)
    words = text.split()
    lines = []

    # Determine line breaking, width and height

    current_line = words[0]
    total_width = get_width(current_line, font)

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        width = get_width(test_line, font)
        if width <= max_width:
            current_line = test_line
            total_width = max(total_width, width)
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    ascent, descent = font.getmetrics()
    line_height = descent + ascent
    total_height = line_height * len(lines)

    # Create the final image

    image = Image.new("1", (total_width, total_height), 0)
    draw = ImageDraw.Draw(image)

    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=255)
        y += line_height

    pixels = image.load()

    return to_block(pixels, 0, 0, total_width, total_height)
