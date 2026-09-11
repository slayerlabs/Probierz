---
type: synteza
id: BENCH-S7
title: "Leaderboard: BPB-primary + INDISTINGUISHABLE-GATE (rozstrzyga T8 vs AT8)"
status: propozycja
parents: ["BENCH-T8", "BENCH-AT8", "BENCH-S6"]
author: Arkadiusz Słota
date: 2026-09-11
---

# S7 — Jak zestawiać modele, żeby liczba znaczyła to, co mówi

## Rozstrzygnięcie
Metryka (T8) daje moc i wspólną skalę; confound (AT8) blokuje atrybucję cross-cell. Godzenie: **rozdziel PYTANIE OD ATRYBUCJI**.

- **BPB-primary** — odpowiada „kto najlepiej modeluje polski" dla DOWOLNEGO modelu (jedna skala). To ranking modelowania języka, nie recepty.
- **mean margin (d3, ciągła)** — oś confirming o większej mocy niż accuracy; accuracy zostaje jako trzecia, pomocnicza.
- **Atrybucję przyczyny** („trening/rozmiar A > B") wolno orzekać **tylko w komórce kontrolowanej** (ten sam tokenizer_vocab i params).

## INDISTINGUISHABLE-GATE (reguła tablicy, obowiązkowa)
1. Komórka kontrolowana = wiersze o tym samym `(tokenizer_vocab, params)`.
2. Wewnątrz komórki **A > B tylko gdy CI paired-delta rozłączne z 0**. Inaczej „nieodróżnialne przy tej mocy".
3. vs chance (acc): wg położenia całego CI względem 0.50.
4. Między komórkami: dozwolony wynik, ale `badge:confound:tokenizer|size` — nigdy atrybucja.

## Bramki nośności metryki
- **Round-trip/coverage tokenizera** (SPRAWDZONE ✓): encode→decode==oryginał, 0 UNK → cross-tokenizer BPB bez ślepego pola (Polock 2.279 to realne złe modelowanie, nie kara-UNK).
- **Dekontaminacja per-model** (GRANICA): held-out nie w treningu DANEGO modelu; modele zewnętrzne bez deklaracji → `badge:unverified:leak`.
- **Gate 1 — ≥3 seedy treningowe** (OTWARTY): paired-bootstrap łapie próbkę, NIE seed treningowy → ordering pojedynczych runów jest checkpoint-level (`caveat:single-seed`), recepta dopiero po ≥3 seedach.
- **Gate 3 — paired-bootstrap istotność** (ZAMKNIĘTY ✓).
- **Zakres stosowalności / saturacja:** d3 różnicuje dopóki `acc_core < ~0.9`; wyżej → trudniejszy rdzeń. d3 = reżim mały/średni; BPB bez sufitu.

## Wynik empiryczny (2026-09-11)
Komórka (110M, 32000) rozstrzygnięta: **v3 < Slayer < v2** (BPB), potwierdzone przez mean margin na dwóch rozmiarach rdzenia (v2=148, v3=273). Trzy niezależne sygnały zgodne → ranking **checkpoint-level** (single-seed). Cross-cell (45M, Polock) tylko z badge confound.

## Prowieniencja
`leaderboard/LEADERBOARD.md` @ `leaderboard-d3` (fabryka-track); `benchmarks/d3-skladnia-v2|v3` (Probierz); `tools/{bpb_scorer,scorer_hf,run_forced_choice}.py`.

---
parents: [[../10-Tezy/T8-Metryka-Ciagla-BPB|T8]] · [[../15-Antytezy/AT8-Confound-Tokenizera-Overlapping-CI|AT8]] · [[S6-Warunek-Rzetelnego-Lamania|S6]] · decyzja: [[../20-Decyzje/D-DEC3-Leaderboard-Eksperymentalny|DEC3]]
