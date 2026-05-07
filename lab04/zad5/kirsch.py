import cv2
import numpy as np
import matplotlib.pyplot as plt


def kirsch_edge_detector(image_path):
    # Wczytanie obrazu wejściowego g (8-bit)
    g = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if g is None:
        return "Błąd: Nie można wczytać obrazu."

    # Definicja bazowego jądra h1 (Kirsch)
    h1 = np.array([[5, 5, 5], [-3, 0, -3], [-3, -3, -3]], dtype=np.float32)

    # Definicja wszystkich 8 jąder (rotacja o 45 stopni)
    kernels = [
        h1,
        np.array([[5, 5, -3], [5, 0, -3], [-3, -3, -3]]),  # h2 (45 deg)
        np.array([[5, -3, -3], [5, 0, -3], [5, -3, -3]]),  # h3 (90 deg)
        np.array([[-3, -3, -3], [5, 0, -3], [5, 5, -3]]),  # h4 ...
        np.array([[-3, -3, -3], [-3, 0, -3], [5, 5, 5]]),
        np.array([[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]),
        np.array([[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]]),
        np.array([[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]]),
    ]

    # Wykonanie splotów dla każdego jądra
    results = []
    for h in kernels:
        # Wykonujemy splot i zachowujemy tylko wartości dodatnie
        res = cv2.filter2D(g.astype(np.float32), -1, h)
        results.append(res)

    # Wyznaczenie obrazu f(m,n) = max{g * hi}
    f = np.zeros_like(results[0])
    for res in results:
        f = np.maximum(f, res)

    # Normalizacja do zakresu 8-bitowego (0-255)
    f_final = np.clip(f, 0, 255).astype(np.uint8)

    # Wizualizacja
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(g, cmap="gray")
    plt.title("Oryginał (g)")
    plt.subplot(1, 2, 2)
    plt.imshow(f_final, cmap="gray")
    plt.title("Krawędzie Kirscha (f)")
    plt.show()

    cv2.imwrite("krawedzie_kirscha.png", f_final)


# Wywołanie dla obrazu wejściowego
kirsch_edge_detector("Escher.png")
