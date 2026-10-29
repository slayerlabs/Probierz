---
type: metoda
id: BENCH-METODA-POMIAR
title: "Model pomiaru: IRT, Rasch per wymiar, panel i pomiar porównawczy"
status: propozycja
author: Arkadiusz Słota
date: 2026-07-02
---

# Model pomiaru: IRT, Rasch per wymiar, panel i pomiar porównawczy

Surowy odsetek poprawnych odpowiedzi zależy od doboru trudności itemów, więc nie nadaje się do porównywania modeli między zestawami. Ten dokument opisuje, jak rozdzielamy zdolność modelu od parametrów itemu (rodzina Item Response Theory), dlaczego przy realnym panelu 5–12 modeli domyślnym wariantem jest 1PL/Rasch estymowany osobno dla każdego wymiaru, oraz jak pomiar porównawczy (Bradley-Terry / Elo) i bootstrap chronią przed fałszywą precyzją. Dla benchmarków wynika z tego, co raportujemy dla każdego modelu i wymiaru oraz kiedy dwa modele uznajemy za rozróżnione.

## Dlaczego nie surowy pass-rate

Ten sam model uzyskuje różny wynik na zestawie łatwym i trudnym, więc pass-rate nie jest niezmienniczy względem zestawu. IRT rozdziela dwie wielkości: zdolność modelu $\theta$ oraz parametry itemu (trudność, dyskryminacja), co pozwala oszacować $\theta$ w skali niezależnej od konkretnego zestawu.

Rodzina modeli IRT jest uzasadniona jako formalizm rozdziału zdolność–trudność. Wybór konkretnego wariantu (1PL/Rasch, 2PL, 3PL) zależy od liczności panelu: przy realnym panelu 5–12 modeli domyślny jest 1PL/Rasch, a 2PL/3PL dopuszczamy tylko po wykazaniu identyfikowalności (zob. niżej „Hierarchia modeli”). Wzory poniżej podają pełną postać (2PL/3PL); Rasch to przypadek $a_j \equiv 1$, $c_j = 0$.

## Model pomiaru: Rasch i Bradley-Terry

### Postać formalna IRT

Dla modelu o zdolności $\theta$ i itemu $j$ o trudności $b_j$ i dyskryminacji $a_j$ prawdopodobieństwo poprawnej odpowiedzi w modelu dwuparametrowym (2PL) wynosi:

$$
P(X_{j}=1 \mid \theta) = \frac{1}{1 + e^{-a_j\,(\theta - b_j)}}
$$

Model Rascha (1PL) to szczególny przypadek $a_j \equiv 1$ (dyskryminacja wspólna dla wszystkich itemów), redukujący liczbę parametrów do jednego na item.

Rozszerzenie trójparametrowe (3PL) dodaje dolną asymptotę $c_j$ (prawdopodobieństwo poprawnej odpowiedzi przy niskim $\theta$, np. trafienie w zadaniu wyboru):

$$
P(X_{j}=1 \mid \theta) = c_j + \frac{1 - c_j}{1 + e^{-a_j\,(\theta - b_j)}}
$$

- $\theta$ — zdolność modelu (parametr latentny, estymowany);
- $b_j$ — trudność itemu (wartość $\theta$, przy której $P = (1+c_j)/2$);
- $a_j$ — dyskryminacja (nachylenie krzywej w $b_j$; im wyższe, tym ostrzej item rozdziela modele);
- $c_j$ — zgadywanie (dolna asymptota; dla zadań generatywnych z rubryką pass/fail zwykle $c_j \approx 0$).

### Informacja itemu i dobór trudności

Informacja Fishera itemu (2PL) jako funkcja $\theta$:

$$
I_j(\theta) = a_j^{2}\, P_j(\theta)\,\bigl(1 - P_j(\theta)\bigr)
$$

Maksimum wypada przy $P_j(\theta) = 0.5$, czyli $\theta = b_j$. Item niesie najwięcej informacji o modelach, których zdolność jest zbliżona do jego trudności. To formalne uzasadnienie doboru trudności (zob. [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]]): itemy rozwiązywane przez wszystkie modele ($b_j \ll \theta$) lub przez żaden ($b_j \gg \theta$) mają $P(1-P) \to 0$, więc informację bliską zeru, i należy je odrzucić. „Punkt dyskryminacji” to formalnie $\theta \approx b_j$ przy wysokim $a_j$.

### Estymacja

Parametry itemów oraz zdolności modeli $\{\theta_i\}$ estymujemy łącznie z macierzy odpowiedzi [model × item] metodą największej wiarygodności (MML) lub estymacją bayesowską. Warunkiem identyfikowalności jest panel wielu modeli (zob. „Panel kalibracyjny”): pojedynczy model nie pozwala rozdzielić $\theta$ od $b_j$. Liczba parametrów zależy od wariantu: 1PL/Rasch $J + M$ (przed normalizacją), 2PL $2J + M$.

### Hierarchia modeli (od najmniej do najbardziej wymagającego danych)

Model pomiaru estymujemy osobno dla każdego wymiaru D_i (każdy wymiar ma własną skalę zdolności; zob. [[Wymiary-i-rubryka|wymiary i rubryka]]). Wielowymiarowość konstruktu jest reprezentowana przez zbiór osobnych modeli, nie przez jeden parametr globalny. Formalizm nie jest ustalony z góry na 2PL, lecz zależy od liczności panelu:

1. **Model porównawczy (Bradley-Terry / Elo)** — pomiar zawsze dostępny, także przy najmniejszym panelu. Estymuje względną zdolność modeli na wymiarze D_i z wyników parami (który z pary rozwiązuje item, gdy drugi zawodzi). Nie zakłada skali absolutnej ani parametrów itemów. Stanowi pomiar kontrolny dla każdego wymiaru.
2. **1PL / Rasch (domyślny model absolutny).** Jeden parametr trudności $b_j$ na item, dyskryminacja wspólna:

   $$
   P\!\left(X_j = 1 \mid \theta^{(i)}\right) = \frac{1}{1 + e^{-(\theta^{(i)} - b_j)}}
   $$

   Bilans: $J + M - 1$ parametrów przy $M \cdot J$ obserwacjach — istotnie lepiej uwarunkowany niż 2PL (zob. tabelę w „Ograniczenia założeń IRT przy małym panelu”).
3. **2PL (warunkowo).** Dodaje dyskryminację $a_j$ per item. Dopuszczalny tylko, gdy: (a) obs/param ≥ 5 przy dostępnym M i J, oraz (b) test ilorazu wiarygodności (2PL vs 1PL) wykazuje istotną poprawę dopasowania przewyższającą karę za parametry (AIC/BIC). W przeciwnym razie pozostajemy przy 1PL. 3PL ($c_j$) stosujemy tylko dla itemów z realnym zgadywaniem (wybór zamknięty); dla itemów generatywnych z rubryką pass/fail $c_j = 0$.

Gdy skali absolutnej nie da się zidentyfikować, pomiarem głównym jest model porównawczy.

## Ograniczenia założeń IRT przy małym panelu

Klasyczny IRT (2PL/3PL) opiera się na założeniach, z których każde jest problematyczne dla oceny LLM:

1. **Jednowymiarowość.** 2PL/3PL zakłada jeden parametr latentny $\theta$ na model, a konstrukt jest z założenia wielowymiarowy (D1–D6). Jednowymiarowy IRT na zestawie mieszającym wymiary daje $\theta$ będące nieokreśloną kombinacją wymiarów, czyli wielkość nieinterpretowalną. Założenie modelu pomiaru byłoby wtedy sprzeczne z założeniem konstruktu. Stąd osobny model dla każdego wymiaru.
2. **Lokalna niezależność.** IRT zakłada, że przy ustalonym $\theta$ odpowiedzi na różne itemy są niezależne: $P(X_j, X_k \mid \theta) = P(X_j \mid \theta)\,P(X_k \mid \theta)$. W ocenie LLM jest to naruszane co najmniej dwoma mechanizmami: (a) itemy dzielące ten sam kontekst lub schemat promptu są skorelowane ponad $\theta$; (b) wrażliwość na format (zob. [[Wymiary-i-rubryka|wymiary i rubryka]], „Test parafraz (niezmienniczość promptu)”) wprowadza wspólny czynnik zakłócający — model o określonym stylu formatowania koreluje błędy między itemami niezależnie od zdolności.
3. **Niezmienniczość parametrów (parameter invariance).** IRT zakłada, że $b_j, a_j$ są własnością itemu, niezależną od populacji odpowiadających. Dla LLM populacja jest mała, niestacjonarna (nowe modele co kilka miesięcy) i nie jest próbą losową z żadnej populacji — modele dzielą architektury i dane treningowe. Oszacowania $b_j, a_j$ mogą nie przenosić się na modele spoza panelu kalibracyjnego.
4. **Uwarunkowanie estymacji (zarzut najcięższy).** Nawet przy spełnionych założeniach 1–3 estymacja absolutnej zdolności $\theta$ i dwóch parametrów itemu z panelu 5–12 modeli jest źle uwarunkowana. Dla małej liczby odpowiadających lepiej uwarunkowany jest pomiar porównawczy (Bradley-Terry / Elo na parach modeli): estymuje tylko względną zdolność, wymaga mniej parametrów i nie zakłada absolutnej skali. IRT dostarcza więcej (skala absolutna, parametry itemów), ale przy dostępnej liczności ta dodatkowa struktura jest nieidentyfikowalna — płacimy wariancją za informację, na której wyznaczenie nie starcza danych.

### Bilans stopni swobody

2PL na wymiar ma $2J + M - 2$ parametrów ($a_j, b_j$ na item, $\theta_m$ na model, minus 2 więzy normalizacji skali) przy $M \cdot J$ binarnych obserwacjach (1 bit każda).

| M modeli | J itemów | #param | #obs | obs/param |
|---|---|---|---|---|
| 5 | 10 | 23 | 50 | 2.2 |
| 8 | 10 | 26 | 80 | 3.1 |
| 12 | 20 | 50 | 240 | 4.8 |

Stabilna MLE wymaga zwykle obs/param ≥ 5–10; w psychometrii dla 2PL rekomenduje się N ≥ ~500 respondentów dla stabilnego $a_j$. Panel LLM (5–12 modeli) jest o 1.5–2 rzędy wielkości poniżej. Parametr dyskryminacji $a_j$, estymowany z nachylenia krzywej po 5–12 punktach $\theta$, jest szczególnie niestabilny. Model 1PL/Rasch ma $J + M - 1$ parametrów i jest znacznie lepiej uwarunkowany.

Gdyby te ograniczenia zignorować, IRT 2PL/3PL byłby źle specyfikowany i źle uwarunkowany: $\theta$ nieinterpretowalne (naruszona jednowymiarowość), zaniżone błędy standardowe (naruszona lokalna niezależność), niestabilne $a_j$ (mały, nielosowy panel). Wynik liczbowy sprawiałby wrażenie precyzyjnego pomiaru, nie będąc nim. Odpowiedzią są: redukcja parametrów (domyślnie Rasch), pomiar porównawczy jako kontrolny lub główny, osobny model na wymiar, kontrola założeń i kwantyfikacja niepewności opisane w kolejnych sekcjach.

## Panel kalibracyjny

Estymacja wymaga panelu ≥5 modeli o zróżnicowanej zdolności (od słabszego do mocniejszego), zgodnie z wymaganiami gradientu trudności (zob. [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]]). Model oceniany (np. Slayer v49) jest jednym z węzłów panelu, nie jedynym punktem.

Ograniczenie jest jawne: nawet 1PL przy M≈5–12 jest umiarkowanie uwarunkowany. Dlatego (a) pomiar porównawczy jest zawsze raportowany obok modelu absolutnego, (b) przy sprzeczności obu priorytet ma porównawczy jako mniej zależny od założeń.

## Kontrola założeń

- **Lokalna niezależność:** statystyka reszt $Q_3$ dla par itemów; itemy dzielące kontekst lub schemat promptu grupujemy w testlety albo rozdzielamy konteksty.
- **Dopasowanie itemu (item fit):** empiryczna proporcja poprawnych w funkcji $\theta^{(i)}$ porównana z krzywą logistyczną; itemy o istotnym niedopasowaniu są odrzucane lub rewidowane.
- **Przenośność (DIF):** differential item functioning na modelach spoza panelu kalibracyjnego.

## Kwantyfikacja niepewności

Panel jest mały i nielosowy, więc stosujemy bootstrap dwustronny (resampling po itemach i po modelach) i podajemy przedziały ufności dla każdej estymaty ($\theta^{(i)}$ lub rangi porównawczej, $b_j$). Dwa modele uznajemy za rozróżnione na wymiarze D_i tylko, gdy ich przedziały ufności nie zachodzą na siebie. Brak rozróżnienia raportujemy jawnie, nie ukrywamy go za punktową estymatą.

## Rozłączność wymiarów w modelu pomiaru

Ta sekcja zasila kryterium rozłączności wymiarów (zob. [[Wymiary-i-rubryka|wymiary i rubryka]], „Kryterium rozłączności”) i je wzmacnia.

**Odwrócenie rankingu** między wymiarami D_i, D_j liczy się jako dowód niezależnego sygnału tylko wtedy, gdy jest istotne: dla pary modeli (X, Y) przedziały ufności zdolności nie zachodzą na siebie w obu wymiarach, a kierunek relacji jest przeciwny. Pojedyncze nieistotne odwrócenie (mieszczące się w CI) traktujemy jako szum, nie dowód.

**Próg jednowymiarowości** (zastępuje sztywne „90%”): udział wariancji pierwszej składowej porównujemy z rozkładem odniesienia z analizy równoległej (parallel analysis Horna: losowe permutacje macierzy [model × wymiar]). Konstrukt uznajemy za wielowymiarowy tylko, gdy druga składowa wyjaśnia istotnie więcej wariancji niż jej odpowiednik w danych permutowanych. Eliminuje to arbitralność progu.

## Wynik pomiaru (co raportujemy)

Dla każdego modelu i każdego wymiaru D_i:
- ranga porównawcza (Bradley-Terry / Elo) z CI — zawsze;
- $\hat{\theta}^{(i)}$ z CI (1PL; 2PL tylko warunkowo) — gdy identyfikowalne;
- surowy pass-rate (do interpretacji);
- rozkład trybów awarii (zob. [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]], „Taksonomia awarii”);
- wskaźnik wrażliwości na parafrazę promptu (zob. [[Wymiary-i-rubryka|wymiary i rubryka]], „Test parafraz (niezmienniczość promptu)”).

## Kiedy to podejście uznajemy za błędne

IRT zakłada określony kształt krzywej charakterystycznej itemu (ICC). Jeśli empiryczna proporcja poprawnych odpowiedzi w funkcji oszacowanego $\theta$ istotnie odbiega od krzywej logistycznej dla wielu itemów, założenie danego wariantu IRT jest nietrafne dla LLM i model pomiaru wymaga rewizji lub zejścia do pomiaru porównawczego. Systematyczne niedopasowanie w obrębie wymiaru oznacza nietrafność formalizmu dla tego wymiaru i wymusza przejście na model porównawczy (Bradley-Terry / Elo).

## Miejsce w metodzie

Ten dokument zamyka etap modelu matematycznego. Kolejny etap to baseline: przejazd panelu przez minimalne zestawy per wymiar (audyt czystości [[../../tools/contamination_check.py|contamination_check.py]] → 0% jako warunek wstępny; zob. [[Kontaminacja-i-wymiana|kontaminacja i wymiana]]), estymacja (porównawcza + 1PL) i weryfikacja warunków obalenia taksonomii wymiarów (zob. [[Wymiary-i-rubryka|wymiary i rubryka]]). Faza research po baseline potwierdza liczby (replikacja, stabilność estymat, wrażliwość na dobór panelu). Dopiero potem następuje eval właściwy.

Status źródeł (2026-07-02): uzasadnienie IRT i opis ograniczeń były w dyskusji, operacyjny model pomiaru miał status propozycji.

## Powiązane

[[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]] · [[Wymiary-i-rubryka|wymiary i rubryka]] · [[Kontaminacja-i-wymiana|kontaminacja i wymiana]] · [[../../tools/contamination_check.py|narzędzie]]
