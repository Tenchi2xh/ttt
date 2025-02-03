from collections.abc import Sequence

from ..engine import Bit, Canvas, RasterBit


class Row(RasterBit):
    def __init__(self, targets: Sequence[Bit], gap: int = 0):
        self.targets = targets
        self.gap = gap

    def to_canvas(self, available_width: int) -> Canvas:
        # TODO: better layouting
        individual_width = (
            available_width - self.gap * (len(self.targets) - 1)
        ) // len(self.targets)

        canvases = [target.to_canvas(individual_width) for target in self.targets]

        total_width = sum(c.width for c in canvases) + self.gap * (len(canvases) - 1)
        max_height = max(c.height for c in canvases)

        result = Canvas.new(total_width, max_height, 0)
        x = 0
        # TODO: vertical align options
        for canvas in canvases:
            result.paste(canvas, x, (max_height - canvas.height) // 2)
            x += canvas.width + self.gap

        return result
