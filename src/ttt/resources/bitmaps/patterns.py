import json
from typing import Union
import importlib.resources

from PIL import Image

from .decode import decode


patterns = json.loads(importlib.resources.read_text(__package__, f"patterns.json"))


def get_pattern(query: Union[int, str]) -> Image:
    if isinstance(query, int):
        if query < 0 or query >= len(patterns):
            raise ValueError(f"Pattern number should be between 0 and {len(patterns) - 1}.")
        pattern = patterns[query]
    else:
        pattern = next(filter(lambda p: p["n"] == query, patterns), None)
        if pattern is None:
            raise ValueError(f"Unknown pattern '{query}'.")

    pixels = decode(pattern["p"], pattern["w"], pattern["h"])
    return Image.fromarray(pixels, mode="L")
