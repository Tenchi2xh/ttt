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


def to_color_blocks(np.ndarray[np.uint8_t, ndim=2] pixels, int x0, int y0, int width, int height):
    cdef int pixels_height = pixels.shape[0]
    cdef int pixels_width = pixels.shape[1]

    if pixels.dtype != np.uint8:
        raise ValueError("pixels must be a 2D NumPy array of uint8")

    cdef int output_rows = (height + 3) // 4
    cdef int output_cols = (width + 1) // 2

    cdef np.ndarray[np.uint8_t, ndim=2] binary_output = np.zeros((output_rows, output_cols), dtype=np.uint8)
    cdef np.ndarray[np.uint8_t, ndim=3] color_output = np.zeros((output_rows, output_cols, 2), dtype=np.uint8)

    cdef int row_block, col_block, dy, dx, x, y
    cdef int max_count_fg, max_count_bg, current_count, color_index
    cdef int color_counts[256]
    cdef uint8_t block_value
    cdef uint8_t fg, bg

    for row_block in range(output_rows):
        for col_block in range(output_cols):
            block_value = 0

            for color_index in range(256):
                color_counts[color_index] = 0

            # Count colors
            for dy in range(4):
                for dx in range(2):
                    x = x0 + col_block * 2 + dx
                    y = y0 + row_block * 4 + dy

                    if x < pixels_width and y < pixels_height:
                        color_index = pixels[y, x]
                        color_counts[color_index] += 1

            # Find two most common colors
            fg = bg = 0
            max_count_fg = max_count_bg = 0

            for color_index in range(256):
                current_count = color_counts[color_index]
                if current_count > max_count_fg:
                    bg = fg
                    max_count_bg = max_count_fg
                    fg = color_index
                    max_count_fg = current_count
                elif current_count > max_count_bg:
                    bg = color_index
                    max_count_bg = current_count

            # Make binary block using fg
            for dy in range(4):
                for dx in range(2):
                    x = x0 + col_block * 2 + dx
                    y = y0 + row_block * 4 + dy

                    if x < pixels_width and y < pixels_height:
                        if pixels[y, x] == fg:
                            block_value |= (1 << (dy * 2 + dx))

            binary_output[row_block, col_block] = block_value
            color_output[row_block, col_block, 0] = fg
            color_output[row_block, col_block, 1] = bg

    return binary_output, color_output
