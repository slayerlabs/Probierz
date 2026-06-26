---
type: protokol
id: BENCH-PROTOKOL
title: "Protokół ślepej wymiany benchmarków (commitment + reveal)"
status: aktywny
author: Arkadiusz Słota
date: 2026-06-26
---

# Protokół ślepej wymiany (Team A ↔ Team B)

> Operacyjny rdzeń T2/S1. Cel: niezależny ground truth bez spalania przewagi (AT1).
> Zasada: **nie ufamy obietnicom — ufamy hashom i jednorazowości.**

## Role
- **Autor** (np. Team A): buduje benchmark, trzyma pulę itemów w sekrecie, zna SWOJE dane treningowe.
- **Ewaluowany** (Team B): dostaje ujawniony zestaw RAZ, odpala swoje modele, zwraca surowe odpowiedzi + wyniki.
- Symetrycznie w drugą stronę.

## Kroki (jedna runda)

| # | Krok | Komenda / artefakt |
|---|---|---|
| 1 | **Audyt własny** — autor sprawdza zestaw vs SWÓJ trening | `contamination_check.py --train <swój> --eval <zestaw>` → musi być 0% |
| 2 | **Commit** — publikujesz hash + datę + liczbę itemów, treść tajna | `git hash-object zestaw.jsonl` lub `sha256sum`; zapis w `rejestr-commitów.md` |
| 3 | **Reveal** — przekazujesz zestaw drugiemu teamowi (1 ewaluacja) | szyfrowany transfer; znacznik czasu |
| 4 | **Ewaluacja** — B odpala modele, zwraca odpowiedzi + scoring + taksonomię awarii | format poniżej |
| 5 | **Weryfikacja commitu** — porównujesz hash zwróconego zestawu z krokiem 2 | `sha256sum` musi się zgadzać (B nie podmienił) |
| 6 | **Spalenie** — zestaw → `spalony` w manifeście, NIGDY więcej jako aktywny eval | wpis w `PROVENANCE-Manifest.md` |
| 7 | **Audyt międzyrundowy** — przed kolejną rundą: czy modele B wchłonęły spalony zestaw | `contamination_check.py` — łapie **po fakcie** (nie blokuje w trakcie rundy) |

## Format zwrotu wyników (B → A)
```json
{"item_id": "...", "model": "...", "odpowiedz": "...", "wynik": 0|1|częściowy,
 "tryb_awarii": "halucynacja|błędny-plan|ciche-pominięcie|format|pętla|brak"}
```

## Niezmienniki (łamią → runda nieważna)
- Hash z kroku 2 == hash w kroku 5 (integralność).
- Każdy zestaw użyty jako eval **dokładnie raz**.
- Autor NIE widzi puli itemów drugiego teamu (symetria ślepoty).
- Wynik bez `tryb_awarii` = niepełny (taksonomia obowiązkowa, S3).

## Model zaufania (trust-minimized, NIE trustless)
Commitment (hash) daje **integralność**: A nie podmieni zestawu pod wynik, B nie zwróci innego niż dostał.
Ale **nic kryptograficznie nie blokuje**, by Team B po reveal douczył modele na ujawnionym zestawie w **tej samej**
rundzie. Realnym zabezpieczeniem jest **jednorazowość + spalenie** (krok 6) oraz **audyt międzyrundowy** (krok 7),
który taki przeciek łapie **po fakcie**. Świadomie: **redukujemy pokusę, nie eliminujemy jej kryptograficznie**.
To i tak istotnie mocniejsze niż self-benchmark (Goodhart/M3): niezależny autor + integralność + jednorazowość.
_(doprecyzowanie z review Xaviera, 2026-06-26)_

## Powiązania
[[../docs/25-Syntezy/S1-Commitment-Protokol|S1]] · [[../docs/10-Tezy/T2-Wymiana-Blind|T2]] · [[PROVENANCE-Manifest|manifest]]
