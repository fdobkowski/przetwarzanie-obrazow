import cv2
import numpy as np
import matplotlib.pyplot as plt

def iterative_3class_otsu(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Nie znaleziono pliku obrazu pod ścieżką: {image_path}")

    T_prev = -100
    
    T_curr, _ = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    print(f"Start: Początkowy, globalny próg Otsu = {T_curr}")
    iteration = 1

    while abs(T_curr - T_prev) >= 2:
        T_prev = T_curr

        bg_pixels = image[image < T_prev]
        obj_pixels = image[image >= T_prev]

        mu_bg = np.mean(bg_pixels) if len(bg_pixels) > 0 else 0
        mu_obj = np.mean(obj_pixels) if len(obj_pixels) > 0 else 255

        intermediate_mask = (image >= mu_bg) & (image <= mu_obj)
        intermediate_pixels = image[intermediate_mask]

        if len(intermediate_pixels) == 0:
            print("Brak pikseli w klasie pośredniej. Zatrzymanie algorytmu.")
            break

        intermediate_2d = intermediate_pixels.reshape(1, -1)
        T_curr, _ = cv2.threshold(intermediate_2d, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        print(f"Iteracja {iteration}:")
        print(f"  Średnia tła = {mu_bg:.2f}, Średnia obiektu = {mu_obj:.2f}")
        print(f"  Analiza {len(intermediate_pixels)} pikseli pogranicza -> Nowy próg = {T_curr}")
        print(f"  Delta = {abs(T_curr - T_prev)}")
        
        iteration += 1

    print(f"\n[Zakończono] Osiągnięto warunek stopu (\u0394 < 2). Ostateczny próg = {T_curr}")

    _, final_binary = cv2.threshold(image, T_curr, 255, cv2.THRESH_BINARY)

    return image, final_binary, T_curr

if __name__ == "__main__":
    sciezka_do_pliku = 'roze.png' 
    
    try:
        oryginalny, wynikowy, ostateczny_prog = iterative_3class_otsu(sciezka_do_pliku)

        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.title("Oryginał (Grayscale)")
        plt.imshow(oryginalny, cmap='gray', vmin=0, vmax=255)
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.title(f"Wynik - Próg trójklasowy (T = {ostateczny_prog})")
        plt.imshow(wynikowy, cmap='gray', vmin=0, vmax=255)
        plt.axis('off')

        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Wystąpił błąd: {e}")