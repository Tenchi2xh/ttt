from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import List, Self

from PIL import Image, ImageDraw, ImageOps
from PIL.ImageFont import FreeTypeFont
import numpy as np

from . import term
from .blit import blit
from .convert import to_blocks


@dataclass
class Raw:
    x: int
    y: int
    text: str
    invert: bool


class Canvas:
    def __init__(self, contents: Image.Image | str):
        self.raws: List[Raw] = []

        if isinstance(contents, Image.Image):
            self.image = contents
        else:
            lines = contents.splitlines()
            width = max(len(l) for l in lines)
            height = len(lines)
            self.image = Image.new("1", (width * 2, height * 4), 0)
            for i, line in enumerate(lines):
                self.raws.append(Raw(x=0, y=i * 4, text=line, invert=False))

        self.draw = ImageDraw.Draw(self.image)

    @classmethod
    def new(cls, width: int, height: int, color: int):
        image = Image.new("1", (width, height), color)
        return cls(image)

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    def pixels(self):
        return np.array(self.image).transpose().astype(np.uint8) * 255

    def put_pixel(self, x: int, y: int, fill: int):
        self.image.putpixel((x, y), fill)

    def paste(self, other: Self | Image.Image, x: int, y: int):
        if isinstance(other, Image.Image):
            self.image.paste(other, (x, y))
        else:
            self.image.paste(other.image, (x, y))
            for raw in other.raws:
                self.raws.append(
                    replace(raw,
                        x=raw.x + x,
                        y=raw.y + y
                    )
                )

    def shifted_raws(self, dx: int, dy: int, toggle_invert: bool = False):
        return [
            replace(
                raw,
                x=raw.x + dx,
                y=raw.y + dy,
                invert=not raw.invert if toggle_invert else raw.invert
            )
            for raw in self.raws
        ]

    def invert(self):
        result = Canvas(ImageOps.invert(self.image))
        for raw in self.raws:
            result.raws.append(replace(raw, invert=not raw.invert))
        return result

    def draw_text(self, x: int, y: int, text: str, font: FreeTypeFont, fill: int):
        self.draw.text((x, y), text=text, font=font, fill=fill)


class Bit(ABC):
    @abstractmethod
    def to_canvas(self, available_width: int) -> Canvas:
        pass

    def blit(self, available_width: int = term.get_size()[0] * 2, invert: bool = False):
        canvas = self.to_canvas(available_width=available_width)
        if invert:
            canvas = canvas.invert()

        image = canvas.image
        pixels = np.array(image).astype(np.uint8) * 255
        blocks = to_blocks(pixels, 0, 0, image.width, image.height, invert=False)

        output_buffer = blit(blocks, do_print=False)
        buffer_width = max(len(l) for l in output_buffer)

        # TODO: respect raw.invert
        # - Make a grid 'inverts' the size of output_buffer, all False
        # - When adding a raw line, flip all relevant bools if invert is true
        # - At the end, insert invert ANSIs

        invert_flags = [[False for _ in range(buffer_width)] for _ in range(len(output_buffer))]
        raw_inverted = False

        for raw in canvas.raws:
            row = raw.y // 4
            col_from = raw.x // 2
            col_to = min(buffer_width, col_from + len(raw.text))
            line = output_buffer[row]
            output_buffer[row] = line[:col_from] + raw.text + line[col_to:]
            if raw.invert:
                raw_inverted = True
                invert_flags[row][col_from : col_to] = [not f for f in invert_flags[row][col_from : col_to]]

        if raw_inverted:
            inverted_buffer = []

            for chars, flags in zip(output_buffer, invert_flags):
                row = []
                inverted = False

                for char, flag in zip(chars, flags):
                    if flag and not inverted:
                        row.append(term.INVERT)
                        inverted = True
                    elif not flag and inverted:
                        row.append(term.RESET)
                        inverted = False
                    row.append(char)

                if inverted:
                    row.append(term.RESET)

                inverted_buffer.append("".join(row))

            output_buffer = inverted_buffer

        print("\n".join(output_buffer))


class RawBit(Bit):
    # TODO: Breakable and non-breakable mode, use available_width
    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def to_canvas(self, available_width: int) -> Canvas:
        return Canvas(self.raw_text)


class RasterBit(Bit, ABC):
    @abstractmethod
    def to_canvas(self, available_width: int) -> Canvas:
        pass
