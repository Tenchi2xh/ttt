import ffmpeg
import numpy as np

from .blocks import to_block_numpy
from ..core.time import callback_timer


def video_metrics(file: str):
    probe = ffmpeg.probe(file)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    if video_stream is None:
        raise ValueError("No video stream found in the file.")

    width = int(video_stream["width"])
    height = int(video_stream["height"])

    sar = video_stream.get("sample_aspect_ratio", "1:1")
    sar_num, sar_den = map(int, sar.split(":"))

    scaled_width = width * sar_num // sar_den
    scaled_height = height

    r_frame_rate = video_stream.get("r_frame_rate", "30/1")
    num, den = map(int, r_frame_rate.split("/"))
    frame_rate = num / den
    frame_time = 1000 / frame_rate

    return scaled_width, scaled_height, frame_time


def video_frames(
    file: str,
    output_width: int, output_height: int,
    invert: bool=False,
    dither: bool=False,
    resize: bool=True,
    preserve_ratio=True,
    enable_metrics: bool=False
):
    input_width, input_height, target_frame_time = video_metrics(file)

    if not resize and (input_width > output_width or input_height > output_height):
        resize = True
        preserve_ratio = True

    if not resize:
        output_width = input_width
        output_height = input_height
    elif preserve_ratio:
        scaled_width = output_height * input_width / input_height
        scaled_height = output_width * input_height / input_width
        if scaled_width < output_width:
            output_width = int(scaled_width)
        else:
            output_height = int(scaled_height)

    pix_fmt = "monob" if dither else "gray"

    process = (
        ffmpeg
        .input(file)
        .filter("scale", output_width, output_height)
        .output("pipe:", format="rawvideo", pix_fmt=pix_fmt)
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    row_bytes = (output_width + 7) // 8
    bytes_to_read = row_bytes * output_height if dither else output_width * output_height
    shape = (output_height, row_bytes) if dither else (output_height, output_width)

    def make_frame_8bit(in_bytes):
        return np.where(frame > 127, 255, 0)

    def make_frame_1bit(in_bytes):
        return np.unpackbits(frame, axis=1)[:, :output_width] * 255

    make_frame = make_frame_1bit if dither else make_frame_8bit

    global print
    if not enable_metrics:
        print = lambda *_: None

    while True:
        step_times = []

        def display_metrics(elapsed: float, name: str):
            nonlocal step_times
            step_times.append((name, elapsed))

        with callback_timer(display_metrics, "io"):
            in_bytes = process.stdout.read(bytes_to_read)

        if not in_bytes:
            break

        with callback_timer(display_metrics, "numpy"):
            frame = np.frombuffer(in_bytes, np.uint8).reshape(shape)
            binary_frame = make_frame(in_bytes)

        with callback_timer(display_metrics, "blocks"):
            blocks = to_block_numpy(binary_frame, x0=0, y0=0, width=output_width, height=output_height, invert=invert)

        yield (output_width, output_height, blocks, step_times, target_frame_time)

    process.wait()
