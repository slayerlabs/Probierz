---
type: benchmark
id: BENCH-WYT-V1
title: "d1-wytrzymalosc-obliczeniowa-v1 — długie bezbłędne łańcuchy (stress-test)"
status: eval-only
parents: ["BENCH-T7", "BENCH-S6", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-wytrzymalosc-obliczeniowa-v1 🇵🇱

> **8 zadań: długie, deterministyczne łańcuchy obliczeniowe.** Pod-kategoria **wytrzymałość
> obliczeniowa** (S6, demarkacja): mało „myślenia", dużo bezbłędnego wykonania — kumulacja błędu jest
> zabójcza. Stress-test wg T7 (łamanie do niskiego pass-rate).

## Demarkacja (S6 pkt 4)
To NIE głębia rozumowania. Strategia jest oczywista (znany algorytm: Fibonacci, modulo, Collatz);
trudność leży w **wykonaniu długiego łańcucha bez błędu**. Osobny zestaw `d1-glebia-rozumowania-v1`
mierzy drugą pod-kategorię (planowanie/wgląd). Nie sumować wskaźników — różne konstrukty.

## Gradient trudności (długość łańcucha)
| ID | Zadanie | Kroki | GT |
|---|---|---|---|
| WYT-01 | Fibonacci F(10) | ~10 | 55 |
| WYT-02 | 2 do kwadratu ×3 | 3 | 256 |
| WYT-03 | 10! mod 1000 | ~10 | 800 |
| WYT-04 | Fibonacci F(20) | ~18 | 6765 |
| WYT-05 | 7^50 mod 13 | 50 / Fermat | 10 |
| WYT-06 | Collatz od 27 (liczba kroków) | **111** | 111 |
| WYT-07 | 7^100 mod 13 | 100 / Fermat | 9 |
| WYT-08 | a(n)=a²−2a+2, a(1)=3, a(6) | 5, kwadratowo | 4294967297 |

## Żelazny GT (S6 pkt 1)
Wszystkie odpowiedzi **zweryfikowane programowo** (symulacja/iteracja) przed przejazdem — zero GT „z
głowy". WYT-08 = 2³²+1 (liczby rosną kwadratowo: 3→5→17→257→65537→4294967297).

## Ocena / stress-test
Typ `liczba` (porównanie numeryczne). 3 parafrazy/item (AT5). Cel orientacyjny: niski pass-rate (T7),
ale kryterium to bramka S6, nie sama liczba. Przy 0/N → test odniesienia (nemotron-4B) czy to granica
Slayera czy floor (S6 pkt 3).

## Powiązania
[[../../docs/10-Tezy/T7-Charakterystyka-Przez-Lamanie|T7]] · [[../../docs/25-Syntezy/S6-Warunek-Rzetelnego-Lamania|S6]] · siostra: [[../d1-glebia-rozumowania-v1/README|d1-glebia-rozumowania-v1]]
