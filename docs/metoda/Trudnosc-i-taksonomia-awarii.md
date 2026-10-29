---
type: metoda
id: BENCH-METODA-TRUDNOSC
title: "Trudność i taksonomia awarii"
status: propozycja
author: Arkadiusz Słota
date: 2026-06-26
---

# Trudność i taksonomia awarii

Benchmark ma znajdować realne braki modeli, ale jeśli jest za trudny, wszystkie modele dostają około 0% i wynik nie niesie sygnału ani informacji o progresie. Jeśli jest za łatwy, wszyscy trafiają w sufit. Ten dokument opisuje, jak dobieramy trudność itemów, żeby benchmark był wymagający w punkcie dyskryminacji, czyli tam, gdzie różnice między modelami są największe, oraz jak klasyfikujemy porażki, żeby wynik pokazywał, gdzie model się łamie.

## Co mierzymy

Wynik ma rozróżniać modele (rozrzut większy niż szum) i pokazywać, *gdzie* model się łamie. Taki wynik jest mapą do poprawy, a nie tylko oceną. Trudność mierzymy na realnym sygnale z odpowiedzi modeli, a nie deklarujemy jej z góry.

Wymagający benchmark nie oznacza benchmarku, na którym wszyscy mają 0%. Celujemy w punkt dyskryminacji: trudność, przy której modele różnią się najbardziej. W modelu IRT maksymalna informacja itemu przypada tam, gdzie p(sukces) ≈ 0.5, a nie 0 (zob. [[Model-pomiaru-IRT|model pomiaru IRT]]).

## Gradient trudności

Itemy tworzą gradient od „trudne” do „prawie niemożliwe”, a nie jedną ścianę. W IRT dyskryminacja itemu jest ważniejsza niż sama jego trudność.

Procedura doboru itemów:
1. Kandydatów na itemy uruchamiamy na panelu kalibracyjnym złożonym z wielu modeli, od słabego do mocnego (zob. [[Model-pomiaru-IRT|model pomiaru IRT, panel kalibracyjny]]). Item, który łamie wszystkie modele albo żadnego, niesie mało informacji i jest odrzucany lub przesuwany.
2. Zachowujemy itemy o p(sukces) w paśmie 0.2–0.8, bo tam jest sygnał progresu.

## Floor effect i sufit

Znane ryzyko: jeśli benchmark jest naprawdę bardzo trudny, wszystkie modele dostają około 0%, dyskryminacja jest zerowa, nie wiadomo, który model jest lepszy, i nie widać progresu (floor effect). Za łatwy benchmark daje odwrotny problem: sufit. Wymóg łamania modeli i wymóg mierzalnego progresu pozostają ze sobą w napięciu.

Drugie ryzyko to cyrkularność kalibracji. Żeby wiedzieć, że item dyskryminuje, trzeba go uruchomić na modelach, które dopiero chcemy ocenić. IRT wymaga wielu modeli i wielu odpowiedzi; przy małej próbce (np. N=5 u Xaviera) oszacowanie trudności ma bardzo dużą wariancję.

Bez kalibracji wymóg „wymagający, ale mierzalny” nie ma procedury i prowadzi albo do ściany (0% wszędzie), albo do arbitralnego doboru itemów pod z góry założony wynik.

Jak to kontrolujemy:
- Kalibrujemy na panelu istniejących modeli, a nie na jednym ocenianym modelu, więc trudność jest zmierzona na niezależnej próbce.
- Ponieważ mała próbka daje dużą wariancję, minimalny panel to ≥ 5 modeli, a oszacowanie trudności ma przedział ufności z bootstrapu.

## Taksonomia awarii

Nie raportujemy samej accuracy, tylko to, *jak* model pęka. Każdą porażkę klasyfikujemy do jednej z kategorii:
`halucynacja` / `błędny-plan` / `ciche-pominięcie` / `format` / `pętla`.

Ciche pominięcie jest najgorszym trybem awarii, bo jest niewidoczne bez audytu (analogicznie do false-discard u Xaviera w sandboksie).

## Rotacja poprzeczki

Benchmark jest utrzymywany na bieżąco: gdy modele nasycą pasmo trudności, dodajemy trudniejsze itemy (rotacja itemów), żeby skala progresu nie kończyła się na suficie.

## Kiedy to podejście uznajemy za błędne

Jeśli bez kalibracji na panelu nie da się uniknąć ani ściany (0% wszędzie), ani arbitralnego doboru itemów pod założony wynik, wymóg „wymagający, ale mierzalny” pozostaje hasłem bez procedury. Procedura opisana wyżej (panel ≥ 5 modeli, pasmo p(sukces) 0.2–0.8, bootstrap CI na trudności) jest odpowiedzią na ten zarzut.

## Powiązane

[[../00-Cele/C1-Cel|C1]] · [[Model-pomiaru-IRT|model pomiaru IRT]] · [[Lamanie-modeli|łamanie modeli]]
