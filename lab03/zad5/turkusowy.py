import cv2
import numpy as np
import matplotlib.pyplot as plt

def turkusowy(img_rgb_path, img_edge_path):
    bakterie_rgb = cv2.imread(img_rgb_path, cv2.IMREAD_COLOR)
    krawedzie = cv2.imread(img_edge_path, cv2.IMREAD_GRAYSCALE)
    
    if bakterie_rgb is None or krawedzie is None:
        raise FileNotFoundError("Nie znaleziono plików.")

    b, g, r = cv2.split(bakterie_rgb)
    
    krawedzie_inv = cv2.bitwise_not(krawedzie)

    r_out = cv2.bitwise_and(r, krawedzie_inv)
    
    g_out = cv2.bitwise_or(g, krawedzie)
    b_out = cv2.bitwise_or(b, krawedzie)

    result_b = cv2.merge([b_out, g_out, r_out])

    return result_b

try:
    wynik_b = turkusowy('bakterieRGB.png', 'bakterie_krawedzie.png')
    cv2.imwrite('wynik_bakterie_cyjan.jpg', wynik_b)
    print("[SUKCES] Zapisano wynik dla zadania (b): wynik_bakterie_cyjan.jpg")
except Exception as e:
    print(f"Błąd w zadaniu B: {e}")