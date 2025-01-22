from dataclasses import dataclass
import importlib.resources
import json
from typing import List


@dataclass
class Font:
    id: str
    name: str
    author: str
    url: str
    size: int
    transform: List[str]
    charsets: List[str]
    binary: bytes


def load_font(name: str):
    metadata = json.loads(importlib.resources.read_text(__package__, f"{name}.json"))
    font = importlib.resources.read_binary(__package__, f"{name}.ttf")

    assert all(k in metadata for k in ("name", "author", "url", "size"))

    return Font(
        id=name,
        name=metadata["name"],
        author=metadata["author"],
        url=metadata["url"],
        size=metadata["size"],
        transform=metadata.get("transform", []),
        charsets=metadata["charsets"],
        binary=font
    )


font_names = ["monogram", "notjamblackletter", "vhsgothic", "gumballthickwires", "kiwisoda"]

all_fonts = [load_font(n) for n in font_names]
