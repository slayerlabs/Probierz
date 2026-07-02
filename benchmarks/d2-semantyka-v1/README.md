---
type: benchmark
id: BENCH-D2-SEMANTYKA-V1
title: "d2-semantyka-v1 — wymiar D2: semantyka / wierność znaczeniu"
status: eval-only
parents: ["BENCH-T4", "BENCH-S4", "BENCH-S5"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d2-semantyka-v1 🇵🇱

> **10 zadań interpretacji znaczenia** z gradientem trudności (poziomy 1–4). Mierzy wymiar **D2**
> konstruktu ([[../../docs/10-Tezy/T4-Dekompozycja-Wymiarow|T4]]): czy model chwyta *znaczenie*, nie
> powierzchnię leksykalną. Każdy item ma **zamknięty zbiór klas odpowiedzi** (`klasy_odpowiedzi`) i
> deterministyczną rubrykę pass/fail (T5).

> ⚠️ **v1 PUBLICZNY = demonstrator/template** (AT1: spala się po ujawnieniu). Realne zestawy do
> ślepej wymiany trzymaj w sekrecie i hashuj przed reveal.

## Czystość (held-out) — zmierzona
`tools/contamination_check.py` vs `datasets/seed_500_training_final.jsonl` (n=13, any-match):
**CZYSTY 0%** — frakcja 0.000, span 0 tok. Warunek wstępny (C1/T1) spełniony.

## Zakres wymiaru i demarkacja (S4)
D2 obciąża **interpretację znaczenia**, a rozumowanie jest **trywialne** (0–1 krok) — odwrotnie niż D1.
Reguła dominującego obciążenia (S4): o wyniku decyduje poprawne odczytanie znaczenia, nie długość
łańcucha wnioskowania. Item wymagający wielu kroków należałby do D1.

Zjawiska pokryte: **negacja** (w tym podwójna), **kwantyfikatory** (ogólny/egzystencjalny),
**entailment/hiponimia**, **zakres kwantyfikatorów** (scope: `∀∃` vs `∃∀`), **monotoniczność**,
**presupozycja**, **implikatura skalarna vs logika**, **koreferencja zaimka** (typ Winograd).

Pułapka każdego itemu: odpowiedź **powierzchniowa** (dopasowanie słów, implikatura potoczna) różni
się od poprawnej **znaczeniowo/logicznie**. Model bez reprezentacji znaczenia ulega pułapce.

## Gradient trudności (S3/T3)
Poziom 1 (negacja prosta) → poziom 4 (scope, presupozycja, implikatura, koreferencja). Poziom to
hipoteza; kalibracja empiryczna ($b_j$) po przejeździe panelu (S5).

## Schemat itemu (`eval.jsonl`)
```json
{"id":"D2-L3-01","wymiar":"D2","poziom_trudnosci":3,"zjawisko":"zakres-kwantyfikatora",
 "spec_parafrazy":["<parafraza 1>","<parafraza 2>","<parafraza 3>"],
 "uzasadnienie_wzorcowe":["<krok interpretacji>"],
 "odpowiedz_kanoniczna":"nie",
 "typ_odpowiedzi":"kanoniczny_tekst",
 "klasy_odpowiedzi":["tak","nie"],
 "kryterium_pass":"<rubryka>","tryb_awarii":"halucynacja","demarkacja_D2":"<dlaczego D2, nie D1>"}
```

- **`klasy_odpowiedzi`** — zamknięty zbiór dopuszczalnych odpowiedzi. Grader wykrywa **którą klasę**
  wybrał model (najdłuższa pasująca fraza wygrywa: „nie wiadomo" nie jest mylone z „nie"). To czyni
  ocenę deterministyczną mimo odpowiedzi w języku naturalnym.
- **`uzasadnienie_wzorcowe`** — poprawna ścieżka interpretacji (do klasyfikacji trybu awarii).

## Ocena (rubryka + taksonomia awarii, S3)
- **Pass/Fail:** wykryta klasa == `odpowiedz_kanoniczna` (grader z priorytetem najdłuższej frazy).
- **Tryb awarii** przy fail: głównie `halucynacja` (błędna interpretacja znaczenia); dalej
  `bledny-plan`, `format`. Klasyfikacja przez ≥2 graderów przy rozbieżności (S4).
- **Test niezmienniczości promptu (AT5):** 3 parafrazy/item; wynik = mediana, wrażliwość raportowana osobno.

## Pomiar (S5)
Wynik zasila estymację $\theta^{(D2)}$: Bradley-Terry + 1PL/Rasch, bootstrap CI. Panel ≥5 modeli.
Macierz [model × wymiar] wejściem do testu rozłączności D1↔D2 (S4: istotne odwrócenia, analiza równoległa).

## Użycie
```bash
python ../../tools/contamination_check.py --train <trening.jsonl> --eval eval.jsonl   # musi 0%
python ../../tools/run_eval.py --eval eval.jsonl --base-url <url> --model <id> --out wyniki.json
```

## Status / następne
v1, eval-only, niespalony, audyt 0%. Otwarte: (1) przejazd panelu → kalibracja + $\theta^{(D2)}$;
(2) **walidacja demarkacji D1↔D2** — czy itemy D2 korelują silniej z D2 niż z D1 (wymaga obu zestawów
na panelu); (3) rozbudowa po pilotażu.

## Powiązania
[[../../docs/10-Tezy/T4-Dekompozycja-Wymiarow|T4]] · [[../../docs/10-Tezy/T5-Falsyfikowalna-Rubryka|T5]] · [[../../docs/25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · [[../../docs/25-Syntezy/S5-MIRT-Panel|S5]] · siostra: [[../d1-rozumowanie-v1/README|d1-rozumowanie-v1]]
