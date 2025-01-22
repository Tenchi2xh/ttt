from PIL import Image
import numpy as np


def load(file: str):
    image = Image.open(file).convert("1", dither=Image.NONE)
    width, height = image.size
    return image, width, height
