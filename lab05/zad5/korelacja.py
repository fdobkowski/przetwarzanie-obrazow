import cv2
import numpy as np
import matplotlib.pyplot as plt


def znajdz_i_porownaj(wzorzec_gray, sekcja_gray):
    res = cv2.matchTemplate(wzorzec_gray, sekcja_gray, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    start_x, start_y = max_loc
    S_h, S_w = sekcja_gray.shape[:2]

    wzorzec_cropped = wzorzec_gray[start_y : start_y + S_h, start_x : start_x + S_w]

    diff = cv2.absdiff(wzorzec_cropped, sekcja_gray)
    _, mapa_roznic = cv2.threshold(diff, 35, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3, 3), np.uint8)
    mapa_roznic = cv2.dilate(mapa_roznic, kernel, iterations=1)

    return mapa_roznic, np.sum(mapa_roznic > 0)


def main():
    wzorzec = cv2.imread("TMS.png", cv2.IMREAD_GRAYSCALE)
    if wzorzec is None:
        return

    sekcje_pliki = {
        "A": "TMS_a.png",
        "B": "TMS_b.png",
        "C": "TMS_c.png",
        "D": "TMS_d.png",
        "E": "TMS_e.png",
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    axes[0].imshow(wzorzec, cmap="gray")
    axes[0].set_title("WZORZEC (TMS.png)", fontweight="bold")
    axes[0].axis("off")

    for i, (litera, nazwa) in enumerate(sekcje_pliki.items()):
        sekcja_img = cv2.imread(nazwa, cv2.IMREAD_GRAYSCALE)
        ax = axes[i + 1]

        if sekcja_img is not None:
            mapa, bledy = znajdz_i_porownaj(wzorzec, sekcja_img)
            ax.imshow(sekcja_img, cmap="gray")
            ax.imshow(mapa, cmap="Reds", alpha=0.5)
            status = "ZGODNA" if bledy < 15 else "BŁĘDNA"
            ax.set_title(
                f"Sekcja {litera}: {status}", color="green" if bledy < 15 else "red"
            )
        else:
            ax.set_title(f"Sekcja {litera}: Brak pliku")
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("Zestawienie_TMS_Wyniki.png", dpi=200)
    print("Zestawienie wygenerowane do: 'Zestawienie_TMS_Wyniki.png'")
    plt.show()


if __name__ == "__main__":
    main()
