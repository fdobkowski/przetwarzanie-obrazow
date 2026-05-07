import cv2
import numpy as np
import matplotlib.pyplot as plt


def apply_filters(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Błąd wczytywania pliku."

    h_a = (
        np.array(
            [
                [0, 0, 1, 0, 0],
                [0, 2, 2, 2, 0],
                [1, 2, 5, 2, 1],
                [0, 2, 2, 2, 0],
                [0, 0, 1, 0, 0],
            ],
            dtype=np.float32,
        )
        / 25.0
    )

    h_b = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)

    h_c = np.array([[1, 0, -1], [1, 1, -1], [1, 0, -1]], dtype=np.float32)

    h_d = np.array([[1, -1, -1], [1, -2, -1], [1, 1, 1]], dtype=np.float32)

    res_a = cv2.filter2D(img, -1, h_a)
    res_b = cv2.filter2D(img, -1, h_b)
    res_c = cv2.filter2D(img, -1, h_c)
    res_d = cv2.filter2D(img, -1, h_d)

    titles = ["Oryginał", "h_a", "h_b", "h_c", "h_d"]
    images = [img, res_a, res_b, res_c, res_d]
    filenames = ["oryginal.png", "h_a.png", "h_b.png", "h_c.png", "h_d.png"]

    for image, filename in zip(images, filenames):
        cv2.imwrite(filename, image)

    plt.figure(figsize=(20, 10))
    for i in range(5):
        plt.subplot(1, 5, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("zestawienie_filtrowania.png")
    plt.close()


apply_filters("skarpetyIPhone.png")
