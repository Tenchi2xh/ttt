import click
from functools import wraps

from ..core.blit import blit as do_blit
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
    help="Specify the font to use for rendering the text. Default is 'monogram'."
)


def inject_blitter(command_function):
    @invert_option
    @outline_option
    @click.pass_context
    @wraps(command_function)
    def wrapper(ctx, invert, outline_modes, *args, **kwargs):
        def blit(render_target: RenderTarget):
            return do_blit(render(outline(outline_modes, render_target), invert=invert))

        ctx.invoke(command_function, blit=blit, *args, **kwargs)

    return wrapper
