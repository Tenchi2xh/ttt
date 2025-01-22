import click

from .ttt import ttt
from .util import invert_option

from ..core import term
from ..core.time import get_callback_timer
from ..core.blit import blit
from ..core.video import video_frames


@ttt.command()
@click.argument("file")
@click.option(
    "-d", "--dither",
    is_flag=True,
    help="Dither the output to simulate shades of gray."
)
@click.option(
    "--no-resize",
    is_flag=True,
    help="Display the video in its original resolution (only use for small videos; overriden if too big)."
)
@click.option(
    "--fill",
    is_flag=True,
    help="Disregard aspect ratio and fill the screen (overriden by '--no-resize')."
)
@click.option(
    "-m", "--metrics",
    is_flag=True,
    help="Show frame rate metrics."
)
@invert_option
def watch(file, dither, no_resize, fill, invert, metrics):
    """
    Watch a video provided by the given FILE.
    """

    timer = get_callback_timer(enable=metrics)

    screen_width, screen_height = term.get_size()
    screen_width *= 2
    screen_height *= 4

    frames = video_frames(
        file,
        screen_width, screen_height,
        invert=invert,
        dither=dither,
        resize=not(no_resize),
        preserve_ratio=not(fill),
        enable_metrics=metrics,
    )

    with term.full_screen():
        with term.hide_cursor():
            term.clear_screen()
            for width, height, frame, total_time in frames:
                with timer(display_metrics, total_time):
                    ox = (screen_width - width) // (2 * 2)
                    oy = (screen_height - height) // (2 * 4)
                    term.move_cursor(0, oy)
                    blit(frame, offset=ox, end="")


def display_metrics(elapsed: float, total_time: float):
    term.move_cursor(0, 0)
    blit_time = elapsed
    total_time += blit_time
    print(f"frame rate:\t{1000 / total_time:.1f} FPS")
    print(f"frame time:\t{total_time:7.4f}ms")
    print(f"- blit:\t\t{blit_time:7.4f}ms")
