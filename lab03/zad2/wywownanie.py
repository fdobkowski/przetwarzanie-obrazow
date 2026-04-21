import cv2
import numpy as np
import matplotlib.pyplot as plt

def equalization(image_path, check_levels=[40, 45, 50]):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Nie znaleziono pliku obrazu: {image_path}")

    M, N = img.shape
    total_pixels = M * N
    G = 256

   
    hist = np.histogram(img.flatten(), bins=G, range=[0, G])[0]
    h_s = hist.cumsum()

    H_s = h_s / total_pixels

    
    mapping = np.round((G - 1) * H_s).astype('uint8')

    checked_mapping_results = {g: mapping[g] for g in check_levels}
    print(f"Weryfikacja wartości wejściowych g -> Heq(g):")
    for g, Heq_g in checked_mapping_results.items():
        print(f"  {g} -> {Heq_g}")

    equalized_img = cv2.LUT(img, mapping)

    hist_equalized = np.histogram(equalized_img.flatten(), bins=G, range=[0, G])[0]

    return img, hist, h_s, H_s, mapping, checked_mapping_results, equalized_img, hist_equalized

if __name__ == "__main__":
    sciezka_koszula = 'RezydencjaDiabla.png'

    try:
        (orig_img, orig_hist, h_s, H_s, mapping, verified_vals, eq_img, eq_hist) = \
            equalization(sciezka_koszula)

        cv2.imwrite('koszulaA_equalized.jpg', eq_img)
        print("\n[SUKCES] Zapisano obraz wyjściowy: koszulaA_equalized.jpg")

        fig = plt.figure(figsize=(15, 10))
        fig.suptitle("Analiza Wyrównania Histogramu (Wykład)", fontsize=16)

        ax1 = fig.add_subplot(2, 3, 1)
        ax1.set_title("1. Obraz Wejściowy (koszulaA)")
        ax1.imshow(orig_img, cmap='gray', vmin=0, vmax=255)
        ax1.axis('off')

        ax2 = fig.add_subplot(2, 3, 2)
        ax2.set_title("2. Histogram Wejściowy h(g)")
        ax2.bar(range(256), orig_hist, color='lightgray', width=1.0)
        ax2.set_xlim([0, 256])
        ax2.set_xlabel("Jasność (g)")
        ax2.set_ylabel("Liczba pikseli")

        ax3 = fig.add_subplot(2, 3, 3)
        ax3.set_title("3. Krzywa Transformacji H_eq(g)\ni punkty weryfikacji")
        ax3.plot(range(256), mapping, color='blue', linewidth=2, label='H_eq(g)')
        
        colors = ['red', 'green', 'magenta']
        for i, g in enumerate(verified_vals.keys()):
            Heq_g = verified_vals[g]
            ax3.scatter(g, Heq_g, color=colors[i], s=100, edgecolors='black', zorder=10)
            ax3.axhline(Heq_g, color=colors[i], linestyle='--', alpha=0.5)
            ax3.axvline(g, color=colors[i], linestyle='--', alpha=0.5)
            ax3.annotate(f"{g}->{Heq_g}", (g, Heq_g), textcoords="offset points", xytext=(0,10), ha='center', color=colors[i], fontweight='bold')

        ax3.set_xlim([0, 256])
        ax3.set_ylim([0, 256])
        ax3.set_xlabel("Jasność wejściowa (g)")
        ax3.set_ylabel("Jasność wyjściowa Heq(g)")
        ax3.legend()
        ax3.grid(True, which='both', linestyle='--', linewidth=0.5)

        ax4 = fig.add_subplot(2, 3, 4)
        ax4.set_title("4. Obraz Wyjściowy Wyrównany (eq)")
        ax4.imshow(eq_img, cmap='gray', vmin=0, vmax=255)
        ax4.axis('off')

        ax5 = fig.add_subplot(2, 3, 5)
        ax5.set_title("5. Histogram Wyjściowy Heq(g)")
        ax5.bar(range(256), eq_hist, color='blue', width=1.0)
        ax5.set_xlim([0, 256])
        ax5.set_xlabel("Jasność (g)")
        ax5.set_ylabel("Liczba pikseli")
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        
        plt.savefig('wyrownanie.png', dpi=150)
        print("[SUKCES] Zapisano wykres analizy: wyrownanie.png")
        
        plt.show()

    except Exception as e:
        print(f"Wystąpił błąd: {e}")