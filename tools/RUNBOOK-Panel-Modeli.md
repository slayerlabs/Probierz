---
type: runbook
id: BENCH-RB-PANEL
title: "Runbook: przejazd panelu modeli (baseline) z zarządzaniem VRAM"
status: aktywny
author: Arkadiusz Słota
date: 2026-07-02
---

# Runbook — przejazd panelu modeli przez zestawy eval

> Jak przejechać panel ≥5 modeli przez zestawy D1–D6 na maszynie z **ograniczonym VRAM (4 GB)**.
> Zasada: **jeden model naraz** (sekwencyjnie), rozładowanie po użyciu. Panel jest warunkiem
> wniosków (S5, DEC1) — bez niego estymacja i test rozłączności są nieidentyfikowalne.

## Skład panelu (gradient słaby→mocny)
| Model | Rozmiar | Endpoint |
|---|---|---|
| `bielik-1.5b-v3.0-instruct` | 1.5B | LM Studio `http://127.0.0.1:1234/v1` |
| `qwen/qwen3-1.7b` | 1.7B | LM Studio |
| `nvidia/nemotron-3-nano-4b` | 4B | LM Studio |
| `google/gemma-3n-e4b` | ~4B | LM Studio |
| `slayer-v49-qwen3.5-27b` | 27B | proxy `http://127.0.0.1:8799/v1` (patrz runbook proxy) |

## Ograniczenie VRAM (4 GB) — twarda reguła
- **Nigdy dwa modele generatywne naraz.** LM Studio używa **JIT loading**: ładuje model przy pierwszym
  żądaniu, `not-loaded` gdy nieużywany. Realnie w VRAM jest tylko aktualnie odpytywany model.
- Po skończeniu przejazdu danym modelem: **rozładuj**, zanim ruszysz następny.
- Slayer jest zdalny (przez proxy) — nie zajmuje lokalnego VRAM; można go przejechać niezależnie.

## Procedura (per model LM Studio)
```bash
# 1. przejazd obu wymiarow tym samym modelem (model laduje sie raz, JIT)
python run_eval.py --eval ../benchmarks/d1-rozumowanie-v1/eval.jsonl \
  --base-url http://127.0.0.1:1234/v1 --model <MODEL> \
  --out ../benchmarks/d1-rozumowanie-v1/wyniki-<MODEL_SLUG>.json
python run_eval.py --eval ../benchmarks/d2-semantyka-v1/eval.jsonl \
  --base-url http://127.0.0.1:1234/v1 --model <MODEL> \
  --out ../benchmarks/d2-semantyka-v1/wyniki-<MODEL_SLUG>.json

# 2. ROZLADUJ model (zwolnij VRAM) przed nastepnym
lms unload <MODEL>          # lub: lms unload --all
lms ps                      # weryfikacja: brak loaded generatywnych
```

## Sprzątanie końcowe
```bash
lms unload --all            # zwolnij caly VRAM po panelu
```

## Uwagi operacyjne
- Runner ma **checkpoint per item + wznawianie** — przerwanie (timeout, unload w zlym momencie) nie
  traci postepu; ponowne uruchomienie z tym samym `--out` dokancza.
- Lokalne modele bywaja wolne (gemma ~25 s/wywolanie); 10 itemow × 3 parafrazy = ~12 min/wymiar.
- Nazwa pliku wynikowego: `wyniki-<model-slug>.json` w katalogu danego wymiaru (obok `eval.jsonl`).
- Po zebraniu macierzy [model × wymiar]: estymacja (Bradley-Terry + 1PL, bootstrap CI, S5) + test
  rozlacznosci (S4). Patrz DEC1 dla mini-testu D1↔D2.

## Powiązania
[[../docs/25-Syntezy/S5-MIRT-Panel|S5]] · [[../docs/20-Decyzje/D-DEC1-Kolejnosc-Wymiary-Vs-Panel|DEC1]] · [[../docs/90-Ewaluacja/Stan|Stan]]
