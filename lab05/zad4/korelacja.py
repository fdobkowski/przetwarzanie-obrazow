import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter


def save_pattern_to_txt(pattern_rgb):
    R, G, B = pattern_rgb[:, :, 0], pattern_rgb[:, :, 1], pattern_rgb[:, :, 2]
    np.savetxt("wzorzec_R.txt", R, fmt="%d")
    np.savetxt("wzorzec_G.txt", G, fmt="%d")
    np.savetxt("wzorzec_B.txt", B, fmt="%d")
    print("Zapisano wartości tekstowe kanałów wzorca do plików .txt")


def correlate_channel(image_channel, pattern_channel):

    res = cv2.matchTemplate(image_channel, pattern_channel, cv2.TM_CCOEFF_NORMED)
    return res.astype(np.float32)


def find_top_5_peaks(combined_correlation, pattern_shape, threshold=0.1):

    local_max = maximum_filter(combined_correlation, size=20) == combined_correlation
    detected_peaks = local_max & (combined_correlation > threshold)

    coordinates = np.argwhere(detected_peaks)
    values = combined_correlation[detected_peaks]

    top_indices = np.argsort(values)[::-1][:5]

    peaks = []
    for idx in top_indices:
        y, x = coordinates[idx]
        peaks.append((x, y, values[idx]))
    return peaks


def main():
    img_bgr = cv2.imread("Webb's_First_Deep_Field.jpg")
    pattern_bgr = cv2.imread("wzorzecSMACS2.jpg")

    if img_bgr is None or pattern_bgr is None:
        print(
            "Błąd: Nie można załadować plików graficznych. Upewnij się, że pliki są w tym samym folderze."
        )
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    pattern_rgb = cv2.cvtColor(pattern_bgr, cv2.COLOR_BGR2RGB)

    save_pattern_to_txt(pattern_rgb)

    print("Obliczanie korelacji dla niezależnych kanałów...")
    corr_R = correlate_channel(img_rgb[:, :, 0], pattern_rgb[:, :, 0])
    corr_G = correlate_channel(img_rgb[:, :, 1], pattern_rgb[:, :, 1])
    corr_B = correlate_channel(img_rgb[:, :, 2], pattern_rgb[:, :, 2])

    corr_R = np.clip(corr_R, 0, 1)
    corr_G = np.clip(corr_G, 0, 1)
    corr_B = np.clip(corr_B, 0, 1)

    print("Mnożenie współczynników korelacji kanałów (operacja 32-bitowa)...")
    combined_corr = corr_R * corr_G * corr_B

    ph, pw, _ = pattern_rgb.shape
    peaks = find_top_5_peaks(combined_corr, (ph, pw))

    print("\n--- 5 NAJBARDZIEJ PRAWDOPODOBNYCH POZYCJI WZORCA ---")
    for i, (x, y, score) in enumerate(peaks):
        print(
            f"Pozycja {i+1}: Piksel (X: {x}, Y: {y}) | Połączony współczynnik: {score:.5f}"
        )
    result_img = img_rgb.copy()
    for i, (x, y, score) in enumerate(peaks):
        color = (0, 255, 0) if i == 0 else (255, 0, 0)
        cv2.rectangle(result_img, (x, y), (x + pw, y + ph), color, 3)
        cv2.putText(
            result_img, f"#{i+1}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
        )

    cv2.imwrite(
        "Zlokalizowany_Wzorzec_Pelny.png", cv2.cvtColor(result_img, cv2.COLOR_RGB2BGR)
    )
    print(
        "\nZapisano pełnowymiarowy obraz z ramkami do: 'Zlokalizowany_Wzorzec_Pelny.png'"
    )

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))

    im0 = axes[0].imshow(combined_corr, cmap="hot")
    axes[0].set_title(
        "32-bitowa Mapa Korelacji (Iloczyn R x G x B)", fontsize=12, fontweight="bold"
    )
    fig.colorbar(im0, ax=axes[0], orientation="horizontal", pad=0.05)

    axes[1].imshow(result_img)
    axes[1].set_title(
        "Zlokalizowane obiekty (Zielony = Pozycja #1)", fontsize=12, fontweight="bold"
    )
    axes[1].axis("off")

    plt.tight_layout()

    nazwa_zestawienia = "Zestawienie_Korelacji_Webb.png"
    plt.savefig(nazwa_zestawienia, dpi=200, bbox_inches="tight")
    print(f"Zapisano zbiorcze zestawienie graficzne do pliku: '{nazwa_zestawienia}'")

    plt.show()


if __name__ == "__main__":
    main()
