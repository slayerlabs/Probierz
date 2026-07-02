---
type: synteza
id: BENCH-S5
title: "Model pomiaru: IRT per wymiar + panel kalibracyjny + bootstrap CI"
status: propozycja
parents: ["BENCH-T6", "BENCH-AT6", "BENCH-S3", "BENCH-S4"]
author: Arkadiusz Słota
date: 2026-07-02
---

# S5 — Operacyjny model pomiaru (rozstrzyga AT6)

## Rozstrzygnięcie
Stosujemy **IRT estymowany osobno per wymiar** D_i z taksonomii S4, nie jeden model globalny. Każdy
wymiar ma własną skalę zdolności $\theta^{(i)}$. Rozwiązuje to zarzut jednowymiarowości z AT6:
jednowymiarowy IRT jest poprawny **w obrębie** wymiaru, który przeszedł warunek obalenia S4
(rozłączność + wariancja niesprowadzalna). Wielowymiarowość konstruktu jest reprezentowana przez zbiór
osobnych modeli, nie przez jeden parametr.

## Specyfikacja
1. **Model per wymiar.** Dla wymiaru D_i i itemów $j \in D_i$: model 2PL

   $$
   P\!\left(X_{j}=1 \mid \theta^{(i)}\right) = \frac{1}{1 + e^{-a_j\,(\theta^{(i)} - b_j)}}
   $$

   Wariant 3PL ($c_j$) tylko dla itemów z realnym zgadywaniem (np. wybór zamknięty); dla itemów
   generatywnych z rubryką pass/fail przyjmujemy $c_j = 0$, co redukuje wariancję estymacji przy małym
   panelu (AT6).

2. **Panel kalibracyjny (identyfikowalność).** Estymacja wymaga panelu ≥5 modeli o zróżnicowanej
   zdolności (od słabszego do mocniejszego), zgodnie z S3. Parametry itemów $\{a_j, b_j\}$ i zdolności
   $\{\theta^{(i)}_m\}$ estymujemy łącznie z macierzy odpowiedzi [model × item] w obrębie wymiaru.
   Model oceniany (np. Slayer v49) jest jednym z węzłów panelu, nie jedynym punktem — inaczej $\theta$
   i $b$ są nieidentyfikowalne.

3. **Lokalna niezależność (kontrola).** Po estymacji liczymy statystykę reszt (np. $Q_3$) dla par
   itemów. Itemy dzielące kontekst lub schemat promptu, wykazujące zależność ponad $\theta^{(i)}$,
   grupujemy w **testlety** (item złożony oceniany łącznie) albo rozdzielamy konteksty. Adresuje to
   punkt 2 z AT6.

4. **Kwantyfikacja niepewności (mały, nielosowy panel).** Ponieważ panel jest mały i nie jest próbą
   losową (AT6), stosujemy **bootstrap dwustronny**: resampling po itemach i po modelach; raportujemy
   przedziały ufności dla $\theta^{(i)}$ każdego modelu i dla $\{a_j, b_j\}$. Modele uznajemy za
   rozróżnione na wymiarze D_i tylko, gdy przedziały ufności $\theta^{(i)}$ nie zachodzą na siebie.

5. **Dopasowanie modelu (falsyfikacja T6).** Dla każdego itemu porównujemy empiryczną proporcję
   poprawnych odpowiedzi w funkcji $\theta^{(i)}$ z krzywą logistyczną (item fit). Itemy o istotnym
   niedopasowaniu odrzucamy lub rewidujemy; systematyczne niedopasowanie w obrębie wymiaru oznacza
   nietrafność 2PL/3PL dla tego wymiaru i wymusza rewizję modelu pomiaru.

## Wynik pomiaru (co raportujemy)
Dla każdego modelu i każdego wymiaru D_i:
- $\hat{\theta}^{(i)}$ z przedziałem ufności (bootstrap);
- pass-rate surowy (dla porównania i interpretacji);
- rozkład trybów awarii (taksonomia S3);
- wskaźnik wrażliwości na parafrazę promptu (AT5).

Macierz $[\text{model} \times \hat{\theta}^{(i)}]$ zasila test rozłączności S4 (odwrócenia rankingu,
analiza czynnikowa) — pomiar i konstrukt są sprzężone: wynik S5 jest wejściem do warunku obalenia S4.

## Miejsce w metodzie
S5 zamyka etap **model matematyczny**. Kolejny etap to **baseline**: przejazd panelu modeli przez
minimalne zestawy per wymiar (audyt czystości `contamination_check.py` → 0% jako warunek wstępny),
estymacja $\theta^{(i)}$, weryfikacja warunków obalenia S4. Dopiero po baseline następuje research i
eval właściwy.

## Powiązania
parents: [[../10-Tezy/T6-IRT-Model-Pomiaru|T6]] · [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc|AT6]] · [[S3-IRT-Taksonomia|S3]] · [[S4-Taksonomia-Wymiarow|S4]] · cel: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]]
