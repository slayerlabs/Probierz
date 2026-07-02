---
type: teza
id: BENCH-T6
title: "Model matematyczny pomiaru: IRT (2PL/3PL)"
status: w-dyskusji
parents: ["BENCH-C2", "BENCH-S3"]
author: Arkadiusz Słota
date: 2026-07-02
---

# T6 — Item Response Theory jako model pomiaru

## Teza
Pomiar zdolności modelu formalizujemy przez **Item Response Theory (IRT)**, nie przez surowy
pass-rate. Surowy odsetek poprawnych odpowiedzi zależy od doboru trudności itemów w zestawie: ten sam
model uzyskuje różny wynik na zestawie łatwym i trudnym, więc pass-rate nie jest **niezmienniczy
względem zestawu**. IRT rozdziela dwie wielkości: zdolność modelu $\theta$ oraz parametry itemu
(trudność, dyskryminacja), co pozwala oszacować $\theta$ w skali niezależnej od konkretnego zestawu.

## Model formalny
Dla modelu o zdolności $\theta$ i itemu $j$ o trudności $b_j$ i dyskryminacji $a_j$, prawdopodobieństwo
poprawnej odpowiedzi (model dwuparametrowy, 2PL):

$$
P(X_{j}=1 \mid \theta) = \frac{1}{1 + e^{-a_j\,(\theta - b_j)}}
$$

Rozszerzenie trójparametrowe (3PL) dodaje **dolną asymptotę** $c_j$ (prawdopodobieństwo poprawnej
odpowiedzi przy niskim $\theta$, np. trafienie w zadaniu wyboru):

$$
P(X_{j}=1 \mid \theta) = c_j + \frac{1 - c_j}{1 + e^{-a_j\,(\theta - b_j)}}
$$

- $\theta$ — zdolność modelu (parametr latentny, estymowany);
- $b_j$ — trudność itemu (wartość $\theta$, przy której $P = (1+c_j)/2$);
- $a_j$ — dyskryminacja (nachylenie krzywej w $b_j$; im wyższe, tym ostrzej item rozdziela modele);
- $c_j$ — zgadywanie (dolna asymptota; dla zadań generatywnych z rubryką pass/fail zwykle $c_j \approx 0$).

## Informacja itemu i dobór trudności
Informacja Fishera itemu (2PL) jako funkcja $\theta$:

$$
I_j(\theta) = a_j^{2}\, P_j(\theta)\,\bigl(1 - P_j(\theta)\bigr)
$$

Maksimum przy $P_j(\theta) = 0.5$, czyli $\theta = b_j$. Item niesie najwięcej informacji o modelach,
których zdolność jest zbliżona do jego trudności. Uzasadnia to formalnie S3: itemy łamiące wszystkie
modele ($b_j \gg \theta$) lub żadnego ($b_j \ll \theta$) mają $P(1-P) \to 0$, więc informacja bliska
zeru — należy je odrzucić. „Punkt dyskryminacji" z S3 to formalnie $\theta \approx b_j$ przy wysokim
$a_j$.

## Estymacja
Parametry itemów $\{a_j, b_j, c_j\}$ oraz zdolności modeli $\{\theta_i\}$ estymujemy łącznie z macierzy
odpowiedzi [model × item] metodą największej wiarygodności (MML) lub estymacją bayesowską. Warunkiem
identyfikowalności jest **panel wielu modeli** (S5): pojedynczy model nie pozwala rozdzielić $\theta$
od $b_j$.

## Falsyfikacja
IRT zakłada określony kształt krzywej charakterystycznej itemu (ICC). Model podlega weryfikacji przez
**dopasowanie itemu** (item fit): jeśli empiryczna proporcja poprawnych odpowiedzi w funkcji
oszacowanego $\theta$ istotnie odbiega od krzywej logistycznej dla wielu itemów → założenie 2PL/3PL
jest nietrafne dla LLM i model pomiaru wymaga rewizji (patrz AT6).

## Powiązania
parent: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · podstawa: [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · kontra: [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc|AT6]] · synteza: [[../25-Syntezy/S5-MIRT-Panel|S5]]
