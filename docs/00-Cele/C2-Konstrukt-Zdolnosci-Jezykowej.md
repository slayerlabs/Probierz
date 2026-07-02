---
type: cel
id: BENCH-C2
title: "Cel — mierzalny konstrukt zdolności językowej LLM"
status: aktywny
parents: ["BENCH-C1"]
author: Arkadiusz Słota
date: 2026-07-02
---

# C2 — Co właściwie mierzymy w modelu językowym

## Problem (krok 1 metody naukowej)
C1 rozwiązuje **jak testować uczciwie** (provenance, czystość, anty-Goodhart). Nie odpowiada na
pytanie logicznie wcześniejsze: **co w modelu językowym w ogóle mierzymy i według jakiej definicji.**
Bez tego „benchmark LLM" to zbiór zadań dobranych intuicyjnie — mierzy *coś*, ale nie wiadomo co,
więc wynik nie jest interpretowalny ani porównywalny między zestawami.

Istniejący `csharp-solid-v1` mierzy **zdolność aplikacyjną** (spec → kod, stosowanie SOLID). To
legalny wymiar, ale wąski i inżynierski. Nasz cel jest szerszy: **zdolność modelu jako modelu
językowego** — rdzeniowe własności przetwarzania języka, nie konkretne umiejętności biznesowe.

## Cel
Zdefiniować **konstrukt** „zdolność językowa LLM" jako zbiór **rozłącznych, mierzalnych wymiarów**,
tak by każdy benchmark deklarował *który wymiar* mierzy i *jaką rubryką*. Konstrukt jest fundamentem
pod model matematyczny pomiaru (Warstwa 2, IRT) i pod baseline (przejazd panelem modeli).

> **Konstrukt** (termin z psychometrii) = teoretyczna własność, której nie mierzymy wprost, tylko
> przez obserwowalne wskaźniki (itemy). „Zdolność językowa" jest konstruktem tak jak „inteligencja"
> — nie ma jej na wyjściu API, wnioskujemy ją z wzorca odpowiedzi.

## Kryteria sukcesu (falsyfikowalne)
1. **Rozłączność:** wymiary konstruktu są operacyjnie rozróżnialne — istnieje ≥1 para modeli, która
   odwraca ranking między dwoma wymiarami (model X > Y na wymiarze A, ale X < Y na wymiarze B).
   Jeśli ranking jest identyczny na wszystkich wymiarach dla wszystkich modeli → wymiary się nie
   rozróżniają (patrz kryterium obalenia).
2. **Pokrycie:** taksonomia obejmuje rdzeniowe własności językowe, nie tylko zadania aplikacyjne;
   każdy wymiar ma uzasadnienie „dlaczego to własność JĘZYKOWA, nie domenowa".
3. **Operacjonalizacja:** dla każdego wymiaru istnieje szablon itemu z **falsyfikowalną rubryką**
   pass/fail (nie proxy typu perplexity — patrz T5).
4. **Zgodność z pomiarem:** taksonomia wpina się w model matematyczny (Warstwa 2) — każdy wymiar
   estymowany osobno, z panelem kalibracyjnym (spójne z S3).

## Kryterium obalenia (całego konstruktu)
Jeśli **analiza czynnikowa** wyników panelu modeli pokaże, że jeden czynnik ogólny (analogia *g*
z psychometrii) tłumaczy ≥ ~90% wariancji między wymiarami — to dekompozycja jest artefaktem,
a „zdolność językowa" jest praktycznie jednowymiarowa. Wtedy taksonomia (T4) upada i wracamy do
jednego zagregowanego wyniku. **To jest bramka: konstrukt wielowymiarowy przechodzi tylko, jeśli
wymiary realnie się rozjeżdżają na danych.** (por. AT4)

## Zakres
Definicja konstruktu + taksonomia wymiarów + szablony itemów per wymiar. NIE: gotowy duży zestaw
(to produkt iteracyjny, faza po baseline).

## Metoda (kolejność, nienegocjowalna)
**problem → model matematyczny → baseline → research → eval.**
C2 = *problem* (co mierzymy). Warstwa 2 (T6/S5) = *model matematyczny* (jak estymujemy). Dopiero
potem *baseline* (przejazd panelem), *research*, *eval*. Żaden benchmark nie rusza modelu Slayera,
zanim konstrukt i model pomiaru nie są zdefiniowane — inaczej mierzymy bez interpretacji.

## Powiązania
parent: [[C1-Cel|C1]] · tezy: [[../10-Tezy/T4-Dekompozycja-Wymiarow|T4]] · [[../10-Tezy/T5-Falsyfikowalna-Rubryka|T5]] · kontra: [[../15-Antytezy/AT4-Splatanie-Czynnik-G|AT4]] · [[../15-Antytezy/AT5-Format-Nie-Zdolnosc|AT5]] · synteza: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]]
