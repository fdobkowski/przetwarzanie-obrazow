import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

src = Image.open("lwy.png").convert("L")
src_arr = np.array(src, dtype=np.float64)
H, W = src_arr.shape

M4 = (
    np.array(
        [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], dtype=np.float64
    )
    / 16.0
)

LEVELS = np.array([0, 64, 128, 192, 255], dtype=np.float64)
step = 255.0 / (len(LEVELS) - 1)  # 63.75

i_idx = np.arange(H)[:, None] % 4
j_idx = np.arange(W)[None, :] % 4
t_norm = M4[i_idx, j_idx]

result = np.zeros((H, W), dtype=np.float64)
for k in range(len(LEVELS) - 1):
    threshold = LEVELS[k] + t_norm * step
    result = np.where(src_arr >= threshold, LEVELS[k + 1], result)

result = result.astype(np.uint8)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.imshow(src_arr.astype(np.uint8), cmap="gray", vmin=0, vmax=255)
ax1.set_title("Oryginał")
ax1.axis("off")
ax2.imshow(result, cmap="gray", vmin=0, vmax=255)
ax2.set_title("Bayer 4×4 – 5 poziomów {0, 64, 128, 192, 255}")
ax2.axis("off")
plt.tight_layout()
plt.savefig("bayer4_5level_porownanie.png", dpi=150)
plt.show()
