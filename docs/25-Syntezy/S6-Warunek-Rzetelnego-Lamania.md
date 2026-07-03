---
type: synteza
id: BENCH-S6
title: "Warunek rzetelnego stress-testu (rozstrzyga T7 vs AT7)"
status: propozycja
parents: ["BENCH-T7", "BENCH-AT7", "BENCH-S3", "BENCH-S4"]
author: Arkadiusz Słota
date: 2026-07-02
---

# S6 — Kiedy „łamanie modelu" liczy się jako pomiar

## Rozstrzygnięcie
Celowane łamanie (T7) jest uprawnione **tylko** gdy zestaw przejdzie **bramkę rzetelności** (poniżej).
Bez niej niski pass-rate mierzy jakość zestawu, nie zdolność modelu (AT7). „Max 3/N" to **cel
orientacyjny**, nie kryterium akceptacji — kryterium jest bramka, nie sama liczba.

## Bramka rzetelnego łamania (5 warunków, wszystkie wymagane)
1. **Żelazny GT.** Każdy item ma odpowiedź weryfikowaną **programowo** (symulacja/brute-force)
   przed przejazdem. Zero GT „z głowy". Dowód w commicie (skrypt weryfikujący).
2. **Rozstrzygalność i jednoznaczność.** Item ma dokładnie jedną poprawną odpowiedź, prompt jest
   wewnętrznie spójny (bez sprzeczności typu D5B-SEQ-01). Jeśli dopuszcza >1 model świata → odrzucić.
3. **Nie floor, lecz punkt dyskryminacji.** Cel: niskie, ale **niezerowe** p. Jeśli Slayer uzyska
   0/N → **uruchom model odniesienia** (nemotron-4B, liga A). Gdy odniesienie też 0 → to floor
   (zestaw za trudny dla wszystkich, zero dyskryminacji), nie „granica Slayera" — obniżyć trudność.
4. **Czysta demarkacja pod-kategorii.** Rozdzielić i **osobno raportować**:
   - `wytrzymalosc-obliczeniowa` (długie bezbłędne wykonanie: modulo, silnia, Collatz),
   - `glebia-rozumowania` (planowanie wnioskowania: układy, constraint, inclusion-exclusion).
   Nie sumować w jeden wskaźnik — to różne konstrukty (AT7 pkt 3).
5. **Gradient, nie ściana.** Itemy o rosnącej trudności w obrębie kategorii, by zobaczyć *gdzie* p
   spada (próg załamania), a nie tylko *że* jest nisko.

## Procedura interpretacji wyniku
- **p w paśmie ~0.1–0.4 przy spełnionej bramce** → prawidłowy stress-test; raportuj *które* itemy
  łamią + tryb awarii (S3).
- **p = 0 u Slayera** → test odniesienia (pkt 3). Odniesienie zdaje cokolwiek → realna granica
  Slayera (mocny wynik). Odniesienie też 0 → floor, zrewiduj zestaw.
- **p wysokie mimo trudności** → sufit nieprzełamany, podnieś poprzeczkę (rotacja, S3).

## Konsekwencja dla „max 3"
Prośba „wyduś max 3/N" jest realizowana jako: **projektuj trudne itemy spełniające bramkę, celuj w
niskie p, ale akceptuj wynik jaki wyjdzie.** Jeśli Slayer zdaje więcej niż 3 mimo trudności spełniającej
bramkę — to jest **wynik o modelu** (jest mocny), nie porażka zestawu. Nie naginamy itemów, by
sztucznie zejść do 3 (to byłby Goodhart / pozorna trudność).

## Zapis w praktyce
Brutalne zestawy (`*-brutal-*`, `*-extreme-*`) deklarują w README: (a) skrypt weryfikacji GT,
(b) pod-kategorię (wytrzymałość vs głębia), (c) wynik odniesienia jeśli Slayer=0. To czyni stress-test
audytowalnym.

## Powiązania
parents: [[../10-Tezy/T7-Charakterystyka-Przez-Lamanie|T7]] · [[../15-Antytezy/AT7-Floor-I-Pozorna-Trudnosc|AT7]] · [[S3-IRT-Taksonomia|S3]] · [[S4-Taksonomia-Wymiarow|S4]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
