from base64 import b64decode

import numpy as np


def decode(encoded: str, width: int, height: int):
    original_shape = (height, width)
    decoded = b64decode(encoded)
    unpacked = np.unpackbits(np.frombuffer(decoded, dtype=np.uint8))
    pixels = unpacked[:np.prod(original_shape)].reshape(original_shape).astype(np.uint8) * 255

    return pixels
