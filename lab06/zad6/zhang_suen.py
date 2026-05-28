import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

SASIEDZTWO = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
]


def sasiedzi(obraz: np.ndarray, r: int, c: int) -> list[int]:
    h, w = obraz.shape
    out = []
    for dr, dc in SASIEDZTWO:
        rr, cc = r + dr, c + dc
        if 0 <= rr < h and 0 <= cc < w:
            out.append(int(obraz[rr, cc]))
        else:
            out.append(0)
    return out


def licznik_B(p: list[int]) -> int:
    return sum(p)


def licznik_A(p: list[int]) -> int:
    seq = p + [p[0]]
    return sum(1 for i in range(8) if seq[i] == 0 and seq[i + 1] == 1)


def warunki_krok1(p: list[int]) -> tuple[bool, dict]:
    B = licznik_B(p)
    A = licznik_A(p)
    p2, p3, p4, p5, p6, p7, p8, p9 = p
    c1 = 2 <= B <= 6
    c2 = A == 1
    c3 = (p2 * p4 * p6) == 0
    c4 = (p4 * p6 * p8) == 0
    return (c1 and c2 and c3 and c4), {
        "B": B,
        "A": A,
        "2<=B<=6": c1,
        "A==1": c2,
        "p2*p4*p6==0": c3,
        "p4*p6*p8==0": c4,
    }


def warunki_krok2(p: list[int]) -> tuple[bool, dict]:
    """Warunki usunięcia w kroku 2."""
    B = licznik_B(p)
    A = licznik_A(p)
    p2, p3, p4, p5, p6, p7, p8, p9 = p
    c1 = 2 <= B <= 6
    c2 = A == 1
    c3 = (p2 * p4 * p8) == 0
    c4 = (p2 * p6 * p8) == 0
    return (c1 and c2 and c3 and c4), {
        "B": B,
        "A": A,
        "2<=B<=6": c1,
        "A==1": c2,
        "p2*p4*p8==0": c3,
        "p2*p6*p8==0": c4,
    }


CMAP = ListedColormap(["black", "white", "#e53935"])


def rysuj(ax, obraz: np.ndarray, oznaczone: set[tuple[int, int]], tytul: str) -> None:
    plansza = obraz.astype(int).copy()
    for r, c in oznaczone:
        plansza[r, c] = 2
    ax.imshow(plansza, cmap=CMAP, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title(tytul, fontsize=9)
    ax.set_xticks(np.arange(-0.5, obraz.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, obraz.shape[0], 1), minor=True)
    ax.grid(which="minor", color="lightgray", linewidth=0.5)
    ax.tick_params(
        which="both", bottom=False, left=False, labelbottom=False, labelleft=False
    )


def jeden_podkrok(
    obraz: np.ndarray,
    warunki_fn,
) -> tuple[np.ndarray, set[tuple[int, int]]]:
    do_usuniecia: set[tuple[int, int]] = set()
    h, w = obraz.shape
    for r in range(h):
        for c in range(w):
            if obraz[r, c] != 1:
                continue
            p = sasiedzi(obraz, r, c)
            usun, _ = warunki_fn(p)
            if usun:
                do_usuniecia.add((r, c))
    nowy = obraz.copy()
    for r, c in do_usuniecia:
        nowy[r, c] = 0
    return nowy, do_usuniecia


def zhang_suen_klatki(
    obraz: np.ndarray,
) -> list[tuple[np.ndarray, set[tuple[int, int]], str]]:
    obraz = obraz.copy().astype(np.uint8)
    klatki: list[tuple[np.ndarray, set[tuple[int, int]], str]] = [
        (obraz.copy(), set(), "Stan początkowy")
    ]
    iteracja = 0
    while True:
        iteracja += 1

        _, usun1 = jeden_podkrok(obraz, warunki_krok1)
        klatki.append((obraz.copy(), usun1, f"Iter {iteracja} • krok 1: zaznaczone"))
        for r, c in usun1:
            obraz[r, c] = 0
        klatki.append((obraz.copy(), set(), f"Iter {iteracja} • krok 1: po usunięciu"))

        _, usun2 = jeden_podkrok(obraz, warunki_krok2)
        klatki.append((obraz.copy(), usun2, f"Iter {iteracja} • krok 2: zaznaczone"))
        for r, c in usun2:
            obraz[r, c] = 0
        klatki.append((obraz.copy(), set(), f"Iter {iteracja} • krok 2: po usunięciu"))

        if not usun1 and not usun2:
            break

    klatki[-1] = (klatki[-1][0], klatki[-1][1], "Wynik końcowy")
    return klatki


def rysuj_klatki(
    tytul: str, klatki: list[tuple[np.ndarray, set[tuple[int, int]], str]]
):
    n = len(klatki)
    kolumny = min(n, 5)
    wiersze = (n + kolumny - 1) // kolumny
    fig, axes = plt.subplots(wiersze, kolumny, figsize=(2.2 * kolumny, 2.4 * wiersze))
    fig.suptitle(tytul, fontsize=11)
    axes = np.atleast_1d(axes).flatten()
    for i, (obr, ozn, t) in enumerate(klatki):
        rysuj(axes[i], obr, ozn, t)
    for j in range(n, len(axes)):
        axes[j].axis("off")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    return fig


WZORY = {
    "wzor 1 (róg / L w prawym górnym)": np.array(
        [
            [0, 1, 0],
            [0, 1, 1],
            [0, 0, 0],
        ],
        dtype=np.uint8,
    ),
    "wzor 2 (krótki łuk / hak)": np.array(
        [
            [0, 0, 0],
            [0, 1, 1],
            [0, 1, 0],
        ],
        dtype=np.uint8,
    ),
    "wzor 3 (skos)": np.array(
        [
            [0, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
        ],
        dtype=np.uint8,
    ),
    "wzor 4 (kwadrat 2x2 w narożniku)": np.array(
        [
            [0, 1, 0],
            [1, 1, 0],
            [0, 0, 0],
        ],
        dtype=np.uint8,
    ),
}


if __name__ == "__main__":
    nazwy_plikow = ["a", "b", "c", "d"]
    for (nazwa, wzor), nazwa_pliku in zip(WZORY.items(), nazwy_plikow):
        obraz = np.pad(wzor, 2, mode="constant", constant_values=0)
        klatki = zhang_suen_klatki(obraz)
        fig = rysuj_klatki(nazwa, klatki[:3])
        fig.savefig(f"{nazwa_pliku}.png", dpi=150, bbox_inches="tight")
    plt.show()
