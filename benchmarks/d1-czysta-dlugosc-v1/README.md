---
type: benchmark
id: BENCH-CDL-V1
title: "d1-czysta-dlugosc-v1 — symulacja bez skrótu (celowany stress-test)"
status: eval-only
parents: ["BENCH-T7", "BENCH-S6"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-czysta-dlugosc-v1 🇵🇱

> **8 zadań: długa symulacja BEZ wzoru zamkniętego.** Celowany atak na zrefinowaną słabość Slayera
> wykrytą w `d1-wytrzymalosc-obliczeniowa-v1`: model radzi sobie z długimi obliczeniami **gdy istnieje
> skrót** (Fermat, wzór), lecz pęka na **czystej długości bez skrótu** (Collatz-111 → 0/3). Ten zestaw
> eliminuje skróty — trzeba wykonać N kroków symulacji.

## Hipoteza testowana
Jeśli słabość to „długość bez skrótu" (nie długość ogólnie), to zestaw złożony wyłącznie z takich zadań
powinien dać **niski pass-rate** — realizacja celu T7 („łamanie") uczciwie, bez naginania (S6).

## Pokrycie (brak wzoru zamkniętego w każdym)
| ID | Zadanie | Kroki symulacji | GT |
|---|---|---|---|
| CDL-01 | Collatz od 63 (liczba kroków) | 107 | 107 |
| CDL-02 | Collatz od 97 | 118 | 118 |
| CDL-03 | Collatz od 871 | **178** | 178 |
| CDL-04 | robot, 28 komend, Manhattan | 28 | 3 |
| CDL-05 | bubble sort [9 el.], liczba zamian | ~inwersje | 16 |
| CDL-06 | iteracja warunkowa ×20 | 20 | 2097151 |
| CDL-07 | a=(3a+1) mod 100, ×15 | 15 | 2 |
| CDL-08 | Collatz od 27, licz parzyste | ~110 + zliczanie | 70 |

## Żelazny GT (S6 pkt 1)
Wszystkie odpowiedzi **zweryfikowane symulacją programową** przed przejazdem. Żaden item nie ma
obejścia matematycznego — jedyna droga to wykonanie kroków.

## Demarkacja
Pod-kategoria wytrzymałość obliczeniowa (S6), wariant „bez skrótu". Odróżnia się od
`d1-wytrzymalosc-obliczeniowa-v1` (tam część itemów miała skrót — Fermat/wzór — i Slayer je zdawał).

## Ocena / interpretacja (S6 pkt 3)
Typ `liczba`, 3 parafrazy (AT5). Cel: niski pass-rate. Przy 0/N → test odniesienia (nemotron-4B):
jeśli odniesienie też 0 → floor (za trudne dla wszystkich); jeśli odniesienie zdaje → realna granica
Slayera.

## Powiązania
[[../../docs/10-Tezy/T7-Charakterystyka-Przez-Lamanie|T7]] · [[../../docs/25-Syntezy/S6-Warunek-Rzetelnego-Lamania|S6]] · [[../d1-wytrzymalosc-obliczeniowa-v1/README|wytrzymałość-v1]] · [[../../docs/90-Ewaluacja/Analiza-Stress-Test-D1|analiza stress-test]]
