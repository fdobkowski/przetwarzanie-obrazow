import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

g = cv2.imread("Odd_Moon.png", cv2.IMREAD_GRAYSCALE)
g_float = g.astype(np.float32)

h1 = np.ones((3, 3), dtype=np.float32) / 9.0
h2 = np.array([[0, 1, -1]], dtype=np.float32)

g1 = convolve2d(g_float, h1, mode="same", boundary="symm")
g2 = convolve2d(g1, h2, mode="same", boundary="symm")

h3 = convolve2d(h1, h2, mode="full")
g3 = convolve2d(g_float, h3, mode="same", boundary="symm")

g2_8bit = np.clip(g2, 0, 255).astype(np.uint8)
g3_8bit = np.clip(g3, 0, 255).astype(np.uint8)

g2_32bit_vis = cv2.normalize(g2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

cv2.imwrite("oryginal.png", g)
cv2.imwrite("g1.png", np.clip(g1, 0, 255).astype(np.uint8))
cv2.imwrite("g2.png", g2_8bit)
cv2.imwrite("g2_32bit.png", g2_32bit_vis)
cv2.imwrite("g3.png", g3_8bit)

plt.figure(figsize=(15, 5))
plt.subplot(1, 4, 1)
plt.imshow(g1, cmap="gray")
plt.title("g1 = g * h1")
plt.axis("off")
plt.subplot(1, 4, 2)
plt.imshow(g2_8bit, cmap="gray")
plt.title("g2 (8-bit black)")
plt.axis("off")
plt.subplot(1, 4, 3)
plt.imshow(g2_32bit_vis, cmap="gray")
plt.title("g2 (32-bit gray)")
plt.axis("off")
plt.subplot(1, 4, 4)
plt.imshow(g3_8bit, cmap="gray")
plt.title("g3 = g * h3 (8-bit)")
plt.axis("off")

plt.tight_layout()
plt.show()

print("Rozmiar jądra h3:", h3.shape)
