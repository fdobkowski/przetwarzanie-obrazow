import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("nosorozec.png", cv2.IMREAD_GRAYSCALE)
if img is None:
    print(f"Błąd: Nie znaleziono pliku nosorozec.png")
    img = np.zeros((300, 300), dtype=np.uint8)
    cv2.putText(
        img, "BRAK NOSOROZEC.PNG", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2
    )

blurred = cv2.GaussianBlur(img, (15, 15), 3)

unsharp_mask = cv2.subtract(img, blurred)

k = 1.5
highboost = cv2.addWeighted(
    img.astype(np.float32), 1.0, unsharp_mask.astype(np.float32), k, 0
)
highboost = np.clip(highboost, 0, 255).astype(np.uint8)

cv2.imwrite("oryginal.png", img)
cv2.imwrite("blurred.png", blurred)
cv2.imwrite("unsharp_mask_view.png", unsharp_mask)
cv2.imwrite("highboost.png", highboost)

images = [img, blurred, unsharp_mask, highboost]
titles = ["Oryginał", "Wygładzony (Gauss)", "Nieostra maska", f"Highboost (k={k})"]

plt.figure(figsize=(20, 5))
for i in range(4):
    plt.subplot(1, 4, i + 1)
    plt.imshow(images[i], cmap="gray")
    plt.title(titles[i])
    plt.axis("off")

plt.tight_layout()
plt.savefig("highboost_result.png")
plt.close()
