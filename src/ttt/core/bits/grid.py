from collections.abc import Sequence
from typing import override

from ttt.core.engine import Canvas

from ..engine import Bit, RasterBit


class Grid(RasterBit):
    def __init__(self, targets: Sequence[Bit], gap: int = 4):
        self.targets = targets
        self.gap = gap

    @override
    def to_canvas(self, available_width: int) -> Canvas:
        canvases = [t.to_canvas(available_width) for t in self.targets]

        rows: list[list[Canvas]] = []
        rows_positions = [[(0, 0)]]
        current_row = [canvases[0]]

        total_width = canvases[0].width
        total_height = 0
        max_height = canvases[0].height
        row_width = total_width

        for canvas in canvases[1:]:
            new_width = row_width + self.gap + canvas.width

            if new_width <= available_width:
                current_row.append(canvas)
                rows_positions[len(rows)].append((row_width + self.gap, total_height))
                row_width = new_width
                total_width = max(total_width, new_width)
                max_height = max(max_height, canvas.height)
            else:
                rows.append(current_row)
                row_width = canvas.width
                current_row = [canvas]
                total_height += max_height + self.gap
                rows_positions.append([(0, total_height)])

        rows.append(current_row)
        total_height += max_height

        result = Canvas.new(total_width, total_height, 0)
        for row, positions in zip(rows, rows_positions):
            for canvas, position in zip(row, positions):
                result.paste(canvas, position[0], position[1])

        return result
