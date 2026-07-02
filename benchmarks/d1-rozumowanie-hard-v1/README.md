---
type: benchmark
id: BENCH-D1-HARD-V1
title: "d1-rozumowanie-hard-v1 — D1 brutalny (przebicie sufitu)"
status: eval-only
parents: ["BENCH-T4", "BENCH-S3", "BENCH-S4", "BENCH-S5"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-rozumowanie-hard-v1 🇵🇱

> **11 brutalnych zadań rozumowania wieloetapowego** (poziomy 7–10). Cel: **przebić sufit** — na
> `d1-rozumowanie-v1` górna półka panelu (gemma, Slayer, qwen) uzyskała 8–10/10, brak dyskryminacji
> u góry. Ten zestaw celuje w prawdziwy pułap modeli.

## Motywacja (z research panelu 5×2)
Analiza `Analiza-Panel-D1-D2.md`: D1 (łatwy) miał **sufit** dla mocnych modeli — 10/10 (gemma), 9/10
(Slayer) z nierozróżnialnymi CI. Lekcja: itemy za łatwe → brak informacji o górnej połowie panelu (S3:
maksimum informacji przy p≈0.5, nie p≈1). Ten zestaw podnosi trudność tam, gdzie modele realnie pękają.

## Czystość — zmierzona
`contamination_check.py` vs `seed_500_training_final`: **CZYSTY 0%** (span 0 tok).

## Ground-truth — zweryfikowany niezależnie
Każda `odpowiedz_kanoniczna` **potwierdzona programowo** (brute-force / niezależne obliczenie): układy
równań, brute-force permutacji (L9-02, L9-03), logika kłamców przez wyczerpanie 2³ przypadków (L8-02),
składanie mnożników procentowych (L10-01). Rubryka jest tak dobra jak jej GT — dlatego GT są sprawdzone,
nie zadeklarowane.

## Zakres i demarkacja (S4)
D1: **głębia łańcucha wnioskowania**, semantyka trywialna (język prosty, jednoznaczny). Trudność leży w
liczbie i współzależności kroków, nie w interpretacji znaczenia (to byłoby D2).

Typy pułapek (kuszą do skrótu dającego złą odpowiedź):
- **złe równanie** (L7): przesunięcie czasu w układzie („za 6 lat");
- **średnia ważona vs prosta** (L8-01), **znak przy odpływie** (L8-03);
- **wyczerpująca analiza przypadków** (L8-02 logika kłamców);
- **ruch względny z przesuniętym startem** (L9-01 pociągi);
- **zliczanie permutacji pod ograniczeniami** (L9-02);
- **wykrycie sprzeczności** (L9-03 — warunki niespełnialne, odp. „sprzecznosc"; test czy model nie
  „halucynuje" odpowiedzi na źle postawione zadanie);
- **składanie procentów zamiast sumowania** (L10-01);
- **układ równań z czasem w dwie strony** (L10-02);
- **model robotniko-dni w fazach** (L10-03).

## Gradient (S3/T3)
Poziomy 7–10 (długość łańcucha / liczba współzależnych ograniczeń): 2 itemy L7, 3× L8, 3× L9, 3× L10.

## Schemat, ocena, pomiar
Identyczne jak `d1-rozumowanie-v1` (schemat itemu, grader deterministyczny, 3 parafrazy/item, taksonomia
awarii S3, estymacja S5). Itemy z odpowiedzią zamkniętą mają `klasy_odpowiedzi` (L8-02, L9-03).

## Użycie
```bash
python ../../tools/contamination_check.py --train <trening.jsonl> --eval eval.jsonl
python ../../tools/run_eval.py --eval eval.jsonl --base-url <url> --model <id> --out wyniki.json
```

## Status / następne
v1, eval-only, audyt 0%, GT zweryfikowane. Cel: przejazd panelu → sprawdzić, czy przebija sufit
(rozrzut w górnej połowie: gemma vs Slayer vs qwen). Wynik zasili estymację $\theta^{(D1)}$ z szerszym
zakresem trudności (lepsza kalibracja $b_j$, S5).

## Powiązania
[[../d1-rozumowanie-v1/README|d1-rozumowanie-v1]] (łatwy) · [[../../docs/90-Ewaluacja/Analiza-Panel-D1-D2|analiza panelu]] · [[../../docs/25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../../docs/25-Syntezy/S5-MIRT-Panel|S5]]
