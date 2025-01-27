def _generate_x11_palette():
    palette = []

    palette += [
        [  0,   0,   0], [205,   0,   0], [  0, 205,   0], [205, 205,   0],
        [  0,   0, 238], [205,   0, 205], [  0, 205, 205], [229, 229, 229],
        [127, 127, 127], [255,   0,   0], [  0, 255,   0], [255, 255,   0],
        [ 92,  92, 255], [255,   0, 255], [  0, 255, 255], [255, 255, 255]
    ]

    for r in range(6):
        for g in range(6):
            for b in range(6):
                palette.append([int(r * 51), int(g * 51), int(b * 51)])  # 51 = 255 / 5

    for gray in range(24):
        level = int(gray * 10 + 8)  # Scale to [8, 248]
        palette.append([level, level, level])

    return palette


x11_256_palette = _generate_x11_palette()

sorted_palette = list(sorted(x11_256_palette, key= lambda c: (c[0], c[1], c[2])))

unsort_indices = [x11_256_palette.index(color) for color in sorted_palette]
