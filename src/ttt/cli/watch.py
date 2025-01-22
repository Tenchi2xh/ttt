import time
import click
from typing import List, Tuple

from .ttt import ttt
from .util import invert_option

from ..core import term
from ..core.time import callback_timer
from ..core.blit import blit
from ..core.video import video_frames


@ttt.command()
@click.argument("file")
@click.option(
    "-D", "--disable-dithering",
    is_flag=True,
    help="Disable dithering."
)
@click.option(
    "-R", "--no-resize",
    is_flag=True,
    help="Display the video in its original resolution (only use for small videos; overriden if too big)."
)
@click.option(
    "-f", "--fill",
    is_flag=True,
    help="Disregard aspect ratio and fill the screen (overriden by '--no-resize')."
)
@click.option(
    "-a", "--enable-audio",
    is_flag=True,
    help="Enable audio (synchronization not guaranteed)."
)
@click.option(
    "-F", "--disable-frame-rate-limit",
    is_flag=True,
    help="Disable frame rate limit (mutes the audio)."
)
@click.option(
    "-m", "--enable-metrics",
    is_flag=True,
    help="Show frame rate metrics."
)
@invert_option
def watch(file, disable_dithering, no_resize, fill, invert, enable_audio, disable_frame_rate_limit, enable_metrics):
    """
    Watch a video provided by the given FILE.
    """

    if disable_frame_rate_limit:
        enable_audio = False

    screen_width, screen_height = term.get_size()
    screen_width *= 2
    screen_height *= 4

    frames = video_frames(
        file,
        screen_width, screen_height,
        invert=invert,
        dither=not(disable_dithering),
        resize=not(no_resize),
        preserve_ratio=not(fill),
        enable_metrics=enable_metrics,
        enable_audio=enable_audio,
    )

    global print
    if not enable_metrics:
        print = lambda *_: None

    overshoot = 0

    def display_metrics_and_wait(elapsed: float, step_times: List[Tuple[str, float]], target_frame_time: float):
        nonlocal overshoot
        term.move_cursor(0, 0)

        total_time = sum(t for _, t in step_times)
        blit_time = elapsed
        idle_time, sleep_time = 0, 0
        total_time += blit_time

        if not disable_frame_rate_limit:
            idle_time = max(0, target_frame_time - total_time - overshoot)
            start = time.time()
            if idle_time > 0:
                time.sleep(idle_time / 1000)
            sleep_time = (time.time() - start) * 1000
            total_time += sleep_time
            overshoot = sleep_time - idle_time

        step_times.extend([("blit", blit_time), ("idle", sleep_time)])
        print(f"frame rate: {1000 / total_time:5.1f} FPS   ")
        print(f"frame time:  {total_time:7.4f}ms   ")
        for s, t in step_times:
            print(f"- {s + ':':10s} {t:7.4f}ms   ")


    with term.full_screen():
        with term.hide_cursor():
            term.clear_screen()
            for width, height, frame, step_times, target_frame_time in frames:
                with callback_timer(display_metrics_and_wait, step_times, target_frame_time):
                    ox = (screen_width - width) // (2 * 2)
                    oy = (screen_height - height) // (2 * 4)
                    term.move_cursor(0, oy)
                    blit(frame, offset=ox, end="")


