---
type: metoda
id: BENCH-METODA-LAMANIE
title: "Łamanie modeli: charakterystyka granicy i warunek rzetelnego stress-testu"
status: propozycja
author: Arkadiusz Słota
date: 2026-07-02
---

# Łamanie modeli: charakterystyka granicy i warunek rzetelnego stress-testu

Dopóki model przechodzi zestaw wysoko, nie znamy jego granicy. Ten dokument opisuje, jak celowo sprowadzać pass-rate nisko, żeby zobaczyć, gdzie i jak model pęka, oraz jakie warunki musi spełnić taki zestaw, żeby niski wynik mierzył model, a nie wady zestawu. Dla benchmarków wynika z tego bramka rzetelności obowiązkowa dla zestawów `*-brutal-*` i `*-extreme-*` oraz procedura interpretacji wyniku zerowego.

## Charakterystyka przez łamanie

Dopóki model przechodzi zestaw wysoko (sufit: 90–100%), wiemy tylko, że jest „co najmniej tak dobry”. Charakterystyka zdolności wymaga zestawów, na których model realnie się łamie: pass-rate celowo sprowadzony nisko (orientacyjnie 2–3 / N), bo dopiero tam widać, gdzie i jak pęka. To operacjonalizacja fazy „stress-test” w charakterystyce Slayera (DEC2).

Uzasadnienie:
- **Sufit nie daje informacji.** D1-łatwy (9–10/10), D6 (100%), D5a (8/8) nie zawężają oszacowania zdolności. Informacja itemu jest maksymalna przy p≈0.5, a znikoma przy p≈1 (zob. [[Model-pomiaru-IRT|model pomiaru IRT]] i [[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]]).
- **Tryby awarii ujawniają się pod obciążeniem.** Dopiero gdy model zawodzi, taksonomia awarii (zob. [[Trudnosc-i-taksonomia-awarii|taksonomia awarii]]) daje sygnał diagnostyczny: czy to błędny plan, kumulacja błędu w długim łańcuchu, czy ciche pominięcie.
- **Dotychczasowa empiria.** Jedyny wymiar, w którym Slayer realnie pękł, to D1 przy głębokiej wieloetapowości (extreme 0.83). To wskazuje kierunek: zwiększać długość i kumulację łańcucha.

### Docelowy poziom trudności

Celujemy w 2–3 / N, nie w 0 / N. Pass-rate równy 0 dla wszystkich modeli to floor effect: zero dyskryminacji, benchmark nie odróżnia modelu słabego od mocnego (zob. [[Trudnosc-i-taksonomia-awarii|floor effect i sufit]]). Punkt 2–3/N leży blisko dolnego pasma informacyjnego, ale zachowuje sygnał: część itemów jeszcze przechodzi, więc widać, które konkretnie łamią model.

### Co realnie obciąża rozumowanie

- **Długi bezbłędny łańcuch**: kumulacja błędu (Collatz, iterowane potęgowanie, rekurencja rosnąca).
- **Śledzenie stanu przez wiele kroków**: symulacja, ciągi.
- **Precyzja liczbowa**: modulo, silnia, duże liczby (brak miejsca na „zaokrąglenie w głowie”).
- **Constraint satisfaction / inclusion-exclusion**: wiele współzależnych warunków.

## Pozorna trudność

Ustawianie z góry docelowego pass-rate („max 3/N”) grozi odwróceniem kierunku wnioskowania: zamiast mierzyć zdolność, projektujemy pod wynik. Znane ryzyka są cztery:

1. **Floor effect.** Jeśli itemy są tak trudne, że wszystkie modele dostają ~0, benchmark nie odróżnia słabego od mocnego. Cel „max 3” łatwo przestrzelić w 0, a wtedy wynik Slayera jest nieinterpretowalny: nie wiadomo, czy 0 to jego granica, czy granica wszystkich.
2. **Pozorna trudność to nie trudność zdolnościowa.** Najłatwiej „złamać” model itemem, który jest po prostu zły: ma błędny GT, jest nierozstrzygalny, niejednoznaczny albo zawiera pułapkę w treści polecenia (jak sprzeczny prompt D5B-SEQ-01). Wtedy porażka mierzy wadę zestawu, nie model. Ryzyko rośnie z trudnością: im bardziej złożony item, tym łatwiej autorowi samemu pomylić się w GT.
3. **Pomieszanie obliczeń z rozumowaniem.** Itemy typu „Collatz od 27 = 111 kroków” albo „7^100 mod 13” łamią model przez arytmetyczną wytrzymałość (bezbłędne wykonanie 100+ operacji), nie przez głębię rozumowania. To realna słabość LLM, ale inny konstrukt niż D1 (planowanie wnioskowania). Mieszanie ich zaciera, co właściwie mierzymy, i narusza rozłączność wymiarów (zob. [[Wymiary-i-rubryka|wymiary i rubryka]]).
4. **Goodhart na trudności.** „Celuj w 2–3/N” to metryka, pod którą można optymalizować dobór itemów i dostać zestaw, który wygląda na bardzo trudny, a faktycznie testuje wąską, przypadkową niszę (np. tylko długie mnożenie modulo), a nie szerokie rozumowanie.

Bez zabezpieczeń zestaw „na max 3” daje liczbę, która wygląda na twardą charakterystykę granicy Slayera, a faktycznie mierzy: (a) czy przestrzeliliśmy w floor, (b) ile itemów ma wadliwe GT, (c) jaką wąską zdolność arytmetyczną przypadkiem trafiliśmy. Wniosek „Slayer łamie się na rozumowaniu” byłby wtedy nieuprawniony.

## Warunek rzetelnego łamania

Celowane łamanie jest uprawnione tylko wtedy, gdy zestaw przejdzie bramkę rzetelności opisaną niżej. Bez niej niski pass-rate mierzy jakość zestawu, nie zdolność modelu. „Max 3/N” to cel orientacyjny, nie kryterium akceptacji; kryterium jest bramka, nie sama liczba.

Bramka ma 5 warunków, wszystkie są wymagane:

1. **Żelazny GT.** Każdy item ma odpowiedź weryfikowaną programowo (symulacja/brute-force) przed przejazdem. Zero GT „z głowy”. Dowodem jest skrypt weryfikujący w commicie.
2. **Rozstrzygalność i jednoznaczność.** Item ma dokładnie jedną poprawną odpowiedź, a prompt jest wewnętrznie spójny (bez sprzeczności typu D5B-SEQ-01). Jeśli item dopuszcza więcej niż jeden model świata, odrzucamy go.
3. **Nie floor, lecz punkt dyskryminacji.** Cel: niskie, ale niezerowe p. Jeśli Slayer uzyska 0/N, uruchamiamy model odniesienia (nemotron-4B, liga A). Gdy odniesienie też ma 0, to floor (zestaw za trudny dla wszystkich, zero dyskryminacji), a nie „granica Slayera”; należy obniżyć trudność.
4. **Czysta demarkacja pod-kategorii.** Rozdzielamy i osobno raportujemy:
   - `wytrzymalosc-obliczeniowa` (długie bezbłędne wykonanie: modulo, silnia, Collatz),
   - `glebia-rozumowania` (planowanie wnioskowania: układy, constraint, inclusion-exclusion).
   Nie sumujemy ich w jeden wskaźnik, bo to różne konstrukty (zob. ryzyko 3 w sekcji „Pozorna trudność”).
5. **Gradient, nie ściana.** Itemy o rosnącej trudności w obrębie kategorii, by zobaczyć, gdzie p spada (próg załamania), a nie tylko, że jest nisko.

## Interpretacja wyniku

- **p w paśmie ~0.1–0.4 przy spełnionej bramce**: prawidłowy stress-test. Raportujemy, które itemy łamią model, oraz tryb awarii (zob. [[Trudnosc-i-taksonomia-awarii|taksonomia awarii]]).
- **p = 0 u Slayera**: test odniesienia (pkt 3). Jeśli odniesienie zdaje cokolwiek, to realna granica Slayera (mocny wynik). Jeśli odniesienie też ma 0, to floor i zestaw trzeba zrewidować.
- **p wysokie mimo trudności**: sufit nieprzełamany, podnosimy poprzeczkę (zob. [[Trudnosc-i-taksonomia-awarii|rotacja poprzeczki]]).

Prośba „wyduś max 3/N” jest realizowana tak: projektujemy trudne itemy spełniające bramkę, celujemy w niskie p, ale akceptujemy wynik, jaki wyjdzie. Jeśli Slayer zdaje więcej niż 3 mimo trudności spełniającej bramkę, to jest wynik o modelu (jest mocny), a nie porażka zestawu. Nie naginamy itemów, by sztucznie zejść do 3, bo byłby to Goodhart i pozorna trudność.

## Zapis w praktyce

Zestawy brutalne (`*-brutal-*`, `*-extreme-*`) deklarują w README: (a) skrypt weryfikacji GT, (b) pod-kategorię (wytrzymałość vs głębia), (c) wynik odniesienia, jeśli Slayer=0. To czyni stress-test audytowalnym.

## Kiedy to podejście uznajemy za błędne

Charakterystykę przez łamanie uznajemy za błędną, jeśli okaże się, że niski pass-rate osiągamy tylko przez itemy wadliwe lub nierozstrzygalne (zob. „Pozorna trudność”). Wtedy „łamanie” mierzy jakość zestawu, nie model. Rozstrzyga o tym warunek rzetelnego łamania.

## Powiązane

[[Trudnosc-i-taksonomia-awarii|trudność i taksonomia awarii]] · [[Wymiary-i-rubryka|wymiary i rubryka]] · [[Model-pomiaru-IRT|model pomiaru IRT]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
