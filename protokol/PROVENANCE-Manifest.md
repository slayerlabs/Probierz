---
type: manifest
id: BENCH-PROVENANCE
title: "Manifest provenance — trening-only vs eval-only"
status: żywy-dokument
author: Arkadiusz Słota
date: 2026-06-26
---

# Manifest provenance

> Mapa danych: co MOŻE iść do treningu, co JEST zarezerwowane na eval. Granica twarda.
> Etykieta to hipoteza — kolumna **Audyt** to dowód (`contamination_check.py`). Aktualizuj po każdej zmianie.

## Zasada
- `trening-only` — wolno trenować; NIGDY jako eval.
- `eval-only` — NIGDY w treningu; wymaga audytu 0% vs cały trening przed użyciem.
- `spalony` — był eval, został ujawniony (wymiana) → wraca do puli treningowej jawnie, koniec jako eval.
- **Warianty** (`v2`, `variants_all`) = ten sam item; nie rozdzielaj train/eval po wariantach (AT2).

## Rejestr (slayerlabs)

| Dataset | Źródło | Etykieta | Audyt overlap | Uwaga |
|---|---|---|---|---|
| `seed_500_training_final.jsonl` | slayerlabs/datasets | trening-only | — (jest treningiem) | PL prompt + C# (SOLID) |
| `seed_500_training.jsonl` | slayerlabs/datasets | trening-only | wariant `final` | nie używać jako eval |
| `seed_500_training_v2.jsonl` | slayerlabs/datasets | trening-only | wariant `final` | nie używać jako eval |
| `seed_500_training_variants_all.jsonl` | slayerlabs/datasets | trening-only | wariant `final` | nie używać jako eval |
| `test_verification.jsonl` | slayerlabs/datasets | **SKAŻONY** ❌ | **100% (any-match, n=13)** — span do 217 tok, 60% frakcja≈1 | NIE jest held-out — przeklasyfikować do treningu LUB zbudować świeży eval |
| `academy/lab/data/korpus-pl.txt` | pochodna seed_500 | trening-only | pochodna treningu | korpus hello-world GPT |
| `benchmarks/csharp-solid-v1/eval.jsonl` | Probierz (od zera) | **eval-only** ✅ | **CZYSTY 0%** (any-match vs seed_500, span 0) | 15 itemów adwersarialnych SOLID, domeny spoza seed_500 |

## Wniosek z pierwszego audytu
„Provenance po nazwie" zawiodło: `test_verification` brzmi jak eval, a przecieka w **100%** (any-match).
**Eval-only buduje się świeżo i audytuje**, nie dziedziczy nazwy. Pierwszy czysty eval-only **już jest**:
`csharp-solid-v1` (15 itemów SOLID, audyt 0%). Następne: rozbudowa + kolejne domeny + drugi team (T2).

## Powiązania
[[../docs/10-Tezy/T1-Provenance-Kontaminacja|T1]] · [[../docs/25-Syntezy/S2-Audyt-Overlap|S2]] · [[../tools/contamination_check.py|narzędzie]]
