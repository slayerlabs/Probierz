---
type: antyteza
id: BENCH-AT7
title: "Celowane łamanie produkuje floor effect i myli pozorną trudność ze zdolnością"
status: w-dyskusji
parents: ["BENCH-T7"]
author: Arkadiusz Słota
date: 2026-07-02
---

# AT7 — „Wyduszanie max 3" jest metodologicznie niebezpieczne (steelman)

## Najmocniejsza wersja
Ustawianie z góry docelowego pass-rate („max 3/N") odwraca kierunek wnioskowania: zamiast **mierzyć**
zdolność, **projektujemy pod wynik**. To rodzi cztery poważne zagrożenia:

1. **Floor effect (zabójca dyskryminacji).** Jeśli itemy są tak trudne, że wszystkie modele dostają
   ~0, benchmark nie odróżnia słabego od mocnego (AT3). „Max 3" łatwo przestrzelić w 0 — a wtedy wynik
   Slayera jest nieinterpretowalny (nie wiadomo, czy 0 to jego granica czy granica wszystkich).

2. **Pozorna trudność ≠ trudność zdolnościowa.** Najłatwiej „złamać" model itemem, który jest po
   prostu **zły**: błędny GT, zadanie nierozstrzygalne, niejednoznaczne, albo z pułapką w treści
   polecenia (jak sprzeczny prompt D5B-SEQ-01). Wtedy fail mierzy wadę zestawu, nie model. Ryzyko
   rośnie z trudnością — im bardziej złożony item, tym łatwiej autorowi samemu się pomylić w GT.

3. **Confounding: obliczenia vs rozumowanie.** Itemy typu „Collatz od 27 = 111 kroków" albo „7^100 mod
   13" łamią model, ale przez **arytmetyczną wytrzymałość** (bezbłędne wykonanie 100+ operacji), nie
   przez głębię rozumowania. To realna słabość LLM, ale **inny konstrukt** niż D1 (planowanie
   wnioskowania). Mieszanie ich zaciera, *co* właściwie mierzymy — narusza demarkację (S4).

4. **Goodhart na trudności.** „Celuj w 2–3/N" to metryka, pod którą można optymalizować dobór itemów —
   i dostać zestaw, który wygląda na bezlitosny, a faktycznie testuje wąską, przypadkową niszę
   (np. tylko długie mnożenie modulo), nie szerokie rozumowanie.

## Konsekwencja, jeśli prawdziwa
Zestaw „na max 3" bez zabezpieczeń daje liczbę, która **wygląda** na twardą charakterystykę granicy
Slayera, a faktycznie mierzy: (a) czy przestrzeliliśmy w floor, (b) ile itemów ma wadliwe GT, (c) jaką
wąską zdolność arytmetyczną przypadkiem trafiliśmy. Wniosek „Slayer łamie się na rozumowaniu" byłby
wtedy nieuprawniony.

## Czego wymaga, by ją odeprzeć (kierunek dla S6)
- **żelazny GT** — każdy item weryfikowany programowo (symulacja/brute-force) PRZED przejazdem;
- **nie floor, lecz punkt dyskryminacji** — celować w niskie, ale niezerowe p; przy 0/N u Slayera
  sprawdzić model odniesienia (czy ktokolwiek zdaje — inaczej to floor, nie granica Slayera);
- **czysta demarkacja** — rozdzielić „wytrzymałość obliczeniowa" od „głębia rozumowania" na osobne
  pod-kategorie, nie mieszać w jednym wskaźniku;
- **gradient, nie ściana** — itemy o rosnącej trudności, by zobaczyć *gdzie* p spada, a nie tylko *że*
  jest nisko.

## Powiązania
parent: [[../10-Tezy/T7-Charakterystyka-Przez-Lamanie|T7]] · pokrewne: [[AT3-Floor-Effect|AT3]] · rozstrzyga: [[../25-Syntezy/S6-Warunek-Rzetelnego-Lamania|S6]] · demarkacja: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]]
