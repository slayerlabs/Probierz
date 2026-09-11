---
type: antyteza
id: BENCH-AT8
title: "Confound tokenizera/rozmiaru + błąd overlapping-CI — metryka nie atrybutuje przyczyny"
status: w-dyskusji
parents: ["BENCH-T8"]
author: Arkadiusz Słota
date: 2026-09-11
---

# AT8 — Nawet tokenizer-fair liczba nie mówi DLACZEGO A > B

## Antyteza
Metryka (nawet BPB, tokenizer-fair jako liczba) rankuje „kto lepiej modeluje", ale **NIE atrybutuje przyczyny**. Dwie pułapki:

1. **Confound cross-cell.** Modele różniące się tokenizerem+danymi+rozmiarem naraz nie dają czystego wniosku o żadnym z tych czynników. „Niższy BPB" ≠ „lepszy trening/rozmiar" — to `badge:confound`, nie atrybucja.
2. **Błąd overlapping-CI.** Nakładanie się MARGINALNYCH przedziałów ufności dwóch modeli ≠ brak różnicy. Poprawny test różnicy to **paired-delta** (resampling tych samych itemów), nie porównanie słupków.

## Dowód (2026-09-11)
- **Flip 45M:** GoLLeM-45M (vocab 32568) „wygrał" na accuracy d3 (0.689) i „przegrał" na BPB (1.159 vs ~1.0 dla 110M/32000). **Obie liczby są cross-cell** (inny tokenizer) — żadna nie atrybutuje. Wniosek „45M najlepszy" był artefaktem szumnej osi; wniosek „110M lepszy" byłby TYM SAMYM błędem cross-cell w drugą stronę.
- **Overlapping-CI:** marginalne CI BPB {v2,v3,Slayer} nakładają się → pozornie „nieodróżnialne". Paired-delta (skorelowane różnice per-doc) daje wąskie CI rozłączne z 0 → jednak rozróżnialne. Sam wzrok na słupki mylił.

## Kryterium (kiedy antyteza słabnie)
Gdyby dwie niezależne tok-fair metryki zgadzały się KIERUNKIEM cross-cell mimo różnych tokenizerów, atrybucja byłaby bezpieczniejsza. **Empiria: rozjechały się (45M) → confound realny.** W komórce kontrolowanej (ten sam tokenizer+rozmiar) confound znika i atrybucja jest legalna.

## Prowieniencja
Te same źródła co [[BENCH-T8]]; `results/bpb_perdoc.json`, `results/bpb_stats_report.md`.

---
parent: [[BENCH-T8]] · synteza: [[../25-Syntezy/S7-Leaderboard-BPB-Gate|S7]]
