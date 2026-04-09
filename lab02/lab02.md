# Zad1

### Pkt a)
![zad1](zad1/Plot%20of%20PlytkaFresnela.png_HiRes.png)

Dla próbkowania co 50px punkty próbkowania trafiają w strefę aliasingową i zrekonstruowany sygnał będzie tam zniekształcony. Środkowa część znajduje się w strefie, gdzie rekonstrukcja będzie możliwa. Minimalna częstotliwość, aby próbkować obraz, by jego rekonstrukcja była możliwa wynosi ok. 30px.

### Pkt b)

Na zrekonstruowanym obrazie widoczne są dwa główne efekty.
Pierwszym jest efekt bloków pikselowych widoczny w całym obrazie gdzie każda próbka została powiększona do jednolitego kwadratu bez interpolacji, co daje charakterystyczny "schodkowy" wygląd. Drugim jest aliasing widoczny na obrzeżach obrazu w postaci fałszywego wzoru szachownicowego. Pierścienie Fresnela są tam tak gęste, że próbkowanie jest zbyt rzadkie.

### Pkt c)

![zad1b](zad1/PlytkaFresnela-2.png)


# Zad2

![a](zad2/tygrysA.png)

min = 0
max = 255

```
Kontrast globalny = (255 - 0) / 255 = 1
```

```
Kontrast lokalny = 2.156
```

![b](zad2/tygrysB.png)

```
Kontrast globalny = (255 - 0) / 255 = 1
```
```
Kontrast lokalny = 2.023
```

![c](zad2/tygrysC.png)

```
Kontrast globalny = (214 - 41) / 255 ~ 0.678
```
```
Kontrast lokalny = 1.458
```

# Zad3

### PNG -> GIF

![gif](zad3/Result%20of%20osaRGB_PNG_GIF.png)

`Średnia: 97.320`

### PNG -> JPG

![jpg](zad3/Result%20of%20osaRGB_PNG_JPG.png)

`Średnia: 15.889` <- Lepsza wartość

# Zad4

![FFT](zad4/FFT%20of%20koszulaA.png)
![FFT](zad4/FFT%20of%20koszulaB.png)

Widmo obrazu A posiada dominującą oś poziomą odpowiadającą pionowym pasom koszuli, podczas gdy w widmie B oś ta jest wyraźnie obrócona zgodnie z kątem nachylenia materiału. Dodatkowe rozmyte promienie w obu widmach wynikają z różnej orientacji prążków na kołnierzyku i mankietach względem głównej części tkaniny.

![FFT](zad4/Inverse%20FFT%20of%20koszulaAA.png)
![FFT](zad4/Inverse%20FFT%20of%20koszulaAB.png)
![FFT](zad4/Inverse%20FFT%20of%20koszulaAC.png)


# Zad5

### Pkt a)

![FFT](zad5/FFT%20of%20Untitled.png)

### Pkt b)

![FFT](zad5/Plot%20of%20Inverse%20FFT%20of%20Untitled.png)
![FFT](zad5/Inverse%20FFT%20of%20Untitled.png)

Zjawisko widoczne na profilach liniowych to efekt Gibbsa. Objawia się on charakterystycznymi oscylacjami (tętnieniami) jasności w pobliżu krawędzi paska.