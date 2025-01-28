from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Self, Tuple

import numpy as np
from PIL import Image

from . import term
from .convert import to_blocks


@dataclass
class RenderTarget:
    renderable: "Renderable"
    kwargs: Dict[str, Any] = field(default_factory=dict)


class Renderable(ABC):
    @abstractmethod
    def to_image(self, available_width: int, **kwargs) -> Image:
        pass

    def __call__(self, **kwargs) -> RenderTarget:
        return RenderTarget(self, kwargs)

    def render(self, available_width: int = term.get_size()[0] * 2, invert: bool = False, **kwargs):
        image = self.to_image(available_width=available_width, **kwargs)
        pixels = np.array(image).astype(np.uint8) * 255
        blocks = to_blocks(pixels, 0, 0, image.width, image.height, invert=invert)

        return blocks

def render(target: RenderTarget, invert: bool = False):
    return target.renderable.render(invert=invert, **target.kwargs)
