---
type: synteza
id: BENCH-S1
title: "Commitment + zestaw jednorazowy + rotacja"
status: propozycja
parents: ["BENCH-T2", "BENCH-AT1"]
author: Arkadiusz Słota
date: 2026-06-26
---

# S1 — Jak wymieniać, by nie spalić (rozstrzyga AT1)

## Rozstrzygnięcie
Blind exchange (T2) działa, jeśli benchmark jest **jednorazowy** i chroniony **commitment scheme** —
nie polegamy na obietnicy „nie trenowałem".

## Protokół (skrót — pełny w `protokol/PROTOKOL-Wymiany.md`)
1. **Commit:** team A publikuje **hash** zestawu (SHA-256) + datę, ZANIM go ujawni. Treść trzyma w sekrecie.
2. **Reveal jednorazowy:** A ujawnia zestaw tylko do **jednej** ewaluacji modeli B; B ewaluuje, zwraca wyniki + odpowiedzi modelu.
3. **Spalony po użyciu:** ujawniony zestaw oznaczony `spalony` w manifeście → NIGDY więcej jako eval (może iść do treningu jawnie).
4. **Rotacja:** A trzyma pulę itemów; każda runda losuje świeży podzbiór, reszta zostaje tajna.
5. **Audyt następnej iteracji:** przed kolejną rundą — `contamination_check.py` modelu B vs spalone zestawy (czy B je wchłonął — to OK, byle nie do *aktywnego* eval).

## Dlaczego to broni
- Hash = dowód, że A nie podmienił zestawu pod wynik (anti-Goodhart po stronie autora).
- Jednorazowość = spalenie jest *zaplanowane*, nie przypadkowe → przewaga nie znika, tylko rotuje.
- Koszt rotacji realny, ale to **cena niezależnego ground truth** (jak koszt ślepego audytu w M4).

## Powiązania
parents: [[../10-Tezy/T2-Wymiana-Blind|T2]], [[../15-Antytezy/AT1-Spalanie-Benchmarku|AT1]] · [[../../protokol/PROTOKOL-Wymiany|protokół]]
