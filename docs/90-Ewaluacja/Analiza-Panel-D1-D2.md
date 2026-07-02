---
type: analiza
id: BENCH-ANALIZA-PANEL-D1D2
title: "Analiza panelu 5×2 — rozłączność D1↔D2 (faza research)"
status: aktywny
parents: ["BENCH-C2", "BENCH-S4", "BENCH-S5", "BENCH-DEC1"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza panelu 5 modeli × 2 wymiary (D1 rozumowanie, D2 semantyka)

> Faza **research** wg metody (problem → model matematyczny → baseline → research → eval).
> Cel: rozstrzygnąć rozłączność D1↔D2 (warunek C2/S4) na pierwszym pełnym panelu.

## Panel (gradient słaby→mocny)
5 modeli: bielik-1.5b, qwen3-1.7b, nemotron-4b, gemma-3n-e4b, slayer-v49-27B.
Każdy przejechany przez D1 (10 itemów) i D2 (10 itemów), ocena deterministyczna (T5), 3 parafrazy/item
(AT5, wynik = mediana). Zestawy czyste (audyt 0%, C1/T1). Modele lokalne przez LM Studio, Slayer przez
proxy; sekwencyjnie z rozładowaniem VRAM (4 GB, patrz RUNBOOK-Panel-Modeli).

## Macierz wyników (pass/10)
| Model | D1 | D2 |
|---|---|---|
| gemma-3n-e4b (~4B) | **10** | 7 |
| slayer-v49 (27B) | 9 | **9** |
| nemotron-4b | 8 | 5 |
| qwen3-1.7b (~1.7B) | 8 | 6 |
| bielik-1.5b | **2** | 5 |

## Rankingi (nie są identyczne)
- **D1:** gemma(10) > slayer(9) > nemotron(8) = qwen(8) > bielik(2)
- **D2:** slayer(9) > gemma(7) > qwen(6) > nemotron(5) = bielik(5)

## Statystyki rozłączności
| Miara | Wartość | Interpretacja |
|---|---|---|
| Spearman ρ(D1,D2) po modelach | **0.80** | rankingi różne, ale skorelowane |
| Pearson r(D1,D2) po modelach | **0.58** | umiarkowana korelacja, **nie** bliska 1 |
| Udział 1. składowej głównej | **79%** | **< 90%** → jest miejsce na 2. wymiar |
| Kierunkowe odwrócenia par (D1 vs D2) | 1/10 | slayer vs gemma |
| **Istotne** odwrócenia (bootstrap CI, S4) | **0/10** | brak mocy przy 10 itemach |

## Obserwacje jakościowe (zgodne z konstruktem)
- **Rozjazd bielika:** najsłabszy w rozumowaniu (D1=2, floor), ale przeciętny w semantyce (D2=5).
  Model 1.5B po polsku „rozumie" zdania, ale nie składa wieloetapowego wnioskowania.
- **Rozjazd gemma↔slayer:** gemma (4B) lepsza w D1 (10 vs 9), słabsza w D2 (7 vs 9). Większy Slayer
  ma przewagę w subtelnej semantyce (koreferencja, implikatura), nie w arytmetyce wieloetapowej.
- **D2 systematycznie trudniejszy:** rozrzut D2 (9–5) szerszy i niżej niż D1 (10–2 z jednym floor);
  semantyka lepiej różnicuje górną część panelu.
- Faile skupione na poziomie 4 obu wymiarów (koreferencja, implikatura, pułapka brzegowa) — gradient
  trudności działa.

## Wniosek (uczciwie)
Dane **nie rozstrzygają** rozłączności w sensie twardego kryterium S4:
- **Przeciw jednowymiarowości (AT4):** r=0.58 i 1. składowa 79% (<90%) — konstrukt **nie** wygląda na
  jednowymiarowy; jest wariancja dla drugiego wymiaru. Kierunek i rozjazdy (bielik, gemma↔slayer)
  wspierają dekompozycję.
- **Brak dowodu rozłączności:** 0/10 **istotnych** odwróceń — przy 10 itemach przedziały ufności są
  za szerokie. To **problem mocy statystycznej**, nie brak efektu (por. DEC1, fakt techniczny).

## Konsekwencje operacyjne
1. **Więcej itemów per wymiar** — 10 to za mało na wąskie CI; celować w ~20–30, by istotność odwróceń
   stała się osiągalna.
2. **K ≥ 4 wymiary** (D3–D6) — analiza składowych/równoległa potrzebuje ≥4 kolumn, by testować
   strukturę wielowymiarową (przy K=2 mamy tylko udział 1. składowej, bez analizy równoległej).
3. Panel 5 modeli jest wystarczający jako punkt startowy; rozszerzać przy DIF/stabilności.

## Rozstrzygnięcie DEC1
Wynik potwierdza rekomendację **T-DEC1 z warunkiem**: budować D3–D6 (kierunek wspiera dekompozycję, brak
istotności wynika z mocy nie z efektu), **równolegle zwiększając liczbę itemów**. Nie ma przesłanki do
AT-DEC1 (współliniowość) — r=0.58 i 79% jej przeczą.

## Powiązania
[[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · [[../25-Syntezy/S5-MIRT-Panel|S5]] · [[../20-Decyzje/D-DEC1-Kolejnosc-Wymiary-Vs-Panel|DEC1]] · [[../15-Antytezy/AT4-Splatanie-Czynnik-G|AT4]] · [[Stan|Stan]]
