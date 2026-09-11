---
type: teza
id: BENCH-T8
title: "Metryka ciągła tokenizer-fair (BPB) prymarna; accuracy niewystarczająca"
status: w-dyskusji
parents: ["BENCH-T3", "BENCH-T6"]
author: Arkadiusz Słota
date: 2026-09-11
---

# T8 — Do rankingu (małych) modeli: metryka ciągła i tokenizer-fair

## Teza
Do porównywania modeli językowych — zwłaszcza małych — potrzebna jest metryka **ciągła** i **tokenizer-fair**, nie sama accuracy. Dwie własności:

1. **Ciągłość** — surowy margines/log-prob, bez progowania na 0/1. Ciągła > dyskretna na stosunku sygnał/szum (Signal&Noise, arXiv 2508.13144: perplexity/BPB biją accuracy na małych modelach).
2. **Tokenizer-fair** — mianownik = BAJTY tekstu, nie tokeny. **BPB** (bits-per-byte, `−Σ log₂ P(token|prefiks) / bajty_UTF8`) daje jedną skalę dla dowolnego vocab (32000/32768/12288/bajty) → odblokowuje porównanie **dowolnych** modeli.

## Mechanizm
- **BPB primary** — ranking „kto najlepiej modeluje polski" na wspólnym zdekontaminowanym held-oucie.
- **mean margin (ciągła d3)** — `(logP(dobre) − logP(zle))/bajt` uśredniony po rdzeniu; większa moc niż accuracy na tych SAMYCH parach.
- **accuracy = confirming**, nie primary.

## Kryterium obalenia
Teza upada, jeśli **accuracy przy realistycznym n różnicuje bliskie modele równie mocno** jak BPB/margin (ta sama moc statystyczna). 

**Empiria (2026-09-11, obala kontrtezę):** w komórce (110M, vocab 32000) accuracy przy n=148 i n=273 NIE rozróżniła {v2, v3, Slayer} (CI nakładają się). Metryka ciągła (paired-bootstrap na BPB oraz na margin) rozróżniła: **v3 < Slayer < v2 na BPB**, **v3 > v2 i v3 > Slayer na margin** — istotne. MDE BPB przy n=300 ≈ 0.003; luka 0.02 = ~9 docs. Accuracy była narzędziem o zbyt małej mocy.

## Prowieniencja
- Leaderboard: github/slayerlabs/fabryka-track branch `leaderboard-d3`, `leaderboard/LEADERBOARD.md`.
- Dane: `leaderboard/results/` (per-doc BPB, paired-bootstrap stats, SHA256 piny).
- 5 modeli: GoLLeM-45M/110M-v2/v3, Slayer-110M, Polock-125M.

---
parent: [[BENCH-T3]] · [[BENCH-T6]] · antyteza: [[../15-Antytezy/AT8-Confound-Tokenizera-Overlapping-CI|AT8]] · synteza: [[../25-Syntezy/S7-Leaderboard-BPB-Gate|S7]]
