import numpy as np

colors = [
    np.array([255, 0, 255]),
    np.array([128, 128, 0]),
    np.array([0, 255, 0]),
    np.array([250, 200, 200]),
    np.array([250, 255, 0]),
    np.array([200, 200, 200]),
    np.array([20, 200, 250]),
    np.array([255, 20, 20]),
    np.array([75, 100, 150]),
]

norms = [np.linalg.norm(c) for c in colors]

min_idx = np.argmin(norms)
print(
    f"a) Filtr minimalny: c{min_idx + 1} = {colors[min_idx]} (Norma: {norms[min_idx]:.2f})"
)

max_idx = np.argmax(norms)
print(
    f"b) Filtr maksymalny: c{max_idx + 1} = {colors[max_idx]} (Norma: {norms[max_idx]:.2f})"
)

sum_distances = []
for i, c_i in enumerate(colors):
    dist_sum = sum(np.linalg.norm(c_i - c_j) for c_j in colors)
    sum_distances.append(dist_sum)

median_idx = np.argmin(sum_distances)
print(
    f"c) Filtr medianowy: c{median_idx + 1} = {colors[median_idx]} (Suma odległości: {sum_distances[median_idx]:.2f})"
)
