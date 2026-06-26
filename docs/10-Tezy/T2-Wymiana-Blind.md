---
type: teza
id: BENCH-T2
title: "Wymiana dwóch teamów — blind exchange"
status: w-dyskusji
parents: ["BENCH-C1"]
author: Arkadiusz Słota
date: 2026-06-26
---

# T2 — Dwa teamy, ślepa wymiana

## Teza
Benchmark zbudowany i ewaluowany przez **ten sam team** jest skazany na Goodharta: nieświadomie
dopasujesz model do własnego testu (jak cyrkularność E3 w Dendrometrii — proxy = wynik).

Rozwiązanie: **drugi, niezależny team**. On buduje benchmarki, których **nigdy nie widzieliśmy**;
my budujemy dla niego. Wymieniamy się gotowymi zestawami. Nie da się ograć testu, którego nie znasz
→ wynik jest **niezależnym ground truth**, nie autowalidacją.

## Mechanizm (ten sam co M4 / ślepy audyt Xaviera)
- Team A i Team B trenują niezależnie, każdy zna TYLKO swoje dane treningowe.
- Benchmarki krzyżowe: A ewaluuje modele B i odwrotnie.
- Wymiana wg `protokol/PROTOKOL-Wymiany.md` (commitment + reveal jednorazowy).

## Dlaczego niezależność = ground truth
To generalizacja **M4** („AI-first-pass + human-ground-truth"): tu *drugi team* jest niezależną
weryfikacją zamiast człowieka. I ślepego re-review Xaviera (S2): ewaluator bez dostępu do „kluczy".

## Powiązania
parent: [[BENCH-C1]] · synteza: [[../25-Syntezy/S1-Commitment-Protokol|S1]] · kontra: [[../15-Antytezy/AT1-Spalanie-Benchmarku|AT1]]
