from functools import wraps

import click

from ..core.bits import OutlineMode, outline
from ..core.engine import Bit
from ..resources import font_names


invert_option = click.option(
    "--invert", is_flag=True, help="Draw using inverted colors."
)


outline_option = click.option(
    "-o",
    "--outline",
    "outline_modes",
    type=click.Choice(OutlineMode),  # type: ignore
    multiple=True,
    help="Draw using an outline effect. This option can be repeated.",
)


font_option = click.option(
    "-f",
    "--font",
    type=click.Choice(font_names),
    metavar="FONT",
    default="monogram",
    help=(
        "Specify the font to use for rendering the text. "
        "Use command 'list fonts' to see all fonts. Default is 'monogram'."
    ),
)


def design_option(default: str, resource_type: str):
    return click.option(
        "-d",
        "--design",
        metavar="DESIGN",
        type=str,
        default=default,
        help=(
            f"{resource_type.capitalize} design number or alias. "
            f"Use command 'list {resource_type}s' to see all {resource_type}s."
        ),
    )


def inject_blitter(command_function):
    @invert_option
    @outline_option
    @click.pass_context
    @wraps(command_function)
    def wrapper(ctx, invert, outline_modes, *args, **kwargs):
        def blit(target: Bit):
            return outline(outline_modes, target).blit(invert=invert)

        ctx.invoke(command_function, *args, blit=blit, **kwargs)

    return wrapper
