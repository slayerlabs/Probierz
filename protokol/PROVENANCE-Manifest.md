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
| `test_verification.jsonl` | slayerlabs/datasets | **SKAŻONY** ❌ | **90% overlap vs final** (60% near-verbatim, n=13) | NIE jest held-out — przeklasyfikować do treningu LUB zbudować świeży eval |
| `academy/lab/data/korpus-pl.txt` | pochodna seed_500 | trening-only | pochodna treningu | korpus hello-world GPT |

## Wniosek z pierwszego audytu
„Provenance po nazwie" zawiodło: plik `test_verification` brzmi jak eval, ale przecieka w 90%.
**Eval-only zbiory trzeba budować świeżo i audytować**, nie dziedziczyć nazwy. Brak obecnie czystego
eval-only → pierwsze zadanie produktowe: zbudować i zaudytować zestaw eval-only.

## Powiązania
[[../docs/10-Tezy/T1-Provenance-Kontaminacja|T1]] · [[../docs/25-Syntezy/S2-Audyt-Overlap|S2]] · [[../tools/contamination_check.py|narzędzie]]
