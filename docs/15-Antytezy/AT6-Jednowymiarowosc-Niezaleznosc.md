---
type: antyteza
id: BENCH-AT6
title: "IRT zakłada jednowymiarowość i lokalną niezależność — LLM je naruszają"
status: w-dyskusji
parents: ["BENCH-T6"]
author: Arkadiusz Słota
date: 2026-07-02
---

# AT6 — Założenia IRT są dla LLM nietrafne (steelman)

## Najmocniejsza wersja
Klasyczny IRT (2PL/3PL, T6) opiera się na trzech założeniach, z których każde jest problematyczne dla
oceny LLM:

1. **Jednowymiarowość.** Model 2PL/3PL zakłada jeden parametr latentny $\theta$ na model. Konstrukt z
   T4 jest z założenia **wielowymiarowy** (D1–D6). Zastosowanie jednowymiarowego IRT do zestawu
   mieszającego wymiary daje $\theta$ będące nieokreśloną kombinacją wymiarów — wielkość
   nieinterpretowalną. Założenie modelu pomiaru jest wtedy sprzeczne z założeniem konstruktu.

2. **Lokalna niezależność.** IRT zakłada, że przy ustalonym $\theta$ odpowiedzi na różne itemy są
   niezależne: $P(X_j, X_k \mid \theta) = P(X_j \mid \theta)\,P(X_k \mid \theta)$. W ocenie LLM
   założenie to jest naruszane co najmniej dwoma mechanizmami: (a) itemy dzielące ten sam kontekst lub
   schemat promptu są skorelowane ponad $\theta$; (b) wrażliwość na format (AT5) wprowadza wspólny
   czynnik zakłócający — model o określonym stylu formatowania koreluje błędy między itemami niezależnie
   od zdolności.

3. **Niezmienniczość parametrów (parameter invariance).** IRT zakłada, że $b_j, a_j$ są własnością
   itemu, niezależną od populacji odpowiadających. Dla LLM populacja „odpowiadających" jest mała,
   niestacjonarna (nowe modele co kilka miesięcy) i **nie jest próbą losową** z żadnej populacji —
   modele dzielą architektury i dane treningowe. Oszacowania $b_j, a_j$ mogą nie być przenośne na
   modele spoza panelu kalibracyjnego.

## Dodatkowo: mała próba i identyfikowalność
Estymacja 3PL wymaga wielu odpowiadających na item dla stabilnego oszacowania $\{a_j, b_j, c_j\}$.
Panel LLM liczy realnie od kilku do kilkunastu modeli — o rzędy wielkości mniej niż próby ludzkie, na
których IRT jest zwykle stosowany. Przy takiej liczności estymacja 3PL (zwłaszcza $c_j$) ma wysoką
wariancję, a przedziały ufności dla $\theta$ mogą być zbyt szerokie, by rozdzielić modele.

## Konsekwencja, jeśli prawdziwa
Jednowymiarowy IRT (T6 w wersji podstawowej) jest źle specyfikowany. Bez korekty: $\theta$
nieinterpretowalne (naruszona jednowymiarowość), zaniżone błędy standardowe (naruszona lokalna
niezależność), niestabilne parametry itemów (mały, nielosowy panel). Wynik liczbowy sprawiałby wrażenie
precyzyjnego pomiaru, nie będąc nim.

## Czego wymaga, by ją odeprzeć (kierunek dla S5)
- **wielowymiarowy IRT (MIRT)** lub osobny model jednowymiarowy **per wymiar** D_i (zamiast jednego
  $\theta$ globalnego), zgodnie z warunkiem obalenia S4;
- **test lokalnej niezależności** (np. statystyka $Q_3$ na resztach) i grupowanie itemów dzielących
  kontekst w **testlety**, jeśli zależność jest istotna;
- **kwantyfikacja niepewności** adekwatna do małej próby: bootstrap po itemach i po modelach,
  raportowanie przedziałów ufności dla $\theta$ i dla parametrów itemów;
- **weryfikacja przenośności** parametrów (differential item functioning) na modelach spoza panelu
  kalibracyjnego.

## Powiązania
parent: [[../10-Tezy/T6-IRT-Model-Pomiaru|T6]] · rozstrzyga: [[../25-Syntezy/S5-MIRT-Panel|S5]] · konstrukt: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]]
