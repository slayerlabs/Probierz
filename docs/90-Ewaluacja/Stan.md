---
type: ewaluacja
id: BENCH-STAN
title: "Stan Probierz — żywy dokument"
status: żywy-dokument
author: Arkadiusz Słota
date: 2026-07-02
---

# Stan — co zmierzone, co otwarte

> Aktualizuj po każdym kroku (zasada Slayera). Nic tu nie jest przyjęte bez pomiaru — tylko zmierzone.

## ✓ Co zrobione (zmierzone)
| Element | Stan | Dowód |
|---|---|---|
| `contamination_check.py` | działa + ostrzejszy | self-check 100%; **any-match + span** łapie wtopione kopie (test Xaviera: span 19 tok złapany, frakcja 0.04 by przeszła) |
| Audyt `test_verification` | **SKAŻONY** | **100%** (any-match, n=13); span do 217 tok = całe itemy skopiowane |
| Manifest provenance | v1 | 6 datasetów oznaczonych; `test_verification` przeklasyfikowany |
| Protokół wymiany | v1 | commitment + reveal jednorazowy + rotacja + niezmienniki |
| Know-how dialektyczny (metoda uczciwości) | C1 + T1-3 + AT1-3 + S1-3 | broni się (każda teza ma antytezę + rozstrzygnięcie) |
| Benchmark `csharp-solid-v1` | **CZYSTY 0%** | 15 itemów adwersarialnych SOLID (domeny spoza seed_500); audyt vs seed_500 = 0% (any-match) |
| Review Xaviera (2026-06-26) | wdrożony | fix any-match/span w narzędziu + protokół „trust-minimized"; patrz [[Review-Xavier]] |

## ✓ Warstwa konstruktu i modelu pomiaru (2026-07-02, rozpisane — niezweryfikowane empirycznie)
> Odpowiada na pytanie „**co** mierzymy i **jak** to formalizujemy", logicznie poprzedzające dobór zadań.
> Status: dialektyka domknięta (teza↔antyteza↔synteza z warunkiem obalenia). Dowód empiryczny = faza baseline.

| Element | Stan | Zawartość |
|---|---|---|
| **Warstwa 1 — Konstrukt** | rozpisana | [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej\|C2]] cel; [[../10-Tezy/T4-Dekompozycja-Wymiarow\|T4]] dekompozycja na wymiary D1–D6; [[../10-Tezy/T5-Falsyfikowalna-Rubryka\|T5]] rubryka pass/fail zamiast proxy; [[../15-Antytezy/AT4-Splatanie-Czynnik-G\|AT4]] czynnik g; [[../15-Antytezy/AT5-Format-Nie-Zdolnosc\|AT5]] format vs zdolność; [[../25-Syntezy/S4-Taksonomia-Wymiarow\|S4]] taksonomia + warunek obalenia per wymiar |
| **Warstwa 2 — Model pomiaru** | rozpisana | [[../10-Tezy/T6-IRT-Model-Pomiaru\|T6]] IRT 2PL/3PL; [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc\|AT6]] założenia IRT vs LLM; [[../25-Syntezy/S5-MIRT-Panel\|S5]] IRT per wymiar + panel ≥5 modeli + bootstrap CI |

## ○ Otwarte (kryteria sukcesu C1 + C2)
1. ~~Brak czystego eval-only~~ → **mamy pierwszy:** `csharp-solid-v1` (15 itemów SOLID, CZYSTY 0%). Dalej: rozbudowa + kolejne domeny.
2. **Drugi team** — niezbędny do T2/blind exchange; obecnie brak partnera. Bez niego — autowalidacja.
3. **Panel kalibracyjny** (S3/S5) — brak; trudność itemów i $\theta$ per wymiar niezmierzone → ryzyko floor/sufit.
4. **Overlap embeddingowy** (S2, granica n-gramu) — n-gram nie łapie parafrazy; dodać warstwę semantyczną.
5. **Dowód empiryczny konstruktu (C2/S4)** — rozłączność wymiarów (odwrócenia rankingu, analiza czynnikowa) niezmierzona; T4 ma status w-dyskusji do czasu baseline.
6. **Zestawy per wymiar (D1–D6)** — brak; minimalny zestaw ~5–10 itemów/wymiar + audyt czystości 0% jako warunek wstępny baseline.

## Kryterium obalenia — dwa poziomy
- **C1 (uczciwość):** jeśli nasz „czysty" benchmark daje ten sam ranking co skażony publiczny → przewaga provenance to iluzja. Test wykonalny, gdy istnieje zbiór eval-only + ≥2 modele.
- **C2 (konstrukt):** jeśli pierwsza składowa analizy czynnikowej [model×wymiar] wyjaśnia ≥ ~90% wariancji i brak odwróceń rankingu → konstrukt jednowymiarowy, taksonomia D1–D6 upada (patrz S4).

## Następny krok (priorytet) — faza BASELINE
Zgodnie z metodą **problem → model matematyczny → baseline → research → eval**: warstwa problem (C2)
i model matematyczny (T6/S5) są rozpisane. Następny krok:
1. minimalny zestaw ~5–10 itemów per wymiar D1–D6 (rubryki wg T5, środki zaradcze AT5);
2. audyt czystości `contamination_check.py` → 0% (warunek wstępny);
3. przejazd **panelem ≥5 modeli** (w tym Slayer v49) → macierz [model × wymiar];
4. estymacja $\theta^{(i)}$ (S5) + test warunków obalenia S4 (rozłączność, analiza czynnikowa).
