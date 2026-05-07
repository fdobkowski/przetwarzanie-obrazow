import cv2
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt


def sobel_convolution(image_path):
    g = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if g is None:
        return "Błąd: Nie można wczytać obrazu."

    g = g.astype(np.float32)

    h1 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    h2 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

    g1 = convolve2d(g, h1, mode="same", boundary="symm")
    g2 = convolve2d(g, h2, mode="same", boundary="symm")

    g3 = np.sqrt(g1**2 + g2**2)

    titles = ["Oryginał (g)", "Pionowa (g1)", "Pozioma (g2)", "Obraz wyjściowy (g3)"]
    images = [g, g1, g2, g3]
    filenames = ["oryginal.png", "g1.png", "g2.png", "g3.png"]

    for image, filename, idx in zip(images, filenames, range(4)):
        out = np.abs(image) if idx < 3 else image
        cv2.imwrite(filename, np.clip(out, 0, 255).astype(np.uint8))

    plt.figure(figsize=(16, 4))
    for i in range(4):
        plt.subplot(1, 4, i + 1)
        display_img = np.abs(images[i]) if i < 3 else images[i]
        plt.imshow(display_img, cmap="gray")
        plt.title(titles[i])
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("zestawienie_sobel.png")
    plt.close()

    return g1, g2, g3


g1, g2, g3 = sobel_convolution("Escher.png")
