import numpy as np
from scipy.signal import convolve2d

f = np.array(
    [
        [255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255],
        [255, 255, 0, 0, 0, 255, 255],
        [255, 255, 0, 0, 0, 255, 255],
        [255, 255, 0, 0, 0, 255, 255],
        [255, 255, 255, 255, 255, 255, 255],
        [255, 255, 255, 255, 255, 255, 255],
    ]
)

h1 = np.array([[1], [-1], [0]])
h2 = np.array([[0], [1], [-1]])


def run_task():
    res_h1 = convolve2d(f, h1, mode="same")
    res_h2 = convolve2d(f, h2, mode="same")

    print("--- Zadanie (a): Matematyczny splot ---")
    print("Wynik f * h1:\n", res_h1)
    print("\nWynik f * h2:\n", res_h2)

    same_edges = np.array_equal(np.abs(res_h1), np.abs(res_h2))
    print(f"\nCzy oba sploty wykrywają te same krawędzie? {same_edges}")

    print("\n--- Zadanie (b): Interpretacja w ImageJ ---")

    res_8bit_h1 = np.clip(res_h1, 0, 255).astype(np.uint8)
    res_8bit_h2 = np.clip(res_h2, 0, 255).astype(np.uint8)

    print("Wynik 8-bit h1:\n", res_8bit_h1)
    print("\nWynik 8-bit h2:\n", res_8bit_h2)

    res_32bit = res_h1.astype(np.float32)
    print(
        "\nWynik 32-bit (h1): Zachowuje wartości takie jak w (a), np. -255.0\n",
        res_32bit,
    )


if __name__ == "__main__":
    run_task()
