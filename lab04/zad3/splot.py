import cv2
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt


def solve_convolution_task(image_path):
    g = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if g is None:
        return "Błąd: Nie znaleziono pliku."

    h1 = np.ones((3, 3), dtype=np.float32) / 9.0
    h2 = np.array([[0, 1, -1]], dtype=np.float32)

    g1 = convolve2d(g, h1, mode="same", boundary="symm")
    g2 = convolve2d(g1, h2, mode="same", boundary="symm")

    h3 = convolve2d(h1, h2, mode="full")
    g3 = convolve2d(g, h3, mode="same", boundary="symm")

    difference = np.abs(g2 - g3).max()

    images = [g, g1, np.abs(g2), np.abs(g3)]
    titles = ["Oryginał g", "g1 (g * h1)", "g2 (g1 * h2)", "g3 (g * h3)"]
    filenames = ["oryginal.png", "g1.png", "g2.png", "g3.png"]

    for image, filename in zip(images, filenames):
        cv2.imwrite(filename, np.clip(image, 0, 255).astype(np.uint8))

    plt.figure(figsize=(20, 5))
    for i in range(4):
        plt.subplot(1, 4, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")
    plt.tight_layout()
    plt.savefig("zestawienie_splotu.png")
    plt.close()

    print(f"Maksymalna różnica między g2 a g3: {difference}")
    print(f"Jądro h3 (rozmiar {h3.shape}):\n{h3}")


solve_convolution_task("Odd_Moon.png")
