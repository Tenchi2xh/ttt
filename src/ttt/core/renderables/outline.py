from enum import StrEnum, auto
from typing import List, override

import numpy as np
from PIL import Image

from ..engine import RenderTarget, Renderable


class OutlineMode(StrEnum):
    none = auto()
    soft = auto()
    hard = auto()
    shadow = auto()


class Outline(Renderable):
    def __init__(self, outline_mode: OutlineMode):
        self.mode = outline_mode

    @override
    def to_image(self, available_width: int, target: RenderTarget):
        if self.mode == OutlineMode.none:
            return target.renderable.to_image(available_width=available_width, **target.kwargs)

        else:
            extra_size = 3 if self.mode == OutlineMode.shadow else 2

            image = target.renderable.to_image(available_width=available_width - extra_size, **target.kwargs)
            width, height = image.width + extra_size, image.height + extra_size
            result = Image.new("1", (width, height), 0)

            def draw(dx, dy, negative: bool = False):
                nonlocal image
                _overlay(
                    image=result,
                    overlay=image,
                    x=dx,
                    y=dy,
                    match_color=255,
                    write_color=0 if negative else 255
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

            elif self.mode == OutlineMode.shadow:
                draw(3, 3)
                draw(0, 0, negative=True)
                draw(0, 2, negative=True)
                draw(2, 0, negative=True)
                draw(2, 2, negative=True)
                draw(1, 1)

            return result


def _overlay(image: Image, overlay: Image, x: int, y: int, match_color: int, write_color: int):
    pixels = np.array(overlay).astype(np.uint8) * 255
    for j in range(overlay.height):
        for i in range(overlay.width):
            color = pixels[j, i]
            if color == match_color:
                image.putpixel((x + i, y + j), write_color)


def outline(outline_modes: List[OutlineMode], target: RenderTarget):
    if outline_modes:
        mode = outline_modes[0]
        return outline(
            outline_modes=outline_modes[1:],
            target=Outline(mode)(target=target)
        )
    return target
