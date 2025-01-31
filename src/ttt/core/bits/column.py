from collections.abc import Sequence

from ..engine import Bit, Canvas, RasterBit


class Column(RasterBit):
    def __init__(self, targets: Sequence[Bit], gap: int = 0):
        self.targets = targets
        self.gap = gap

    def to_canvas(self, available_width: int) -> Canvas:
        canvases = [target.to_canvas(available_width) for target in self.targets]
        max_width = max(c.width for c in canvases)
        total_height = sum(c.height for c in canvases) + self.gap * (len(canvases) - 1)

        result = Canvas.new(max_width, total_height, 0)
        y = 0
        for canvas in canvases:
            result.paste(canvas, 0, y)
            y += canvas.height + self.gap

        return result
