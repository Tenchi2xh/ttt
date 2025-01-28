import json
import importlib.resources

from PIL import Image

from .decode import decode


frames = json.loads(importlib.resources.read_text(__package__, f"frames.json"))


def get_frame(index: int) -> Image:
    if index < 0 or index >= len(frames):
        raise ValueError(f"Pattern number should be between 0 and {len(frames) - 1}.")

    pixels = decode(frames[index], 24, 24)

    return Image.fromarray(pixels, mode="L")
