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
from ttt.core.engine import Bit
from ttt.resources import find_font


def example_block(code: str, example: str):
    return f"""
```python
>>> {"\n... ".join(code.splitlines())}
```

<pre>\n{example}\n</pre>
    """


def patch_blit(cls: type[Bit]):
    if hasattr(cls, "_patched"):
        return cls
    cls._patched = True  # type: ignore

    method = cls.blit

    @functools.wraps(method)
    def blit(self, available_width=80 * 2, invert=False, do_print=False):
        return method(
            self, available_width=available_width, invert=invert, do_print=do_print
        )

    cls.blit = blit


bits: list[type[Bit]] = [
    Atlas,
    Banner,
    Column,
    Frame,
    Grid,
    Image,
    Outline,
    Text,
]

others = [
    find_font,
    outline,
    OutlineMode,
]

[patch_blit(cls) for cls in bits]


def define_env(env):
    # [env.macro(cls) for cls in bits]
    # env.macro(find_font)
    # env.macro(outline)
    # env.macro(OutlineMode)
    @env.macro
    def example(code):
        result = eval(
            code,
            {
                **{obj.__name__: obj for obj in bits + others},
            },
        )

        return example_block(code, result)
