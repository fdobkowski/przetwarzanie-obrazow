import cv2
import numpy as np
import matplotlib.pyplot as plt

def plot_cumulative_histogram(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return print("Błąd: Nie znaleziono pliku.")

    hist, bins = np.histogram(img.flatten(), bins=256, range=[0,256])

    cdf = hist.cumsum()

    cdf_normalized = cdf * hist.max() / cdf.max()

    plt.figure(figsize=(10, 5))
    
    plt.bar(range(256), hist, color='lightgray', label='Histogram zwykły')
    
    plt.plot(cdf_normalized, color='blue', label='Histogram skumulowany (skalowany)')
    
    plt.title("Histogram i jego forma skumulowana")
    plt.xlabel("Poziom jasności")
    plt.ylabel("Liczba pikseli")
    plt.legend()
    plt.xlim([0, 256])
    plt.show()

plot_cumulative_histogram('RezydencjaDiabla.png')