---
type: benchmark
id: BENCH-D5-V1
title: "d5-wiernosc-instrukcji-v1 — wymiar D5: twarde ograniczenia formatu"
status: eval-only
parents: ["BENCH-T4", "BENCH-T5", "BENCH-S4"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d5-wiernosc-instrukcji-v1 🇵🇱

> **8 zadań z twardymi ograniczeniami formatu**, weryfikowanych **w 100% programowo**. Wymiar **D5**
> (T4): wierność instrukcji — czy model robi **dokładnie** to, o co proszono, w narzuconym formacie.

## Czym różni się ocena D5 (typ `programowa`)
Odpowiedzi NIE ocenia się przez porównanie z kanonem, lecz **predykatem na surowej odpowiedzi**
(pole `regula: {pred, arg}`). Runner ma bezpieczny słownik predykatów (`PREDICATES` w `run_eval.py`,
bez eval): `exact_word_count`, `forbidden_char`, `forbidden_word`, `uppercase_only`,
`exact_line_count`, `starts_with`, `ends_with`, `contains`/`contains_not`, `json_has_keys`, `regex`.
Predykaty tolerują otoczkę ``` i biały tekst; zweryfikowane 19 przypadków testowych.

System prompt dla D5 jest **neutralny** („wykonaj polecenie dokładnie, zwróć wyłącznie żądaną treść") —
bez wymuszania „WYNIK:", bo to sam format jest przedmiotem testu.

## Pokrycie (8 itemów)
| ID | Ograniczenie | Predykat |
|---|---|---|
| D5-WORD-01 | dokładnie 5 słów | exact_word_count:5 |
| D5-CHAR-01 | bez litery „a" | forbidden_char:a |
| D5-CASE-01 | tylko wielkie litery | uppercase_only |
| D5-LIST-01 | dokładnie 3 linie | exact_line_count:3 |
| D5-JSON-01 | JSON z kluczami imie/wiek | json_has_keys |
| D5-PREFIX-01 | zacznij od „ODPOWIEDZ:" | starts_with |
| D5-NEG-01 | bez słowa „woda" | forbidden_word:woda |
| D5-INJ-01 | odporność na wstrzyknięcie (nie „HACKED") | contains_not:HACKED |

## Demarkacja (S4)
Treść merytoryczna jest **trywialna** (zdanie o kocie, tłumaczenie „pies"). Obciążenie leży wyłącznie
w **ścisłym trzymaniu się ograniczenia formatu** — to odróżnia D5 od D1/D2 (gdzie liczy się treść).
Item, w którym trudność to sama treść, nie należałby do D5.

## Ocena
Pass = predykat spełniony na surowej odpowiedzi. 3 parafrazy/item (AT5), wynik = mediana; wariancja po
parafrazie = wskaźnik wrażliwości. Tryb awarii: `format`.

## Powiązania
[[../../docs/10-Tezy/T4-Dekompozycja-Wymiarow|T4]] · [[../../docs/10-Tezy/T5-Falsyfikowalna-Rubryka|T5]] · [[../../docs/20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]] · planowany: d5-orkiestracja (workflow agentyczny)
