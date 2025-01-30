import tempfile
import wave
import threading
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass

import ffmpeg
import pyaudio
import numpy as np
from PIL import Image

from .colors import x11_256_palette
from .convert import to_blocks, to_color_blocks
from ..core.time import callback_timer


@dataclass
class Frame():
    input_width: int
    input_height: int
    output_width: int
    output_height: int
    blocks: np.ndarray
    colors: Optional[np.ndarray]
    step_times: List[Tuple[str, float]]
    target_frame_time: float


def video_metrics(file: str):
    probe = ffmpeg.probe(file)
    video_stream = next((stream for stream in probe["streams"] if stream["codec_type"] == "video"), None)
    if video_stream is None:
        raise ValueError("No video stream found in the file.")

    width = int(video_stream["width"])
    height = int(video_stream["height"])

    sar = video_stream.get("sample_aspect_ratio", "1:1")
    dar = video_stream.get("display_aspect_ratio", None)
    sar_num, sar_den = map(int, sar.split(":"))

    scaled_width = width * sar_num // sar_den
    scaled_height = height

    if dar:
        dar_num, dar_den = map(int, dar.split(":"))
        scaled_height = scaled_width * dar_den // dar_num

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
    color: bool=True,
    resize: bool=True,
    preserve_ratio=True,
    enable_metrics: bool=False,
    enable_audio: bool=True,
):
    global print

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

    pix_fmt = "pal8" if color else ("monob" if dither else "gray")

    process = ffmpeg.input(file).filter("scale", output_width, output_height)
    if color:
        process = ffmpeg.filter(
            [
                process,
                ffmpeg.input(str(get_palette()))
            ],
            "paletteuse", dither="bayer" if dither else "none",
        )

    process = (
        process
        .output("pipe:", format="rawvideo", pix_fmt=pix_fmt)
        .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    row_bytes = (output_width + 7) // 8
    shape = (output_height, row_bytes) if pix_fmt == "monob" else (output_height, output_width)

    bytes_to_read = shape[0] * shape[1]

    def make_frame_8bit(frame):
        return np.where(frame > 127, np.uint8(255), np.uint8(0))

    def make_frame_1bit(frame):
        return np.unpackbits(frame, axis=1)[:, :output_width] * 255

    make_frame = make_frame_1bit if dither else make_frame_8bit

    if not enable_metrics:
        print = lambda *_: None

    if enable_audio:
        audio_thread = threading.Thread(target=play_audio, args=(file,))
        audio_thread.start()

    while True:
        step_times = []

        def display_metrics(elapsed: float, name: str):
            nonlocal step_times
            step_times.append((name, elapsed))

        with callback_timer(display_metrics, "io"):
            in_bytes = process.stdout.read(bytes_to_read)
            if color:
                # Skip palette data
                process.stdout.read(256 * 4)

        if not in_bytes:
            break

        with callback_timer(display_metrics, "numpy"):
            frame = np.frombuffer(in_bytes, np.uint8).reshape(shape)
            if not color:
                frame = make_frame(frame)

        colors = None
        with callback_timer(display_metrics, "blocks"):
            if not color:
                blocks = to_blocks(frame, 0, 0, output_width, output_height, invert)
            else:
                blocks, colors = to_color_blocks(frame, 0, 0, output_width, output_height)

        yield Frame(
            input_width=input_width,
            input_height=input_height,
            output_width=output_width,
            output_height=output_height,
            blocks=blocks,
            colors=colors,
            step_times=step_times,
            target_frame_time=target_frame_time
        )

    process.wait()
    if audio_thread:
        audio_thread.join()


def play_audio(file: str):
    process = (
        ffmpeg
            .input(file)
            .output("pipe:", format="wav")
            .run_async(pipe_stdout=True, pipe_stderr=True)
    )

    wf = wave.open(process.stdout, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True
    )

    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    stream.stop_stream()
    stream.close()
    p.terminate()


def get_palette():
    palette_path = Path(tempfile.gettempdir()) / "x11_256_palette.png"

    if not palette_path.exists():
        palette_height = 1
        palette_width = len(x11_256_palette)

        palette_image = np.zeros((palette_height, palette_width, 3), dtype=np.uint8)
        palette_image[0, :, :] = np.array(x11_256_palette, dtype=np.uint8)

        Image.fromarray(palette_image).save(palette_path)

    return palette_path
