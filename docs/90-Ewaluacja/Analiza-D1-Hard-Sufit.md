---
type: analiza
id: BENCH-ANALIZA-D1-HARD
title: "Analiza D1-brutalny — przebicie sufitu koryguje ranking (gemma vs Slayer)"
status: aktywny
parents: ["BENCH-T3", "BENCH-S3", "BENCH-D1-HARD-V1"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza — brutalny D1 obala mylący ranking z łatwego zestawu

> Empiryczne potwierdzenie tezy T3/S3: łatwy benchmark daje **mylący** ranking (sufit); dopiero
> bezlitosny w punkcie dyskryminacji ujawnia prawdziwą zdolność.

## Wyniki
| Model | D1-łatwy (10 itemów) | D1-brutalny (11 itemów) |
|---|---|---|
| gemma-3n-e4b (~4B) | **10/10 (1.00)** | **6/11 (0.55)** |
| slayer-v49 (27B) | 9/10 (0.90) | **10/11 (0.91)** |

## Per-item (brutalny) — dominacja Slayera
| Item | Poziom | Slayer | gemma |
|---|---|---|---|
| L7-01, L7-02 | 7 | PASS | PASS |
| L8-01, L8-02 | 8 | PASS | PASS |
| **L8-03** (znak przy odpływie) | 8 | PASS | **fail** |
| L9-01 | 9 | PASS | PASS |
| **L9-02** (permutacje pod ograniczeniami) | 9 | PASS | **fail** |
| L9-03 (wykrycie sprzeczności) | 9 | fail | fail |
| **L10-01** (składanie procentów) | 10 | PASS | **fail (0/3)** |
| L10-02 | 10 | PASS | PASS |
| **L10-03** (robotniko-dni w fazach) | 10 | PASS | **fail** |

- **Slayer zdał 4 itemy, które gemma oblała. Gemma nie zdała żadnego, którego Slayer by nie zdał**
  (dominacja Pareto: Slayer ≥ gemma na każdym itemie).
- Wspólny fail: L9-03 (wykrycie sprzeczności warunków) — trudny dla obu; kandydat na jeszcze wyższy
  poziom dyskryminacji.

## Wniosek
1. **Ranking z łatwego D1 był artefaktem sufitu.** gemma 10/10 vs Slayer 9/10 sugerowało „gemma ≥
   Slayer w rozumowaniu" — **fałsz**. Oba modele umiały szkolną arytmetykę (2–7 kroków); różnica 10 vs
   9 mieściła się w szumie (potwierdzone wcześniej: CI obejmowały 0).
2. **Brutalny zestaw ujawnił prawdziwą zdolność.** Przy łańcuchach 8–10 kroków i pułapkach
   (składanie procentów, permutacje, bilans ze znakiem) gemma 4B załamuje się (0.55), Slayer 27B
   utrzymuje poziom (0.91). To zgodne z oczekiwaniem: większy model ma głębsze rozumowanie
   wieloetapowe — ale **dowód jest empiryczny, nie założony**.
3. **Wrażliwość na parafrazę:** gemma 5/11 wrażliwych (niestabilna pod trudnością), Slayer 1/11
   (stabilny). To dodatkowy wymiar przewagi — nie tylko średnia, ale powtarzalność.

## Znaczenie metodologiczne (T3/S3)
Gdyby modele oceniono wyłącznie łatwym D1, ogłoszono by błędny wniosek „gemma 4B ≈ Slayer 27B w
rozumowaniu". Brutalny zestaw w **punkcie dyskryminacji** (S3: informacja itemu maksymalna przy p≈0.5)
obalił go. To jest operacyjny dowód, po co Probierz istnieje: **czysty benchmark w punkcie
dyskryminacji > łatwy benchmark bez sufitu**.

## Konsekwencje dla pomiaru (S5)
- Zakres trudności `d1-rozumowanie-hard-v1` jest dobrze dobrany dla górnej półki panelu — daje sygnał
  tam, gdzie łatwy zestaw miał sufit. Do estymacji $\theta^{(D1)}$ łączyć oba zestawy (szeroki zakres
  $b_j$: łatwy pokrywa dolną półkę — bielik, hard górną — gemma/Slayer).
- Następny krok: przejazd hard przez resztę panelu (nemotron, qwen, bielik) → pełna macierz z
  rozciągniętym gradientem trudności; wtedy estymacja Rascha ma dane od floor do ceiling.

## Powiązania
[[../10-Tezy/T3-Bezlitosne-Mierzalne|T3]] · [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../../benchmarks/d1-rozumowanie-hard-v1/README|d1-rozumowanie-hard-v1]] · [[Analiza-Panel-D1-D2|analiza panelu 5×2]]
