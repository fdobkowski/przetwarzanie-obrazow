import cv2
import numpy as np
import matplotlib.pyplot as plt


def process_shroud_final(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Błąd wczytywania pliku."

    stretched = np.clip(
        (img.astype(np.float32) - 86) * (255 / (192 - 86)), 0, 255
    ).astype(np.uint8)

    equalized = cv2.equalizeHist(img)

    inverted = cv2.bitwise_not(equalized)

    titles = ["Oryginał", "Rozproszenie", "Wyrównanie", "Inwersja"]
    images = [img, stretched, equalized, inverted]

    plt.figure(figsize=(16, 8))
    for i in range(4):
        plt.subplot(2, 4, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")

        plt.subplot(2, 4, i + 5)
        plt.hist(images[i].ravel(), 256, [0, 256], color="black")
        plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.show()


process_shroud_final("CalunTurynski.png")
