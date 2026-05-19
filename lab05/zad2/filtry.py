import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view


def knn_filter_channel(channel, k=6, window_size=3):
    pad_size = window_size // 2
    padded = np.pad(channel, pad_size, mode="edge").astype(np.float32)

    windows = sliding_window_view(padded, (window_size, window_size))
    H, W = channel.shape
    windows = windows.reshape(H, W, window_size * window_size)

    center_idx = (window_size * window_size) // 2
    centers = windows[..., center_idx : center_idx + 1]

    diffs = np.abs(windows - centers)
    idx = np.argsort(diffs, axis=-1)[..., :k]

    closest_vals = np.take_along_axis(windows, idx, axis=-1)
    filtered_channel = np.mean(closest_vals, axis=-1)

    return np.clip(filtered_channel, 0, 255).astype(np.uint8)


def knn_filter_rgb(img, k=6, window_size=3):
    """Rozdziela obraz na kanały i filtruje k-NN każdy z osobna."""
    b, g, r = cv2.split(img)
    b_f = knn_filter_channel(b, k, window_size)
    g_f = knn_filter_channel(g, k, window_size)
    r_f = knn_filter_channel(r, k, window_size)
    return cv2.merge((b_f, g_f, r_f))


def find_interesting_roi(img_gray, size=60):
    """
    Automatycznie znajduje najbardziej 'kontrastowy/ciekawy' fragment obrazu
    (np. spadochron, tekst), obliczając odchylenie standardowe w oknach.
    """
    H, W = img_gray.shape
    best_std = -1
    best_coords = (H // 2, W // 2)

    for y in range(size, H - size, 20):
        for x in range(size, W - size, 20):
            crop = img_gray[y - size : y + size, x - size : x + size]
            current_std = np.std(crop)
            if current_std > best_std:
                best_std = current_std
                best_coords = (y, x)

    return best_coords


def main():
    img_path = "spadochronNASA.png"
    img_bgr = cv2.imread(img_path)

    if img_bgr is None:
        print(f"Błąd: Nie można wczytać pliku '{img_path}'.")
        return

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    print("Rozpoczęto przetwarzanie filtrów liniowych...")
    avg_rgb = cv2.blur(img_rgb, (3, 3))
    gauss_rgb = cv2.GaussianBlur(img_rgb, (3, 3), 2)

    print(
        "Rozpoczęto przetwarzanie nieliniowego filtra k-NN (to może chwilę potrwać)..."
    )
    knn_rgb = knn_filter_rgb(img_rgb, k=6, window_size=3)

    cv2.imwrite("1_Oryginal.png", img_bgr)
    cv2.imwrite("2_Usredniajacy.png", cv2.cvtColor(avg_rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite("3_Gauss.png", cv2.cvtColor(gauss_rgb, cv2.COLOR_RGB2BGR))
    cv2.imwrite("4_kNN.png", cv2.cvtColor(knn_rgb, cv2.COLOR_RGB2BGR))
    print("Zapisano 4 obrazy w oryginalnym rozmiarze.")

    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    cy, cx = find_interesting_roi(img_gray, size=50)
    zoom_size = 100

    y1, y2 = cy - zoom_size, cy + zoom_size
    x1, x2 = cx - zoom_size, cx + zoom_size

    crop_oryg = img_rgb[y1:y2, x1:x2]
    crop_avg = avg_rgb[y1:y2, x1:x2]
    crop_gaus = gauss_rgb[y1:y2, x1:x2]
    crop_knn = knn_rgb[y1:y2, x1:x2]

    fig, axes = plt.subplots(1, 4, figsize=(20, 6))
    crops = [crop_oryg, crop_avg, crop_gaus, crop_knn]
    titles = [
        "Oryginał (Zoom)",
        "Uśredniający 3x3 (Zoom)",
        "Gauss 3x3 (Zoom)",
        "k-NN k=6 (Zoom)",
    ]

    for ax, crop_img, title in zip(axes, crops, titles):
        ax.imshow(crop_img)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.axis("off")

    plt.tight_layout()

    zestawienie_filename = "5_Zestawienie_Zoom.png"
    plt.savefig(zestawienie_filename, dpi=200, bbox_inches="tight")
    print(f"Zapisano piąty obraz: '{zestawienie_filename}'.")

    plt.show()


if __name__ == "__main__":
    main()
