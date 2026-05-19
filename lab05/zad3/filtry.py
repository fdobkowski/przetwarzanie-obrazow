import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view

# =====================================================================
# I. IMPLEMENTACJE ALGORYTMÓW ZGODNIE Z PRZESŁANYMI WZORAMI
# =====================================================================


def eliminacja_izolowanych_rgb(img, theta=25.5):
    H, W, C = img.shape
    padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode="edge").astype(np.float32)
    windows = sliding_window_view(padded, (3, 3), axis=(0, 1)).reshape(H, W, C, 9)

    centers = windows[..., 4:5]

    mask_otoczenia = [0, 1, 2, 3, 5, 6, 7, 8]
    otoczenie = windows[..., mask_otoczenia]
    mu = np.mean(otoczenie, axis=-1, keepdims=True)
    roznica = np.sqrt(np.sum((centers - mu) ** 2, axis=2, keepdims=True))

    warunek = roznica >= theta
    wynik = np.where(warunek, mu, centers)

    return np.clip(wynik.squeeze(-1), 0, 255).astype(np.uint8)


def filtr_medianowy_rgb(img):
    return cv2.medianBlur(img, 3)


def filtr_sredniozakresowy_rgb(img):
    H, W, C = img.shape
    padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode="edge")
    windows = sliding_window_view(padded, (3, 3), axis=(0, 1)).reshape(H, W, C, 9)

    v_min = np.min(windows, axis=-1).astype(np.float32)
    v_max = np.max(windows, axis=-1).astype(np.float32)

    wynik = 0.5 * (v_min + v_max)
    return np.clip(wynik, 0, 255).astype(np.uint8)


def filtr_sredniej_ucietej_rgb(img, k=2):
    H, W, C = img.shape
    padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode="edge")
    windows = sliding_window_view(padded, (3, 3), axis=(0, 1)).reshape(H, W, C, 9)

    posortowane = np.sort(windows, axis=-1)

    uciete = posortowane[..., k : 9 - k]

    wynik = np.mean(uciete, axis=-1)
    return np.clip(wynik, 0, 255).astype(np.uint8)


def filtr_symmetric_nearest_neighbor_rgb(img):
    H, W, C = img.shape
    padded = np.pad(img, ((1, 1), (1, 1), (0, 0)), mode="edge").astype(np.float32)
    windows = sliding_window_view(padded, (3, 3), axis=(0, 1)).reshape(H, W, C, 9)

    centrum = windows[..., 4:5]

    pary_symetryczne = [(0, 8), (1, 7), (2, 6), (3, 5)]
    wybrane_piksele = []

    for idx_a, idx_b in pary_symetryczne:
        piksel_a = windows[..., idx_a : idx_a + 1]
        piksel_b = windows[..., idx_b : idx_b + 1]

        odleglosc_a = np.sqrt(np.sum((piksel_a - centrum) ** 2, axis=2, keepdims=True))
        odleglosc_b = np.sqrt(np.sum((piksel_b - centrum) ** 2, axis=2, keepdims=True))

        wybrany = np.where(odleglosc_a < odleglosc_b, piksel_a, piksel_b)
        wybrane_piksele.append(wybrany)

    wszystkie_wybrane = np.concatenate(wybrane_piksele, axis=-1)
    wynik = np.mean(wszystkie_wybrane, axis=-1)

    return np.clip(wynik, 0, 255).astype(np.uint8)


def main():
    sciezka_obrazu = "Jellyfish.png"
    img_rgb = cv2.imread(sciezka_obrazu)

    if img_rgb is None:
        print(f"Błąd: Plik o nazwie '{sciezka_obrazu}' nie został znaleziony.")
        return

    print("Rozpoczęto obliczenia filtrów nieliniowych na całym obrazie...")

    f_izolowane = eliminacja_izolowanych_rgb(img_rgb, theta=25.5)
    f_mediana = filtr_medianowy_rgb(img_rgb)
    f_midrange = filtr_sredniozakresowy_rgb(img_rgb)
    f_trimmed = filtr_sredniej_ucietej_rgb(img_rgb, k=2)
    f_snn = filtr_symmetric_nearest_neighbor_rgb(img_rgb)

    cv2.imwrite(
        "a_Eliminacja_Izolowanych.png", cv2.cvtColor(f_izolowane, cv2.COLOR_RGB2BGR)
    )
    cv2.imwrite("b_Medianowy.png", cv2.cvtColor(f_mediana, cv2.COLOR_RGB2BGR))
    cv2.imwrite("c_Sredniozakresowy.png", cv2.cvtColor(f_midrange, cv2.COLOR_RGB2BGR))
    cv2.imwrite("d_Srednia_Ucieta.png", cv2.cvtColor(f_trimmed, cv2.COLOR_RGB2BGR))
    cv2.imwrite("e_Symmetric_NN.png", cv2.cvtColor(f_snn, cv2.COLOR_RGB2BGR))
    print("Zapisano 5 osobnych, pełnowymiarowych obrazów wyjściowych.")

    fig, axes = plt.subplots(2, 3, figsize=(19, 11))
    lista_obrazow = [img_rgb, f_izolowane, f_mediana, f_midrange, f_trimmed, f_snn]
    tytuly = [
        "Oryginał (Pełna skala)",
        "a) Eliminacja punktów izolowanych ($\Theta = 10\%$)",
        "b) Filtr medianowy 3x3",
        "c) Filtr średniozakresowy 3x3",
        "d) Filtr średniej uciętej ($k=2$)",
        "e) Symmetric Nearest Neighbor (SNN)",
    ]

    for i, ax in enumerate(axes.ravel()):
        ax.imshow(lista_obrazow[i])
        ax.set_title(tytuly[i], fontsize=13, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("Zestawienie_Wynikowe_Pelne.png", dpi=150, bbox_inches="tight")
    print("Zapisano zbiorczy plik porównawczy: 'Zestawienie_Wynikowe_Pelne.png'.")
    plt.show()


if __name__ == "__main__":
    main()
