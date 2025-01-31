import importlib.resources
import json
from base64 import b64decode
from typing import Optional, TypedDict

import numpy as np
from PIL import Image


class Resource(TypedDict):
    name: Optional[str]
    width: int
    height: int
    data: str
    author: str


def load_resources(file: str) -> list[Resource]:
    return json.loads(importlib.resources.read_text(__package__, file))  # type: ignore


def resource_getter(
    resource_type: str,
    all_resources: list[Resource],
):
    def getter(query: str | int) -> Image.Image:
        try:
            query = int(query)
        except ValueError:
            pass

        if isinstance(query, int):
            if query < 0 or query >= len(all_resources):
                raise ValueError(
                    f"{resource_type.capitalize()} number should be "
                    f"between 0 and {len(all_resources) - 1}."
                )
            resource = all_resources[query]
        else:
            resource = next(filter(lambda p: p["name"] == query, all_resources), None)
            if resource is None:
                raise ValueError(f"Unknown {resource_type} '{query}'.")

        pixels = decode(resource["data"], resource["width"], resource["height"])
        return Image.fromarray(pixels, mode="L").convert("1", dither=Image.Dither.NONE)

    return getter


def decode(encoded: str, width: int, height: int):
    shape = (height, width)
    decoded = b64decode(encoded)
    unpacked = np.unpackbits(np.frombuffer(decoded, dtype=np.uint8))
    pixels = unpacked[: np.prod(shape)].reshape(shape).astype(np.uint8) * 255

    return pixels
