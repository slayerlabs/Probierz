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
1. **Frakcja n-gramów (n=13, Llama-style):** % okien itemu pokrytych treningiem; frakcja > próg → skażone.
2. **Any-match + najdłuższy span (domyślna, ostrzejsza reguła):** JAKIEKOLWIEK trafienie 13-gramu (lub długi wspólny span) flaguje item — łapie **wtopione kopie** (skopiowana odpowiedź w oryginalnym promptcie), które sama frakcja przepuszcza. _(fix Xaviera)_
3. **Near-verbatim (frakcja ≈ 1.0):** dosłowne kopie całych itemów → usuń bezwzględnie.
4. **Dedup pochodnych:** warianty (`v2`, `variants_all`) = ten sam item; nie rozdzielaj train/eval po wariantach.
5. **Bramka:** benchmark wychodzi DOPIERO przy **0% skażonych** (frakcja ORAZ span).

## Dowód, że to konieczne
`test_verification` vs `seed_500` → **100% skażonych** (span do **217 tok** = całe itemy skopiowane; n=13, any-match).
Demo wtopionej kopii: 20-tok dosłowny fragment + padding → frakcja 0.04 (stary próg by **przepuścił**), ale span 19 tok → **złapany**. Audyt 0.5s.

## Granica metody (uczciwie)
N-gram łapie dosłowność, nie **parafrazę/semantykę** (AT2 ma rację częściowo). Następny krok:
overlap embeddingowy (sentence-transformers) jako druga warstwa — jak relewancja E5 w Dendrometrii.

## Powiązania
parents: [[../10-Tezy/T1-Provenance-Kontaminacja|T1]], [[../15-Antytezy/AT2-Przeciek-Mimo-Od-Zera|AT2]] · [[../../tools/contamination_check.py|narzędzie]]
