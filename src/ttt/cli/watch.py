import shutil
import time

import click

from ..core import term
from ..core.blit import blit, blit_colors
from ..core.time import callback_timer
from ..core.video import Frame, video_frames
from .ttt import ttt
from .util import invert_option


@ttt.command()
@click.argument("file", metavar="FILE | URL")
@click.option("-D", "--disable-dithering", is_flag=True, help="Disable dithering.")
@click.option("-c", "--color", is_flag=True, help="Enable color mode.")
@click.option(
    "-R",
    "--no-resize",
    is_flag=True,
    help=(
        "Display the video in its original resolution "
        "(only use for small videos; overriden if too big)."
    ),
)
@click.option(
    "-f",
    "--fill",
    is_flag=True,
    help="Disregard aspect ratio and fill the screen (overriden by '--no-resize').",
)
@click.option(
    "-a",
    "--enable-audio",
    is_flag=True,
    help="Enable audio (synchronization not guaranteed).",
)
@click.option(
    "-F",
    "--disable-frame-rate-limit",
    is_flag=True,
    help="Disable frame rate limit (mutes the audio).",
)
@click.option("-m", "--enable-metrics", is_flag=True, help="Show frame rate metrics.")
@invert_option
def watch(  # noqa: C901
    file,
    disable_dithering,
    color,
    no_resize,
    fill,
    invert,
    enable_audio,
    disable_frame_rate_limit,
    enable_metrics,
):
    """
    Watch a video provided by the given FILE or URL.
    """

    if shutil.which("ffmpeg") is None:
        raise click.UsageError(
            "ffmpeg is not installed or not available in the PATH. "
            "Please install ffmpeg and try again."
        )

    if disable_frame_rate_limit:
        enable_audio = False

    screen_width, screen_height = term.get_size()
    screen_width *= 2
    screen_height *= 4

    frames = video_frames(
        file,
        screen_width,
        screen_height,
        invert=invert,
        dither=not (disable_dithering),
        color=color,
        resize=not (no_resize),
        preserve_ratio=not (fill),
        enable_metrics=enable_metrics,
        enable_audio=enable_audio,
    )

    global print

    if not enable_metrics:

        def print(*_):
            return None

    overshoot = 0

    min_fps = float("inf")
    max_fps = 0
    sum_fps = 0.0
    frame_count = 0

    def display_metrics_and_wait(elapsed: float, frame: Frame):
        nonlocal overshoot, min_fps, max_fps, sum_fps, frame_count
        term.move_cursor(0, 0)

        total_time = sum(t for _, t in frame.step_times)
        blit_time = elapsed
        idle_time, sleep_time = 0, 0
        total_time += blit_time

        if not disable_frame_rate_limit:
            idle_time = max(0, frame.target_frame_time - total_time - overshoot)
            start = time.time()
            if idle_time > 0:
                time.sleep(idle_time / 1000)
            sleep_time = (time.time() - start) * 1000
            total_time += sleep_time
            overshoot = sleep_time - idle_time

        fps = 1000 / total_time
        min_fps = min(fps, min_fps)
        max_fps = max(fps, max_fps)
        sum_fps += fps
        frame_count += 1

        input_res = f"{frame.input_width}x{frame.input_height}"
        output_res = f"{frame.output_width}x{frame.output_height}"
        extra_steps = [("blit", blit_time), ("idle", sleep_time)]

        print(f"  input res {input_res:>11s} ")
        print(f" output res {output_res:>11s} ")
        print(f" frame rate {fps:7.1f} FPS ")
        for s, t in frame.step_times + extra_steps:
            print(f" {s:>10s} {t:8.3f} ms ")
        print(f"      total {total_time:8.3f} ms ")

    def blit_mono(pixels, _, offset, end):
        return blit(pixels, offset, end)

    do_blit = blit_colors if color else blit_mono

    with term.full_screen():
        with term.hide_cursor():
            term.clear_screen()
            for frame in frames:
                with callback_timer(display_metrics_and_wait, frame):
                    ox = (screen_width - frame.output_width) // (2 * 2)
                    oy = (screen_height - frame.output_height) // (2 * 4)
                    term.move_cursor(0, oy)
                    do_blit(frame.blocks, frame.colors, offset=ox, end="")  # type: ignore

    if enable_metrics:
        print(f"Min FPS: {min_fps:7.1f} FPS")
        print(f"Max FPS: {max_fps:7.1f} FPS")
        print(f"Avg FPS: {sum_fps / frame_count:7.1f} FPS")
