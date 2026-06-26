---
type: cel
id: BENCH-C1
title: "Cel — bezlitosne, kontaminacyjnie czyste benchmarki"
status: aktywny
author: Arkadiusz Słota
date: 2026-06-26
---

# C1 — Cel

## Po co
Budować benchmarki, które **łamią modele** (znajdują realne słabości), ale w skali dającej
**mierzalny progres** — nie floor effect. Przewaga strukturalna: **tworzymy dane od zera**, więc
*wiemy* co jest w treningu → możemy udowodnić, że eval jest czysty (held-out).

## Kryteria sukcesu (falsyfikowalne)
1. **Czystość:** każdy wydany benchmark przechodzi audyt kontaminacji (`contamination_check.py` → 0% skażonych itemów > próg).
2. **Dyskryminacja:** benchmark *rozróżnia* modele (rozrzut wyników > losowy szum; nie wszyscy 0%, nie wszyscy 100%).
3. **Niezależność:** ≥1 benchmark zbudowany przez **drugi team** (blind), wymieniony wg protokołu — Ty go nie widziałeś przed ewaluacją.
4. **Taksonomia:** wynik to nie sama liczba, lecz *jak* model pęka (mapa trybów awarii).

## Kryterium obalenia
Jeśli benchmark, który zbudowaliśmy, daje **identyczny ranking** co publiczny skażony benchmark
(np. MMLU) → nasza przewaga (provenance) jest iluzją, metoda do przemyślenia.

## Zakres
Know-how + protokoły + runnable narzędzia audytu. NIE: gotowy duży benchmark (to produkt iteracyjny).

## Powiązania
[[BENCH-T1]] · [[BENCH-T2]] · [[BENCH-T3]] · [[../90-Ewaluacja/Stan|Stan]]
