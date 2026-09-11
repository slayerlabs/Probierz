---
type: benchmark
id: BENCH-D3-SKLADNIA-V3
title: "d3-skladnia-v3 — skala v2 (więcej par w rdzeniu)"
status: eval-only
parents: ["BENCH-D3-SKLADNIA-V2"]
date: 2026-09-11
---

# d3-skladnia-v3 🇵🇱

> Skala v2. **872 pary** (Morfeusz 2, 12 zjawisk), **273 w rdzeniu** (`headline_core`) — ~2× względem v2 (148).
> Ta sama metoda, ten sam pipeline i te same 3 sita co v2 (patrz `../d3-skladnia-v2/README.md`).

## Metoda i sita (identyczne z v2)

- Para minimalna forced-choice, byte-normalizowana. Chance = 0.50.
- 3 sita: **discriminating** (baseline order-4 nie rozwiązuje, `margin_norm <= 0.0`) → **novelty** (błędna fraza nieobecna w treningu, skan 11 289 649 dokumentów) → **validity** (`ratio_zle_dobre <= 0.10`).
- `headline_core = discriminating && zle_novel && validity`. Pola per-item jak w v2 (`validity`, `zle_novel`, `ratio_zle_dobre`, `discriminating`, `baseline_margin_norm`, `headline_core`).

## Liczby

- Pool: 872 (cap ~80/zjawisko). Discriminating: 342/872. **Rdzeń (headline_core): 273.**

| zjawisko | rdzeń | | zjawisko | rdzeń |
|---|---|---|---|---|
| case-prep-dat | 41 | | agr-adj-liczba | 33 |
| case-verb-dat | 40 | | case-num-gen | 28 |
| case-verb-inst | 35 | | agr-adj-rodzaj | 23 |
| past-rodzaj-subj | 18 | | case-verb-gen | 15 |
| aspekt-fut-inf | 15 | | case-neg-gen | 14 |
| case-prep-gen | 8 | | case-prep-ins | 3 |

(Cienkie: case-prep-ins 3, case-prep-gen 8 — częste przyimki „z/bez" częściej trafiają do treningu → więcej odpada na skażeniu. Aspekt 15 — ograniczony leksykon par aspektowych; do targetowego dosypania.)

## Uruchomienie

Te same narzędzia co v2 — tylko `--eval` wskazuje v3:

```
python tools/scorer_hf.py --model <id> --eval benchmarks/d3-skladnia-v3/eval.jsonl --out ll.jsonl
python tools/run_forced_choice.py --eval benchmarks/d3-skladnia-v3/eval.jsonl --scorer logprob --ll-file ll.jsonl --model <nazwa> --outdir wynik/
```

Wynik headline = accuracy (i mean margin) na `headline_core` (273). Szczegóły i „Krok 5" (filtr rdzenia): `../d3-skladnia-v2/JAK-URUCHOMIC.md`.

## Status

`eval-only`, publiczny demonstrator (spala się po ujawnieniu). 273 rdzeń daje mocniejszą oś confirming niż v2; werdykt produkcyjny + wersja tajna jak w v2.

## Zakres stosowalności (saturacja, nie sztywny rozmiar)

d3 różnicuje modele w oknie między podłogą a sufitem na rdzeniu; granica zależy od **saturacji**, nie od samej liczby parametrów.

- **Sufit:** gdy model opanuje podstawową morfoskładnię, `acc_core` → ~1.0 i benchmark przestaje różnicować. Reguła: użyteczne dopóki `acc_core < ~0.9`; powyżej → trudniejszy rdzeń.
- **Podłoga:** bardzo słaby/nietrenowany model = chance/anty-chance, też nie różnicuje.
- **Obecne modele fabryki (8M–110M) są w oknie** (0.4–0.7 na rdzeniu). Duże modele (~1.5B) prawdopodobnie blisko sufitu → d3 dla nich słabo różnicuje.
- **Metryka ciągła (mean margin) i BPB** rozciągają zakres: margin ma większą moc niż acc, BPB nie ma sufitu w użytecznym zakresie.

Krótko: d3 to benchmark reżimu małych/średnich modeli; granicę raportuj przez `acc_core` (saturacja), nie przez sztywny próg parametrów.
