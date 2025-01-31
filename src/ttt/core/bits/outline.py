from enum import StrEnum, auto
from typing import override

from ..engine import Bit, Canvas, RasterBit


class OutlineMode(StrEnum):
    none = auto()
    soft = auto()
    hard = auto()
    shadow = auto()


class Outline(RasterBit):
    def __init__(self, outline_mode: OutlineMode, target: Bit):
        self.mode = outline_mode
        self.target = target

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        if self.mode == OutlineMode.none:
            return self.target.to_canvas(available_width)

        else:
            extra_size = 3 if self.mode == OutlineMode.shadow else 2

            canvas = self.target.to_canvas(available_width - extra_size)
            width, height = canvas.width + extra_size, canvas.height + extra_size

            result = Canvas.new(width, height, 0)
            result.raws = canvas.raws

            def draw(dx, dy, negative: bool = False):
                nonlocal canvas
                _overlay(
                    base=result,
                    overlay=canvas,
                    x=dx,
                    y=dy,
                    match_color=255,
                    write_color=0 if negative else 255,
                )

            if self.mode in (OutlineMode.soft, OutlineMode.hard):
                draw(0, 1)
                draw(2, 1)
                draw(1, 0)
                draw(1, 2)

                if self.mode == OutlineMode.hard:
                    draw(0, 0)
                    draw(2, 0)
                    draw(0, 2)
                    draw(2, 2)

                draw(1, 1, negative=True)
                result.raws = result.shifted_raws(1, 1, toggle_invert=True)

            elif self.mode == OutlineMode.shadow:
                draw(3, 3)
                draw(0, 0, negative=True)
                draw(0, 2, negative=True)
                draw(2, 0, negative=True)
                draw(2, 2, negative=True)
                draw(1, 1)
                result.raws = result.shifted_raws(1, 1)

            return result


def _overlay(
    base: Canvas, overlay: Canvas, x: int, y: int, match_color: int, write_color: int
):
    pixels = overlay.pixels()
    for j in range(overlay.height):
        for i in range(overlay.width):
            color = pixels[i, j]
            if color == match_color:
                base.put_pixel(x + i, y + j, write_color)


def outline(outline_modes: list[OutlineMode], target: Bit) -> Bit:
    if outline_modes:
        mode = outline_modes[0]
        return outline(
            outline_modes=outline_modes[1:], target=Outline(mode, target=target)
        )
    return target
