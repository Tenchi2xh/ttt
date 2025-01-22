import importlib.resources
import json

from ...core.types import Font


def load_font(name: str):
    if "." in name:
        filename = name
        name = name.split(".")[0]
    else:
        filename = f"{name}.ttf"

    metadata = json.loads(importlib.resources.read_text(__package__, f"{name}.json"))
    font = importlib.resources.read_binary(__package__, filename)

    assert all(k in metadata for k in ("name", "author", "url", "size"))

    return Font(
        id=name,
        name=metadata["name"],
        author=metadata["author"],
        url=metadata["url"],
        size=metadata["size"],
        offset_y=metadata.get("offset_y"),
        line_height=metadata.get("line_height"),
        transform=metadata.get("transform", []),
        charsets=metadata["charsets"],
        binary=font
    )


_fonts = [
    "monogram",
    "arkpixel.ttc",
    "silver",
    "vhsgothic",
    "avenuepixel",
    "pixelae",
    "kiwisoda",
    "notjamblackletter",
]

all_fonts = [load_font(n) for n in _fonts]

font_names = [f.id for f in all_fonts]
