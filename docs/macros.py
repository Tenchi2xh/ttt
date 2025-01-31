import functools

from ttt.core.bits import (
    Atlas,
    Banner,
    Column,
    Frame,
    Grid,
    Image,
    Outline,
    OutlineMode,
    Text,
    outline,
)
from ttt.resources import find_font


# TODO: Include in theme
style = """
font-family: Iosevka Kotan Term;
line-height: 1.2;
"""


def pre(text: str):
    return f'<pre style="{style}">\n{text}\n</pre>'


def patch_blit(cls):
    if hasattr(cls, "_patched"):
        return cls

    cls._patched = True
    method = cls.blit

    @functools.wraps(method)
    def blit(self, available_width=74 * 2, invert=False, do_print=False):
        return pre(
            method(
                self, available_width=available_width, invert=invert, do_print=do_print
            )
        )

    cls.blit = blit


[
    patch_blit(cls)
    for cls in [
        Atlas,
        Banner,
        Column,
        Frame,
        Grid,
        Image,
        Outline,
        Text,
    ]
]


def define_env(env):
    env.variables["Atlas"] = Atlas
    env.variables["Banner"] = Banner
    env.variables["Column"] = Column
    env.variables["Frame"] = Frame
    env.variables["Grid"] = Grid
    env.variables["Image"] = Image
    env.variables["Outline"] = Outline
    env.variables["OutlineMode"] = OutlineMode
    env.variables["Text"] = Text

    env.macro(find_font)
    env.macro(outline)
    env.macro(pre)
