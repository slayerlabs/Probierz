---
type: benchmark
id: BENCH-D5-ORK-HARD-V1
title: "d5-orkiestracja-hard-v1 — dłuższe workflow (granica planowania sekwencji)"
status: eval-only
parents: ["BENCH-D5-ORK-V1", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d5-orkiestracja-hard-v1 🇵🇱

> **6 zadań: dłuższe i złożone workflow orkiestracji.** Cel: **zlokalizować granicę** planowania
> sekwencji Slayera. `d5-orkiestracja-v1` pokazał, że 2-krokowy workflow (read→write) bywa niestabilny
> (1/3). Tu sprawdzamy 3–5 kroków, warunki, zależności danych i dystraktor.

## Motywacja (z analizy D5)
Hipoteza „mocny krok, słaby łańcuch": Slayer solidny na pojedynczym wywołaniu, słabszy w planowaniu
sekwencji. Ten zestaw z gradientem długości ma pokazać, **gdzie dokładnie** się łamie (przy ilu krokach).

## Pokrycie (gradient długości + typy)
| ID | Długość | Test | Predykat |
|---|---|---|---|
| D5BH-SEQ3-01 | 3 | search→write→read | json_seq_order |
| D5BH-SEQ4-01 | 4 | read→search→write→run | json_seq_order |
| D5BH-SEQ5-01 | 5 | dokładna sekwencja 5 kroków | json_seq_len_order |
| D5BH-COND-01 | 3 | warunkowe (ścieżka gdy plik istnieje) | json_seq_order |
| D5BH-DEP-01 | 2 | zależność danych (wynik→zapis, referencja) | json_seq_dep |
| D5BH-SEQ4-02 | 4 | dystraktor (BEZ search mimo wzmianki) | json_seq_no_tool |

## Co testuje
- **Długość planu:** czy przy 3/4/5 krokach Slayer podaje pełną sekwencję, czy urywa.
- **Zależność danych:** czy krok zapisu odwołuje się do wyniku wyszukiwania (placeholder/referencja),
  czy „gubi" przepływ danych między krokami.
- **Dystraktor:** zadanie wspomina „nie używaj search" — czy model pomija zbędne narzędzie.
- **Warunkowość:** plan dla zadanej gałęzi warunku.

## Ocena
Predykaty JSON-aware (`run_eval.py`): `json_seq_order` (podciąg w kolejności), `json_seq_len_order`
(dokładna długość+kolejność), `json_seq_dep` (referencja do wyniku w ostatnim kroku), `json_seq_no_tool`
(sekwencja bez zabronionego narzędzia). Zweryfikowane. 3 parafrazy/item (AT5), wynik = mediana.

## Powiązania
[[../d5-orkiestracja-v1/README|d5-orkiestracja-v1]] · [[../../docs/90-Ewaluacja/Analiza-D5-Wiernosc-Instrukcji|analiza D5]] · [[../../docs/20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
