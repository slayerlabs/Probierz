---
type: review
id: BENCH-REVIEW-XAVIER
title: "Review zewnętrzny — Xavier (APL), 2026-06-26"
status: wdrożony
recenzent: Xavier (APL)
author: Arkadiusz Słota
date: 2026-06-26
---

# Review Xaviera — Probierz

> Zewnętrzna ocena: README + nitki T/AT/S + protokół wymiany + manifest + `contamination_check.py`.

## Werdykt
Spójny, samodokumentujący projekt w etosie Slayera. Najmocniejsze: pierwszy audyt znalazł, że **własny**
`test_verification.jsonl` jest skażony — i zamiast schować, przeklasyfikowano go i wpisano „brak czystego
eval-only" jako pierwsze zadanie. „We ship the uncomfortable finding" w praktyce.

## Zweryfikowane niezależnie (nie na słowo)
- **Narzędzie poprawne** — Xavier odpalił na syntetyku z kontrolowanym przeciekiem: dosłowna kopia → overlap 1.0 + flaga; oryginał → 0. Logika n-gramowa OK. ✅
- **Headline 90% — NIE odtworzony niezależnie:** `slayerlabs/datasets` zwraca 404 (Xavier nie jest collaboratorem). Nie podważa, ale uczciwie nie potwierdził 1:1.

## Znaleziska → wdrożone
1. **[FIX] Próg frakcyjny przepuszczał wtopione kopie.** 20-tok dosłowny fragment + padding → frakcja ~0.17, „czysty" — mimo dokładnej kopii (najgroźniejszy realny przeciek: skopiowana ODPOWIEDŹ w oryginalnym promptcie).
   → **Wdrożone:** dodano **any-match** (≥1 trafienie 13-gramu, Llama-style) + **najdłuższy wspólny span**; werdykt skażony, gdy frakcja>próg **LUB** span≥próg. Zweryfikowane: demo span 19 tok **złapany** (frakcja 0.04 by przeszła). `test_verification` pod nową regułą = **100%** (był 90%).
2. **[DOPRECYZOWANE] Protokół trust-minimized, nie trustless.** Hash = integralność, ale nie blokuje kryptograficznie douczenia B na ujawnionym zestawie w tej samej rundzie; realne zabezpieczenie = jednorazowość + spalenie + audyt międzyrundowy (po fakcie).
   → **Wdrożone:** sekcja „Model zaufania (trust-minimized, NIE trustless)" w `PROTOKOL-Wymiany.md`.

## Otwarte (akcja po stronie Arka)
- **Dostęp Xaviera do `slayerlabs/datasets`** (collaborator) → odtworzy headline 90/100% audytu 1:1. Do tego czasu headline = zmierzony przez nas, niezweryfikowany niezależnie.

## Docenione (jego punkty)
- reuse mechanizmu n-gram z `micro-models` (detektor dosłownej pamięci) — spójność z dorobkiem labu;
- AT1/AT2/AT3 to realne ryzyka, a S1/S2/S3 je adresują;
- „ciche błędy = najgorszy tryb awarii" = ta sama asymetria co false-discard z jego AT2 sandboxa.

## Powiązania
[[Stan|Stan]] · [[../../protokol/PROTOKOL-Wymiany|protokół]] · [[../25-Syntezy/S2-Audyt-Overlap|S2]] · [[../../tools/contamination_check.py|narzędzie]]
