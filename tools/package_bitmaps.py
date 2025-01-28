import re
import json
from pathlib import Path
from zipfile import ZipFile
from base64 import b64encode

import numpy as np
from PIL import Image


def encode(image: Image):
    pixels = np.array(image)
    packed_bits = np.packbits(pixels.flatten()).tobytes()
    b64 = b64encode(packed_bits)
    return b64.decode("utf-8")


def write_flat_json(objects, file):
    with open(file, "w") as f:
        f.write("[\n")
        f.write(",\n".join(json.dumps(o) for o in objects))
        f.write("\n]\n")


def package_frames():
    file = "resources/1bit_frames_by_PiiiXL.png"
    image = Image.open(file).convert("1", dither=Image.NONE)

    size = 24
    x0, y0 = 16, 288
    dx, dy = 0, 0

    frames = []

    i = 0
    while True:
        frame = image.crop((x0 + dx, y0 + dy, x0 + dx + size, y0 + dy + size))
        array = np.array(frame)
        if np.all(array == 0):
            if dx == 0:
                break
            else:
                dy += size
                dx = 0
                continue

        frames.append(encode(frame))
        dx += size

    write_flat_json(frames, "src/ttt/resources/bitmaps/frames.json")


def package_patterns():
    packs = [f"resources/1bit_patterns_pack{i}_by_lettercore.zip" for i in range(1, 4)]
    pattern = re.compile(r".*patterns/.*n.png")

    overrides = {
        65: "bug",
    }

    patterns = []

    for pack in packs:
        with ZipFile(pack) as zf:
            for file in filter(pattern.match, zf.namelist()):
                stem = Path(file).stem.rstrip("n")

                number = int(stem[:3])
                name = stem[3:]
                if number in overrides:
                    name = overrides[number]

                with zf.open(file) as f:
                    image = Image.open(f).convert("1", dither=Image.NONE)

                    patterns.append({
                        "n": name,
                        "w": image.width,
                        "h": image.height,
                        "p": encode(image),
                    })

    write_flat_json(patterns, "src/ttt/resources/bitmaps/patterns.json")

# TODO: When a --list-patterns command is made, credit the author there

if __name__ == "__main__":
    # package_patterns()
    package_frames()
