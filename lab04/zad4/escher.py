import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d


def solve_sobel_8bit(image_path):
    g = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if g is None:
        return

    g_float = g.astype(np.float32)

    h1 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    h2 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)

    res_g1 = convolve2d(g_float, h1, mode="same", boundary="symm")
    res_g2 = convolve2d(g_float, h2, mode="same", boundary="symm")

    g1_8bit = np.clip(res_g1, 0, 255).astype(np.uint8)
    g2_8bit = np.clip(res_g2, 0, 255).astype(np.uint8)

    g3 = np.sqrt(
        np.square(g1_8bit.astype(np.float32)) + np.square(g2_8bit.astype(np.float32))
    )

    g3_8bit = np.clip(g3, 0, 255).astype(np.uint8)

    cv2.imwrite("g1.png", g1_8bit)
    cv2.imwrite("g2.png", g2_8bit)
    cv2.imwrite("g3.png", g3_8bit)

    plt.figure(figsize=(16, 5))

    images = [g, g1_8bit, g2_8bit, g3_8bit]
    titles = [
        "Oryginał (g)",
        "g1 (8-bit: Pionowa)",
        "g2 (8-bit: Pozioma)",
        "g3 (sqrt sumy kwadratów)",
    ]

    for i in range(4):
        plt.subplot(1, 4, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("zestawienie_sobel.png", dpi=150, bbox_inches="tight")
    plt.show()


solve_sobel_8bit("Escher.png")
