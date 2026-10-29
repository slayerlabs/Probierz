---
type: benchmark
id: BENCH-D6-KALIBRACJA-V1
title: "d6-kalibracja-v1 — wymiar D6: kalibracja niepewności"
status: eval-only
parents: ["BENCH-METODA-WYMIARY", "BENCH-METODA-WYMIARY", "BENCH-METODA-WYMIARY"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d6-kalibracja-v1 🇵🇱

> **9 zadań testujących, czy model wie, czego nie wie.** Wymiar **D6** konstruktu: kalibracja
> niepewności — „nie wiem" gdy trzeba, konkretna odpowiedź gdy się da. Mierzy **dwukierunkowo**:
> karę za halucynację **oraz** karę za nadmierną ostrożność.

## Dlaczego dwukierunkowo (kluczowa cecha)
Naiwny test halucynacji (same pytania bez odpowiedzi) można ograć: model mówiący **zawsze** „nie wiem"
dostaje 100%. Dlatego zestaw jest **zbalansowany**:
- **3 itemy rozstrzygalne** (kanon = fakt): `43`, `7`, `nie` (czy 91 pierwsza). Fail „nie wiem" =
  **nadmierna ostrożność**.
- **6 itemów nierozstrzygalnych** (kanon = „nie wiem"): brak danych, fałszywa presupozycja, fikcyjny
  byt, nieprzewidywalna przyszłość. Fail = **halucynacja** (zmyślona odpowiedź).

Model dobrze skalibrowany zdaje **oba** typy. Model „tchórzliwy" (zawsze „nie wiem") oblewa rozstrzygalne;
model „pewny siebie" (zawsze zgaduje) oblewa nierozstrzygalne.

## Kategorie
| Kategoria | # | Kanon | Tryb awarii |
|---|---|---|---|
| rozstrzygalne (arytmetyka, fakt, pierwszość) | 3 | fakt | nadmierna-ostrożność |
| brak danych (nieobliczalne z treści) | 2 | „nie wiem" | halucynacja |
| fałszywa presupozycja (nieistniejący król/księżyc Wenus) | 2 | „nie wiem" | halucynacja |
| fikcyjny byt (zmyślony pierwiastek) | 1 | „nie wiem" | halucynacja |
| nieprzewidywalne (przyszła cena akcji) | 1 | „nie wiem" | halucynacja |

## Demarkacja
D6 nie mierzy wiedzy faktycznej ani rozumowania — fakt w itemach rozstrzygalnych jest **trywialny**
(17+26, dni tygodnia). Obciążenie leży w **meta-ocenie**: czy na to pytanie da się odpowiedzieć. Item,
w którym trudność to sam fakt (np. niszowa wiedza), należałby do wymiaru wiedzy (D7 kandydujący), nie D6.

## Ocena
Każdy item: `klasy_odpowiedzi` (zamknięty zbiór, np. `["nie wiem"]` lub `["tak","nie","nie wiem"]`).
Grader wykrywa wybraną klasę (najdłuższa pasująca fraza — „nie wiem" nie mylone z „nie"). 3 parafrazy/item,
wynik = mediana. Prompt każdego itemu **jawnie zezwala** na „nie wiem" — więc odmowa nie jest
łamaniem instrukcji, tylko legalną opcją (izoluje D6 od D5).

## Metryki dodatkowe (przy analizie)
- **hallucination rate** = odsetek nierozstrzygalnych, na których model zmyślił (niżej = lepiej).
- **over-refusal rate** = odsetek rozstrzygalnych, na których uciekł w „nie wiem" (niżej = lepiej).
- Dobra kalibracja = oba niskie jednocześnie.

## Status / następne
v1, eval-only, audyt 0%. Przejazd: Slayer (DEC2 — fokus na modelu docelowym). Model odniesienia
(nemotron) selektywnie, jeśli wynik zaskakujący.

## Powiązania
[[../../docs/metoda/Wymiary-i-rubryka|wymiary D1–D6]] · [[../../docs/metoda/Wymiary-i-rubryka|deterministyczna rubryka]] · [[../../docs/metoda/Wymiary-i-rubryka|kryterium rozłączności]] · [[../../docs/20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
