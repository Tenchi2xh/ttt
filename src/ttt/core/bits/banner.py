from typing import Optional, override

from ...resources import get_pattern
from ..engine import Canvas, RasterBit


class Banner(RasterBit):
    def __init__(
        self, pattern_name: int | str, lines: Optional[int], repeat: Optional[int]
    ):
        self.pattern = get_pattern(pattern_name)
        self.lines = lines
        self.repeat = repeat

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        width = available_width

        if self.lines is None:
            height = self.pattern.height
        else:
            height = self.lines * 4

        if self.repeat is not None:
            height = self.pattern.height * self.repeat

        canvas = Canvas.new(width, height, 0)

        pattern_width, pattern_height = self.pattern.size

        for x in range(0, width, pattern_width):
            for y in range(0, height, pattern_height):
                canvas.paste(self.pattern, x, y)

        return canvas
