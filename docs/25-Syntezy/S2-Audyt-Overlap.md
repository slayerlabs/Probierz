---
type: synteza
id: BENCH-S2
title: "Obowiązkowy audyt overlapu + dedup"
status: propozycja
parents: ["BENCH-T1", "BENCH-AT2"]
author: Arkadiusz Słota
date: 2026-06-26
---

# S2 — Mierz, nie deklaruj (rozstrzyga AT2)

## Rozstrzygnięcie
Etykieta `eval-only` w manifeście to **hipoteza**, nie gwarancja. Każda para trening↔eval przechodzi
**obowiązkowy audyt** `contamination_check.py` PRZED wydaniem benchmarku. Provenance + pomiar, nie sama deklaracja.

## Procedura
1. **N-gram overlap (n=13, Llama-style):** % itemów eval z overlapem > próg → skażone.
2. **Near-verbatim (overlap ≈ 1.0):** dosłowne kopie → usuń bezwzględnie.
3. **Dedup pochodnych:** warianty (`v2`, `variants_all`) traktuj jak ten sam item — nie rozdzielaj train/eval po wariantach.
4. **Bramka:** benchmark wychodzi DOPIERO przy **0% skażonych**.

## Dowód, że to konieczne
`test_verification` vs `seed_500` → **90% skażonych, 60% near-verbatim** (mean 0.84). Gdyby polegać na
nazwie „verification", użylibyśmy skażonego eval. Audyt to złapał w 0.5s.

## Granica metody (uczciwie)
N-gram łapie dosłowność, nie **parafrazę/semantykę** (AT2 ma rację częściowo). Następny krok:
overlap embeddingowy (sentence-transformers) jako druga warstwa — jak relewancja E5 w Dendrometrii.

## Powiązania
parents: [[../10-Tezy/T1-Provenance-Kontaminacja|T1]], [[../15-Antytezy/AT2-Przeciek-Mimo-Od-Zera|AT2]] · [[../../tools/contamination_check.py|narzędzie]]
