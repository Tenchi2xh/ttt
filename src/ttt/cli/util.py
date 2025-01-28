import click

from ..core.effects import OutlineMode


invert_option = click.option(
    "--invert",
    is_flag=True,
    help="Draw using inverted colors."
)

outline_option = click.option(
    "-o", "--outline", "outline_modes",
    type=click.Choice(OutlineMode),
    multiple=True,
    help="Add an effect to the drawing. This option can be repeated."
)
