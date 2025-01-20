import click

from .blit import blit
from .convert import load_atlas, load_image


@click.group()
def ttt():
    pass


@ttt.command("blit")
@click.argument("file", type=click.Path(exists=True, dir_okay=False))
def blit_command(file):
    blocks = load_image(file)
    blit(blocks)


@ttt.command()
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
        blit(blocks)
    else:
        for b in blocks:
            blit(b)


if __name__ == "__main__":
    ttt()
