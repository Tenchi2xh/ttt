from PIL import Image


def load(file: str):
    img = Image.open(file).convert("1", dither=Image.NONE)
    width, height = img.size
    pixels = img.load()
    return pixels, width, height
