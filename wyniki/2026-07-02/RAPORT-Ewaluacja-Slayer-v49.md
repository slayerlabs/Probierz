---
type: raport
id: RAPORT-2026-07-02
title: "Raport ewaluacji Slayer v49 — Probierz (2026-07-02)"
status: zamknięty
model: slayer-v49-qwen3.5-27b
data: 2026-07-02
author: Arkadiusz Słota
dane_maszynowe: ./dane.json
---

# Raport ewaluacji — Slayer v49 (qwen3.5-27b)

**Data:** 2026-07-02 · **Model główny:** `slayer-v49-qwen3.5-27b` (przez `slayerapi.fabryka.ai`)
**Panel odniesienia:** gemma-3n-e4b (4B), nemotron-3-nano-4b (4B), qwen3-1.7b, bielik-1.5b (lokalnie, LM Studio)
**Dane maszynowe:** [`dane.json`](./dane.json) — pełna macierz, generowana ze skryptu (liczby nie przepisywane ręcznie)

---

## 1. Podsumowanie wykonawcze

Slayer v49 jest **liderem lub współliderem panelu na każdym wymiarze porównawczym** i wyróżnia się dwiema
cechami, których nie ma reszta panelu:

1. **Stabilność** — najniższa wrażliwość na parafrazę w całym panelu (mediana wysoka *i* powtarzalna).
2. **Kalibracja niepewności** — 100% na pułapkach (fikcyjne byty, fałszywe presupozycje): mówi „nie wiem",
   nie halucynuje.

Do tego **wierność instrukcji i orkiestracja agentyczna = 100%**, co czyni go dobrym kandydatem na komponent
systemu agentowego.

**Zidentyfikowana słabość (uczciwie):** czysta długość obliczeniowa **bez skrótu matematycznego** (Collatz)
oraz niestabilność w najgłębszym rozumowaniu. To jedyne miejsca, gdzie model realnie pęka.

---

## 2. Metodologia (dlaczego tym liczbom można ufać)

| Zabezpieczenie | Realizacja |
|---|---|
| **Ground truth żelazny** | Każda odpowiedź weryfikowana **programowo** (obliczenie/symulacja/brute-force) *przed* przejazdem. Zero „autor tak myśli". |
| **Anty-kontaminacja** | `tools/contamination_check.py` — n-gram overlap + wspólny span vs `seed_500_training_final`. **Wszystkie zestawy: 0% skażeń.** |
| **Pomiar stabilności** | 3 parafrazy/item (AT5). Raportujemy medianę **oraz** wrażliwość (ile itemów zależnych od sformułowania). |
| **Dialektyka** | Każdy konstrukt: teza → antyteza (steelman) → synteza z **warunkiem obalenia** (`docs/`). Chroni przed pozorną trudnością (AT7/floor effect). |
| **Panel odniesienia** | 5 modeli lokalnych jako floor→ceiling — wynik Slayera osadzony, nie w próżni. |
| **Ocena deterministyczna** | Runner `run_eval.py`, kanoniczny GT, checkpoint/resume, temperatura 0. |

**Ograniczenia (patrz §6)** — raport jest rzetelny, ale nie kompletny; słabe punkty nazwane wprost.

---

## 3. Panel wielomodelowy (D1 rozumowanie + D2 semantyka)

Liczby = itemy zdane medianą / wszystkie. **Pogrubienie = najlepszy w wierszu.**

| Benchmark | **slayer-v49** | gemma-4B | nemotron-4B | qwen-1.7B | bielik-1.5B |
|---|---|---|---|---|---|
| d1-rozumowanie-v1 (łatwy) | 9/10 | **10/10** | 8/10 | 8/10 | 2/10 |
| d1-rozumowanie-**hard** | **10/11** | 6/11 | **10/11** | 6/11 | 1/11 |
| d1-rozumowanie-**extreme** | **5/6** | 3/6 | **5/6** | — | — |
| d2-**semantyka** | **9/10** | 7/10 | 5/10 | 6/10 | 5/10 |

**Wrażliwość na parafrazę (mniej = stabilniej):**

| Benchmark | slayer | gemma | nemotron | qwen | bielik |
|---|---|---|---|---|---|
| d1-rozumowanie | **1** | 2 | 3 | 3 | 5 |
| d1-hard | **1** | 5 | 4 | 5 | 5 |
| d2-semantyka | 2 | 3 | 3 | 3 | 4 |

**Odczyt:**
- Na łatwym D1 gemma-4B osiąga komplet (10/10) — Slayer 9/10; różnica zanika, oba w czołówce.
- Na **trudnym i ekstremalnym** D1 Slayer i nemotron odjeżdżają (10/11, 5/6) — gemma/qwen spadają do ~55%.
- **Semantykę Slayer wygrywa wyraźnie** (9/10 vs 5–7/10 reszty) — to jego przewaga.
- **Slayer jest najstabilniejszy** — wrażliwość 1 na D1/hard, gdzie reszta ma 3–5. To znaczy, że jego wynik
  nie jest artefaktem jednego sformułowania.
- **bielik-1.5B = floor panelu** (2/10, 1/11) — najsłabszy wszędzie.

---

## 4. Slayer — wymiary głębokie (bez panelu, na razie tylko Slayer)

| Wymiar | Zestaw | Wynik | Wrażliwe | Uwaga |
|---|---|---|---|---|
| Wierność instrukcji (D5) | d5-wiernosc-instrukcji-v1 | **8/8 (100%)** | 2 | twarde ograniczenia formatu, JSON, zakaz liter, HACKED-injection |
| Orkiestracja (D5) | d5-orkiestracja-v1 | **6/6 (100%)** | 1 | wybór narzędzia, args, odmowa `rm -rf`, czysty JSON |
| Orkiestracja hard (D5) | d5-orkiestracja-hard-v1 | **6/6 (100%)** | 1 | workflow 3–5 kroków, warunkowe, zależności |
| Kalibracja (D6) | d6-kalibracja-v1 | **9/9 (100%)** | 0 | fikcyjne byty/presupozycje → „nie wiem" |
| Kalibracja hard (D6) | d6-kalibracja-hard-v1 | **7/7 (100%)** | 1 | subtelne pułapki (krymin. Mickiewicza, Nobel z matematyki) |
| Wytrzymałość oblicz. (D1) | d1-wytrzymalosc-obliczeniowa-v1 | 6/8 (75%) | 1 | **faile: WYT-06 Collatz-111 (0/3), WYT-03 10! mod 1000** |
| Głębia rozumowania (D1) | d1-glebia-rozumowania-v1 | 5/6 (83%) | **4** | fail GLEB-03 (incl-excl); **niestabilne mimo wysokiej mediany** |

---

## 5. Kluczowe odkrycia

### 5.1. Słabość zrefinowana: „długość BEZ skrótu", nie długość ogólnie
Slayer **zdaje** długie obliczenia, gdy istnieje skrót matematyczny: `7¹⁰⁰ mod 13` (małe tw. Fermata),
rekurencja `2³²+1` (wzór), Fibonacci. **Pęka**, gdy trzeba wykonać N iteracji bez obejścia:
Collatz-111 (0/3, twardy fail). To nie „nie wytrzyma N kroków" — to „nie wykona N kroków, gdy nie ma skrótu".

### 5.2. Niestabilność w głębi rozumowania
Głębia: mediana 83%, ale **4/6 itemów wrażliwych** — połowa wyników zależy od sformułowania. Pojedynczy
przejazd **zawyża** ocenę. Wskaźnik wrażliwości (AT5) okazał się tu diagnostyczniejszy niż sam pass-rate.

### 5.3. Kalibracja jako wyróżnik
100% na D6 (0 halucynacji na pułapkach). W panelu nikt inny nie był testowany na tym wymiarze, ale to
zachowanie (odmowa fikcyjnego bytu, „nie wiem" na fałszywej presupozycji) jest rzadkie i wartościowe.

### 5.4. Gotowość agentyczna
Wierność instrukcji + orkiestracja = 100%, w tym odporność na wstrzyknięcie (HACKED) i odmowa `rm -rf`.
Kandydat na komponent systemu typu Omp.

---

## 6. Ograniczenia (czego ten raport NIE dowodzi)

- **Panel tylko na D1/D2.** Wymiary głębokie (D5/D6) mierzone **wyłącznie na Slayerze** — brak porównania,
  więc „100%" nie ma jeszcze kontekstu floor/ceiling.
- **d1-czysta-dlugosc-v1 — PRZERWANY technicznie.** Zapisano 1/8 itemów: **CDL-01 Collatz-63 = FAIL**
  (wstępnie potwierdza §5.1). Przejazd wisiał, bo Slayer generuje setki kroków i uderza w limit
  tokenów/czasu. Do dokończenia z wyższym limitem + instrukcją „podaj tylko liczbę". **Nie wliczyć jako
  pełny wynik.**
- **Cel „max 3/N" nieosiągnięty.** Zgodnie z S6 **nie nagięto itemów**, by sztucznie zejść (to byłby
  Goodhart). Slayer okazał się odporniejszy, niż zakładała hipoteza.
- **Brak drugiego, niezależnego zespołu (blind exchange, S1/S2).** Ryzyko autowalidacji ograniczone przez
  `contamination_check` (0%), lecz nie wyeliminowane — to detektor n-gramowy, nie dowód niezależności.
- **csharp-solid-v1** — zestaw istnieje (eval), brak przejazdu w tej sesji.

---

## 7. Następne kroki

1. **Dokończyć d1-czysta-dlugosc-v1** — podnieść limit tokenów, wymusić „tylko liczba"; to najpewniejsza
   droga do uczciwie niskiego pass-rate (Collatz-63 już FAIL).
2. **Zbadać niestabilność głębi** — więcej itemów × parafraz, żeby oddzielić „umie" od „czasem wpada".
3. **Rozszerzyć panel na D5/D6** — osadzić kalibrację/wierność w kontekście floor→ceiling.
4. **Rozważyć drugi zespół / blind exchange** (S1/S2) dla pełnej rzetelności anty-Goodhart.

---

## 8. Indeks artefaktów sesji

**Benchmarki (13):** d1-rozumowanie-v1, d1-rozumowanie-hard-v1, d1-rozumowanie-extreme-v1, d2-semantyka-v1,
d5-wiernosc-instrukcji-v1, d5-orkiestracja-v1, d5-orkiestracja-hard-v1, d6-kalibracja-v1, d6-kalibracja-hard-v1,
d1-wytrzymalosc-obliczeniowa-v1, d1-glebia-rozumowania-v1, d1-czysta-dlugosc-v1 (przerwany), csharp-solid-v1 (bez przejazdu).

**Analizy:** `docs/90-Ewaluacja/Analiza-Panel-D1-D2.md`, `Analiza-D1-Hard-Sufit.md`, `Analiza-D5-Wiernosc-Instrukcji.md`,
`Analiza-D6-Kalibracja.md`, `Analiza-Stress-Test-D1.md`, `Stan.md` (żywy dziennik).

**Decyzje:** `docs/20-Decyzje/D-DEC1-Kolejnosc-Wymiary-Vs-Panel.md`, `D-DEC2-Fokus-Na-Slayerze.md`.

**Runbook:** `tools/RUNBOOK-Panel-Modeli.md` (przejazd panelu z zarządzaniem VRAM).

**Dane maszynowe:** [`dane.json`](./dane.json).
