import numpy as np
from PIL import Image

D = np.array([[7, 1, 5], [3, 0, 2], [4, 8, 6]], dtype=np.float64)

T = (D + 1) / (D.size + 1) * 255


def pixel_pattern(x, y, image):
    if isinstance(image, np.ndarray):
        g = float(image[y, x])
    else:
        g = float(np.array(image.convert("L"))[y, x])

    pattern = np.where(g >= T, 255, 0).astype(np.uint8)
    symbols = {0: "■", 255: "□"}
    for row in range(3):
        line = "  ".join(symbols[pattern[row, col]] for col in range(3))
        print(f"  {line}")

    return pattern


if __name__ == "__main__":
    src = Image.open("lwy.png").convert("L")
    pattern = pixel_pattern(x=33, y=74, image=src)
