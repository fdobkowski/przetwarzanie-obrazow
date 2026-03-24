import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

src = Image.open("potworek_pixelart.png").convert("RGBA")
src = src.resize((50, 65), Image.NEAREST)
src_arr = np.array(src, dtype=np.float64)

SRC_H, SRC_W = src_arr.shape[:2]
DST_H, DST_W = 650, 500
SCALE_X = DST_W / SRC_W
SCALE_Y = DST_H / SRC_H


def src_coords():
    """Zwraca tablice (dst_H, dst_W) z ciągłymi wsp. x_s, y_s w obrazie źródłowym."""
    dst_x = np.arange(DST_W)
    dst_y = np.arange(DST_H)

    x_s = (dst_x + 0.5) / SCALE_X - 0.5
    y_s = (dst_y + 0.5) / SCALE_Y - 0.5
    x_s = np.clip(x_s, 0, SRC_W - 1)
    y_s = np.clip(y_s, 0, SRC_H - 1)
    xx, yy = np.meshgrid(x_s, y_s)
    return xx, yy


# ─────────────────────────────────────────────────────────────────────────────
# (a) Nearest Neighbor
# ─────────────────────────────────────────────────────────────────────────────
def nearest_neighbor(arr, xx, yy):
    xi = np.round(xx).astype(int)
    yi = np.round(yy).astype(int)
    return arr[yi, xi]


# ─────────────────────────────────────────────────────────────────────────────
# (b) Nearest Neighbor – średnia
# ─────────────────────────────────────────────────────────────────────────────
def nearest_neighbor_avg2(arr, xx, yy):
    x0 = np.floor(xx).astype(int)
    x1 = np.clip(x0 + 1, 0, SRC_W - 1)
    y0 = np.floor(yy).astype(int)
    y1 = np.clip(y0 + 1, 0, SRC_H - 1)

    fx = xx - np.floor(xx)
    fy = yy - np.floor(yy)

    use_vertical = fy[..., np.newaxis] >= fx[..., np.newaxis]

    horiz = (arr[y0, x0].astype(np.float64) + arr[y0, x1].astype(np.float64)) / 2.0
    vert = (arr[y0, x0].astype(np.float64) + arr[y1, x0].astype(np.float64)) / 2.0

    return np.where(use_vertical, vert, horiz)


# ─────────────────────────────────────────────────────────────────────────────
# (c) Interpolacja dwuliniowa
# ─────────────────────────────────────────────────────────────────────────────
def bilinear(arr, xx, yy):
    x0 = np.floor(xx).astype(int)
    x1 = np.clip(x0 + 1, 0, SRC_W - 1)
    y0 = np.floor(yy).astype(int)
    y1 = np.clip(y0 + 1, 0, SRC_H - 1)

    fx = (xx - x0)[..., np.newaxis]
    fy = (yy - y0)[..., np.newaxis]

    Q00 = arr[y0, x0].astype(np.float64)
    Q10 = arr[y0, x1].astype(np.float64)
    Q01 = arr[y1, x0].astype(np.float64)
    Q11 = arr[y1, x1].astype(np.float64)

    top = Q00 * (1 - fx) + Q10 * fx
    bottom = Q01 * (1 - fx) + Q11 * fx
    return top * (1 - fy) + bottom * fy


# ─────────────────────────────────────────────────────────────────────────────
# (d) Interpolacja dwuliniowa – średnia
# ─────────────────────────────────────────────────────────────────────────────
def midrange(arr, xx, yy):
    x0 = np.floor(xx).astype(int)
    x1 = np.clip(x0 + 1, 0, SRC_W - 1)
    y0 = np.floor(yy).astype(int)
    y1 = np.clip(y0 + 1, 0, SRC_H - 1)

    Q00 = arr[y0, x0].astype(np.float64)
    Q10 = arr[y0, x1].astype(np.float64)
    Q01 = arr[y1, x0].astype(np.float64)
    Q11 = arr[y1, x1].astype(np.float64)

    def lum(q):
        return 0.299 * q[..., 0] + 0.587 * q[..., 1] + 0.114 * q[..., 2]

    L = np.stack([lum(Q00), lum(Q10), lum(Q01), lum(Q11)], axis=-1)
    quads = np.stack([Q00, Q10, Q01, Q11], axis=-2)

    idx_max = np.argmax(L, axis=-1)
    idx_min = np.argmin(L, axis=-1)

    h_idx, w_idx = np.mgrid[0:DST_H, 0:DST_W]
    px_max = quads[h_idx, w_idx, idx_max]
    px_min = quads[h_idx, w_idx, idx_min]

    return (px_max + px_min) / 2.0


xx, yy = src_coords()

results = {
    "(a) Nearest Neighbor": nearest_neighbor(src_arr, xx, yy),
    "(b) NN – śr. 2 najbliższych": nearest_neighbor_avg2(src_arr, xx, yy),
    "(c) Bilinear": bilinear(src_arr, xx, yy),
    "(d) Midrange (max+min)/2": midrange(src_arr, xx, yy),
}

file_names = {
    "(a) Nearest Neighbor": "out_a_nearest_neighbor.png",
    "(b) NN – śr. 2 najbliższych": "out_b_nn_avg2.png",
    "(c) Bilinear": "out_c_bilinear.png",
    "(d) Midrange (max+min)/2": "out_d_midrange.png",
}

for label, data in results.items():
    img = Image.fromarray(np.clip(data, 0, 255).astype(np.uint8))
    img.save(file_names[label])
    print(f"Zapisano: {file_names[label]}")

fig, axes = plt.subplots(1, 5, figsize=(20, 6))
fig.suptitle("Skalowanie 50×65 → 500×650", fontsize=14)

axes[0].imshow(src_arr.astype(np.uint8))
axes[0].set_title("Oryginał (50×65)")
axes[0].axis("off")

for ax, (label, data) in zip(axes[1:], results.items()):
    ax.imshow(np.clip(data, 0, 255).astype(np.uint8))
    ax.set_title(label, fontsize=9)
    ax.axis("off")

plt.tight_layout()
plt.savefig("porownanie_metod.png", dpi=150, bbox_inches="tight")
plt.show()
