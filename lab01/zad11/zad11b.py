import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

src = Image.open("lwy.png").convert("L")
src_arr = np.array(src, dtype=np.float64)
H, W = src_arr.shape

JJN = [
    (0, +1, 7 / 48),
    (0, +2, 5 / 48),
    (+1, -2, 3 / 48),
    (+1, -1, 5 / 48),
    (+1, 0, 7 / 48),
    (+1, +1, 5 / 48),
    (+1, +2, 3 / 48),
    (+2, -2, 1 / 48),
    (+2, -1, 3 / 48),
    (+2, 0, 5 / 48),
    (+2, +1, 3 / 48),
    (+2, +2, 1 / 48),
]


def quantize_1bit(value, T=80):
    return 255.0 if value >= T else 0.0


def quantize_5level(value):
    if value < 40:
        return 64.0
    elif value < 60:
        return 128.0
    elif value < 120:
        return 192.0
    else:
        return 255.0


def jjn_dither(img_arr, quantize_fn):
    arr = img_arr.copy()
    H, W = arr.shape
    for y in range(H):
        for x in range(W):
            old = arr[y, x]
            new = quantize_fn(old)
            arr[y, x] = new
            err = old - new
            for dy, dx, w in JJN:
                ny, nx = int(y + dy), int(x + dx)
                if 0 <= ny < H and 0 <= nx < W:
                    arr[ny, nx] += err * w
    return np.clip(arr, 0, 255).astype(np.uint8)


result_a = jjn_dither(src_arr, quantize_1bit)
result_b = jjn_dither(src_arr, quantize_5level)


fig, axes = plt.subplots(1, 3, figsize=(13, 5))
fig.suptitle("Dithering Jarvis-Judice-Ninke", fontsize=13)

axes[0].imshow(src_arr.astype(np.uint8), cmap="gray", vmin=0, vmax=255)
axes[0].set_title("Oryginał (szarości)")
axes[0].axis("off")

axes[1].imshow(result_a, cmap="gray", vmin=0, vmax=255)
axes[1].set_title("(a) 1-bit, próg T = 80")
axes[1].axis("off")

axes[2].imshow(result_b, cmap="gray", vmin=0, vmax=255)
axes[2].set_title("(b) 5 poziomów {0, 64, 128, 192, 255}")
axes[2].axis("off")

plt.tight_layout()
plt.savefig("jjn_porownanie.png", dpi=150, bbox_inches="tight")
plt.show()
