import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

src = Image.open("lwy.png").convert("L")
src_arr = np.array(src, dtype=np.float64)
H, W = src_arr.shape

D = np.array([[7, 1, 5], [3, 0, 2], [4, 8, 6]], dtype=np.float64)

T = (D + 1) / (D.size + 1) * 255

i_idx = np.arange(H)[:, None] % 3
j_idx = np.arange(W)[None, :] % 3
threshold_map = T[i_idx, j_idx]

result = np.where(src_arr >= threshold_map, 255, 0).astype(np.uint8)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
ax1.imshow(src_arr.astype(np.uint8), cmap="gray", vmin=0, vmax=255)
ax1.set_title("Oryginał")
ax1.axis("off")
ax2.imshow(result, cmap="gray", vmin=0, vmax=255)
ax2.set_title("Dithering zmiennym progiem 3×3")
ax2.axis("off")
plt.tight_layout()
plt.savefig("ordered_dither_porownanie.png", dpi=150)
plt.show()
