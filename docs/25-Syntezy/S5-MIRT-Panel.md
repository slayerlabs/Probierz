---
type: synteza
id: BENCH-S5
title: "Model pomiaru: Rasch/1PL per wymiar + panel + bootstrap; 2PL warunkowo"
status: propozycja
parents: ["BENCH-T6", "BENCH-AT6", "BENCH-S3", "BENCH-S4"]
author: Arkadiusz Słota
date: 2026-07-02
---

# S5 — Operacyjny model pomiaru (rozstrzyga AT6)

## Rozstrzygnięcie
Model pomiaru estymujemy **osobno per wymiar** D_i z taksonomii S4 (każdy wymiar ma własną skalę
zdolności), ale wybór formalizmu jest **warunkowany licznością panelu**, nie ustalony z góry na 2PL.
Rozstrzyga to AT6 (nietrafny formalizm przy małym panelu): domyślny model to **1PL / Rascha**;
2PL dopuszczamy tylko po wykazaniu wystarczającej liczności; przy niemożności identyfikacji skali
absolutnej stosujemy **pomiar porównawczy** (Bradley-Terry / Elo). Wielowymiarowość konstruktu jest
reprezentowana przez zbiór osobnych modeli, nie przez jeden parametr globalny.

## Hierarchia modeli (od najmniej do najbardziej wymagającego danych)
1. **Model porównawczy (Bradley-Terry / Elo)** — pomiar zawsze dostępny, także przy najmniejszym
   panelu. Estymuje **względną** zdolność modeli na wymiarze D_i z wyników parami. Nie zakłada skali
   absolutnej ani parametrów itemów. Stanowi **pomiar kontrolny** dla każdego wymiaru.
2. **1PL / Rasch (domyślny model absolutny).** Jeden parametr trudności $b_j$ na item, dyskryminacja
   wspólna:

   $$
   P\!\left(X_j = 1 \mid \theta^{(i)}\right) = \frac{1}{1 + e^{-(\theta^{(i)} - b_j)}}
   $$

   Bilans: $J + M - 1$ parametrów przy $M \cdot J$ obserwacjach — istotnie lepiej uwarunkowany niż 2PL
   (por. tabela w AT6).
3. **2PL (warunkowo).** Dodaje dyskryminację $a_j$ per item. Dopuszczalny **tylko**, gdy: (a) obs/param
   ≥ 5 przy dostępnym M i J, oraz (b) test ilorazu wiarygodności (2PL vs 1PL) wykazuje istotną poprawę
   dopasowania przewyższającą karę za parametry (AIC/BIC). W przeciwnym razie pozostajemy przy 1PL.
   3PL ($c_j$) tylko dla itemów z realnym zgadywaniem (wybór zamknięty); dla itemów generatywnych z
   rubryką pass/fail $c_j = 0$.

## Panel kalibracyjny (identyfikowalność)
Estymacja wymaga panelu ≥5 modeli o zróżnicowanej zdolności (od słabszego do mocniejszego), zgodnie z
S3. Model oceniany (np. Slayer v49) jest jednym z węzłów panelu, nie jedynym punktem. **Ograniczenie
jawne (z AT6):** nawet 1PL przy M≈5–12 jest umiarkowanie uwarunkowany; dlatego (a) pomiar porównawczy
jest zawsze raportowany obok modelu absolutnego, (b) przy sprzeczności obu — priorytet ma porównawczy
jako mniej zależny od założeń.

## Kontrola założeń
- **Lokalna niezależność:** statystyka reszt $Q_3$ dla par itemów; itemy dzielące kontekst lub schemat
  promptu grupujemy w **testlety** albo rozdzielamy konteksty (adresuje punkt 2 z AT6).
- **Dopasowanie itemu (item fit):** empiryczna proporcja poprawnych w funkcji $\theta^{(i)}$ vs krzywa
  logistyczna; itemy o istotnym niedopasowaniu odrzucane/rewidowane. Systematyczne niedopasowanie w
  wymiarze oznacza nietrafność formalizmu i wymusza zejście do modelu porównawczego.
- **Przenośność (DIF):** differential item functioning na modelach spoza panelu kalibracyjnego.

## Kwantyfikacja niepewności (mały, nielosowy panel)
**Bootstrap dwustronny** (resampling po itemach i po modelach); przedziały ufności dla każdej estymaty
($\theta^{(i)}$ lub rangi porównawczej, $b_j$). Dwa modele uznajemy za **rozróżnione** na wymiarze D_i
tylko, gdy ich przedziały ufności nie zachodzą na siebie. Brak rozróżnienia raportowany jawnie (nie
ukrywany za punktową estymatą).

## Warunek rozłączności wymiarów (wejście do S4, wzmocnione)
**Odwrócenie rankingu** między wymiarami D_i, D_j liczy się jako dowód niezależnego sygnału **tylko
gdy jest istotne**: dla pary modeli (X, Y) przedziały ufności zdolności nie zachodzą na siebie w **obu**
wymiarach, a kierunek relacji jest przeciwny. Pojedyncze nieistotne odwrócenie (mieszczące się w CI)
traktujemy jako szum, nie dowód.

**Próg jednowymiarowości (zastępuje sztywne „90%"):** udział wariancji pierwszej składowej porównujemy
z **rozkładem odniesienia z analizy równoległej** (parallel analysis Horna: losowe permutacje macierzy
[model × wymiar]). Konstrukt uznajemy za wielowymiarowy tylko, gdy druga składowa wyjaśnia istotnie
więcej wariancji niż jej odpowiednik w danych permutowanych. Eliminuje to arbitralność progu.

## Wynik pomiaru (co raportujemy)
Dla każdego modelu i każdego wymiaru D_i:
- ranga porównawcza (Bradley-Terry / Elo) z CI — **zawsze**;
- $\hat{\theta}^{(i)}$ z CI (1PL; 2PL tylko warunkowo) — gdy identyfikowalne;
- pass-rate surowy (interpretacja);
- rozkład trybów awarii (taksonomia S3);
- wskaźnik wrażliwości na parafrazę promptu (AT5).

## Miejsce w metodzie
S5 zamyka etap **model matematyczny**. Kolejny etap to **baseline**: przejazd panelu przez minimalne
zestawy per wymiar (audyt czystości `contamination_check.py` → 0% jako warunek wstępny), estymacja
(porównawcza + 1PL), weryfikacja warunków obalenia S4. Faza **research** po baseline potwierdza liczby
(replikacja, stabilność estymat, wrażliwość na dobór panelu). Dopiero potem eval właściwy.

## Powiązania
parents: [[../10-Tezy/T6-IRT-Model-Pomiaru|T6]] · [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc|AT6]] · [[S3-IRT-Taksonomia|S3]] · [[S4-Taksonomia-Wymiarow|S4]] · cel: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]]
