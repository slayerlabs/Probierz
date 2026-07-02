---
type: ewaluacja
id: BENCH-STAN
title: "Stan Probierz — żywy dokument"
status: żywy-dokument
author: Arkadiusz Słota
date: 2026-07-02
---

# Stan — co zmierzone, co otwarte

> Aktualizuj po każdym kroku (zasada Slayera). Nic tu nie jest przyjęte bez pomiaru — tylko zmierzone.

## ✓ Co zrobione (zmierzone)
| Element | Stan | Dowód |
|---|---|---|
| `contamination_check.py` | działa + ostrzejszy | self-check 100%; **any-match + span** łapie wtopione kopie (test Xaviera: span 19 tok złapany, frakcja 0.04 by przeszła) |
| Audyt `test_verification` | **SKAŻONY** | **100%** (any-match, n=13); span do 217 tok = całe itemy skopiowane |
| Manifest provenance | v1 | 6 datasetów oznaczonych; `test_verification` przeklasyfikowany |
| Protokół wymiany | v1 | commitment + reveal jednorazowy + rotacja + niezmienniki |
| Know-how dialektyczny (metoda uczciwości) | C1 + T1-3 + AT1-3 + S1-3 | broni się (każda teza ma antytezę + rozstrzygnięcie) |
| Benchmark `csharp-solid-v1` | **CZYSTY 0%** | 15 itemów adwersarialnych SOLID (domeny spoza seed_500); audyt vs seed_500 = 0% (any-match) |
| Review Xaviera (2026-06-26) | wdrożony | fix any-match/span w narzędziu + protokół „trust-minimized"; patrz [[Review-Xavier]] |
| Benchmark `d1-rozumowanie-v1` | **CZYSTY 0%** | 10 itemów rozumowania wieloetapowego (gradient 2–6 kroków); audyt vs seed_500 = 0% (span 0 tok) |
| Runner `tools/run_eval.py` | działa | przejazd OpenAI-compat + ocena deterministyczna + test parafraz; checkpoint per item + wznawianie |
| Baseline D1 — Slayer v49 | **zmierzony (1 model)** | 9/10 pass (mediana parafraz); 1 item wrażliwy; patrz sekcja „Baseline D1" |

## ✓ Warstwa konstruktu i modelu pomiaru (2026-07-02, rozpisane + recenzja wewnętrzna)
> Odpowiada na pytanie „**co** mierzymy i **jak** to formalizujemy", logicznie poprzedzające dobór zadań.
> Status: dialektyka domknięta (teza↔antyteza↔synteza z warunkiem obalenia); przeszła recenzję wewnętrzną.

| Element | Stan | Zawartość |
|---|---|---|
| **Warstwa 1 — Konstrukt** | rozpisana + zrecenzowana | [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej\|C2]] cel; [[../10-Tezy/T4-Dekompozycja-Wymiarow\|T4]] dekompozycja na wymiary D1–D6; [[../10-Tezy/T5-Falsyfikowalna-Rubryka\|T5]] rubryka pass/fail zamiast proxy; [[../15-Antytezy/AT4-Splatanie-Czynnik-G\|AT4]] czynnik g; [[../15-Antytezy/AT5-Format-Nie-Zdolnosc\|AT5]] format vs zdolność; [[../25-Syntezy/S4-Taksonomia-Wymiarow\|S4]] taksonomia + kryterium demarkacji + warunek obalenia per wymiar (D7/PL kandydujące) |
| **Warstwa 2 — Model pomiaru** | rozpisana + zrecenzowana | [[../10-Tezy/T6-IRT-Model-Pomiaru\|T6]] rodzina IRT (Rasch/2PL/3PL); [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc\|AT6]] założenia + nietrafność 2PL przy małym panelu; [[../25-Syntezy/S5-MIRT-Panel\|S5]] **Rasch/1PL domyślny** + Bradley-Terry porównawczy + bootstrap CI |

### Recenzja wewnętrzna (2026-07-02) — wdrożona
Krytyczna weryfikacja dialektyki (5 osi). Znaleziska wdrożone:
- **[KRYT.] 2PL nieidentyfikowalny przy panelu 5–12 modeli** (bilans obs/param ≈ 2–5) → S5 zmieniony na **1PL/Rasch domyślny**; 2PL warunkowo; **Bradley-Terry/Elo** porównawczy zawsze dostępny. AT6 rozszerzony o zarzut wyboru formalizmu + tabelę bilansu.
- **[KRYT.] próg „90% wariancji" arbitralny** → C2/S4/T4 zmienione na **analizę równoległą Horna**.
- **[IST.] „pojedyncze odwrócenie rankingu" za słabe przy szumie** → wzmocnione do **istotnego odwrócenia** (CI bootstrap nie zachodzą w obu wymiarach).
- **[IST.] granice wymiarów zazębiają się** → S4 dostał **kryterium demarkacji** + wymiary kandydujące D7/PL.

### Baseline D1 (rozumowanie wieloetapowe) — pierwszy węzeł panelu
Model: **Slayer v49** (przez lokalny proxy). Zestaw: 10 itemów, gradient 2–6 kroków. Ocena
deterministyczna (T5), 3 parafrazy/item (AT5).

| Metryka | Wartość |
|---|---|
| Pass (mediana parafraz) | **9/10 (0.90)** |
| Itemy wrażliwe na parafrazę | 1 |
| Jedyny fail | `D1-L4-02` (zbiorniki, ograniczenie fizyczne) — 1/3 parafraz, wrażliwy |

**Interpretacja (uczciwie):**
- Sygnał jakościowy zgodny z projektem: jedyny fail to item z **pułapką brzegową** (nie można wylać
  45 l z 30 l) — jednocześnie **wrażliwy na parafrazę**. Item różnicuje.
- **9/10 to sufit dla pojedynczego modelu** → słaba dyskryminacja (AT3/S3). To **nie jest** ocena
  trudności zestawu — trudność $b_j$ jest niemierzalna z jednego modelu (S5). Wynik potwierdza
  konieczność **panelu ≥5 modeli**.
- Estymacja $\theta^{(D1)}$ / Rascha / Bradleya-Terry'ego **wstrzymana** do zebrania panelu — z jednym
  modelem parametry nieidentyfikowalne (zgodnie z AT6/S5).

## ○ Otwarte (kryteria sukcesu C1 + C2)
1. ~~Brak czystego eval-only~~ → **dwa czyste zestawy:** `csharp-solid-v1`, `d1-rozumowanie-v1` (0%).
2. **Drugi team** — niezbędny do T2/blind exchange; obecnie brak partnera. Bez niego — autowalidacja.
3. **Panel kalibracyjny** (S3/S5) — **1/≥5 modeli** (Slayer). Brakuje ≥4 modeli (słaby→mocny) do
   estymacji trudności i rozłączności.
4. **Overlap embeddingowy** (S2, granica n-gramu) — n-gram nie łapie parafrazy; dodać warstwę semantyczną.
5. **Dowód empiryczny konstruktu (C2/S4)** — rozłączność wymiarów niezmierzona (wymaga panelu × ≥2 wymiary).
6. **Zestawy per wymiar** — **D1 gotowy** (10 itemów, 0%). Brakuje **D2–D6**.
7. **Identyfikowalność modelu pomiaru** — potwierdzone empirycznie, że 1 model nie wystarcza; pytanie
   otwarte: czy 1PL stabilny przy realnym M; jeśli nie → wyłącznie Bradley-Terry.

## Kryterium obalenia — dwa poziomy
- **C1 (uczciwość):** jeśli nasz „czysty" benchmark daje ten sam ranking co skażony publiczny → przewaga provenance to iluzja. Test wykonalny, gdy istnieje zbiór eval-only + ≥2 modele.
- **C2 (konstrukt):** jeśli w analizie równoległej tylko pierwsza składowa [model×wymiar] przekracza poziom odniesienia z permutacji **oraz** brak istotnych odwróceń rankingu → konstrukt jednowymiarowy, taksonomia D1–D6 upada (procedura: S4).

## Następny krok (priorytet)
Baseline D1 zwalidował całą ścieżkę (dane → audyt 0% → runner → przejazd → ocena). Dalej, równolegle:
1. **Zestawy D2–D6** — analogicznie do D1 (rubryka T5, parafrazy AT5, demarkacja S4, audyt 0%).
2. **Panel modeli** — dodać ≥4 modele obok Slayera (słaby→mocny; kandydaci lokalni przez LM Studio),
   przejazd D1 całym panelem → pierwsza macierz [model × wymiar].
3. Po zebraniu panelu × ≥2 wymiary: **estymacja** (Bradley-Terry + 1PL, bootstrap CI, S5) + **test
   warunków obalenia** S4 (istotne odwrócenia, analiza równoległa).
Faza **research** po baseline: potwierdzenie liczb (replikacja, stabilność estymat, wrażliwość na dobór panelu).
