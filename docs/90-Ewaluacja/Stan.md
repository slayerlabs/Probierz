---
type: ewaluacja
id: BENCH-STAN
title: "Stan Probierz — żywy dokument"
status: żywy-dokument
author: Arkadiusz Słota
date: 2026-06-26
---

# Stan — co zmierzone, co otwarte

> Aktualizuj po każdym kroku (zasada Slayera). Nic tu nie jest „gotowe na słowo" — tylko zmierzone.

## ✓ Co zrobione (zmierzone)
| Element | Stan | Dowód |
|---|---|---|
| `contamination_check.py` | działa + ostrzejszy | self-check 100%; **any-match + span** łapie wtopione kopie (test Xaviera: span 19 tok złapany, frakcja 0.04 by przeszła) |
| Audyt `test_verification` | **SKAŻONY** | **100%** (any-match, n=13); span do 217 tok = całe itemy skopiowane |
| Manifest provenance | v1 | 6 datasetów oznaczonych; `test_verification` przeklasyfikowany |
| Protokół wymiany | v1 | commitment + reveal jednorazowy + rotacja + niezmienniki |
| Know-how dialektyczny | C1 + T1-3 + AT1-3 + S1-3 | broni się (każda teza ma antytezę + rozstrzygnięcie) |
| Benchmark `csharp-solid-v1` | **CZYSTY 0%** | 15 itemów adwersarialnych SOLID (domeny spoza seed_500); audyt vs seed_500 = 0% (any-match) |
| Review Xaviera (2026-06-26) | wdrożony | fix any-match/span w narzędziu + protokół „trust-minimized"; patrz [[Review-Xavier]] |

## ○ Otwarte (kryteria sukcesu C1)
1. ~~Brak czystego eval-only~~ → **mamy pierwszy:** `csharp-solid-v1` (15 itemów SOLID, CZYSTY 0%). Dalej: rozbudowa + kolejne domeny.
2. **Drugi team** — niezbędny do T2/blind exchange; obecnie brak partnera. Bez niego — autowalidacja.
3. **Panel kalibracyjny** (S3) — brak; trudność itemów niezmierzona → ryzyko floor/sufit.
4. **Overlap embeddingowy** (S2, granica n-gramu) — n-gram nie łapie parafrazy; dodać warstwę semantyczną.

## Kryterium obalenia całości (C1)
Jeśli nasz „czysty" benchmark daje ten sam ranking co skażony publiczny → przewaga provenance to iluzja.
Test wykonalny dopiero, gdy istnieje zbiór eval-only (pkt 1) + ≥2 modele.

## Następny krok (priorytet)
**Zbuduj pierwszy zestaw eval-only** z danych spoza `seed_500` + przepuść przez `contamination_check.py`
do 0% — to odblokowuje wszystko inne.
