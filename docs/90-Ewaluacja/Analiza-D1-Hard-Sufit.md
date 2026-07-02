---
type: analiza
id: BENCH-ANALIZA-D1-HARD
title: "Analiza D1-brutalny — przebicie sufitu koryguje ranking (panel 5 modeli)"
status: aktywny
parents: ["BENCH-T3", "BENCH-S3", "BENCH-D1-HARD-V1"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza — brutalny D1 obala mylący ranking z łatwego zestawu

> Empiryczne potwierdzenie tezy T3/S3: łatwy benchmark daje **mylący** ranking (sufit); dopiero
> bezlitosny w punkcie dyskryminacji ujawnia prawdziwą zdolność.

## Pełny panel 5 modeli — D1 łatwy vs brutalny
| Model | D1-łatwy (10) | D1-brutalny (11) | delta |
|---|---|---|---|
| Slayer v49 (27B) | 9/10 (90%) | **10/11 (91%)** | +1pp |
| nemotron-4b | 8/10 (80%) | **10/11 (91%)** | +11pp |
| gemma-3n-e4b (4B) | **10/10 (100%)** | 6/11 (55%) | **−45pp** |
| qwen3-1.7b | 8/10 (80%) | 6/11 (55%) | −25pp |
| bielik-1.5b | 2/10 (20%) | 1/11 (9%) | −11pp |

### Ranking na D1-brutalnym (prawdziwa głębia rozumowania)
1. **Slayer v49 (27B) — 91%**
2. **nemotron-4b — 91%**
3. gemma-3n-e4b (4B) — 55%
4. qwen3-1.7b — 55%
5. bielik-1.5b — 9%

## Kluczowa obserwacja: dwuklasowość ukryta przez sufit
Na **łatwym** D1 górna czwórka była nierozróżnialna (8–10/10) — ranking sugerował nawet **gemma (10) >
Slayer (9)**. Brutalny zestaw ujawnił **dwie ligi rozumowania wieloetapowego**:
- **Liga A (~91%):** Slayer 27B i **nemotron-4b** — utrzymują poziom na łańcuchach 8–10 kroków.
- **Liga B (~55%):** gemma-4B i qwen-1.7B — załamują się na głębokich pułapkach (procenty składane,
  permutacje, bilans ze znakiem).
- **Floor:** bielik-1.5b (9%).

**Rozmiar nie determinuje wyniku:** nemotron-4b (4B) dorównał Slayerowi 27B, a gemma-4B (ten sam rząd
wielkości co nemotron) spadła do ligi B. Głębia rozumowania jest **cechą modelu, nie tylko skali** —
dokładnie sygnał, który łatwy benchmark całkowicie zamaskował.

## Per-item (Slayer vs gemma, brutalny) — dominacja Slayera
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
- Wspólny fail: L9-03 (wykrycie sprzeczności warunków) — trudny dla obu (nawet Slayer oblał, nemotron
  zdał 2/3); kandydat na jeszcze wyższy poziom dyskryminacji.

## Wniosek
1. **Ranking z łatwego D1 był artefaktem sufitu.** gemma 10/10 vs Slayer 9/10 sugerowało „gemma ≥
   Slayer w rozumowaniu" — **fałsz**. Różnica mieściła się w szumie (CI obejmowały 0).
2. **Brutalny zestaw ujawnił prawdziwą zdolność.** Przy łańcuchach 8–10 kroków górna liga (Slayer,
   nemotron) trzyma 91%, dolna (gemma, qwen) spada do 55%. Dowód empiryczny, nie założony.
3. **Wrażliwość na parafrazę:** Slayer 1/11, nemotron 4/11, gemma 5/11 — górna liga stabilniejsza
   również pod parafrazą (nie tylko wyższa średnia).

## Znaczenie metodologiczne (T3/S3)
Gdyby modele oceniono wyłącznie łatwym D1, ogłoszono by błędny wniosek „gemma 4B ≈ Slayer 27B w
rozumowaniu". Brutalny zestaw w **punkcie dyskryminacji** (S3: informacja itemu maksymalna przy p≈0.5)
obalił go i ujawnił dwuklasowość. To operacyjny dowód, po co Probierz istnieje: **czysty benchmark w
punkcie dyskryminacji > łatwy benchmark bez sufitu**.

## Konsekwencje dla pomiaru (S5)
- Łączenie łatwego + brutalnego D1 daje szeroki zakres trudności $b_j$ (floor: bielik → ceiling:
  Slayer/nemotron) — dobre dane do kalibracji Rascha.
- L9-03 (sprzeczność) łamie nawet ligę A — kandydat na poziom 11+ przy kolejnej rotacji poprzeczki.
- Do rozróżnienia ligi A (Slayer vs nemotron, oba 91%) potrzeba **jeszcze trudniejszych itemów** —
  sufit wrócił, tylko wyżej.

## Powiązania
[[../10-Tezy/T3-Bezlitosne-Mierzalne|T3]] · [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../../benchmarks/d1-rozumowanie-hard-v1/README|d1-rozumowanie-hard-v1]] · [[Analiza-Panel-D1-D2|analiza panelu 5×2]]
