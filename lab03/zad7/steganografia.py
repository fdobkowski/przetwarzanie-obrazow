import cv2
import numpy as np
import matplotlib.pyplot as plt


def steganografia(carrier_path, secret_path):
    carrier = cv2.imread(carrier_path, cv2.IMREAD_GRAYSCALE)
    secret = cv2.imread(secret_path, cv2.IMREAD_GRAYSCALE)

    if carrier is None or secret is None:
        return "Błąd: Nie znaleziono plików."

    secret = cv2.resize(secret, (carrier.shape[1], carrier.shape[0]))

    _, secret_bin = cv2.threshold(secret, 128, 1, cv2.THRESH_BINARY)

    extracted_secret = cv2.bitwise_and(carrier, 1) * 255

    carrier_cleaned = cv2.bitwise_and(carrier, 254)

    stego_image = cv2.bitwise_or(carrier_cleaned, secret_bin)

    cv2.imwrite("stego_image.png", stego_image)

    titles = [
        "Oryginalny Nośnik",
        "Odczytany sekret (a)",
        "Nowy sekret (bin)",
        "Obraz po ukryciu (b)",
    ]
    images = [carrier, extracted_secret, secret_bin * 255, stego_image]

    plt.figure(figsize=(16, 8))
    for i in range(4):
        plt.subplot(1, 4, i + 1)
        plt.imshow(images[i], cmap="gray")
        plt.title(titles[i])
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("wynik_steganografii.png")

    plt.show()

    diff = cv2.absdiff(carrier, stego_image)
    print(f"Maksymalna różnica jasności: {np.max(diff)}")  # Powinna wynosić 1


steganografia("HelicobacterPylori_modified.png", "CalunTurynski.png")
