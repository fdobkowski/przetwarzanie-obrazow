import cv2
import numpy as np
import matplotlib.pyplot as plt


def van_cittert_deconvolution(image_path, original_path=None):
    g = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)

    orig = None
    if original_path:
        orig = cv2.imread(original_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)

    h = (
        np.array(
            [
                [1, 4, 6, 4, 1],
                [4, 16, 24, 16, 4],
                [6, 24, 36, 24, 6],
                [4, 16, 24, 16, 4],
                [1, 4, 6, 4, 1],
            ],
            dtype=np.float32,
        )
        / 256.0
    )

    f_hat = g.copy()

    iterations = [2, 5, 15]
    results = {}

    for i in range(1, max(iterations) + 1):
        blurred_est = cv2.filter2D(f_hat, -1, h, borderType=cv2.BORDER_REFLECT)

        f_hat = f_hat + (g - blurred_est)

        if i in iterations:
            results[i] = np.clip(f_hat, 0, 255).copy()

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    for idx, k in enumerate(iterations):
        result_img = results[k].astype(np.uint8)
        diff = cv2.absdiff(results[k], g)
        diff_norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX).astype(
            np.uint8
        )

        axes[0, idx].imshow(result_img, cmap="gray", vmin=0, vmax=255)
        axes[0, idx].set_title(f"Dekonwolucja (k={k})")
        axes[0, idx].axis("off")

        axes[1, idx].imshow(diff_norm, cmap="gray", vmin=0, vmax=255)
        axes[1, idx].set_title(f"Różnica do wejścia (k={k})")
        axes[1, idx].axis("off")

        cv2.imwrite(f"dekonwolucja_k{k}.png", result_img)
        cv2.imwrite(f"roznica_k{k}.png", diff_norm)

    plt.tight_layout()
    plt.savefig("zestawienie_van_cittert.png")
    plt.close()


van_cittert_deconvolution("Lego_GwiazdaSmierci_filtered.png")
