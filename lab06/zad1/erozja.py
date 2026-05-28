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


def wczytaj_txt(sciezka: str) -> np.ndarray:
    return np.loadtxt(sciezka, dtype=np.uint8)


def zapisz_txt(sciezka: str, obraz: np.ndarray) -> None:
    np.savetxt(sciezka, obraz, fmt="%d", delimiter="\t")


if __name__ == "__main__":
    obraz = wczytaj_txt("Untitled.txt")

    se = np.array(
        [
            [1, 1, 1],
        ],
        dtype=np.uint8,
    )
    anchor = (0, 2)

    wynik = erozja(obraz, se, anchor=anchor)
    zapisz_txt("erozja_wynik.txt", wynik)

    print("Obraz wejściowy:")
    print(obraz)
    print("\nObraz po erozji:")
    print(wynik)
