---
type: benchmark
id: BENCH-D3-SKLADNIA-V2
title: "d3-skladnia-v2 — wymiar D3: składnia / morfoskładnia (pary minimalne, skala)"
status: eval-only
parents: ["BENCH-D3-SKLADNIA-V1"]
date: 2026-09-11
---

# d3-skladnia-v2 🇵🇱

> Skala v1. **472 pary minimalne** wygenerowane automatycznie (Morfeusz 2), przepuszczone przez 3 sita.
> **148 par w rdzeniu** (`headline_core`) — powyżej progu ≥85 potrzebnego do sensownego porównania modeli.
> Ta sama modalność co v1: wybór wymuszony (forced-choice), chance = 0.50.

> ⚠️ **v2 jest PUBLICZNY = demonstrator/template.** Model trenowany po ujawnieniu może go wchłonąć
> (AT1: benchmark spala się po ujawnieniu). Do prawdziwego ślepego werdyktu trzymaj wersję zahashowaną/tajną.

## Jak powstał (generacja + 3 sita)

1. **Generacja (Morfeusz 2).** Dla 12 zjawisk morfoskładni generator tworzy pary z form podanych przez
   Morfeusz 2 (słownik odmiany). Użyto tylko **jednoznacznych rządów** (przyimki `bez`/`ku`/`przeciwko`/`nad`,
   czasowniki `szukać`/`przyglądać się`/`interesować się`/…), forma błędna = mianownik — żeby uniknąć
   pułapki, w której „błędna" forma jest w innym czytaniu poprawna (np. `w las` = biernik ruchu w v1).
   Powstało 472 kandydatów (≤32 bajty, deduplikowane).
2. **Sito discriminating** (`admission.py`, baseline n-gram order-4 na czystym held-oucie): para jest
   `discriminating`, jeśli baseline jej NIE rozwiązuje (`baseline_margin_norm <= 0.0`, byte-normalizowany).
   Przeszło **179/472**.
3. **Sito skażenia (novelty)**: pełny skan **11 289 649 dokumentów** treningu (`slayer-pl-8x3b`, 8 packów,
   równolegle). `zle_novel = true`, gdy błędna fraza NIE występuje w treningu (`freq_zle == 0`).
4. **Sito validity (ratio)**: `ratio_zle_dobre = freq_zle / freq_dobre`. Gdy `ratio > 0.10`, forma „błędna"
   jest podejrzanie częsta = prawdopodobnie gramatyczna w innym czytaniu → `validity = false` (odrzucona).

**Rdzeń** = `discriminating && zle_novel && validity` = **148 par**.

## Pola per-item w `eval.jsonl`

- `discriminating` (bool) — baseline order-4 nie rozwiązuje pary (`baseline_margin_norm <= 0.0`).
- `baseline_margin_norm` (float) — margines byte-normalizowany baseline (ujemny/zero = nie rozwiązuje).
- `contamination_scanned` (bool) — czy para była skanowana (skanowano kandydatów discriminating).
- `freq_dobre`, `freq_zle` (int|null) — liczba wystąpień frazy poprawnej/błędnej w treningu (null = nieskanowane).
- `ratio_zle_dobre` (float|null) — `freq_zle/freq_dobre`.
- `zle_novel` (bool|null) — błędna fraza nieobecna w treningu (`freq_zle == 0`).
- `validity` (bool|null) — para uznana za ważną (`ratio <= 0.10`).
- `headline_core` (bool) — `validity && zle_novel && discriminating`. Zbiór do liczenia wyniku raportowanego.

## Jak liczyć wynik

- **Wynik headline = accuracy na `headline_core` (148 par).** NIE na wszystkich 472.
- Naiwne accuracy na 472 jest nieważne (zawiera pary za-łatwe, skażone i validity-fail).
- Baseline (n-gram) na rdzeniu ma z definicji acc ≈ 0 (rdzeń = tam gdzie baseline zawodzi); rdzeń służy do
  pomiaru przewagi modelu nad baseline, nie do oceny baseline.

## Rdzeń wg zjawiska (148)

| zjawisko | rdzeń |
|---|---|
| agr-adj-liczba | 15 |
| agr-adj-rodzaj | 15 |
| aspekt-fut-inf | 15 |
| case-neg-gen | 6 |
| case-num-gen | 16 |
| case-prep-dat | 18 |
| case-prep-gen | 2 |
| case-prep-ins | 1 |
| case-verb-dat | 17 |
| case-verb-gen | 7 |
| case-verb-inst | 18 |
| past-rodzaj-subj | 18 |

(Przypadek po przyimkach `bez`/`z` — case-prep-gen/ins — ma cienki rdzeń, bo te frazy częściej trafiają do
treningu, więc więcej odpadło na sicie skażenia. Do zbalansowania w kolejnej rundzie generacji.)

## Status i ograniczenia (uczciwie)

- **148 ≥ 85** — rdzeń przekracza próg rzetelności; nadaje się do sensownego porównania modeli (A vs B),
  inaczej niż v1 (7 par). Przedziały ufności per-zjawisko dla cienkich zjawisk (ins=1, gen=2) pozostają szerokie.
- Progi (`margin_norm <= 0.0` discriminating; `ratio <= 0.10` validity) pochodzą z v1 (ustalone w rundzie pomiaru i audytu danych)
  — do potwierdzenia dla v2.
- `status: eval-only` — publiczny demonstrator; werdykt produkcyjny na wersji tajnej + realnych checkpointach.
