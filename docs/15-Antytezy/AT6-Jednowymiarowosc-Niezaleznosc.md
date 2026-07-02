---
type: antyteza
id: BENCH-AT6
title: "IRT jest nietrafnym formalizmem dla małego panelu modeli"
status: w-dyskusji
parents: ["BENCH-T6"]
author: Arkadiusz Słota
date: 2026-07-02
---

# AT6 — Założenia i wybór IRT są dla oceny LLM nietrafne (steelman)

## Najmocniejsza wersja
Klasyczny IRT (2PL/3PL, T6) opiera się na założeniach, z których każde jest problematyczne dla oceny
LLM, a sam wybór IRT jest wątpliwy przy realnej liczności panelu:

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

4. **Nietrafny wybór formalizmu (zarzut najcięższy).** Nawet gdyby założenia 1–3 były spełnione,
   estymacja **absolutnej** zdolności $\theta$ i dwóch parametrów itemu z panelu 5–12 modeli jest źle
   uwarunkowana (patrz „Bilans" niżej). Dla małej liczby odpowiadających lepiej uwarunkowany jest
   **pomiar porównawczy**: model Bradleya-Terry'ego lub ocena typu Elo na **parach modeli** (który z
   pary rozwiązuje item, gdy drugi zawodzi) estymuje tylko względną zdolność, wymaga mniej parametrów i
   nie zakłada absolutnej skali. IRT dostarcza więcej (skala absolutna, parametry itemów), ale przy
   dostępnej liczności ta dodatkowa struktura jest nieidentyfikowalna — płacimy wariancją za informację,
   której danych nie starcza, by wyznaczyć.

## Bilans stopni swobody (kwantyfikacja punktu 4)
2PL per wymiar ma $2J + M - 2$ parametrów ($a_j, b_j$ na item, $\theta_m$ na model, minus 2 więzy
normalizacji skali) przy $M \cdot J$ **binarnych** obserwacjach (1 bit każda).

| M modeli | J itemów | #param | #obs | obs/param |
|---|---|---|---|---|
| 5 | 10 | 23 | 50 | 2.2 |
| 8 | 10 | 26 | 80 | 3.1 |
| 12 | 20 | 50 | 240 | 4.8 |

Stabilna MLE wymaga zwykle obs/param ≥ 5–10; w psychometrii 2PL rekomenduje się N ≥ ~500
respondentów dla stabilnego $a_j$. Panel LLM (5–12 modeli) jest o 1.5–2 rzędy wielkości poniżej.
Parametr dyskryminacji $a_j$, estymowany z nachylenia krzywej po 5–12 punktach $\theta$, jest
szczególnie niestabilny.

## Konsekwencja, jeśli prawdziwa
IRT 2PL/3PL (T6 w wersji podstawowej) jest źle specyfikowany i źle uwarunkowany: $\theta$
nieinterpretowalne (naruszona jednowymiarowość), zaniżone błędy standardowe (naruszona lokalna
niezależność), niestabilne $a_j$ (mały, nielosowy panel). Wynik liczbowy sprawiałby wrażenie
precyzyjnego pomiaru, nie będąc nim.

## Czego wymaga, by ją odeprzeć (kierunek dla S5)
- **redukcja liczby parametrów:** domyślnie model **1PL / Rascha** ($a_j$ wspólne, tylko $b_j$ na item)
  — bilans $J + M - 1$ parametrów, znacznie lepiej uwarunkowany; 2PL tylko warunkowo, po wykazaniu
  wystarczającej liczności;
- **alternatywa porównawcza:** Bradley-Terry / Elo na parach modeli jako pomiar główny lub kontrolny,
  gdy skala absolutna jest nieidentyfikowalna;
- osobny model **per wymiar** D_i (nie jeden $\theta$ globalny), zgodnie z warunkiem obalenia S4;
- **test lokalnej niezależności** ($Q_3$ na resztach) i grupowanie itemów dzielących kontekst w
  **testlety**;
- **kwantyfikacja niepewności** adekwatna do małej próby: bootstrap po itemach i po modelach,
  przedziały ufności dla wszystkich estymat; brak rozdzielenia modeli raportowany jawnie;
- **weryfikacja przenośności** parametrów (differential item functioning) na modelach spoza panelu.

## Powiązania
parent: [[../10-Tezy/T6-IRT-Model-Pomiaru|T6]] · rozstrzyga: [[../25-Syntezy/S5-MIRT-Panel|S5]] · konstrukt: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]]
