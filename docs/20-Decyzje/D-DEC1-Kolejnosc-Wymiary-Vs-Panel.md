---
type: decyzja
id: BENCH-DEC1
title: "Decyzja — kolejność: budować D3–D6 czy najpierw rozszerzyć panel?"
status: otwarta
parents: ["BENCH-C2", "BENCH-S4", "BENCH-S5"]
author: Arkadiusz Słota
date: 2026-07-02
---

# DEC1 — Czy budować D3–D6 „na zapas", zanim panel coś potwierdzi?

## Kontekst (co wiemy z baseline D1+D2)
Slayer v49 dał **9/10 na obu wymiarach** — sufit dla jednego modelu. Mamy macierz [1 model × 2 wymiary],
z której **nie da się** wyliczyć rozłączności (S4) ani zdolności (S5). Pytanie operacyjne: co robić
dalej — dokładać wymiary (D3–D6) czy dokładać modele (panel)?

## Fakt techniczny (zmienia kalkulację)
Test rozłączności konstruktu (C2/S4) i estymacja pomiaru (S5) mają **dwa niezależne wymogi liczności**:
- **liczba modeli M** — dla stabilnej macierzy kowariancji między wymiarami potrzeba M ≳ K+3
  (K = liczba wymiarów); dla estymacji Rascha/Bradleya-Terry'ego panel ≥5 (S5/AT6);
- **liczba wymiarów K** — test wielowymiarowości potrzebuje K, na którym analiza równoległa/PCA ma co
  wykrywać. Przy **K=2** jest tylko **1 para** wymiarów do odwrócenia rankingu (C(2,2)=1) i praktycznie
  brak „drugiej składowej" — moc testu rozłączności jest minimalna. Przy **K≥4**: ≥6 par, PCA ma
  strukturę do analizy.

Wniosek: **ani sam panel na D1+D2, ani same wymiary bez panelu nie wystarczą.** Pierwszy sensowny test
C2 wymaga *jednocześnie* K≥~4 wymiarów **i** M≥~7 modeli.

## Teza (T-DEC1): budować D3–D6 teraz
Zestawy D3–D6 są potrzebne niezależnie od wyniku panelu, bo:
1. bez K≥4 test rozłączności jest bezsilny — budowa wymiarów to warunek konieczny pierwszego wniosku;
2. wzorzec konstrukcji jest ustalony (D1/D2: rubryka T5, parafrazy AT5, demarkacja S4, audyt 0%) —
   koszt krańcowy niski, ryzyko błędu małe;
3. budowa wymiarów i zbieranie panelu są **równoległe** (niezależne zasoby: projektowanie itemów vs
   dostęp do modeli) — sekwencyjne czekanie marnuje czas.

## Antyteza (AT-DEC1, steelman): nie budować, dopóki panel nie potwierdzi D1↔D2
1. **Ryzyko pracy w próżnię.** Jeśli panel pokaże, że nawet D1 i D2 są współliniowe (jeden czynnik),
   to dekompozycja jest wątpliwa — a D3–D6 zbudowane wcześniej są stratą i trzeba je przeprojektować
   lub odrzucić. Kolejność „najpierw najtańszy test falsyfikujący" nakazuje sprawdzić D1↔D2 zanim się
   inwestuje w resztę.
2. **Ryzyko Goodharta / doboru pod tezę (AT4).** Projektując 6 wymiarów naraz, przed jakimkolwiek
   sygnałem empirycznym, autor utrwala założoną strukturę — i potem „znajduje" ją w danych. Zbudowanie
   D3–D6 po zobaczeniu, że D1↔D2 realnie się rozdzielają na panelu, jest metodologicznie czystsze.
3. **Panel na D1+D2 NIE jest bezwartościowy.** Nawet 1 para wymiarów daje pierwszy test: jeśli na
   panelu ≥5 modeli D1 i D2 dają **identyczny ranking** (brak odwrócenia, wysoka korelacja), to mocny
   sygnał ostrzegawczy dla całej dekompozycji — tani i szybki, przed inwestycją w D3–D6.

## Warunek rozstrzygnięcia (falsyfikowalny)
Rozstrzygamy **empirycznie, minimalnym testem**, nie deklaracją:
1. Zbuduj panel ≥5 modeli (słaby→mocny) — potrzebny w KAŻDYM wariancie.
2. Przejedź **D1+D2** całym panelem → macierz [M × 2].
3. Policz korelację rankingów D1 vs D2 i liczbę istotnych odwróceń (CI bootstrap, S5).
   - **Jeśli ranking D1 i D2 istotnie się rozjeżdża** (≥1 istotne odwrócenie, korelacja wyraźnie < 1)
     → dekompozycja ma wsparcie → **buduj D3–D6** (teza T-DEC1 wygrywa), by wzmocnić test do K≥4.
   - **Jeśli D1 i D2 dają praktycznie identyczny ranking** (brak odwróceń, korelacja ≈ 1) → sygnał
     współliniowości → **wstrzymaj D3–D6**, zrewiduj taksonomię/demarkację (AT-DEC1 wygrywa, AT4 rośnie).

## Rekomendacja (do akceptacji)
**Sekwencja: panel → mini-test D1↔D2 → decyzja o D3–D6.** To godzi obie strony: panel jest potrzebny
tak czy inaczej (robimy go pierwszy), a tani mini-test na 2 wymiarach rozstrzyga, czy inwestować w
D3–D6, zanim to zrobimy. Unika zarówno pracy w próżnię (AT-DEC1 pkt 1–2), jak i sekwencyjnego marnowania
czasu (T-DEC1 pkt 3) — bo budowę D3–D6 odpalamy natychmiast po pozytywnym mini-teście, nie po pełnym
6-wymiarowym cyklu.

Warunek wstępny wszystkiego: **panel modeli.** Bez niego decyzja pozostaje otwarta.

## Powiązania
parents: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · [[../25-Syntezy/S5-MIRT-Panel|S5]] · kontra-baza: [[../15-Antytezy/AT4-Splatanie-Czynnik-G|AT4]] · stan: [[../90-Ewaluacja/Stan|Stan]]
