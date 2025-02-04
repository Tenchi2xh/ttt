import functools
import textwrap
from dataclasses import asdict
from typing import Literal

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
from ttt.resources import credits, find_font, get_icon


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


credits_template = """
<table>
<tbody>
    <tr><td>Name</td><td>{name}</td></tr>
    <tr><td>Author</td><td>{author}</td></tr>
    <tr><td>URL</td><td><a href="{url}">{url}</a></td></tr>
    <tr><td>License</td><td><a href="{license_url}">{license_name}</a></td></tr>
</tbody>
</table>
"""

example_template = """<div class="example"><pre>{result}</pre></div>"""

tight_example_template = (
    """<div class="example"><pre class="tight">{result}</pre></div>"""
)

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


def format_credits(category: Literal["font", "icon", "frame", "pattern"]):
    result = []

    for credit in filter(lambda c: c.category == category, credits):
        if category == "font" and credit.asset_ids:
            for font in credit.asset_ids:
                result.append(
                    tight_example_template.format(
                        result=Text(
                            f"{credit.name} by {credit.author}",
                            find_font(font),
                        ).blit(available_width=1000)
                    )
                )
        elif category == "icon" and credit.asset_ids:
            result.append(
                tight_example_template.format(
                    result=Row(
                        [Image(get_icon(asset_id)) for asset_id in credit.asset_ids],
                        gap=4,
                    ).blit(available_width=1000)
                )
            )
        elif category == "pattern" and credit.asset_ids:
            result.append(
                tight_example_template.format(
                    result=Column(
                        [Banner(asset_id, lines=6) for asset_id in credit.asset_ids],
                        gap=4,
                    ).blit()
                )
            )
        elif category == "frame" and credit.asset_ids:
            result.append(
                tight_example_template.format(
                    result=Column(
                        [
                            Frame(
                                int(asset_id),
                                Text("\n", font=find_font("m3x6")),
                                full_width=True,
                            )
                            for asset_id in credit.asset_ids
                        ],
                        gap=4,
                    ).blit()
                )
            )

        result.append(
            credits_template.format(
                license_name=credit.license_name,
                license_url=credit.license_url,
                **asdict(credit),
            )
        )

    return "\n".join(result)


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


def define_env(env):
    env.macro(format_credits)
    env.macro(example)
