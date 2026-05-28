import numpy as np


def hit_or_miss(
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

    maska_hit = se == 1
    maska_miss = se == 0

    for m in range(h):
        for n in range(w):
            okno = obraz_p[m : m + kh, n : n + kw]
            hit_ok = np.all(okno[maska_hit] == 1)
            miss_ok = np.all(okno[maska_miss] == 0)
            if hit_ok and miss_ok:
                wynik[m, n] = 1

    return wynik


def wczytaj_txt(sciezka: str) -> np.ndarray:
    return np.loadtxt(sciezka, dtype=np.int8)


def zapisz_txt(sciezka: str, obraz: np.ndarray) -> None:
    np.savetxt(sciezka, obraz, fmt="%d", delimiter="\t")


if __name__ == "__main__":
    obraz = wczytaj_txt("Untitled.txt")

    se = np.array(
        [
            [0, 0, -1],
            [0, 1, 1],
            [-1, 1, -1],
        ],
        dtype=np.int8,
    )
    anchor = (1, 1)

    wynik = hit_or_miss(obraz, se, anchor=anchor)
    zapisz_txt("hit_or_miss_wynik.txt", wynik)

    print("Obraz wejściowy:")
    print(obraz)
    print("\nObraz po hit-or-miss:")
    print(wynik)
