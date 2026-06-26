---
type: antyteza
id: BENCH-AT2
title: "'Od zera' nie gwarantuje braku przecieku"
status: w-dyskusji
parents: ["BENCH-T1"]
author: Arkadiusz Słota
date: 2026-06-26
---

# AT2 — Provenance to nie magia (steelman)

## Najmocniejsza wersja
„Tworzymy dane od zera" daje kontrolę nad *źródłem*, ale nie nad **podobieństwem semantycznym**:
- **Parafraza** — eval item to przeformułowanie czegoś z treningu; n-gram tego nie złapie.
- **Wspólne źródła publiczne** — generując PL „od zera" i tak czerpiesz z tej samej dystrybucji języka.
- **Bliźniaki w danych** — `seed_500_v2`, `variants_all` to warianty tego samego; etykieta „eval-only" na pochodnej = fałszywa czystość.

**Dowód wspierający tę antytezę:** audyt pokazał `test_verification` = **90% overlap** z treningiem —
mimo że oba „nasze, od zera". Provenance-deklaracja zawiodła; uratował dopiero pomiar.

## Konsekwencja, jeśli prawdziwa
Sama etykieta `eval-only` w manifeście jest bezwartościowa. Potrzebny **obowiązkowy audyt** każdej
pary trening↔eval + dedup, inaczej T1 to iluzja bezpieczeństwa.

## Powiązania
parent: [[../10-Tezy/T1-Provenance-Kontaminacja|T1]] · rozstrzyga: [[../25-Syntezy/S2-Audyt-Overlap|S2]]
