---
type: benchmark
id: BENCH-GLEB-V1
title: "d1-glebia-rozumowania-v1 — planowanie/wgląd (stress-test)"
status: eval-only
parents: ["BENCH-METODA-LAMANIE", "BENCH-METODA-LAMANIE", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-glebia-rozumowania-v1 🇵🇱

> **6 zadań: głębia rozumowania** — planowanie strategii, wgląd, constraint satisfaction. Pod-kategoria
> **głębia** (warunek rzetelnego łamania, demarkacja): mało kroków wykonania, dużo „myślenia" — trzeba wpaść na właściwą metodę,
> a nie tylko bezbłędnie liczyć. Stress-test (łamanie modeli).

## Demarkacja (warunek rzetelnego łamania, pkt 4)
To NIE wytrzymałość obliczeniowa. Tu długi łańcuch nie pomoże — trzeba **wybrać strategię**
(inclusion-exclusion, wzór, systematyczne wyliczenie przypadków). Osobny zestaw
`d1-wytrzymalosc-obliczeniowa-v1` mierzy wykonanie długiego łańcucha. Wskaźniki raportowane osobno.

## Gradient (złożoność strategii)
| ID | Zadanie | Strategia | GT |
|---|---|---|---|
| GLEB-01 | suma 1..200 | wzór Gaussa | 20100 |
| GLEB-02 | podzielne przez 2,3 lub 5 (1..100) | inclusion-exclusion 3 zbiory | 74 |
| GLEB-03 | podzielne przez 3 lub 5, nie przez 15 (1..1000) | incl-excl z wykluczeniem | 401 |
| GLEB-04 | liczby pierwsze ≤ 200 | sito/systematyka | 46 |
| GLEB-05 | 3 domy, 3 warunki koloru | constraint satisfaction | 2 |
| GLEB-06 | permutacje {1..5} z dokładnie 1 pkt stałym | C(5,1)·D(4) | 45 |

## Żelazny GT (warunek rzetelnego łamania, pkt 1)
Wszystkie odpowiedzi **zweryfikowane programowo** (brute-force permutacji dla GLEB-05/06,
inclusion-exclusion i sito dla reszty) przed przejazdem.

## Ocena / stress-test
Typ `liczba`. 3 parafrazy/item. Cel: niski pass-rate; kryterium — warunek rzetelnego łamania. Przy 0/N →
test odniesienia (nemotron-4B) per warunek rzetelnego łamania, pkt 3.

## Powiązania
[[../../docs/metoda/Lamanie-modeli|łamanie modeli]] · [[../../docs/metoda/Lamanie-modeli|warunek rzetelnego łamania]] · siostra: [[../d1-wytrzymalosc-obliczeniowa-v1/README|d1-wytrzymalosc-obliczeniowa-v1]]
