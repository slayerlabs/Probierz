---
type: metoda
id: BENCH-METODA-WYMIARY
title: "Wymiary zdolności językowej i falsyfikowalna rubryka"
status: w-dyskusji
author: Arkadiusz Słota
date: 2026-07-02
---

# Wymiary zdolności językowej i falsyfikowalna rubryka

Dokument opisuje, jak dzielimy zdolność językową LLM na osobno mierzone wymiary i jak oceniamy pojedynczą odpowiedź. Wielowymiarowość traktujemy jako hipotezę, którą trzeba potwierdzić na danych: każdy wymiar zostaje w taksonomii tylko wtedy, gdy niesie sygnał niezależny od wspólnego czynnika ogólnego. Odpowiedzi oceniamy deterministyczną rubryką pass/fail, a nie miarami zastępczymi, i chronimy ten pomiar przed rejestrowaniem formatu, artefaktów promptu i biasu gradera. Dla benchmarków wynika z tego konkretny warunek dopuszczenia itemu oraz bramka, którą każdy wymiar musi przejść w fazie baseline.

## Dlaczego nie jeden wskaźnik

Zdolność językowa LLM nie jest pojedynczą wielkością skalarną. Zakładamy, że jest zbiorem rozłącznych wymiarów mierzalnych osobno, ponieważ modele mogą osiągać na nich rozbieżne wyniki: model o wysokim wyniku w składni może mieć niski wynik w rozumowaniu wieloetapowym, a model o wysokiej wierności instrukcji może być słabo skalibrowany w niepewności. Pojedynczy zagregowany wskaźnik (np. „MMLU %") uśrednia te różnice i usuwa informację diagnostyczną o tym, który wymiar zawodzi.

To założenie jest falsyfikowalne i na razie niezweryfikowane na naszych danych. Do czasu pomiaru ma status w dyskusji, nie „ustalone": zgodnie z zasadą projektu żaden wynik nie jest przyjmowany bez pomiaru. Liczba i granice wymiarów są testowalne empirycznie (rozbieżność rankingów), a nie ustalane arbitralnie.

## Wymiary D1-D6

Lista jest wersją roboczą. Finalna liczba wymiarów wynika z pomiaru (warunek obalenia per wymiar, niżej), nie z ustalenia a priori. Dla każdego wymiaru podajemy, dlaczego jest językowy, a nie domenowy, jak go operacjonalizujemy i jaki jest główny tryb awarii (zob. [[Trudnosc-i-taksonomia-awarii|taksonomia awarii]]).

| ID | Wymiar | Co mierzy | Dlaczego rdzeniowy językowo | Operacjonalizacja (typ itemu) | Główny tryb awarii |
|---|---|---|---|---|---|
| **D1** | Rozumowanie wieloetapowe | łańcuch wnioskowań, kompozycja kroków | rozumienie języka wymaga wiązania przesłanek wyrażonych tekstem | zadania wieloetapowe z jednoznacznym wynikiem końcowym | błędny-plan |
| **D2** | Semantyka / wierność znaczeniu | parafraza, entailment, negacja, zakres kwantyfikatora | rdzeń: reprezentacja *znaczenia*, nie powierzchni leksykalnej | entailment, negacja, zakres kwantyfikatora, parafraza | halucynacja |
| **D3** | Składnia / struktura | zgodność gramatyczna, zależności długodystansowe, zagnieżdżenie | forma języka, niezależna od treści | zależności długodystansowe, zgodność, zagnieżdżenie | format |
| **D4** | Spójność długiego kontekstu | utrzymanie faktów i stanu przez długi tekst wejściowy | pamięć wewnątrzkontekstowa jako własność przetwarzania językowego | odtworzenie faktu/stanu z długiego wejścia (kontrola pozycji) | ciche-pominięcie |
| **D5** | Wierność instrukcji | realizacja polecenia (format, ograniczenia, odmowa błędnej instrukcji) | pragmatyka: odwzorowanie intencji na działanie | ograniczenia formatu, wykluczenia, odmowa błędnej instrukcji | ciche-pominięcie |
| **D6** | Kalibracja niepewności | „nie wiem" vs pewna halucynacja; adekwatność deklarowanej pewności | metajęzykowa reprezentacja granic wiedzy | pytania rozstrzygalne i nierozstrzygalne; adekwatność „nie wiem" | halucynacja |

### Wymiary kandydujące (do rozstrzygnięcia w baseline)

- **D7 Wiedza faktyczna** — rozdzielenie „braku wiedzy" od „braku rozumowania". Ryzyko: wchodzi w zakres kontaminacji (zob. [[Kontaminacja-i-wymiana|kontaminacja i wymiana]]) i domeny, nie czystej zdolności językowej. Status: otwarty. Włączamy go tylko, jeśli przejdzie kryterium demarkacji i warunek obalenia niezależnie od D1 i D6.
- **Multilingwalność / jakość PL** — Slayer jest modelem ukierunkowanym na polski, więc jakość PL jest istotna praktycznie. Otwarte pytanie: czy to osobny wymiar, czy przekrój (każdy wymiar D1–D6 mierzony w PL i porównawczo w innym języku). Wstępnie przyjmujemy przekrój, nie wymiar; rozstrzyga baseline (czy ranking modeli na D_i zależy od języka).

## Reguła dominującego obciążenia

Wymiary D1–D6 częściowo zazębiają się pojęciowo: rozumowanie wymaga semantyki, a wierność instrukcji obejmuje format. Dlatego item należy do wymiaru D_i, jeśli jego rubryka pass/fail jest wrażliwa przede wszystkim na D_i, a pozostałe wymiary są kontrolowane (utrzymane na poziomie trywialnym), tak by nie decydowały o wyniku. Przykłady:

- **D1 vs D2:** item D1 (rozumowanie) ma semantykę trywialną (proste zdania) i obciąża wyłącznie liczbę i poprawność kroków wnioskowania; item D2 (semantyka) ma rozumowanie jednokrokowe i obciąża interpretację znaczenia (negacja, kwantyfikator).
- **D3 vs D5:** D3 (składnia) dotyczy poprawności strukturalnej języka odpowiedzi; D5 (wierność instrukcji) dotyczy zgodności z poleceniem (format wyjścia, ograniczenia). Błąd formatu wyjścia wymuszonego instrukcją należy do D5, nie do D3.

Reguła jest testowalna: jeśli itemy przypisane do D_i korelują wynikami silniej z innym wymiarem niż z własnym (analiza obciążeń), demarkacja zawiodła i item wymaga przeprojektowania.

## Ryzyko: jeden czynnik ogólny

Najpoważniejsze zastrzeżenie wobec dekompozycji pochodzi z psychometrii. Wyniki różnych testów poznawczych są dodatnio skorelowane, co prowadzi do czynnika ogólnego *g*: pojedyncza zmienna latentna wyjaśnia większość wariancji, a wymiary są jej lokalnymi przejawami. Dla LLM argument jest silniejszy, bo wszystkie wymiary mają wspólną przyczynę: ten sam pretrening na tym samym korpusie, tę samą architekturę i tę samą skalę. Konkretnie:

1. **Dominacja skali.** Model większy lub lepiej trenowany osiąga empirycznie wyższy wynik na wszystkich osiach jednocześnie. Jeśli ranking modeli jest zbliżony na D1–D6, sześć wymiarów niesie tyle informacji co jeden, a koszt itemów i kalibracji rośnie sześciokrotnie bez wzrostu rozdzielczości pomiaru.
2. **Korelacja wejść.** Rozumowanie (D1) wymaga rozumienia semantyki (D2), które wymaga analizy składni (D3). Wymiary byłyby wtedy zależnymi poziomami tej samej kompetencji, a pomiar D1 obejmowałby częściowo D2 i D3; rozdzielenie byłoby pozorne.
3. **Wynik analizy czynnikowej.** W macierzy [model × wymiar] pierwsza składowa (PCA / analiza czynnikowa) może wyjaśniać większość wariancji, analogicznie do *g*. Taksonomia byłaby wtedy nadmiarowa: jeden wskaźnik (z niewielką resztą) opisuje modele równie dokładnie przy niższym koszcie.
4. **Ryzyko konfirmacji.** Autor zakładający wielowymiarowość może dobrać itemy tak, aby wymiary się rozdzielały. Rozłączność byłaby wtedy artefaktem konstrukcji zestawu, nie własnością modeli.

Jeśli to zastrzeżenie się potwierdzi, zdolność językowa jest praktycznie jednowymiarowa (plus składnik resztowy). Probierz raportowałby wtedy jeden wskaźnik (ewentualnie z korektami resztowymi) zamiast sześciu osi, a Warstwa 2 (MIRT per wymiar) redukuje się do jednowymiarowego IRT, czyli prostszego modelu o niższym koszcie estymacji (zob. [[Model-pomiaru-IRT|model pomiaru IRT]]).

Deklaracja „wymiary są różne" nie wystarcza; wymagany jest dowód na danych. Jest to kryterium obalenia z C2: warunek empiryczny, który konstrukt musi spełnić, zanim uznamy wielowymiarowość. Przeciw konfirmacyjnemu doborowi itemów rozłączność musi utrzymać się na itemach dobranych niezależnie, np. itemach drugiego teamu w ślepej wymianie (zob. [[Kontaminacja-i-wymiana|kontaminacja i wymiana]]).

## Kryterium rozłączności

Wymiary są rozłączne operacyjnie, jeśli na panelu modeli występuje istotne odwrócenie rankingu: istnieje para modeli (X, Y) i para wymiarów (A, B) taka, że X > Y na A oraz X < Y na B, przy czym przedziały ufności zdolności (bootstrap, zob. [[Model-pomiaru-IRT|panel kalibracyjny]]) nie zachodzą na siebie w obu wymiarach. Istotne odwrócenie na parze wymiarów jest dowodem niezależnego sygnału; odwrócenie mieszczące się w przedziałach ufności traktujemy jako szum. Brak istotnych odwróceń na żadnej parze oznacza współliniowość wymiarów, czyli przypadek czynnika ogólnego.

### Warunek obalenia per wymiar (bramka)

Wymiar D_i pozostaje w taksonomii wyłącznie wtedy, gdy na panelu ≥5 modeli spełnia oba warunki:

1. **Rozłączność (istotna).** Istnieje istotne odwrócenie rankingu względem innego wymiaru: para modeli (X, Y) taka, że X>Y na D_i oraz X<Y na D_j, przy nienakładających się przedziałach ufności (bootstrap) w obu wymiarach. Pojedyncze odwrócenie mieszczące się w przedziałach ufności jest szumem, nie dowodem. Brak istotnego odwrócenia względem wszystkich pozostałych wymiarów oznacza, że D_i jest współliniowy i należy go scalić z najsilniej skorelowanym wymiarem.
2. **Wariancja niesprowadzalna.** Po usunięciu pierwszej składowej głównej (wspólny czynnik) wariancja resztowa D_i przekracza próg szumu pomiarowego oszacowany z powtórzeń itemów (parafraz, zob. niżej) i przedziałów bootstrap. Wariancja resztowa w granicach szumu oznacza, że D_i nie niesie sygnału ponad czynnik wspólny, i wymiar usuwamy.

### Warunek obalenia całej taksonomii

Wcześniejsza wersja kryterium (2026-07-02, opis ryzyka czynnika ogólnego) wymagała, by pierwsza składowa analizy czynnikowej wyjaśniała < ~90% wariancji. Zastąpiliśmy ten sztywny próg analizą równoległą Horna (parallel analysis): udział wariancji kolejnych składowych głównych macierzy [model × wymiar] porównujemy z rozkładem odniesienia z losowych permutacji tej macierzy. Konstrukt uznajemy za wielowymiarowy tylko wtedy, gdy druga (i dalsze) składowa wyjaśnia istotnie więcej wariancji niż jej odpowiednik w danych permutowanych. Jeśli tylko pierwsza składowa przekracza próg permutacyjny oraz brak jakiegokolwiek istotnego odwrócenia rankingu, konstrukt jest praktycznie jednowymiarowy: taksonomia redukuje się do jednego wymiaru zbiorczego, a Warstwa 2 do jednowymiarowego modelu (1PL/Rasch lub porównawczy, zob. [[Model-pomiaru-IRT|model pomiaru: Rasch i Bradley-Terry]]). Eliminuje to arbitralność progu „90%".

### Plan pomiaru w fazie baseline

1. Minimalny zestaw ~5–10 itemów per wymiar (D1–D6), audyt czystości `contamination_check.py` → 0%.
2. Przejazd panelem ≥5 modeli (od słabszego do mocniejszego, w tym Slayer v49).
3. Macierz wynik[model × wymiar]; obliczyć: (a) liczbę istotnych odwróceń rankingu (wg przedziałów ufności z panelu), (b) korelacje między wymiarami, (c) analizę równoległą liczby składowych głównych powyżej poziomu odniesienia z permutacji.

Wielowymiarowość utrzymujemy, gdy jest ≥1 istotne odwrócenie na większości par wymiarów oraz ≥2 składowe powyżej poziomu odniesienia z analizy równoległej.

## Deterministyczna rubryka

Każdy wymiar mierzymy zadaniem z jawną, falsyfikowalną rubryką: deterministycznym kryterium rozstrzygającym pass/fail dla danej odpowiedzi w sposób powtarzalny. Odrzucamy miary zastępcze (proxy), które korelują ze zdolnością, lecz nie mierzą jej bezpośrednio:

- **perplexity / log-loss** — mierzy dopasowanie rozkładu do korpusu, nie poprawność rozumowania; model o niższej perplexity może częściej generować pewne, lecz nieprawdziwe odpowiedzi (halucynacje).
- **podobieństwo embeddingowe do wzorca** — premiuje podobieństwo powierzchniowe; przepuszcza odpowiedzi poprawne stylistycznie, lecz błędne merytorycznie.
- **sam wybór A/B/C/D (multiple choice bez uzasadnienia)** — podatny na zgadywanie i skróty formatu; mierzy eliminację dystraktorów, nie zdolność generatywną.

Celem Probierza (C1) jest pomiar zdolności, nie artefaktu. Proxy powiela problem kontaminacji po stronie metryki: dostarcza wielkość skorelowaną ze zdolnością, więc formalnie przypomina pomiar, lecz optymalizacja pod nią (Goodhart) rozdziela wartość metryki od zdolności rzeczywistej. Rubryka pass/fail jest bezpośrednia: definiuje, co poprawne rozwiązanie musi zawierać lub wykonać, i to podlega weryfikacji.

### Wymogi rubryki (warunek dopuszczenia itemu)

Rubryka jest dopuszczalna wyłącznie, gdy spełnia wszystkie wymogi:

1. **Falsyfikowalność** — istnieje obserwowalna odpowiedź, która ją oblewa (jeśli każda odpowiedź przechodzi, rubryka nie mierzy niczego).
2. **Determinizm dla gradera** — dwóch niezależnych graderów (człowiek lub LLM-sędzia) przypisuje ten sam pass/fail; docelowo mierzona jest zgodność między graderami (np. Cohen κ).
3. **Odporność na format** — pass zależy od treści lub zachowania, nie od przypadkowego formatowania (w przeciwnym razie pomiar rejestruje format, zob. niżej).
4. **Powiązanie z taksonomią awarii** — fail jest klasyfikowany: `halucynacja` / `błędny-plan` / `ciche-pominięcie` / `format` / `pętla` (zob. [[Trudnosc-i-taksonomia-awarii|taksonomia awarii]]). Wynik = pass-rate oraz rozkład trybów awarii.

Rubryki spełniające te wymogi, razem ze środkami ochrony przed formatem opisanymi niżej (niezmienniczość promptu, rozdział formatu od treści, kontrola skrótów, grader trust-minimized), są warunkiem dopuszczenia itemu do zestawu.

### Relacja do istniejącego benchmarku

`csharp-solid-v1` realizuje już ten wzorzec (`kryterium_pass` + `tryb_awarii` w schemacie itemu). Tu uogólniamy go z pojedynczego benchmarku do reguły obowiązującej wszystkie wymiary konstruktu.

### Wymiary bez rozstrzygalnej rubryki

Rubrykę weryfikujemy operacyjnie. Jeśli dla wymiaru D_i nie można skonstruować rubryki spełniającej cztery wymogi (np. „naturalność stylu" bywa nierozstrzygalna deterministycznie), to albo wymiar jest źle zdefiniowany (powrót do definicji i demarkacji wymiarów), albo należy mierzyć go porównawczo (ranking par, nie pass/fail).

## Ryzyko: pomiar formatu zamiast zdolności

Pass/fail z rubryki może rejestrować wrażliwość na powierzchnię promptu, czyli zmienną odrębną od kompetencji językowej:

1. **Wrażliwość na sformułowanie promptu.** Ta sama zdolność daje pass albo fail zależnie od sformułowania polecenia, kolejności przykładów, obecności instrukcji „rozwiąż krokowo", nagłówków, języka polecenia. Pomiar rejestruje wtedy reakcję modelu na konwencję promptowania autora. Inny zespół z inną konwencją uzyska inny ranking; brak niezmienniczości oznacza brak pomiaru konstruktu.
2. **Parsowanie jako ukryty warunek zaliczenia.** Automatyczna weryfikacja wyjścia wymusza format (JSON, „Odpowiedź: X", bloki kodu). Model kompetentny, lecz rozwlekły, dostaje fail na etapie parsowania; model niekompetentny, lecz zgodny formalnie, dostaje pass. Pomiar łączy wtedy D5 (wierność instrukcji) z pozostałymi wymiarami.
3. **Skróty i artefakty datasetu.** Modele wykorzystują regularności statystyczne: pozycję poprawnej odpowiedzi, jej długość, słowa-klucze w dystraktorach, styl poprawnej odpowiedzi. Wysoki wynik może wynikać z eksploatacji regularności zestawu, nie z rozumienia.
4. **Bias gradera LLM.** Grader LLM preferuje odpowiedzi we własnym stylu i jest podatny na iniekcję instrukcji. Wysoka zgodność między graderami może wynikać ze wspólnego biasu dwóch graderów tej samej rodziny, nie z trafności rubryki.

Gdyby te efekty dominowały, wyniki Probierza byłyby nieidentyfikowalne: nie dałoby się rozdzielić, jaka część pass-rate to zdolność, a jaka zgodność z formatem lub artefaktem. Ranking modeli odpowiadałby na pytanie „który model lepiej pasuje do przyjętej konwencji", a nie „który model językowy jest lepszy", co podważa interpretowalność wyniku (cel C2). Poniższe środki są obowiązkowe w konstrukcji zestawu.

## Test parafraz (niezmienniczość promptu)

Każdy item występuje w ≥3 parafrazach polecenia. Wynik wymiaru to statystyka odporna na parafrazę (mediana), a wariancję po parafrazie raportujemy osobno jako wskaźnik wrażliwości (sygnał dla D5, nie szum). Te same powtórzenia służą do oszacowania progu szumu pomiarowego w warunku wariancji niesprowadzalnej.

## Pozostałe środki ochrony pomiaru

- **Rozdział formatu od treści:** parsowanie tolerancyjne plus osobny wymiar wierności formatu (D5), aby błąd formatu nie był klasyfikowany jako błąd rozumowania (D1) ani inny błąd merytoryczny mierzonego wymiaru. Fail z powodu formatu trafia do kategorii `format`, nie `błędny-plan`.
- **Kontrola skrótów:** itemy z permutacją kolejności odpowiedzi i wariantami dystraktorów. Jeśli wynik zależy od permutacji, item mierzy skrót i podlega odrzuceniu (spójne z panelem kalibracyjnym w [[Trudnosc-i-taksonomia-awarii|taksonomii awarii]]).
- **Grader trust-minimized:** ≥2 graderów różnego pochodzenia (człowiek + LLM lub dwie różne rodziny modeli); rozbieżność kieruje item do ręcznego audytu. Wykluczony jest pojedynczy grader LLM tej samej rodziny co model oceniany (spójne ze ślepym audytem, zob. [[Kontaminacja-i-wymiana|kontaminacja i wymiana]]).

## Kiedy to podejście uznajemy za błędne

- **Dekompozycja na wymiary:** brak istotnych odwróceń rankingu oraz tylko pierwsza składowa powyżej poziomu odniesienia z analizy równoległej oznaczają konstrukt jednowymiarowy. Pojedynczy wymiar odpada (scalenie lub usunięcie) według bramki per wymiar opisanej wyżej.
- **Demarkacja:** itemy D_i korelujące silniej z innym wymiarem niż z własnym oznaczają, że reguła dominującego obciążenia zawiodła dla tych itemów.
- **Rubryka pass/fail:** jeśli rubryki pass/fail systematycznie dają niższą zgodność między graderami niż proxy (κ rubryki < κ proxy), to proxy są rzetelniejsze i rezygnujemy z zasady rubryki zamiast proxy.

## Co pozostaje otwarte

- Wszystkie powyższe kryteria czekają na pomiar w fazie baseline; status całości: w dyskusji (taksonomia ma status propozycji).
- Włączenie D7 (wiedza faktyczna).
- Czy jakość PL to osobny wymiar, czy przekrój przez D1–D6.

## Powiązane

[[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · [[Kontaminacja-i-wymiana|kontaminacja i wymiana]] · [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]] · [[Model-pomiaru-IRT|model pomiaru IRT]] · [[../../tools/contamination_check.py|contamination_check.py]]
