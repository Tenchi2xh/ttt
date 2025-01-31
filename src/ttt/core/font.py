from dataclasses import dataclass
from typing import Optional


@dataclass
class Font:
    id: str
    name: str
    author: str
    url: str
    size: int
    offset_y: Optional[int]
    line_height: Optional[int]
    transform: list[str]
    charsets: list[str]
    binary: bytes
