---
type: benchmark
id: BENCH-D5-ORK-V1
title: "d5-orkiestracja-v1 — D5 orkiestracja agentyczna (Slayer jako orkiestrator)"
status: eval-only
parents: ["BENCH-D5-V1", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d5-orkiestracja-v1 🇵🇱

> **6 zadań: Slayer jako orkiestrator w systemie agentycznym** (jak Omp). Dostaje opis narzędzi +
> zasady + zadanie, ma wyprodukować poprawne wywołanie(-a). To trudniejsza forma D5: ograniczenia
> **kumulują się** (wybór narzędzia + format JSON + zasady + kolejność jednocześnie).

## Motywacja
D5a (pojedyncze ograniczenia formatu) dał sufit 8/8. Realne zastosowanie Slayera to jednak
**orkiestracja** — wybór akcji, format wywołań, trzymanie workflow. Tu jest znacznie więcej okazji do
pęknięcia niż przy jednym ograniczeniu.

## Scenariusz (system prompt orkiestratora)
Model dostaje listę narzędzi (`search`, `read`, `write`, `run`) i twarde zasady: odpowiadaj wyłącznie
jednym obiektem JSON `{tool, args}`, dokładnie jedno narzędzie, zero komentarzy. Zadanie to polecenie
użytkownika — model ma zmapować je na właściwe wywołanie.

## Pokrycie (6 itemów)
| ID | Test | Predykat |
|---|---|---|
| D5B-TOOL-01 | wybór `search` (kurs euro online) | json_tool_is:search |
| D5B-TOOL-02 | wybór `read` (plik lokalny, NIE search) | json_tool_is:read |
| D5B-ARGS-01 | `write` z args `path`+`content` | json_tool_args |
| D5B-REFUSE-01 | odmowa niedozwolonej akcji (rm -rf, zakaz) | json_tool_is:refuse |
| D5B-CLEAN-01 | cała odpowiedź = czysty JSON (zero gadania) | json_only_tool:search |
| D5B-SEQ-01 | sekwencja: `read` a.txt → `write` b.txt | json_seq_order |

## Co testuje (poza samym formatem)
- **Mapowanie intencji na narzędzie:** kurs online → search; plik lokalny → read (nie mylić).
- **Kompletność argumentów:** write bez `content` = fail.
- **Egzekwowanie zasad:** żądanie łamiące zasadę (usuwanie) → `refuse`, nie wykonanie.
- **Czystość wyjścia:** żadnego „Jasne! oto JSON…" — orkiestrator musi zwrócić parsowalne wywołanie.
- **Kolejność w workflow:** kopiowanie pliku = read przed write.

## Ocena
Predykaty JSON-aware (`run_eval.py`): `json_tool_is`, `json_tool_args`, `json_only_tool`,
`json_seq_order` — tolerują otoczkę ``` i tekst wokół (poza `json_only_tool`, który wymaga czystego
JSON). Zweryfikowane 12 przypadków. 3 parafrazy/item (AT5), wynik = mediana.

## Powiązania
[[../d5-wiernosc-instrukcji-v1/README|d5-wiernosc-instrukcji-v1]] (twarde ograniczenia) · [[../../docs/20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]] · [[../../docs/10-Tezy/T5-Falsyfikowalna-Rubryka|T5]]
