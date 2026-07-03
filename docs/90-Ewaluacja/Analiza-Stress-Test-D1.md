---
type: analiza
id: BENCH-ANALIZA-STRESS-D1
title: "Analiza stress-test D1 — wytrzymałość vs głębia (bramka S6)"
status: aktywny
parents: ["BENCH-T7", "BENCH-AT7", "BENCH-S6"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza stress-test D1 — dwie pod-kategorie

> Wykonano wg bramki S6: żelazny GT (weryfikacja programowa), demarkacja pod-kategorii, gradient.
> Cel T7: łamanie do niskiego pass-rate. Wynik uczciwie — nie osiągnięto „max 3", ale znaleziono
> istotny wzorzec.

## Wyniki (Slayer v49)
| Pod-kategoria | Pass | Wrażliwe | Twarde faile (0/3) |
|---|---|---|---|
| Wytrzymałość obliczeniowa | 6/8 (75%) | 1 | WYT-06 Collatz-111 |
| Głębia rozumowania | 5/6 (83%) | **4** | — |

## Wytrzymałość: pęka na długości BEZ skrótu
- **FAIL WYT-06 Collatz-111 (0/3, twardy):** 111 iteracji bez obejścia — czysta długość rozłożyła model.
- **FAIL WYT-03 10! mod 1000 (1/3):** błąd w łańcuchu modulo.
- **ZDAŁ z skrótem:** 7^100 mod 13 (Fermat), 7^50 mod 13, rekurencja 2³²+1, Fib-20.

**Wzorzec (rafinacja słabości):** Slayer nie łamie się na „długości" ogólnie — łamie się na **długości
bez możliwości skrótu**. Gdy istnieje obejście matematyczne (małe tw. Fermata dla modulo, wzór
zamknięty), radzi sobie nawet z „7^100". Gdy trzeba wykonać N iteracji bez skrótu (Collatz), pęka.
To ważne: mierzy raczej „czy zna skrót" niż „czy wytrzyma N kroków".

## Głębia: wysoka mediana, ale ALARMUJĄCA niestabilność
- Pass 5/6, ale **4/6 wrażliwych na parafrazę** — połowa wyników zależy od sformułowania.
- **FAIL GLEB-03 (401, incl-excl z wykluczeniem, 1/3):** najtrudniejsza kombinacja warunków.
- Constraint (domy) i permutacje z punktem stałym: zdane, ale permutacje wrażliwe (2/3).

**Kluczowy sygnał:** w głębi rozumowania mediana Slayera jest wysoka, lecz **powtarzalność słaba**.
To znaczy, że pojedynczy przejazd zawyża ocenę — model „czasem wpada" na właściwą strategię, zależnie
od sformułowania. Wskaźnik wrażliwości (AT5) okazał się tu diagnostyczniejszy niż sam pass-rate.

## Odniesienie do celu „max 3" (uczciwie)
Nie zeszliśmy do 2-3/N. Zgodnie z S6 **nie naginam itemów, by sztucznie zejść** (to byłby Goodhart /
pozorna trudność). Wynik przy spełnionej bramce jest wynikiem o modelu: **Slayer jest odporniejszy,
niż zakładała hipoteza „max 3"** — zwłaszcza gdy dostępny jest skrót matematyczny.

Droga do uczciwego niższego pass-rate (następny zestaw): **czysta długość bez skrótu** (kierunek, który
zadziałał — Collatz 0/3). Kandydaci: dłuższe Collatze (od liczb dających 100+ kroków), symulacje
automatu/gry na wiele kroków, ewaluacja długich wyrażeń zagnieżdżonych — wszystko gdzie NIE ma wzoru
zamkniętego. To atakuje zrefinowaną słabość precyzyjnie.

## Wartość metodologiczna (S6 zadziałała)
Demarkacja pod-kategorii dała wynik, którego jeden worek by nie pokazał: **wytrzymałość i głębia łamią
się inaczej** — wytrzymałość twardym failem (Collatz 0/3), głębia niestabilnością (4/6 wrażliwych).
Zsumowane w jeden wskaźnik (11/14=79%) zatarłyby oba sygnały.

## Powiązania
[[../10-Tezy/T7-Charakterystyka-Przez-Lamanie|T7]] · [[../15-Antytezy/AT7-Floor-I-Pozorna-Trudnosc|AT7]] · [[../25-Syntezy/S6-Warunek-Rzetelnego-Lamania|S6]] · [[../../benchmarks/d1-wytrzymalosc-obliczeniowa-v1/README|wytrzymałość]] · [[../../benchmarks/d1-glebia-rozumowania-v1/README|głębia]]
