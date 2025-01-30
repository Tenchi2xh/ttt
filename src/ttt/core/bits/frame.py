from typing import List, override

from PIL.Image import Image

from ..engine import RasterBit, Bit, Canvas
from ...resources import get_frame


class Frame(RasterBit):
    def __init__(
        self,
        index: int,
        target: Bit,
        frame_perfect: bool,
        full_width: bool,
        padding: int,
    ):
        self.frame = get_frame(index)
        self.bits = cut_corners(self.frame, 3)
        self.target = target
        self.frame_perfect = frame_perfect
        self.full_width = full_width
        self.padding = padding

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        frame_size = 8

        target_width = available_width - frame_size * 2 - self.padding * 2
        target_canvas = self.target.to_canvas(available_width=target_width)

        x0 = y0 = frame_size + self.padding
        total_width = target_canvas.width + self.padding * 2 + frame_size * 2
        total_height = target_canvas.height + self.padding * 2 + frame_size * 2

        if self.full_width:
            total_width = available_width
            if self.frame_perfect:
                total_width = total_width - (total_width % 8)
            x0 = (available_width - target_canvas.width) // 2

        if self.frame_perfect:
            new_total_width = ((total_width + 7) // 8) * 8
            new_total_height = ((total_height + 7) // 8) * 8
            x0 += (new_total_width - total_width) // 2
            y0 += (new_total_height - total_height) // 2
            total_width = new_total_width
            total_height = new_total_height

        fill = 0
        if is_white(self.bits[1][1]):
            target_canvas = target_canvas.invert()
            fill = 255

        result = Canvas.new(total_width, total_height, fill)

        for x in range(frame_size, total_width - frame_size, frame_size):
            result.paste(self.bits[0][1], x, 0)
            result.paste(self.bits[2][1], x, total_height - frame_size)

        for y in range(frame_size, total_height - frame_size, frame_size):
            result.paste(self.bits[1][0], 0, y)
            result.paste(self.bits[1][2], total_width - frame_size, y)

        result.paste(self.bits[0][0], 0, 0)
        result.paste(self.bits[0][2], total_width - frame_size, 0)
        result.paste(self.bits[2][0], 0, total_height - frame_size)
        result.paste(self.bits[2][2], total_width - frame_size, total_height - frame_size)

        result.paste(target_canvas, x0, y0)

        self.verbatim_data = {
            "col": x0 // 2,
            "row": y0 // 4,
            "total_rows": total_height // 4,
            "invert": fill == 255,
        }

        return result


def cut_corners(image: Image, divide_by: int):
    width = image.width
    bit_width = width // divide_by

    bits: List[List[Image]] = []

    for y in range(0, width, bit_width):
        row = []
        for x in range(0, width, bit_width):
            row.append(image.crop((x, y, x + bit_width, y + bit_width)))
        bits.append(row)

    return bits


def is_white(image: Image):
    return image.getpixel((3, 3)) == 255
