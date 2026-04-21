import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_custom_pseudocolor(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Nie znaleziono pliku."

    lut_r = np.zeros(256, dtype=np.uint8)
    lut_g = np.zeros(256, dtype=np.uint8)
    lut_b = np.zeros(256, dtype=np.uint8)

    for g in range(256):
        if 0 <= g <= 31:
            lut_b[g] = np.interp(g, [0, 31], [128, 255])
        elif 31 < g <= 95:
            lut_b[g] = 255
        elif 95 < g <= 159:
            lut_b[g] = np.interp(g, [95, 159], [255, 0])
        else:
            lut_b[g] = 0

        if 31 <= g <= 95:
            lut_r[g] = np.interp(g, [31, 95], [0, 255])
        elif 95 < g <= 159:
            lut_r[g] = 255
        elif 159 < g <= 223:
            lut_r[g] = np.interp(g, [159, 223], [255, 0])
        else:
            lut_r[g] = 0

        if 95 <= g <= 159:
            lut_g[g] = np.interp(g, [95, 159], [0, 255])
        elif 159 < g <= 223:
            lut_g[g] = 255
        elif 223 < g <= 255:
            lut_g[g] = np.interp(g, [223, 255], [255, 128])
        else:
            lut_g[g] = 0

    out_r = cv2.LUT(img, lut_r)
    out_g = cv2.LUT(img, lut_g)
    out_b = cv2.LUT(img, lut_b)

    result_img = cv2.merge([out_b, out_g, out_r])
    
    return img, result_img

orig, pseudo = apply_custom_pseudocolor('hiperbolizacja_hyper.png')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Oryginał (Szary)")
plt.imshow(orig, cmap='gray')
plt.subplot(1, 2, 2)
plt.title("Wynik (Pseudokolor wg diagramu)")
plt.imshow(cv2.cvtColor(pseudo, cv2.COLOR_BGR2RGB))
plt.show()