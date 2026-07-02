---
type: synteza
id: BENCH-S4
title: "Taksonomia wymiarów konstruktu z warunkiem obalenia per wymiar"
status: propozycja
parents: ["BENCH-T4", "BENCH-T5", "BENCH-AT4", "BENCH-AT5"]
author: Arkadiusz Słota
date: 2026-07-02
---

# S4 — Taksonomia zdolności językowej (rozstrzyga AT4 i AT5)

## Rozstrzygnięcie
Przyjmujemy taksonomię wielowymiarową (T4) **warunkowo**: każdy wymiar obowiązuje tylko dopóki
spełnia empiryczny **warunek obalenia** (poniżej). Wymiar, który go nie spełnia, zostaje scalony z
innym lub usunięty. Rozstrzyga to AT4 (jednowymiarowość): wielowymiarowość nie jest założeniem, lecz
hipotezą utrzymywaną wyłącznie przy potwierdzeniu na danych. Rubryki (T5) plus środki zaradcze z AT5
(niezmienniczość promptu, rozdział formatu od treści, kontrola skrótów, grader trust-minimized) są
warunkiem dopuszczenia itemu do zestawu.

## Taksonomia (wersja robocza)
| ID | Wymiar | Operacjonalizacja (typ itemu) | Główny tryb awarii (S3) |
|---|---|---|---|
| **D1** | Rozumowanie wieloetapowe | zadania wieloetapowe z jednoznacznym wynikiem końcowym | błędny-plan |
| **D2** | Semantyka / wierność znaczeniu | entailment, negacja, zakres kwantyfikatora, parafraza | halucynacja |
| **D3** | Składnia / struktura | zależności długodystansowe, zgodność, zagnieżdżenie | format |
| **D4** | Spójność długiego kontekstu | odtworzenie faktu/stanu z długiego wejścia (kontrola pozycji) | ciche-pominięcie |
| **D5** | Wierność instrukcji | ograniczenia formatu, wykluczenia, odmowa błędnej instrukcji | ciche-pominięcie |
| **D6** | Kalibracja niepewności | pytania rozstrzygalne i nierozstrzygalne; adekwatność „nie wiem" | halucynacja |

> Lista jest **wersją roboczą**. Finalna liczba wymiarów wynika z pomiaru (patrz warunek obalenia),
> nie z ustalenia a priori.

## Warunek obalenia per wymiar (bramka)
Wymiar D_i pozostaje w taksonomii wyłącznie, gdy na panelu ≥5 modeli (S5) spełnia oba:
1. **Rozłączność:** istnieje ≥1 **odwrócenie rankingu** względem innego wymiaru (para modeli X, Y:
   X>Y na D_i, X<Y na D_j). Brak jakiegokolwiek odwrócenia względem wszystkich pozostałych wymiarów →
   D_i jest współliniowy → **scalić** z najbardziej skorelowanym wymiarem.
2. **Wariancja niesprowadzalna:** po usunięciu pierwszej składowej głównej (wspólny czynnik, AT4)
   wariancja resztowa D_i przekracza próg szumu pomiarowego (oszacowany z powtórzeń itemów). Wariancja
   resztowa poniżej progu → D_i nie niesie sygnału ponad czynnik wspólny → **usunąć**.

## Warunek obalenia całej taksonomii (spójny z C2)
Jeśli pierwsza składowa główna macierzy [model × wymiar] wyjaśnia ≥ ~90% wariancji **oraz** żadna para
wymiarów nie wykazuje odwrócenia rankingu → konstrukt jest praktycznie **jednowymiarowy**. Wtedy
taksonomia zostaje zredukowana do jednego wymiaru zbiorczego, a Warstwa 2 do jednowymiarowego IRT.

## Środki zaradcze z AT5 (obowiązkowe w konstrukcji zestawu)
- **Niezmienniczość promptu:** ≥3 parafrazy polecenia na item; wynik wymiaru = statystyka odporna na
  parafrazę (mediana); wariancja po parafrazie raportowana osobno jako wskaźnik wrażliwości.
- **Rozdział formatu od treści:** parsowanie tolerancyjne; błąd formatu klasyfikowany jako `format`,
  nie jako błąd merytoryczny wymiaru mierzonego.
- **Kontrola skrótów:** permutacja kolejności odpowiedzi i wariantów dystraktorów; item zależny od
  permutacji podlega odrzuceniu (spójne z panelem kalibracyjnym S3).
- **Grader trust-minimized:** ≥2 graderów różnego pochodzenia; rozbieżność kieruje item do audytu
  ręcznego; wykluczony pojedynczy grader LLM tej samej rodziny co model oceniany.

## Powiązania
parents: [[../10-Tezy/T4-Dekompozycja-Wymiarow|T4]] · [[../10-Tezy/T5-Falsyfikowalna-Rubryka|T5]] · [[../15-Antytezy/AT4-Splatanie-Czynnik-G|AT4]] · [[../15-Antytezy/AT5-Format-Nie-Zdolnosc|AT5]] · pomiar: [[S5-MIRT-Panel|S5]] · dyskryminacja/awarie: [[S3-IRT-Taksonomia|S3]]
