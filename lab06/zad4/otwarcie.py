import numpy as np


def erozja(
    obraz: np.ndarray,
    se: np.ndarray,
    anchor: tuple[int, int] | None = None,
) -> np.ndarray:
    h, w = obraz.shape
    kh, kw = se.shape
    ah, aw = anchor if anchor is not None else (kh // 2, kw // 2)

    pad = ((ah, kh - 1 - ah), (aw, kw - 1 - aw))
    obraz_p = np.pad(obraz, pad, mode="constant", constant_values=0)
    wynik = np.zeros_like(obraz)

    for m in range(h):
        for n in range(w):
            okno = obraz_p[m : m + kh, n : n + kw]
            if np.all(okno[se == 1] == 1):
                wynik[m, n] = 1

    return wynik


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


def otwarcie(
    obraz: np.ndarray,
    se: np.ndarray,
    anchor: tuple[int, int] | None = None,
) -> np.ndarray:
    po_erozji = erozja(obraz, se, anchor=anchor)
    return dylatacja(po_erozji, se, anchor=anchor)


def wczytaj_txt(sciezka: str) -> np.ndarray:
    return np.loadtxt(sciezka, dtype=np.uint8)


def zapisz_txt(sciezka: str, obraz: np.ndarray) -> None:
    np.savetxt(sciezka, obraz, fmt="%d", delimiter="\t")


if __name__ == "__main__":
    obraz = wczytaj_txt("Untitled.txt")

    se = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        dtype=np.uint8,
    )

    wynik = otwarcie(obraz, se, (1, 1))
    zapisz_txt("otwarcie_wynik.txt", wynik)

    print("Obraz wejściowy:")
    print(obraz)
    print("\nObraz po otwarciu:")
    print(wynik)
