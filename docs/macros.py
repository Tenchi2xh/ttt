import functools
import textwrap

from ttt.core.bits import (
    Atlas,
    Banner,
    Column,
    Frame,
    Grid,
    Image,
    Outline,
    OutlineMode,
    Row,
    Text,
    outline,
)
from ttt.core.engine import Bit, RawBit
from ttt.resources import find_font, get_icon


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
    Row,
    RawBit,
]

others = {
    "find_font": find_font,
    "outline": outline,
    "OutlineMode": OutlineMode,
    "get_icon": get_icon,
}

[patch_blit(cls) for cls in bits]


example_template = """<div class="example"><pre>{result}</pre></div>"""

command_template = f"""
```bash
❱ {{command}}
```

{example_template}
"""

code_template = f"""
```python
>>> {{code}}
```

{example_template}
"""


def define_env(env):
    @env.macro
    def example(code, command: str | None = None, only_example: bool = False, indent=0):
        result = eval(
            code,
            {
                **{obj.__name__: obj for obj in bits},
                **others,
            },
        )

        if only_example:
            output = example_template.format(result=result)
        elif command:
            output = command_template.format(command=command, result=result)
        else:
            output = code_template.format(
                code="\n... ".join(code.splitlines()), result=result
            )

        return textwrap.indent(output, " " * indent)
