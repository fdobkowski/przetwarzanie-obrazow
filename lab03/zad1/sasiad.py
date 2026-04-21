import cv2
import numpy as np
import matplotlib.pyplot as plt

def steganography_with_save(carrier_path, secret_path):
    # 1. Wczytanie obrazów
    # Nośnik (carrier) i obraz do ukrycia (secret) w skali szarości
    carrier = cv2.imread(carrier_path, cv2.IMREAD_GRAYSCALE)
    secret = cv2.imread(secret_path, cv2.IMREAD_GRAYSCALE)
    
    if carrier is None or secret is None:
        print("Błąd: Nie znaleziono plików.")
        return

    # --- (a) ODCZYT UKRYTEGO OBRAZU (z najmłodszego bitu - LSB) ---
    # Operacja logiczna AND 1 izoluje bit nr 0
    extracted_secret = cv2.bitwise_and(carrier, 1) * 255
    cv2.imwrite('odczytany_sekret_a.png', extracted_secret)

    # --- (b) UKRYWANIE NOWEGO OBRAZU ---
    # Dopasowanie rozmiaru sekretu do nośnika
    secret_resized = cv2.resize(secret, (carrier.shape[1], carrier.shape[0]))
    
    # Progowanie: zamiana sekretu na obraz binarny (tylko wartości 0 i 1)
    _, secret_bin = cv2.threshold(secret_resized, 128, 1, cv2.THRESH_BINARY)

    # Krok 1: Wyzerowanie najniższego bitu w nośniku (AND 254, czyli 11111110)
    carrier_cleaned = cv2.bitwise_and(carrier, 254)
    
    # Krok 2: Wstawienie nowego sekretu (OR)
    stego_image = cv2.bitwise_or(carrier_cleaned, secret_bin)
    
    # ZAPIS NOWEGO UTWORZONEGO OBRAZU Z UKRYTĄ INFORMACJĄ
    cv2.imwrite('obraz_z_ukrytym_sekretem_b.png', stego_image)

    # --- WIZUALIZACJA ZESTAWIENIA ---
    titles = ['Oryginalny Nośnik', 'Odczytany sekret (a)', 'Nowy obraz stego (b)']
    images = [carrier, extracted_secret, stego_image]

    plt.figure(figsize=(15, 5))
    for i in range(3):
        plt.subplot(1, 3, i + 1)
        plt.imshow(images[i], cmap='gray')
        plt.title(titles[i])
        plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('zestawienie_steganografia.png')
    plt.show()

    print("Zadanie zakończone.")
    print("- Zapisano odczytany sekret: odczytany_sekret_a.png")
    print("- Zapisano obraz z nowym sekretem: obraz_z_ukrytym_sekretem_b.png")

# Uruchomienie skryptu
steganography_with_save('HelicobacterPylori_modified.png', 'CalunTurynski.png')