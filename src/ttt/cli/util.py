from typing import List
import click
from functools import wraps

from ..core.blit import blit as do_blit, blit_multiple
from ..core.engine import RenderTarget, render
from ..core.renderables import OutlineMode, outline
from ..resources import font_names


invert_option = click.option(
    "--invert",
    is_flag=True,
    help="Draw using inverted colors."
)


outline_option = click.option(
    "-o", "--outline", "outline_modes",
    type=click.Choice(OutlineMode),
    multiple=True,
    help="Draw using an outline effect. This option can be repeated."
)


font_option = click.option(
    "-f", "--font",
    type=click.Choice(font_names),
    metavar="FONT",
    default="monogram",
    help="Specify the font to use for rendering the text. Use command 'list fonts' to see all fonts. Default is 'monogram'."
)


def inject_blitter(command_function):
    @invert_option
    @outline_option
    @click.pass_context
    @wraps(command_function)
    def wrapper(ctx, invert, outline_modes, *args, **kwargs):
        def blit(render_target: RenderTarget | List[RenderTarget], gap=2):
            if isinstance(render_target, RenderTarget):
                return do_blit(render(outline(outline_modes, render_target), invert=invert))
            return blit_multiple(
                [render(outline(outline_modes, rt), invert=invert) for rt in render_target],
                gap=gap
            )

        ctx.invoke(command_function, blit=blit, *args, **kwargs)

    return wrapper
