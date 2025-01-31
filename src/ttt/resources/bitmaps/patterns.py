import importlib.resources
import json
from typing import Union

from PIL import Image

from .decode import decode


all_patterns = json.loads(importlib.resources.read_text(__package__, "patterns.json"))  # type: ignore
all_patterns.sort(key=lambda p: p["h"])


def get_pattern(query: Union[int, str]) -> Image.Image:
    if isinstance(query, int):
        if query < 0 or query >= len(all_patterns):
            raise ValueError(
                f"Pattern number should be between 0 and {len(all_patterns) - 1}."
            )
        pattern = all_patterns[query]
    else:
        pattern = next(filter(lambda p: p["n"] == query, all_patterns), None)
        if pattern is None:
            raise ValueError(f"Unknown pattern '{query}'.")

    pixels = decode(pattern["p"], pattern["w"], pattern["h"])
    return Image.fromarray(pixels, mode="L").convert("1", dither=Image.Dither.NONE)
