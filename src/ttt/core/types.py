from dataclasses import dataclass
from enum import StrEnum, auto
from typing import List, Optional


@dataclass
class Font:
    id: str
    name: str
    author: str
    url: str
    size: int
    offset_y: Optional[int]
    line_height: Optional[int]
    transform: List[str]
    charsets: List[str]
    binary: bytes


class OutlineMode(StrEnum):
    none = auto()
    soft = auto()
    hard = auto()
