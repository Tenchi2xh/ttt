import json
from typing import Union
import importlib.resources
from base64 import b64decode

import numpy as np
from PIL import Image


patterns = json.loads(importlib.resources.read_text(__package__, f"patterns.json"))


def get_pattern(query: Union[int, str]) -> Image:
    if isinstance(query, int):
        if query < 0 or query > len(patterns) - 1:
            raise ValueError(f"Pattern number should be between 0 and {len(patterns) - 1}.")
        pattern = patterns[query]
    else:
        pattern = next(filter(lambda p: p["n"] == query, patterns), None)
        if pattern is None:
            raise ValueError(f"Unknown pattern '{query}'.")

    original_shape = (pattern["h"], pattern["w"])
    decoded = b64decode(pattern["p"])
    unpacked = np.unpackbits(np.frombuffer(decoded, dtype=np.uint8))
    pixels = unpacked[:np.prod(original_shape)].reshape(original_shape).astype(np.uint8) * 255

    return Image.fromarray(pixels, mode="L")


if __name__ == "__main__":
    get_pattern(42)
