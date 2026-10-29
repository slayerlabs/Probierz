---
type: metoda
id: BENCH-METODA-BPB
title: "Metryka BPB i leaderboard: ranking, atrybucja i bramka nieodróżnialności"
status: propozycja
author: Arkadiusz Słota
date: 2026-09-11
---

# Metryka BPB i leaderboard: ranking, atrybucja i bramka nieodróżnialności

Do porównywania modeli językowych, zwłaszcza małych, sama accuracy ma zbyt małą moc, a liczenie na tokenach uniemożliwia porównanie modeli z różnymi tokenizerami. Dokument opisuje metrykę ciągłą liczoną na bajtach (BPB) jako oś główną, znane ograniczenia takiej liczby (confound tokenizera i rozmiaru, błędne czytanie nakładających się przedziałów ufności) oraz regułę tablicy wyników, która oddziela ranking od atrybucji przyczyny. Dla benchmarków wynika z tego, że wynik między modelami z różnych komórek wolno pokazać, ale wniosek o przyczynie wolno wyciągać tylko w komórce kontrolowanej i tylko przy istotnej różnicy paired-delta.

## Metryka ciągła BPB

Potrzebna jest metryka o dwóch własnościach:

1. **Ciągłość** — surowy margines lub log-prob, bez progowania na 0/1. Metryka ciągła ma lepszy stosunek sygnału do szumu niż dyskretna (Signal&Noise, arXiv 2508.13144: perplexity/BPB biją accuracy na małych modelach).
2. **Tokenizer-fair** — mianownikiem są BAJTY tekstu, nie tokeny. **BPB** (bits-per-byte, `−Σ log₂ P(token|prefiks) / bajty_UTF8`) daje jedną skalę dla dowolnego słownika (32000/32768/12288/bajty), co pozwala porównywać **dowolne** modele.

Role osi w tablicy:

- **BPB primary** — ranking „kto najlepiej modeluje polski" na wspólnym, zdekontaminowanym held-oucie, dla DOWOLNEGO modelu (jedna skala). To ranking modelowania języka, nie recepty treningowej.
- **mean margin (ciągła d3)** — `(logP(dobre) − logP(zle))/bajt` uśredniony po rdzeniu; oś potwierdzająca o większej mocy niż accuracy na tych SAMYCH parach.
- **accuracy** — trzecia, pomocnicza oś potwierdzająca, nie główna.

Empiria (2026-09-11): w komórce (110M, vocab 32000) accuracy przy n=148 i n=273 NIE rozróżniła {v2, v3, Slayer} (CI nakładają się). Metryka ciągła (paired-bootstrap na BPB oraz na margin) rozróżniła istotnie: **v3 < Slayer < v2 na BPB**, **v3 > v2 i v3 > Slayer na margin**. MDE BPB przy n=300 ≈ 0.003; luka 0.02 = ~9 docs. Accuracy okazała się narzędziem o zbyt małej mocy.

## Confound tokenizera i nakładające się CI

Nawet tokenizer-fair liczba rankuje „kto lepiej modeluje", ale **nie mówi, dlaczego A > B**. Są dwie pułapki:

1. **Confound między komórkami.** Modele różniące się naraz tokenizerem, danymi i rozmiarem nie dają czystego wniosku o żadnym z tych czynników. „Niższy BPB" ≠ „lepszy trening/rozmiar" — to `badge:confound`, nie atrybucja.
2. **Błąd overlapping-CI.** Nakładanie się MARGINALNYCH przedziałów ufności dwóch modeli ≠ brak różnicy. Poprawny test różnicy to **paired-delta** (resampling tych samych itemów), nie porównanie słupków.

Obserwacje (2026-09-11):

- **Odwrócenie wyniku 45M:** GoLLeM-45M (vocab 32568) „wygrał" na accuracy d3 (0.689) i „przegrał" na BPB (1.159 vs ~1.0 dla 110M/32000). Obie liczby są porównaniami między komórkami (inny tokenizer), więc żadna nie atrybuuje przyczyny. Wniosek „45M najlepszy" był artefaktem szumnej osi; wniosek „110M lepszy" byłby TYM SAMYM błędem w drugą stronę.
- **Nakładające się CI:** marginalne CI BPB {v2, v3, Slayer} nakładają się, więc modele wydają się nieodróżnialne. Paired-delta (skorelowane różnice per-doc) daje wąskie CI rozłączne z 0, więc jednak są rozróżnialne. Samo patrzenie na słupki wprowadzało w błąd.

Gdyby dwie niezależne metryki tokenizer-fair zgadzały się KIERUNKIEM między komórkami mimo różnych tokenizerów, atrybucja byłaby bezpieczniejsza. Empirycznie rozjechały się (45M), więc confound jest realny. W komórce kontrolowanej (ten sam tokenizer i rozmiar) confound znika i atrybucja jest legalna.

## Bramka leaderboardu

Ranking i atrybucję rozdzielamy: BPB odpowiada na pytanie, kto najlepiej modeluje język, a **atrybucję przyczyny** („trening/rozmiar A > B") wolno orzekać **tylko w komórce kontrolowanej** (ten sam `tokenizer_vocab` i `params`). Reguła tablicy (INDISTINGUISHABLE-GATE), obowiązkowa:

1. Komórka kontrolowana = wiersze o tym samym `(tokenizer_vocab, params)`.
2. Wewnątrz komórki **A > B tylko gdy CI paired-delta jest rozłączne z 0**. W przeciwnym razie: „nieodróżnialne przy tej mocy".
3. Porównanie z losowaniem (accuracy): według położenia całego CI względem 0.50.
4. Między komórkami: wynik dozwolony, ale z `badge:confound:tokenizer|size` — nigdy atrybucja.

## Warunki nośności metryki

- **Round-trip/coverage tokenizera** (sprawdzone): encode→decode==oryginał, 0 UNK, więc BPB między tokenizerami nie ma ślepego pola (Polock 2.279 to realnie złe modelowanie, nie kara za UNK).
- **Dekontaminacja per-model** (granica): held-out nie może być w treningu DANEGO modelu; modele zewnętrzne bez deklaracji dostają `badge:unverified:leak` (zob. [[Kontaminacja-i-wymiana|kontaminacja i wymiana]]).
- **Gate 1 — ≥3 seedy treningowe** (otwarty): paired-bootstrap łapie zmienność próbki, NIE seedu treningowego, więc kolejność pojedynczych runów jest na poziomie checkpointu (`caveat:single-seed`); wniosek o recepcie dopiero po ≥3 seedach.
- **Gate 3 — istotność paired-bootstrap** (zamknięty).
- **Zakres stosowalności i saturacja:** d3 różnicuje, dopóki `acc_core < ~0.9`; wyżej potrzebny jest trudniejszy rdzeń. d3 to reżim modeli małych i średnich; BPB nie ma sufitu (zob. [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]]).

## Wynik empiryczny (2026-09-11)

Komórka (110M, 32000) rozstrzygnięta: **v3 < Slayer < v2** (BPB), potwierdzone przez mean margin na dwóch rozmiarach rdzenia (v2=148, v3=273). Trzy niezależne sygnały są zgodne, więc ranking obowiązuje na poziomie checkpointu (single-seed). Wyniki między komórkami (45M, Polock) pokazujemy tylko z badge confound.

Modele: GoLLeM-45M/110M-v2/v3, Slayer-110M, Polock-125M.

## Kiedy to podejście uznajemy za błędne

- Metrykę ciągłą jako oś główną uznajemy za błędną, jeśli **accuracy przy realistycznym n różnicuje bliskie modele równie mocno** jak BPB/margin (ta sama moc statystyczna). Pomiar z 2026-09-11 (opisany wyżej) temu przeczy.
- Ostrożność wobec atrybucji między komórkami można by złagodzić, gdyby niezależne metryki tokenizer-fair zgadzały się kierunkiem mimo różnych tokenizerów; na 2026-09-11 rozjechały się (45M).

## Co jest otwarte

- Gate 1: ≥3 seedy treningowe na model; do tego czasu ranking ma status checkpoint-level.
- Dekontaminacja modeli zewnętrznych bez deklaracji danych treningowych (`badge:unverified:leak`).
- Trudniejszy rdzeń d3 dla modeli z `acc_core ≥ ~0.9`.

## Prowieniencja

- Leaderboard: github/slayerlabs/fabryka-track, branch `leaderboard-d3`, `leaderboard/LEADERBOARD.md`.
- Dane: `leaderboard/results/` (per-doc BPB, statystyki paired-bootstrap, piny SHA256); `results/bpb_perdoc.json`, `results/bpb_stats_report.md`.
- Benchmarki: `benchmarks/d3-skladnia-v2|v3` (Probierz).
- Narzędzia: `tools/{bpb_scorer,scorer_hf,run_forced_choice}.py`.

## Powiązane

[[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]] · [[Model-pomiaru-IRT|model pomiaru IRT]] · [[Lamanie-modeli|łamanie modeli]] · [[Kontaminacja-i-wymiana|kontaminacja i wymiana]] · decyzja: [[../20-Decyzje/D-DEC3-Leaderboard-Eksperymentalny|DEC3]]
