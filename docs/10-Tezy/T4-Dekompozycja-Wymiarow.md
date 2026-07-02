---
type: teza
id: BENCH-T4
title: "Zdolność językowa jest dekomponowalna na rozłączne wymiary"
status: w-dyskusji
parents: ["BENCH-C2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# T4 — Dekompozycja konstruktu na mierzalne wymiary

## Teza
Zdolność językowa LLM nie jest pojedynczą wielkością skalarną. Jest zbiorem **rozłącznych wymiarów**
mierzalnych osobno, ponieważ modele osiągają na nich **rozbieżne wyniki**: model o wysokim wyniku w
składni może mieć niski wynik w rozumowaniu wieloetapowym; model o wysokiej wierności instrukcji może
być słabo skalibrowany w niepewności. Pojedynczy zagregowany wskaźnik (np. „MMLU %") **uśrednia** te
różnice i usuwa informację diagnostyczną o tym, który wymiar zawodzi.

## Proponowane wymiary (kandydat taksonomii)
Każdy z uzasadnieniem „dlaczego JĘZYKOWY, nie domenowy":

| Wymiar | Co mierzy | Dlaczego rdzeniowy językowo |
|---|---|---|
| **D1 Rozumowanie wieloetapowe** | łańcuch wnioskowań, kompozycja kroków | rozumienie języka wymaga wiązania przesłanek wyrażonych tekstem |
| **D2 Semantyka / wierność znaczeniu** | parafraza, entailment, negacja, zakres kwantyfikatora | rdzeń: reprezentacja *znaczenia*, nie powierzchni leksykalnej |
| **D3 Składnia / struktura** | zgodność gramatyczna, zależności długodystansowe, zagnieżdżenie | forma języka, niezależna od treści |
| **D4 Spójność długiego kontekstu** | utrzymanie faktów i stanu przez długi tekst wejściowy | pamięć wewnątrzkontekstowa jako własność przetwarzania językowego |
| **D5 Wierność instrukcji** | realizacja polecenia (format, ograniczenia, odmowa błędnej instrukcji) | pragmatyka: odwzorowanie intencji na działanie |
| **D6 Kalibracja niepewności** | „nie wiem" vs pewna halucynacja; adekwatność deklarowanej pewności | metajęzykowa reprezentacja granic wiedzy |

> Jest to **kandydat**, nie ustalenie. S4 rozstrzyga finalną listę oraz warunek obalenia per wymiar.
> Liczba i granice wymiarów są **empirycznie testowalne** (rozbieżność rankingów), nie ustalane
> arbitralnie.

## Mechanizm rozłączności (procedura weryfikacji)
Wymiary są rozłączne **operacyjnie**, jeśli na panelu modeli występuje **odwrócenie rankingu**:
istnieje para modeli (X, Y) i para wymiarów (A, B) taka, że X > Y na A oraz X < Y na B. Pojedyncze
odwrócenie na parę wymiarów jest dowodem, że wymiary niosą niezależny sygnał. Brak odwróceń na żadnej
parze oznacza współliniowość wymiarów (zastosowanie ma AT4 / czynnik g).

## Dowód (żadnej tezy bez dowodu — do wykonania w fazie baseline)
Teza jest falsyfikowalna i **niezweryfikowana na naszych danych**. Plan dowodu:
1. minimalny zestaw ~5–10 itemów per wymiar (D1–D6), audyt czystości `contamination_check.py` → 0%;
2. przejazd **panelem ≥5 modeli** (od słabszego do mocniejszego, w tym Slayer v49);
3. macierz wynik[model × wymiar]; obliczyć: (a) liczbę odwróceń rankingu, (b) korelacje między
   wymiarami, (c) analizę czynnikową (udział wariancji wyjaśniany przez 1. składową).
**Wynik pozytywny:** ≥1 odwrócenie na większości par wymiarów oraz 1. składowa < ~90% wariancji.
**Wynik negatywny (obala T4):** brak odwróceń oraz 1. składowa ≥ ~90% → konstrukt jednowymiarowy.

> Do czasu tego pomiaru T4 ma status **w-dyskusji**, nie „ustalone": zgodnie z zasadą projektu żaden
> wynik nie jest przyjmowany bez pomiaru.

## Powiązania
parent: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · siostra: [[T5-Falsyfikowalna-Rubryka|T5]] · kontra: [[../15-Antytezy/AT4-Splatanie-Czynnik-G|AT4]] · synteza: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · pomiar: [[../25-Syntezy/S5-MIRT-Panel|S5]]
