import numpy as np


def dylatacja(
    obraz: np.ndarray,
    se: np.ndarray,
    anchor: tuple[int, int] | None = None,
) -> np.ndarray:
    h, w = obraz.shape
    kh, kw = se.shape
    ah, aw = anchor if anchor is not None else (kh // 2, kw // 2)

    wynik = np.zeros_like(obraz)

    for m in range(h):
        for n in range(w):
            if obraz[m, n] != 1:
                continue
            for i in range(kh):
                for j in range(kw):
                    if se[i, j] != 1:
                        continue
                    om, on = m + i - ah, n + j - aw
                    if 0 <= om < h and 0 <= on < w:
                        wynik[om, on] = 1

    return wynik


def wczytaj_txt(sciezka: str) -> np.ndarray:
    return np.loadtxt(sciezka, dtype=np.uint8)


def zapisz_txt(sciezka: str, obraz: np.ndarray) -> None:
    np.savetxt(sciezka, obraz, fmt="%d", delimiter="\t")


if __name__ == "__main__":
    obraz = wczytaj_txt("Untitled.txt")

    se = np.array(
        [
            [0, 0, 0, 0, 1],
            [1, 0, 0, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1],
        ],
        dtype=np.uint8,
    )
    anchor = (2, 2)

    wynik = dylatacja(obraz, se, anchor=anchor)
    zapisz_txt("dylatacja_wynik.txt", wynik)

    print("Obraz wejściowy:")
    print(obraz)
    print("\nObraz po dylatacji:")
    print(wynik)
