import numpy as np
cimport numpy as np


ctypedef np.uint8_t uint8_t


def to_blocks(np.ndarray[np.uint8_t, ndim=2] pixels, int x0, int y0, int width, int height, bint invert):
    cdef int pixels_height = pixels.shape[0]
    cdef int pixels_width = pixels.shape[1]

    if pixels.dtype != np.uint8:
        raise ValueError("pixels must be a 2D NumPy array of uint8")

    cdef int output_rows = (height + 3) // 4
    cdef int output_cols = (width + 1) // 2

    cdef np.ndarray[np.uint8_t, ndim=2] output = np.zeros((output_rows, output_cols), dtype=np.uint8)

    cdef uint8_t compare_value = 0 if invert else 255

    cdef int row_block, col_block, dy, dx, x, y
    cdef uint8_t block_value

    for row_block in range(output_rows):
        for col_block in range(output_cols):
            block_value = 0

            for dy in range(4):
                for dx in range(2):
                    x = x0 + col_block * 2 + dx
                    y = y0 + row_block * 4 + dy

                    if x < pixels_width and y < pixels_height:
                        if pixels[y, x] == compare_value:
                            block_value |= (1 << (dy * 2 + dx))

            output[row_block, col_block] = block_value

    return output
