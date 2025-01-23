import re
import json
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
from base64 import b64encode
from itertools import groupby

import numpy as np
from PIL import Image


packs = [f"resources/1bit_patterns_pack{i}_by_lettercore.zip" for i in range(1, 4)]
pattern = re.compile(r".*patterns/.*n.png")

overrides = {
    65: "bug",
}


def rle(data: str) -> str:
    return "".join(f"{x}{sum(1 for _ in y)}" for x, y in groupby(data))


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
                b = f.read()
                bytes = BytesIO(b)
                image = Image.open(f).convert("1", dither=Image.NONE)
                width, height = image.size

                pixels = np.array(image)
                packed_bits = np.packbits(pixels.flatten()).tobytes()
                b64 = b64encode(packed_bits)

                patterns.append({
                    "n": name,
                    "w": width,
                    "h": height,
                    "p": b64.decode("utf-8"),
                })


with open("src/ttt/resources/patterns/patterns.json", "w") as f:
    f.write("[\n")
    f.write(",\n".join(json.dumps(p) for p in patterns))
    f.write("\n]\n")

# TODO: When a --list-patterns command is made, credit the author there
