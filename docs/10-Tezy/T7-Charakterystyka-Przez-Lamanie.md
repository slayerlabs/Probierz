---
type: teza
id: BENCH-T7
title: "Charakterystyka granicy modelu wymaga celowanego łamania do niskiego pass-rate"
status: w-dyskusji
parents: ["BENCH-T3", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# T7 — Żeby poznać granicę modelu, trzeba go złamać

## Teza
Dopóki model przechodzi zestaw wysoko (sufit: 90–100%), **nie znamy jego granicy** — wiemy tylko, że
jest „co najmniej tak dobry". Charakterystyka zdolności wymaga zestawów, na których model **realnie się
łamie**: pass-rate celowo sprowadzony nisko (orientacyjnie **2–3 / N**), bo dopiero tam widać *gdzie* i
*jak* pęka. To operacjonalizacja fazy „stress-test" w charakterystyce Slayera (DEC2).

## Uzasadnienie
- **Sufit = brak informacji.** D1-łatwy (9–10/10), D6 (100%), D5a (8/8) nie zawężają oszacowania
  zdolności — informacja itemu maksymalna przy p≈0.5, znikoma przy p≈1 (S3/IRT).
- **Tryby awarii ujawniają się pod obciążeniem.** Dopiero gdy model zawodzi, taksonomia awarii (S3)
  daje sygnał diagnostyczny: czy to błędny plan, kumulacja błędu w długim łańcuchu, ciche pominięcie.
- **Empiria dotychczasowa:** jedyny wymiar, gdzie Slayer realnie pękł, to D1 przy głębokiej
  wieloetapowości (extreme 0.83). To wskazuje kierunek: podkręcać długość/kumulację łańcucha.

## Docelowy poziom trudności (nie „zero")
Celujemy w **2–3 / N**, nie w 0 / N. Powód: pass-rate = 0 dla wszystkich modeli to **floor effect** —
zero dyskryminacji, benchmark nie odróżnia modelu słabego od mocnego (AT3, AT7). Punkt 2–3/N leży
blisko dolnego pasma informacyjnego, ale zachowuje sygnał: część itemów jeszcze przechodzi, więc
widać, które konkretnie łamią model.

## Mechanizm łamania (co realnie obciąża rozumowanie)
- **Długi bezbłędny łańcuch** — kumulacja błędu (Collatz, iterowane potęgowanie, rekurencja rosnąca).
- **Śledzenie stanu przez wiele kroków** — symulacja, ciągi.
- **Precyzja liczbowa** — modulo, silnia, duże liczby (brak miejsca na „zaokrąglenie w głowie").
- **Constraint satisfaction / inclusion-exclusion** — wiele współzależnych warunków.

## Falsyfikacja
T7 jest fałszywa, jeśli okaże się, że niski pass-rate osiągamy **tylko** przez itemy wadliwe lub
nierozstrzygalne (patrz AT7) — wtedy „łamanie" mierzy jakość zestawu, nie model. Warunek rzetelności
łamania rozstrzyga S6.

## Powiązania
parent: [[T3-Bezlitosne-Mierzalne|T3]] · kontra: [[../15-Antytezy/AT7-Floor-I-Pozorna-Trudnosc|AT7]] · synteza: [[../25-Syntezy/S6-Warunek-Rzetelnego-Lamania|S6]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
