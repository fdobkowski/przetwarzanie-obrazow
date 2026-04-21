import cv2
import numpy as np
import matplotlib.pyplot as plt

def czerwony(img_gray_path, img_edge_path):
    bakterie = cv2.imread(img_gray_path, cv2.IMREAD_GRAYSCALE)
    krawedzie = cv2.imread(img_edge_path, cv2.IMREAD_GRAYSCALE)
    
    if bakterie is None or krawedzie is None:
        raise FileNotFoundError("Nie znaleziono plików.")

    merged_a = cv2.merge([bakterie, bakterie, bakterie])

    b, g, r = cv2.split(merged_a)
    
    r_out = cv2.add(r, krawedzie)

    g_out = cv2.subtract(g, krawedzie)
    b_out = cv2.subtract(b, krawedzie)

    result_a = cv2.merge([b_out, g_out, r_out])

    return result_a

try:
    wynik_a = czerwony('bakterie.png', 'bakterie_krawedzie.png')
    cv2.imwrite('wynik_bakterie_czerwone.jpg', wynik_a)
    print("[SUKCES] Zapisano wynik dla zadania (a): wynik_bakterie_czerwone.jpg")
except Exception as e:
    print(f"Błąd w zadaniu A: {e}")