---
type: antyteza
id: BENCH-AT4
title: "Wymiary są splątane — jeden czynnik ogólny (g) tłumaczy wariancję"
status: w-dyskusji
parents: ["BENCH-T4"]
author: Arkadiusz Słota
date: 2026-07-02
---

# AT4 — Dekompozycja jako artefakt; jeden czynnik ogólny (steelman)

## Najmocniejsza wersja
W psychometrii wyniki różnych testów poznawczych są **dodatnio skorelowane**, co prowadzi do czynnika
ogólnego **g**: pojedyncza zmienna latentna wyjaśnia większość wariancji, a wymiary stanowią jej
lokalne przejawy. Dla LLM argument jest silniejszy, ponieważ wszystkie wymiary z T4 mają **wspólną
przyczynę**: ten sam pretrening na tym samym korpusie, tę samą architekturę, tę samą skalę. Model o
większej liczbie parametrów i lepszych danych osiąga wyższy wynik na wszystkich wymiarach jednocześnie.

Konkretnie:
1. **Dominacja skali.** Empirycznie model większy lub lepiej trenowany osiąga wyższy wynik na
   wszystkich osiach jednocześnie. Jeśli ranking modeli jest zbliżony na D1–D6, sześć wymiarów niesie
   tyle informacji co jeden, a koszt itemów i kalibracji rośnie sześciokrotnie bez wzrostu
   rozdzielczości pomiaru.
2. **Korelacja wejść.** Rozumowanie (D1) wymaga rozumienia semantyki (D2), które wymaga analizy
   składni (D3). Wymiary nie są rozłącznymi modułami, lecz zależnymi poziomami tej samej kompetencji;
   pomiar D1 obejmuje częściowo D2 i D3. Rozdzielenie jest wówczas pozorne.
3. **Wynik analizy czynnikowej.** Dla macierzy [model × wymiar] pierwsza składowa (PCA / analiza
   czynnikowa) może wyjaśniać większość wariancji, analogicznie do czynnika *g*. Wtedy taksonomia
   jest nadmiarowa: jeden wskaźnik (z niewielką resztą) opisuje modele równie dokładnie przy niższym
   koszcie.
4. **Ryzyko konfirmacji.** Autor zakładający wielowymiarowość może dobrać itemy tak, aby wymiary się
   rozdzielały (dobór pod tezę). Rozłączność byłaby wtedy artefaktem konstrukcji zestawu, nie
   własnością modeli.

## Konsekwencja, jeśli prawdziwa
T4 upada w mocnej wersji: zdolność językowa jest praktycznie **jednowymiarowa** (plus składnik
resztowy). Probierz raportowałby wówczas **jeden wskaźnik** (ewentualnie z korektami resztowymi)
zamiast sześciu osi. Warstwa 2 (MIRT per wymiar) redukuje się do jednowymiarowego IRT — model
prostszy o niższym koszcie estymacji.

## Czego wymaga, by ją odeprzeć (nie na słowo)
Deklaracja „wymiary są różne" jest niewystarczająca. Wymagany jest dowód na danych:
- ≥1 **odwrócenie rankingu** na większości par wymiarów (X>Y na A, X<Y na B) — dowód niezależnego sygnału;
- pierwsza składowa analizy czynnikowej wyjaśnia **< ~90%** wariancji (pozostaje wariancja dla osobnych wymiarów);
- rozłączność utrzymuje się na **niezależnie dobranych** itemach (nie dobieranych pod tezę), np.
  itemach drugiego teamu (T2, blind), co wyklucza dobór konfirmacyjny.

To jest **kryterium obalenia z C2**. AT4 stanowi warunek empiryczny, który konstrukt musi spełnić,
zanim uznamy wielowymiarowość.

## Powiązania
parent: [[../10-Tezy/T4-Dekompozycja-Wymiarow|T4]] · rozstrzyga: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · pomiar: [[../25-Syntezy/S5-MIRT-Panel|S5]]
