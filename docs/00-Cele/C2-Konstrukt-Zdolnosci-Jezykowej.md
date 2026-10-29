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
pod model matematyczny pomiaru (Warstwa 2) i pod baseline (przejazd panelem modeli).

> **Konstrukt** (termin z psychometrii) = teoretyczna własność, której nie mierzymy wprost, tylko
> przez obserwowalne wskaźniki (itemy). „Zdolność językowa" jest konstruktem tak jak „inteligencja"
> — nie występuje na wyjściu API, wnioskujemy ją z wzorca odpowiedzi.

## Kryteria sukcesu (falsyfikowalne)
1. **Rozłączność:** wymiary konstruktu są operacyjnie rozróżnialne — istnieje ≥1 para modeli z
   **istotnym odwróceniem rankingu** między dwoma wymiarami (X>Y na A, X<Y na B), przy czym przedziały
   ufności zdolności (bootstrap) nie zachodzą na siebie w obu wymiarach. Brak istotnego odwrócenia
   na wszystkich parach → wymiary się nie rozróżniają (patrz kryterium obalenia).
2. **Pokrycie:** taksonomia obejmuje rdzeniowe własności językowe, nie tylko zadania aplikacyjne;
   każdy wymiar ma uzasadnienie „dlaczego to własność JĘZYKOWA, nie domenowa".
3. **Operacjonalizacja:** dla każdego wymiaru istnieje szablon itemu z **falsyfikowalną rubryką**
   pass/fail (nie proxy typu perplexity — zob. deterministyczna rubryka).
4. **Zgodność z pomiarem:** taksonomia wpina się w model matematyczny (Warstwa 2) — każdy wymiar
   estymowany osobno, z panelem kalibracyjnym (spójne z taksonomią awarii i modelem pomiaru).

## Kryterium obalenia (całego konstruktu)
Udział wariancji kolejnych składowych głównych macierzy [model × wymiar] porównujemy z rozkładem
odniesienia z **analizy równoległej** (parallel analysis Horna: losowe permutacje macierzy). Jeśli
**tylko pierwsza** składowa przekracza próg permutacyjny (jeden czynnik ogólny, analogia *g*) **oraz**
brak jakiegokolwiek istotnego odwrócenia rankingu → dekompozycja jest artefaktem, a „zdolność
językowa" jest praktycznie jednowymiarowa. Wtedy taksonomia upada i wracamy do jednego
zagregowanego wyniku. Konstrukt wielowymiarowy przechodzi wyłącznie, jeśli wymiary rozdzielają się na
danych powyżej poziomu odniesienia (por. ryzyko jednego czynnika ogólnego; próg operacyjny w kryterium rozłączności).

## Zakres
Definicja konstruktu + taksonomia wymiarów + szablony itemów per wymiar. NIE: gotowy duży zestaw
(to produkt iteracyjny, faza po baseline).

## Metoda (kolejność, nienegocjowalna)
**problem → model matematyczny → baseline → research → eval.**
C2 = *problem* (co mierzymy). Warstwa 2 = *model matematyczny* (jak estymujemy). Dopiero
potem *baseline* (przejazd panelem), *research* (potwierdzenie liczb: replikacja, stabilność), *eval*.
Żaden benchmark nie rusza modelu Slayera, zanim konstrukt i model pomiaru nie są zdefiniowane —
inaczej mierzymy bez interpretacji.

## Powiązania
parent: [[C1-Cel|C1]] · metoda: [[../metoda/Wymiary-i-rubryka|wymiary, rubryka, kryterium rozłączności]] · [[../metoda/Model-pomiaru-IRT|model pomiaru]]
