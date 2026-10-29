---
type: benchmark
id: BENCH-D1-ROZUMOWANIE-V1
title: "d1-rozumowanie-v1 — wymiar D1: rozumowanie wieloetapowe"
status: eval-only
parents: ["BENCH-METODA-WYMIARY", "BENCH-METODA-WYMIARY", "BENCH-METODA-POMIAR"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-rozumowanie-v1 🇵🇱

> **10 zadań rozumowania wieloetapowego** z gradientem trudności (2–6 kroków wnioskowania). Mierzy
> wymiar **D1** konstruktu (patrz [[../../docs/metoda/Wymiary-i-rubryka|wymiary D1–D6]]): zdolność
> złożenia wielu kroków wnioskowania w poprawny wynik końcowy. Każdy item ma **weryfikowalną
> deterministycznie** odpowiedź kanoniczną (liczba lub tekst kanoniczny) — rubryka pass/fail bez
> uznaniowości.

> ⚠️ **v1 jest PUBLICZNY = demonstrator/template.** Leży w repo, więc modele trenowane później mogą go
> wchłonąć (benchmark spala się po ujawnieniu). Traktuj jak **wzór formatu + dowód metody**, NIE
> jako tajny held-out. Realne zestawy do ślepej wymiany trzymaj w sekrecie i hashuj przed reveal.

## Czystość (held-out) — zmierzona
Audyt `tools/contamination_check.py` vs `datasets/seed_500_training_final.jsonl` (n=13, any-match):
**CZYSTY 0%** — średnia frakcja 0.000, any-match 0, najdłuższy wspólny span **0 tok**. Domeny i
sformułowania dobrane spoza rozkładu danych treningowych. Audyt jest warunkiem wstępnym —
zestaw wchodzi do użytku dopiero po jego przejściu.

## Zakres wymiaru i demarkacja
D1 mierzy **łańcuch wnioskowań**, nie rozumienie znaczenia. Zgodnie z **regułą dominującego
obciążenia**: język itemów jest prosty i jednoznaczny (semantyka trywialna), a o wyniku decyduje
**liczba i poprawność kroków**. To odróżnia D1 od D2 (semantyka: negacja, kwantyfikator, entailment).
Item, który wymaga interpretacji dwuznacznego zdania, należałby do D2 — tu takich nie ma.

## Gradient trudności
Po 2 itemy na poziom 2, 3, 4, 5, 6 kroków wnioskowania. Cel: rozrzut wyników (punkt dyskryminacji),
nie floor/sufit. Poziom = długość wzorcowego łańcucha `kroki_wzorcowe`. Po baseline poziom zostanie
skalibrowany empirycznie na panelu modeli (trudność $b_j$ z modelu Rascha) — deklarowany poziom
to hipoteza, nie pomiar.

## Schemat itemu (`eval.jsonl`)
```json
{"id":"D1-L4-01","wymiar":"D1","poziom_krokow":4,"domena":"wiek-czas",
 "spec_parafrazy":["<parafraza 1>","<parafraza 2>","<parafraza 3>"],
 "kroki_wzorcowe":["<krok 1>","<krok 2>","..."],
 "odpowiedz_kanoniczna":"20",
 "typ_odpowiedzi":"liczba",
 "kryterium_pass":"<rubryka: dokladny warunek zaliczenia>",
 "tryb_awarii":"bledny-plan",
 "demarkacja_D1":"<dlaczego to D1, nie D2>"}
```

- **`spec_parafrazy`** — ≥3 sformułowania tego samego zadania (test niezmienniczości promptu).
  Model odpowiada na każdą parafrazę; wynik itemu = statystyka odporna (mediana), a **wariancja po
  parafrazie** raportowana osobno jako wskaźnik wrażliwości.
- **`odpowiedz_kanoniczna` + `typ_odpowiedzi`** — deterministyczna weryfikacja: `liczba`
  (porównanie numeryczne z tolerancją formatu) lub `kanoniczny_tekst` (dopasowanie znormalizowane).
- **`kroki_wzorcowe`** — ground-truth łańcuch; służy do klasyfikacji trybu awarii (gdzie łańcuch modelu
  odchodzi od wzorca).

## Ocena (rubryka + taksonomia awarii)
- **Pass/Fail** wg `kryterium_pass`: odpowiedź końcowa równa kanonicznej (po normalizacji formatu).
  Rozdział formatu od treści: błąd samego formatu liczby → tryb `format`, nie `bledny-plan`.
- **Tryb awarii** przy fail: `bledny-plan` (zły łańcuch), `ciche-pominiecie` (pominięty krok),
  `halucynacja` (wymyślona dana), `format` (poprawny wynik, zły zapis), `petla` (brak zakończenia).
- **Grader trust-minimized:** wynik końcowy sprawdzalny automatycznie; klasyfikacja trybu awarii przez
  ≥2 graderów różnego pochodzenia przy rozbieżności.

## Pomiar
Wynik zasila estymację zdolności $\theta^{(D1)}$ per model: pomiar porównawczy (Bradley-Terry) +
1PL/Rasch, z przedziałami ufności (bootstrap). Panel ≥5 modeli (w tym Slayer v49). Macierz
[model × wymiar] wejściem do testu rozłączności (istotne odwrócenia, analiza równoległa).

## Użycie
```bash
# audyt czystosci (warunek wstepny, musi byc 0%)
python ../../tools/contamination_check.py \
  --train <wasz_trening.jsonl> --eval eval.jsonl

# hash przed ewentualna wymiana (protokol/PROTOKOL-Wymiany.md)
git hash-object eval.jsonl
```

## Status / następne
v1, eval-only, **niespalony**, audyt 0%. Otwarte: (1) przejazd panelu modeli (baseline) → kalibracja
trudności i estymacja $\theta^{(D1)}$; (2) walidacja demarkacji (czy itemy D1 korelują silniej z D1 niż
z innymi wymiarami — wymaga zestawów D2–D6); (3) rozbudowa liczby itemów po pilotażu.

## Powiązania
[[../../docs/metoda/Wymiary-i-rubryka|wymiary D1–D6]] · [[../../docs/metoda/Wymiary-i-rubryka|deterministyczna rubryka]] · [[../../docs/metoda/Wymiary-i-rubryka|kryterium rozłączności]] · [[../../docs/metoda/Model-pomiaru-IRT|model pomiaru]] · [[../../docs/metoda/Trudnosc-i-taksonomia-awarii|taksonomia awarii]]
