---
type: synteza
id: BENCH-S3
title: "Gradient trudności (IRT) + taksonomia awarii"
status: propozycja
parents: ["BENCH-T3", "BENCH-AT3"]
author: Arkadiusz Słota
date: 2026-06-26
---

# S3 — Bezlitosny w punkcie dyskryminacji (rozstrzyga AT3)

## Rozstrzygnięcie
„Bezlitosny" ≠ „wszyscy 0%". Celujemy w **punkt dyskryminacji** — trudność, gdzie modele *różnią się*
najbardziej (IRT: maksymalna informacja itemu tam, gdzie p(sukces) ≈ 0.5, nie 0).

## Procedura
1. **Panel kalibracyjny:** odpal kandydatów itemów na **wielu modelach** (słaby → mocny). Item, który łamie *wszystkich* lub *nikogo* = niska informacja, odrzuć/przesuń.
2. **Gradient:** zachowaj itemy o p(sukces) w paśmie 0.2–0.8 — tam jest sygnał progresu.
3. **Taksonomia awarii** (nie sama accuracy): każdy fail klasyfikuj —
   `halucynacja` / `błędny-plan` / `ciche-pominięcie` / `format` / `pętla`. Ciche pominięcie =
   najgorszy tryb (niewidoczne bez audytu — jak false-discard u Xaviera, S2 sandboxa).
4. **Rotacja poprzeczki:** gdy modele nasycą pasmo → dodaj trudniejsze itemy (benchmark żyje).

## Anty-cyrkularność (odpowiedź na AT3)
Kalibrujemy na **panelu istniejących modeli**, nie na tym jednym ocenianym → trudność jest zmierzona
na niezależnej próbce. Mała próbka = duża wariancja (AT3 słusznie) → minimalny panel ≥ 5 modeli +
bootstrap CI na oszacowaniu trudności.

## Powiązania
parents: [[../10-Tezy/T3-Bezlitosne-Mierzalne|T3]], [[../15-Antytezy/AT3-Floor-Effect|AT3]]
