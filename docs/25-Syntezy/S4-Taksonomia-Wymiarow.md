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
Przyjmujemy taksonomię wielowymiarową (T4) **warunkowo**: każdy wymiar obowiązuje tylko dopóki spełnia
empiryczny **warunek obalenia** (poniżej). Wymiar, który go nie spełnia, zostaje scalony z innym lub
usunięty. Rozstrzyga to AT4 (jednowymiarowość): wielowymiarowość nie jest założeniem, lecz hipotezą
utrzymywaną wyłącznie przy potwierdzeniu na danych. Rubryki (T5) plus środki zaradcze z AT5
(niezmienniczość promptu, rozdział formatu od treści, kontrola skrótów, grader trust-minimized) są
warunkiem dopuszczenia itemu do zestawu.

## Kryterium demarkacji wymiarów (rozłączność pojęciowa)
Wymiary D1–D6 częściowo się zazębiają na poziomie pojęciowym (rozumowanie wymaga semantyki, wierność
instrukcji obejmuje format). Przyjmujemy **regułę dominującego obciążenia**: item należy do wymiaru
D_i, jeśli jego rubryka pass/fail jest wrażliwa **przede wszystkim** na D_i, a pozostałe wymiary są
kontrolowane (utrzymane na poziomie trywialnym), tak by nie decydowały o wyniku. Przykłady:
- **D1 vs D2:** item D1 (rozumowanie) ma semantykę trywialną (proste zdania), obciąża wyłącznie liczbę
  i poprawność kroków wnioskowania; item D2 (semantyka) ma rozumowanie jednokrokowe, obciąża
  interpretację znaczenia (negacja, kwantyfikator).
- **D3 vs D5:** D3 (składnia) dotyczy poprawności strukturalnej **języka odpowiedzi**; D5 (wierność
  instrukcji) dotyczy **zgodności z poleceniem** (format wyjścia, ograniczenia). Błąd formatu wyjścia
  wymuszonego instrukcją należy do D5, nie D3.
Reguła demarkacji jest **testowalna**: jeśli itemy przypisane do D_i korelują wynikami silniej z innym
wymiarem niż z własnym (analiza obciążeń), demarkacja zawiodła — item wymaga przeprojektowania.

## Taksonomia (wersja robocza)
| ID | Wymiar | Operacjonalizacja (typ itemu) | Główny tryb awarii (S3) |
|---|---|---|---|
| **D1** | Rozumowanie wieloetapowe | zadania wieloetapowe z jednoznacznym wynikiem końcowym | błędny-plan |
| **D2** | Semantyka / wierność znaczeniu | entailment, negacja, zakres kwantyfikatora, parafraza | halucynacja |
| **D3** | Składnia / struktura | zależności długodystansowe, zgodność, zagnieżdżenie | format |
| **D4** | Spójność długiego kontekstu | odtworzenie faktu/stanu z długiego wejścia (kontrola pozycji) | ciche-pominięcie |
| **D5** | Wierność instrukcji | ograniczenia formatu, wykluczenia, odmowa błędnej instrukcji | ciche-pominięcie |
| **D6** | Kalibracja niepewności | pytania rozstrzygalne i nierozstrzygalne; adekwatność „nie wiem" | halucynacja |

### Wymiary kandydujące (do rozstrzygnięcia w baseline)
- **D7 Wiedza faktyczna** — rozdzielenie „braku wiedzy" od „braku rozumowania". Ryzyko: wchodzi w
  zakres kontaminacji (T1) i domeny, nie czystej zdolności językowej. Status: **otwarty** — włączyć
  tylko, jeśli przejdzie kryterium demarkacji i warunek obalenia niezależnie od D1/D6.
- **Multilingwalność / jakość PL** — Slayer jest modelem ukierunkowanym na polski, więc jakość PL jest
  istotna praktycznie. Otwarte pytanie: czy to **osobny wymiar**, czy **przekrój** (każdy wymiar
  D1–D6 mierzony w PL i porównawczo w innym języku). Wstępnie: **przekrój**, nie wymiar — rozstrzyga
  baseline (czy ranking modeli na D_i zależy od języka).

> Lista jest **wersją roboczą**. Finalna liczba wymiarów wynika z pomiaru (warunek obalenia), nie z
> ustalenia a priori.

## Warunek obalenia per wymiar (bramka)
Wymiar D_i pozostaje w taksonomii wyłącznie, gdy na panelu ≥5 modeli (S5) spełnia oba:
1. **Rozłączność (istotna).** Istnieje **istotne odwrócenie rankingu** względem innego wymiaru: para
   modeli (X, Y) taka, że X>Y na D_i oraz X<Y na D_j, przy czym przedziały ufności zdolności (bootstrap,
   S5) **nie zachodzą na siebie w obu wymiarach**. Pojedyncze odwrócenie mieszczące się w przedziałach
   ufności traktujemy jako szum, nie dowód. Brak istotnego odwrócenia względem wszystkich pozostałych
   wymiarów → D_i współliniowy → **scalić** z najsilniej skorelowanym wymiarem.
2. **Wariancja niesprowadzalna.** Po usunięciu pierwszej składowej głównej (wspólny czynnik, AT4)
   wariancja resztowa D_i przekracza próg szumu pomiarowego oszacowany z **powtórzeń itemów** (parafraz,
   AT5) i przedziałów bootstrap. Wariancja resztowa w granicach szumu → D_i nie niesie sygnału ponad
   czynnik wspólny → **usunąć**.

## Warunek obalenia całej taksonomii (spójny z C2)
Zamiast sztywnego progu udziału wariancji stosujemy **analizę równoległą (parallel analysis Horna)**:
udział wariancji kolejnych składowych głównych macierzy [model × wymiar] porównujemy z rozkładem
odniesienia z losowych permutacji tej macierzy. Konstrukt uznajemy za **wielowymiarowy** tylko, gdy
druga (i dalsze) składowa wyjaśnia istotnie więcej wariancji niż jej odpowiednik w danych permutowanych.
Jeśli **tylko pierwsza** składowa przekracza próg permutacyjny **oraz** brak jakiegokolwiek istotnego
odwrócenia rankingu → konstrukt praktycznie **jednowymiarowy**: taksonomia redukuje się do jednego
wymiaru zbiorczego, a Warstwa 2 do jednowymiarowego modelu (1PL/Rasch lub porównawczy, S5). Eliminuje
to arbitralność wcześniejszego progu „90%".

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
