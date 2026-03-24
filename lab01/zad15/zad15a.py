import numpy as np

M4 = np.array(
    [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float64
)

T = M4 / 16.0 * 255.0


def bayer_pattern(x_start, y_start, image, palette="1bit"):
    if isinstance(image, np.ndarray):
        arr = image.astype(np.float64)
    else:
        arr = np.array(image.convert("L"), dtype=np.float64)

    H, W = arr.shape
    size = 4

    pattern = np.zeros((size, size), dtype=np.float64)
    LEVELS = np.array([0, 64, 128, 192, 255], dtype=np.float64)
    step = 255.0 / (len(LEVELS) - 1)

    for dy in range(size):
        for dx in range(size):
            n = y_start + dy
            m = x_start + dx
            i = n % size
            j = m % size
            t = T[i, j]

            if 0 <= n < H and 0 <= m < W:
                g = arr[n, m]
            else:
                g = 0.0

            if palette == "1bit":
                pattern[dy, dx] = 255.0 if g >= t else 0.0

            elif palette == "5level":
                val = 0.0
                t_norm = M4[i, j] / 16.0
                for k in range(len(LEVELS) - 1):
                    threshold = LEVELS[k] + t_norm * step
                    if g >= threshold:
                        val = LEVELS[k + 1]
                pattern[dy, dx] = val

    pattern = pattern.astype(np.uint8)

    symbols = {0: "■", 64: "▒", 128: "▓", 192: "░", 255: "□"}
    for dy in range(size):
        for dx in range(size):
            g_val = pattern[dy, dx]
            sym = symbols.get(int(g_val), str(g_val))
            print(f"{sym:>6}  ", end=" ")
        print()
    return pattern


if __name__ == "__main__":
    g = np.array(
        [
            [176, 181, 194, 182],
            [175, 176, 163, 160],
            [172, 194, 189, 185],
            [207, 179, 181, 205],
        ],
        dtype=np.float64,
    )

    src = np.zeros((254, 254), dtype=np.float64)
    src[250:254, 250:254] = g

    pattern = bayer_pattern(x_start=250, y_start=250, image=src, palette="1bit")
