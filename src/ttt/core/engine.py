from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Self

import numpy as np
from PIL import Image, ImageDraw, ImageOps
from PIL.ImageFont import FreeTypeFont

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
    """Abstraction layer for drawing with pixels and text at the same time."""

    def __init__(self, contents: Image.Image | str):
        """Inits a Canvas.

        Args:
            contents (Image.Image | str):
                Initial contents of this Canvas, either an Image or some verbatim text.
        """
        self.raws: list[Raw] = []

        if isinstance(contents, Image.Image):
            self.image = contents
        else:
            lines = contents.splitlines()
            width = max(len(line) for line in lines)
            height = len(lines)
            self.image = Image.new("1", (width * 2, height * 4), 0)
            for i, line in enumerate(lines):
                self.raws.append(Raw(x=0, y=i * 4, text=line, invert=False))

        self.draw = ImageDraw.Draw(self.image)

    @classmethod
    def new(cls, width: int, height: int, color: int) -> "Canvas":
        """Create a new blank Canvas.

        Args:
            width (int): Width in pixels.
            height (int): Height in pixels.
            color (int): Fill color of the new Canvas (0 = black, 255 = white).

        Returns:
            A new blank Canvas.
        """
        image = Image.new("1", (width, height), color)
        return cls(image)

    @property
    def width(self) -> int:
        """Width of this Canvas."""
        return self.image.width

    @property
    def height(self) -> int:
        """Height of this Canvas."""
        return self.image.height

    def pixels(self) -> np.ndarray:
        """Returns a 2D numpy array representing the pixel values of this Canvas.

        Values are 0 for black and 255 for white.
        """
        return np.array(self.image).transpose().astype(np.uint8) * 255

    def put_pixel(self, x: int, y: int, fill: int):
        """Change the color value of the given pixel coordinates.

        Args:
            x (int): Horizontal coordinate of the pixel.
            y (int): Vertical coordinate of the pixel.
            fill (int): New color value (0 = black, 255 = white).
        """
        self.image.putpixel((x, y), fill)

    def paste(self, other: Self | Image.Image, x: int, y: int):
        """Draw another Canvas on top of this one.

        Args:
            other (Canvas | Image.Image): Other Canvas to draw (or PIL Image).
            x (int): Horizontal offset of where to draw the other Canvas.
            y (int): Vertical offset of where to draw the other Canvas.
        """
        if isinstance(other, Image.Image):
            self.image.paste(other, (x, y))
        else:
            self.image.paste(other.image, (x, y))
            for raw in other.raws:
                self.raws.append(replace(raw, x=raw.x + x, y=raw.y + y))

    def shifted_raws(self, dx: int, dy: int, toggle_invert: bool = False) -> list[Raw]:
        """Returns a copy of the verbatim texts of this Canvas, shifted by an offset.

        Args:
            dx (int): Horizontal offset.
            dy (int): Vertical offset.
            toggle_invert (bool, optional): Also invert the colors of the verbatim text.

        Returns:
            A copy of the verbatim texts with shifted coordinates.
        """
        return [
            replace(
                raw,
                x=raw.x + dx,
                y=raw.y + dy,
                invert=not raw.invert if toggle_invert else raw.invert,
            )
            for raw in self.raws
        ]

    def invert(self):
        """Returns a copy of this Canvas with inverted colors.

        Returns:
            Canvas: A copy of this Canvas with inverted colors.
        """
        result = Canvas(ImageOps.invert(self.image))
        for raw in self.raws:
            result.raws.append(replace(raw, invert=not raw.invert))
        return result

    def draw_text(self, x: int, y: int, text: str, font: FreeTypeFont, fill: int):
        """Draw rasterized text on this Canvas.

        Args:
            x (int): Horizontal coordinate of the text, in pixels.
            y (int): Vertical offset of the text, in pixels.
            text (str): Text to write.
            font (FreeTypeFont): PIL Font object.
            fill (int): Text color (0 = black, 255 = white).
        """
        self.draw.text((x, y), text=text, font=font, fill=fill)


class Bit(ABC):
    """Rendereable element of the *ttt* engine.

    Can be either made from pixels ([RasterBit][ttt.core.engine.RasterBit])
    or verbatim text ([RawBit][ttt.core.engine.RawBit]).
    """

    @abstractmethod
    def to_canvas(self, available_width: int) -> Canvas:
        """Render this Bit into a [Canvas][ttt.core.engine.Canvas].

        Args:
            available_width (int):
                Width budget given to this Bit and its children for rendering.

        Returns:
            A rendered Canvas.
        """
        pass

    def blit(  # noqa: C901
        self,
        available_width: int = term.get_size()[0] * 2,
        invert: bool = False,
        do_print: bool = True,
    ) -> str:
        """Recursively render the Bit tree and convert to printable text.

        Args:
            available_width (int, optional): Width budget given to this Bit
                and its children for rendering. Defaults to current terminal width.
            invert (bool, optional): Render with inverted colors.
            do_print (bool, optional): Also print the final rendered result.

        Returns:
            A rendered Bit
        """
        canvas = self.to_canvas(available_width=available_width)
        if invert:
            canvas = canvas.invert()

        image = canvas.image
        pixels = np.array(image).astype(np.uint8) * 255
        blocks = to_blocks(pixels, 0, 0, image.width, image.height, invert=False)

        output_buffer = blit(blocks, do_print=False)
        buffer_width = max(len(line) for line in output_buffer)

        invert_flags = [
            [False for _ in range(buffer_width)] for _ in range(len(output_buffer))
        ]
        raw_inverted = False

        for raw in canvas.raws:
            row = raw.y // 4
            col_from = raw.x // 2
            col_to = min(buffer_width, col_from + len(raw.text))

            line = output_buffer[row]
            output_buffer[row] = line[:col_from] + raw.text + line[col_to:]

            if raw.invert:
                raw_inverted = True
                invert_flags[row][col_from:col_to] = [
                    not f for f in invert_flags[row][col_from:col_to]
                ]

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

        result = "\n".join(output_buffer)
        if do_print:
            print(result)
        return result


class RawBit(Bit):
    """Renderable Bit representing verbatim text.

    Contents of this type of Bit are *not rendered using pixels* but will instead
    be **outputed as-is to the terminal**.

    Since real text cannot be precisely positioned like pixels, the final position of a
    raw Bit will be rounded to the nearest multiple of 2 horizontally, and 4 vertically.
    """

    # TODO: Breakable and non-breakable mode, use available_width
    def __init__(self, raw_text: str):
        """Inits a RawBit.

        Args:
            raw_text (str): Text content to be rendered verbatim.
        """
        self.raw_text = raw_text

    def to_canvas(self, available_width: int) -> Canvas:
        return Canvas(self.raw_text)


class RasterBit(Bit, ABC):
    """Abstract class for renderable Bits using pixels."""

    @abstractmethod
    def to_canvas(self, available_width: int) -> Canvas:
        pass
