import importlib.resources
import json

from PIL import Image

from .decode import decode


all_icons = json.loads(importlib.resources.read_text(__package__, "icons.json"))  # type: ignore


def get_icon(index: int) -> Image.Image:
    if index < 0 or index >= len(all_icons):
        raise ValueError(f"Icon number should be between 0 and {len(all_icons) - 1}.")

    pixels = decode(all_icons[index], 16, 16)
    return Image.fromarray(pixels, mode="L").convert("1", dither=Image.Dither.NONE)
