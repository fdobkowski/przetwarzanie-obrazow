import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

src = Image.open("lwy.png").convert("L")
arr = np.array(src, dtype=np.float64)
H, W = arr.shape

T = 80
for y in range(H):
    for x in range(W):
        old = arr[y, x]
        new = 255.0 if old >= T else 0.0
        arr[y, x] = new
        err = old - new

        if x + 1 < W:
            arr[y, x + 1] += err * 7 / 16
        if y + 1 < H:
            if x - 1 >= 0:
                arr[y + 1, x - 1] += err * 3 / 16
            arr[y + 1, x] += err * 5 / 16
            if x + 1 < W:
                arr[y + 1, x + 1] += err * 1 / 16

result = np.clip(arr, 0, 255).astype(np.uint8)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.imshow(np.array(src), cmap="gray", vmin=0, vmax=255)
ax1.set_title("Oryginał")
ax1.axis("off")
ax2.imshow(result, cmap="gray", vmin=0, vmax=255)
ax2.set_title("Floyd-Steinberg  T = 80")
ax2.axis("off")
plt.tight_layout()
plt.savefig("dither_fs_T80_porownanie.png", dpi=150)
plt.show()
