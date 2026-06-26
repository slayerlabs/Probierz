---
type: teza
id: BENCH-T1
title: "Kontrola kontaminacji przez provenance"
status: w-dyskusji
parents: ["BENCH-C1"]
author: Arkadiusz Słota
date: 2026-06-26
---

# T1 — Provenance = przewaga nad kontaminacją

## Teza
Największy problem ewaluacji LLM to **kontaminacja**: model widział benchmark w treningu → mierzysz
zapamiętywanie, nie zdolność. Publiczne benchmarki (MMLU, GSM8K) są masowo skażone scrapem.

Nasza przewaga: **dane budujemy od zera** (`slayerlabs/datasets`, `academy/lab`, OpenPL, MicroModels).
Wiemy *dokładnie* co weszło do treningu → możemy **z góry** wyznaczyć dane eval-only, które nigdy
nie trafiają do treningu. To „dwie pieczenie na jednym ogniu": robiąc dane, dostajemy czysty eval.

## Mechanizm
- **Manifest provenance** (`protokol/PROVENANCE-Manifest.md`): każdy dataset oznaczony `trening-only` / `eval-only`, źródło, data.
- Granica trening↔eval jest **twarda** i udokumentowana, nie dorozumiana.

## Dowód (żadnej tezy bez dowodu)
`contamination_check.py` na realnych danych: `test_verification.jsonl` vs `seed_500_training_final.jsonl`
→ **90% itemów skażonych** (mean overlap n-gram 0.84, 60% near-verbatim). Bez audytu ten plik
zostałby użyty jako „test" i zawyżyłby wyniki. Provenance to teza — **audyt to dowód**.

## Powiązania
parent: [[BENCH-C1]] · synteza: [[../25-Syntezy/S2-Audyt-Overlap|S2]] · kontra: [[../15-Antytezy/AT2-Przeciek-Mimo-Od-Zera|AT2]]
