# d3-skladnia — wyniki i legendy eksperymentu

Dokument samodzielny: nie zakłada wcześniejszej wiedzy. Opisuje, czego dotyczył test, co znaczą liczby i jak czytać każdy wykres.

## 1. Czego dotyczył test

Test sprawdza, czy model języka polskiego opanował **morfoskładnię** (reguły odmiany i zgodności form) oraz jak dobrze **przewiduje polski tekst**. W tym zestawie wyników użyto metody **odniesienia** (n-gram), nie wytrenowanego modelu sieciowego — po to, aby ustalić poziom, który wytrenowany model musi przekroczyć.

Testowany materiał: **30 par minimalnych** języka polskiego. Para minimalna to dwa prawie identyczne zdania — jedno poprawne gramatycznie (`dobre`), drugie z jednym błędem morfoskładni (`zle`). Przykład: `dobre = "bez wody"`, `zle = "bez woda"`.

Cztery rodziny zjawisk (ile par): rząd przypadka (10), zgoda przymiotnik–rzeczownik (8), rodzaj w czasie przeszłym (7), aspekt czasownika (5).

## 2. Słownik pojęć (legenda)

- **Model języka** — program, który przypisuje prawdopodobieństwo dowolnemu ciągowi tekstu; równoważnie: przewiduje następny bajt tekstu.
- **Bajt** — pojedyncza jednostka kodowania tekstu (UTF-8). Polskie znaki diakrytyczne (ą, ę, ł, ...) zajmują 2 bajty.
- **Para minimalna** — dwa zdania różniące się jedną cechą gramatyczną: `dobre` (poprawne) vs `zle` (błędne).
- **Forced-choice (wybór wymuszony)** — metoda pomiaru: liczy się prawdopodobieństwo obu zdań; wynik pary jest poprawny, jeśli metoda przypisuje wyższe prawdopodobieństwo zdaniu `dobre`.
- **Accuracy** — udział par, w których metoda wybrała `dobre`. Wartość od 0 do 1. Wybór losowy daje **0.50**.
- **Metoda n-gram (rząd k)** — prosta metoda odniesienia: przewiduje następny bajt na podstawie k poprzednich bajtów. Rząd 1 = 1 bajt kontekstu, rząd 4 = 4 bajty. To „poziom odniesienia" (baseline).
- **BPB (bits-per-byte)** — średnia liczba bitów potrzebna metodzie do zakodowania jednego bajtu tekstu. Niżej = lepsza predykcja. Model losowy = 8.0 (log2 z 256). Metryka ciągła.
- **Held-out** — tekst NIE użyty w treningu, sprawdzony pod kątem braku pokrycia z danymi treningowymi (dekontaminacja mierzona n-gramowo).
- **95% CI (przedział ufności)** — zakres, w którym z 95% pewnością leży prawdziwa wartość; słupki błędu na wykresie.
- **Model testowy** — mały model sieciowy wytrenowany na 2 przykładowych zdaniach (przykład ilustracyjny, nie docelowy).
- **Rdzeń dyskryminujący** — podzbiór par (tu ~8–10), na których metoda odniesienia wypada najsłabiej (accuracy ≤ losowego). To na nim mierzy się wynik modelu docelowego, bo tylko tam jest realna różnica do pokazania.
- **Margines nad baseline** — o ile accuracy modelu docelowego przewyższa accuracy metody odniesienia na rdzeniu dyskryminującym. To jest właściwy wynik modelu, nie samo accuracy.

## 3. Wykres 1 — accuracy metody n-gram według rzędu (plik `01_accuracy_wg_rzedu.png`)

- Oś X: rząd n-gramu (1, 2, 3, 4) = liczba poprzednich bajtów użytych do predykcji.
- Oś Y: accuracy (0–1) na 30 parach.
- Linia niebieska: accuracy metody n-gram; słupki błędu = 95% CI.
- Linia przerywana szara: poziom losowy = 0.50.
- Wartości: rząd 1 = 0.400; rząd 2 = 0.467; rząd 3 = 0.567; rząd 4 = 0.667.
- Odczyt: accuracy rośnie wraz z rzędem. Oznacza to, że test odróżnia metody używające większego kontekstu — czyli mierzy realną różnicę, a nie przypadek.
- Uwaga o wyniku modelu docelowego: ten wykres pokazuje accuracy na WSZYSTKICH 30 parach (metoda odniesienia). Dla wytrenowanego modelu docelowego wynikiem raportowanym (headline) jest accuracy na rdzeniu dyskryminującym (~8–10 par, gdzie metoda odniesienia zawodzi) oraz margines nad baseline — nie accuracy na 30 parach. Przyszłe „0.667 na 30" nie jest wynikiem modelu.

## 4. Wykres 2 — accuracy według rodziny zjawiska (plik `02_accuracy_wg_rodziny.png`)

- Oś X: rodzina zjawiska morfoskładniowego (w nawiasie liczba par n).
- Oś Y: accuracy metody n-gram rzędu 4.
- Linia przerywana szara: poziom losowy = 0.50.
- Wartości: rząd przypadka = 0.40; zgoda przymiotnik–rzeczownik = 0.875; rodzaj w czasie przeszłym = 0.71; aspekt = 0.80.
- Odczyt: metoda n-gram wypada najsłabiej na rządzie przypadka (0.40). Wartość 0.40 jest PONIŻEJ losowego (0.50): metoda nie jest tu neutralna, lecz systematycznie wybiera formę błędną (bo lokalnie częstszą) — jest anty-skorelowana z poprawnością. Wniosek: rząd przypadka to zjawisko, którego prosta metoda kontekstowa nie tylko nie rozwiązuje, ale rozwiązuje odwrotnie — daje to większy zapas (headroom) dla modelu docelowego i wskazuje właściwą oś dyskryminującą.

## 5. Wykres 3 — BPB metody n-gram według rzędu (plik `03_bpb_wg_rzedu.png`)

- Oś X: rząd n-gramu (1–4).
- Oś Y: BPB (bits-per-byte) na tekście held-out. Niżej = lepiej. Model losowy = 8.0.
- Słupki fioletowe: BPB metody n-gram; wartości: rząd 1 = 5.09; rząd 2 = 3.66; rząd 3 = 3.27; rząd 4 = 2.78.
- Linia przerywana czerwona: model testowy (trening na 2 zdaniach) = 5.31.
- Odczyt: BPB metody n-gram maleje wraz z rzędem. Model testowy (5.31) ma BPB wyższe niż n-gram rzędu 1 (5.09) — czyli nie osiągnął nawet poziomu najprostszej metody odniesienia.

## 6. Wynik (dosłownie)

- Test odróżnia metody (accuracy rośnie z rzędem: 0.40 → 0.667).
- Rząd przypadka jest najtrudniejszy dla metody odniesienia (0.40).
- Metryka BPB ma zdefiniowany poziom odniesienia (rząd 1 = 5.09; rząd 4 = 2.78); model testowy go nie osiągnął (5.31).

## 7. Ograniczenia (dosłownie)

- 30 par to mała próba; przedziały ufności są szerokie (ok. ±0.17 dla accuracy).
- Te wyniki dotyczą metody odniesienia (n-gram), nie wytrenowanego modelu docelowego.
- To pomiar poziomu odniesienia (baseline), nie ostateczna ocena modelu. Ocena modelu docelowego wymaga większej próby (≥85 par rozstrzygających) oraz wytrenowanych modeli (8M / 16M / 32M parametrów).

Źródła liczb: `../wyniki-ngram-o1..o4.json` (accuracy, CI, podział na zjawiska); wartości BPB zmierzone na held-oucie (rzędy 0–4); model testowy = przebieg pomiaru na wytrenowanym punkcie kontrolnym.
