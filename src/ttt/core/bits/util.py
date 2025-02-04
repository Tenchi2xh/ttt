from functools import cache
from io import BytesIO
from urllib.parse import urlparse

import requests
from PIL import Image


def is_url(string: str) -> bool:
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@cache
def load_image(file: str):
    if is_url(file):
        response = requests.get(file)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

    else:
        image = Image.open(file)

    return image.convert("1", dither=Image.Dither.NONE)
