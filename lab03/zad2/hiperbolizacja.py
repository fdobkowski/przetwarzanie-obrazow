import cv2
import numpy as np
import matplotlib.pyplot as plt

def perform_hyperbolization(image_path, alpha=-1/3, check_levels=[40, 45, 50]):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Nie znaleziono pliku: {image_path}")

    G = 256
    hist_orig = np.histogram(img.flatten(), bins=G, range=[0, G])[0]
    h_s = hist_orig.cumsum()
    H_s = h_s / img.size

    exponent = 1 / (alpha + 1)
    mapping = np.round((G - 1) * np.power(H_s, exponent)).astype('uint8')

    print(f"Wyniki Hhyper(g) dla alpha = {alpha}:")
    for g in check_levels:
        print(f"  g = {g} -> Hhyper(g) = {mapping[g]}")

    img_hyper = cv2.LUT(img, mapping)
    hist_hyper = np.histogram(img_hyper.flatten(), bins=G, range=[0, G])[0]

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"Hiperbolizacja Histogramu ($\\alpha$ = {alpha:.2f})", fontsize=16)

    axes[0, 0].imshow(img, cmap='gray')
    axes[0, 0].set_title("Oryginał (koszulaA)")
    axes[0, 0].axis('off')

    axes[0, 1].imshow(img_hyper, cmap='gray')
    axes[0, 1].set_title("Po hiperbolizacji (Przyciemniony)")
    axes[0, 1].axis('off')

    axes[1, 0].bar(range(G), hist_orig, color='gray', width=1.0)
    axes[1, 0].set_title("Histogram wejściowy")
    axes[1, 0].set_xlim([0, G])

    axes[1, 1].bar(range(G), hist_hyper, color='black', width=1.0)
    axes[1, 1].set_title("Histogram po hiperbolizacji")
    axes[1, 1].set_xlim([0, G])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('hiperbolizacja.png')
    plt.show()

    return mapping

mapping_results = perform_hyperbolization('RezydencjaDiabla.png')