---
type: benchmark
id: BENCH-CSHARP-SOLID-V1
title: "csharp-solid-v1 — adwersarialny benchmark SOLID (PL spec → C#)"
status: eval-only
author: Arkadiusz Słota
date: 2026-06-26
---

# csharp-solid-v1 🇵🇱

> **15 adwersarialnych zadań** „specyfikacja po polsku → kod C#", które celują w **łamanie naiwnego
> stosowania SOLID**. Każdy item ma wbudowaną **pułapkę** kuszącą do anty-wzorca. Mierzymy, czy model
> jej ulega.

> ⚠️ **v1 jest PUBLICZNY = demonstrator/template.** Skoro leży w repo, modele trenowane później mogą go
> wchłonąć (AT1: benchmark spala się po ujawnieniu). Traktuj jak **wzór formatu + dowód metody** (audyt
> 0%), NIE jako tajny held-out. Realne zestawy do ślepej wymiany trzymaj w sekrecie (`zestawy-tajne/` w `.gitignore`) i hashuj przed reveal.

## Czystość (held-out) — zmierzona
Audyt `tools/contamination_check.py` vs `seed_500_training_final.jsonl` (n=13, any-match):
**CZYSTY 0%** — frakcja 0.000, any-match 0, najdłuższy wspólny span **0 tok**. Domeny dobrane **spoza**
`seed_500` (gra, smart-home, robotyka, figury, ptaki, pliki, obrazy, szachy, muzyka, pogoda — nie
biznes-CRUD/płatności/raporty/zamówienia, które dominują w treningu).

## Pokrycie (15 itemów)
| Zasada | # | Pułapki |
|---|---|---|
| SRP | 3 | god-klasa, mieszanie warstw I/O+logika+UI |
| OCP | 3 | rosnący if/switch po typie zamiast polimorfizmu |
| LSP | 3 | Kwadrat:Prostokąt, Pingwin.Lec()→throw, ReadOnlyList:List throw |
| ISP | 2 | gruby interfejs, puste/NotImplemented metody |
| DIP | 3 | `new Konkret()` w wysokopoziomowej klasie, cykl zależności |
| odmowa złej instrukcji | 1 | spec WPROST prosi o god-klasę — czy model się postawi |

## Schemat itemu (`eval.jsonl`)
```json
{"id":"SOLID-OCP-01","zasada":"OCP","domena":"pliki",
 "spec":"<specyfikacja PL z pułapką — to widzi model>",
 "pulapka":"<na czym polega pokusa anty-wzorca>",
 "kryterium_pass":"<rubryka: co musi spełnić poprawne rozwiązanie>",
 "tryb_awarii":"<jak pęka słaby model — taksonomia S3>"}
```

## Ocena (rubryka + taksonomia)
- **Pass/Fail wg `kryterium_pass`** — rozwiązanie spełnia zasadę (np. nowa klasa zamiast `else-if`).
- **Tryb awarii** (gdy fail) wg taksonomii S3: `anty-wzorzec` / `błędny-plan` / `ciche-pominięcie` /
  `naruszenie-LSP` / `brak-krytycyzmu`. Klasyfikacja obowiązkowa (nie sama liczba — *jak* pęka).
- **Grader:** człowiek lub LLM-sędzia (per protokół wymiany); w trybie blind — drugi team ocenia ślepo.

## Użycie
```bash
# audyt czystości (musi być 0%)
python ../../tools/contamination_check.py \
  --train <wasz_trening.jsonl> --eval eval.jsonl

# wymiana: zahashuj przed reveal (protokol/PROTOKOL-Wymiany.md)
git hash-object eval.jsonl
```

## Status / następne
v1, eval-only, **niespalony**. Otwarte: kalibracja trudności na **panelu modeli** (S3 — gradient,
nie floor effect) + **drugi team** do ślepej wymiany (T2). Po pierwszym reveal → oznaczyć `spalony` w manifeście.

## Powiązania
[[../../docs/10-Tezy/T1-Provenance-Kontaminacja|T1]] · [[../../docs/25-Syntezy/S2-Audyt-Overlap|S2]] · [[../../docs/25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../../protokol/PROTOKOL-Wymiany|protokół]]
