import click
from .ttt import ttt
from ..core.blit import blit as do_blit
from ..core.convert import load_atlas, load_image


@ttt.group()
def blit():
    pass


@blit.command("file")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
def file_command(file):
    blocks = load_image(file)
    do_blit(blocks)


@blit.command()
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
@click.option("-w", "--width", type=int, required=True)
@click.option("-h", "--height", type=int, required=True)
@click.option("-ox", "--offset-x", type=int, default=0)
@click.option("-oy", "--offset-y", type=int, default=0)
@click.option("-gx", "--gap-x", type=int, default=0)
@click.option("-gy", "--gap-y", type=int, default=0)
@click.option("-i", "--index", type=int, default=None)
def atlas(file, width, height, offset_x, offset_y, gap_x, gap_y, index):
    blocks = load_atlas(
        file,
        sprite_width=width,
        sprite_height=height,
        offset_x=offset_x,
        offset_y=offset_y,
        gap_x=gap_x,
        gap_y=gap_y,
        index=index
    )
    if index is not None:
        do_blit(blocks)
    else:
        for b in blocks:
            do_blit(b)
