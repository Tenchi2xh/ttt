import json
import importlib.resources

from PIL import Image

from .decode import decode


all_frames = json.loads(importlib.resources.read_text(__package__, f"frames.json")) # type: ignore


def get_frame(index: int) -> Image.Image:
    if index < 0 or index >= len(all_frames):
        raise ValueError(f"Pattern number should be between 0 and {len(all_frames) - 1}.")

    pixels = decode(all_frames[index], 24, 24)
    return Image.fromarray(pixels, mode="L").convert("1", dither=Image.Dither.NONE)
