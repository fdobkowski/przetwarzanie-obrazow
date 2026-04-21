import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_birds_with_original_plot(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Błąd: Nie znaleziono pliku ptaki.png")
        return
    
    img_float = img.astype(float) / 255.0
    M, N = img_float.shape

    m_coords = np.arange(M).reshape(M, 1)
    n_coords = np.arange(N).reshape(1, N)
    window = np.sin(np.pi * m_coords / M) * np.sin(np.pi * n_coords / N)
    img_a = img_float * window

    kernel = np.ones((3,3), np.float32) / 9
    img_b = cv2.filter2D(img_a, -1, kernel)

    mean_orig = np.mean(img_float)
    mean_b = np.mean(img_b)
    gamma = np.log(mean_orig) / np.log(mean_b) if mean_b > 0 else 1.0
    img_c = np.power(np.clip(img_b, 0, 1), gamma)

    img_d = cv2.filter2D(img_float, -1, kernel)

    titles = [
        "Oryginał",
        "(a) Okno sin", 
        "(b) Wygładzanie (a)", 
        "(c) Gamma (b)", 
        "(d) Uśrednianie oryg."
    ]
    images = [img_float, img_a, img_b, img_c, img_d]

    plt.figure(figsize=(20, 5))
    
    for i in range(5):
        plt.subplot(1, 5, i + 1)
        plt.imshow((np.clip(images[i], 0, 1) * 255).astype(np.uint8), cmap='gray')
        plt.title(titles[i], fontsize=12)
        plt.axis('off')

    plt.tight_layout()
    plt.savefig('pelne_zestawienie_ptaki.png')
    plt.show()

    print(f"Wygenerowano pełne zestawienie. Wyliczona gamma: {gamma:.4f}")

process_birds_with_original_plot('ptaki.png')