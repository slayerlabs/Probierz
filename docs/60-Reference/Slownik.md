---
type: reference
id: BENCH-SLOWNIK
title: "Słownik — Probierz"
status: aktywny
author: Arkadiusz Słota
date: 2026-06-26
---

# Słownik

- **Kontaminacja** — eval „przeciekł" do treningu; model widział odpowiedzi → mierzysz pamięć, nie zdolność.
- **Provenance** — udokumentowane pochodzenie danych (źródło + etykieta trening/eval). Nasza przewaga: dane od zera.
- **N-gram overlap** — miara dosłownego pokrycia (n=13 wg dedup Llama). Ten sam mechanizm n-gram co w `micro-models` (detektor dosłownej pamięci).
- **Near-verbatim** — overlap ≈ 1.0; dosłowna kopia → usuń z eval bezwzględnie.
- **Blind exchange** — dwa teamy wymieniają benchmarki, których wzajemnie nie widziały → niezależny ground truth (anty-Goodhart).
- **Commitment scheme** — publikacja hashu zestawu PRZED ujawnieniem; dowód, że autor nie podmienił go pod wynik.
- **Spalony** — benchmark ujawniony przy wymianie; jednorazowy → wraca do treningu, koniec jako eval.
- **Floor effect** — benchmark tak trudny, że wszyscy ~0% → zero dyskryminacji, brak sygnału progresu.
- **Dyskryminacja (IRT)** — zdolność itemu do rozróżniania modeli; maks. informacja przy p(sukces) ≈ 0.5.
- **Taksonomia awarii** — klasyfikacja *jak* model pęka: halucynacja / błędny-plan / ciche-pominięcie / format / pętla.
- **Ciche pominięcie** — model po cichu nie robi części zadania; najgorszy tryb (niewidoczny bez audytu — por. false-discard, Xavier/M4).
- **Panel kalibracyjny** — zestaw modeli (słaby→mocny) do pomiaru trudności itemu niezależnie od ocenianego.

## Powiązania zewnętrzne
M3 (Goodhart/watcher), M4 (AI-first-pass + ground-truth), Dendrometria (mierz, nie deklaruj), `micro-models` (n-gram), `slayerlabs/datasets`.
