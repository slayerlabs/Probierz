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
| Benchmark `csharp-solid-v1` | **CZYSTY 0%** | 15 itemów adwersarialnych SOLID; audyt vs seed_500 = 0% |
| Review Xaviera (2026-06-26) | wdrożony | fix any-match/span + protokół „trust-minimized"; patrz [[Review-Xavier]] |
| Benchmark `d1-rozumowanie-v1` | **CZYSTY 0%** | 10 itemów rozumowania wieloetapowego (gradient 2–6 kroków); audyt = 0% (span 0 tok) |
| Benchmark `d2-semantyka-v1` | **CZYSTY 0%** | 10 itemów semantyki (negacja/kwantyfikatory/scope/presupozycja/implikatura/koreferencja); audyt = 0% |
| Runner `tools/run_eval.py` | działa | przejazd OpenAI-compat + ocena deterministyczna + test parafraz; checkpoint per item + wznawianie; grader wykrywa klasę odpowiedzi (najdłuższa fraza) |
| Baseline D1 — Slayer v49 | **zmierzony (1 model)** | 9/10 pass; 1 wrażliwy; patrz „Baseline D1/D2" |
| Baseline D2 — Slayer v49 | **zmierzony (1 model)** | 9/10 pass; 2 wrażliwe; fail = koreferencja |

## ✓ Warstwa konstruktu i modelu pomiaru (2026-07-02, rozpisane + recenzja wewnętrzna)
> Odpowiada na pytanie „**co** mierzymy i **jak** to formalizujemy", logicznie poprzedzające dobór zadań.
> Status: dialektyka domknięta (teza↔antyteza↔synteza z warunkiem obalenia); przeszła recenzję wewnętrzną.

| Element | Stan | Zawartość |
|---|---|---|
| **Warstwa 1 — Konstrukt** | rozpisana + zrecenzowana | [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej\|C2]] cel; [[../10-Tezy/T4-Dekompozycja-Wymiarow\|T4]] wymiary D1–D6; [[../10-Tezy/T5-Falsyfikowalna-Rubryka\|T5]] rubryka; [[../15-Antytezy/AT4-Splatanie-Czynnik-G\|AT4]] czynnik g; [[../15-Antytezy/AT5-Format-Nie-Zdolnosc\|AT5]] format vs zdolność; [[../25-Syntezy/S4-Taksonomia-Wymiarow\|S4]] taksonomia + demarkacja + warunek obalenia |
| **Warstwa 2 — Model pomiaru** | rozpisana + zrecenzowana | [[../10-Tezy/T6-IRT-Model-Pomiaru\|T6]] rodzina IRT; [[../15-Antytezy/AT6-Jednowymiarowosc-Niezaleznosc\|AT6]] nietrafność 2PL przy małym panelu; [[../25-Syntezy/S5-MIRT-Panel\|S5]] Rasch/1PL + Bradley-Terry + bootstrap CI |

### Recenzja wewnętrzna (2026-07-02) — wdrożona
- **[KRYT.] 2PL nieidentyfikowalny przy panelu 5–12 modeli** → S5: 1PL/Rasch domyślny + Bradley-Terry; AT6 + tabela bilansu.
- **[KRYT.] próg „90% wariancji" arbitralny** → analiza równoległa Horna (C2/S4/T4).
- **[IST.] słabe „pojedyncze odwrócenie"** → istotne odwrócenie (CI bootstrap).
- **[IST.] zazębianie wymiarów** → kryterium demarkacji S4 + kandydaci D7/PL.

### Baseline D1 + D2 — Slayer v49 (pierwszy węzeł panelu)
Model: **Slayer v49** (proxy lokalny). Ocena deterministyczna (T5), 3 parafrazy/item (AT5).

| Wymiar | Pass (mediana) | Wrażliwe | Fail |
|---|---|---|---|
| **D1** rozumowanie | 9/10 (0.90) | 1 | `D1-L4-02` pułapka brzegowa (nie wylać 45 l z 30 l), 1/3 |
| **D2** semantyka | 9/10 (0.90) | 2 | `D2-L4-03` koreferencja (Winograd), **0/3 twardy fail** |

**Interpretacja (uczciwie):**
- **Sygnał jakościowy trafny:** faile są tam, gdzie miały być — D1 pęka na ograniczeniu fizycznym,
  D2 na koreferencji zaimka (znana trudność LLM) i implikaturze. Gradient trudności działa: poziomy
  1–3 przechodzą, faile na poziomie 4.
- **9/10 na OBU wymiarach = sufit dla jednego modelu.** Slayer nie różnicuje wymiarów przy tej
  trudności → **nie da się jeszcze wykonać testu rozłączności D1↔D2** (S4: istotne odwrócenie
  wymaga pary modeli o rozjeżdżających się wynikach). To empiryczne potwierdzenie AT4/S4: rozłączność
  jest własnością **panelu**, nie pojedynczego modelu.
- Estymacja $\theta$ / Rascha / Bradleya-Terry'ego oraz analiza równoległa **wstrzymane** do panelu —
  z jednym modelem parametry i składowe nieidentyfikowalne (AT6/S5).
- Wniosek operacyjny: **kolejne wymiary bez panelu nie zwiększają mocy dowodowej** — priorytetem staje
  się zebranie panelu ≥5 modeli i przejazd D1+D2 wszystkimi.

## ○ Otwarte (kryteria sukcesu C1 + C2)
1. ~~Brak czystego eval-only~~ → **trzy czyste zestawy:** `csharp-solid-v1`, `d1-rozumowanie-v1`, `d2-semantyka-v1` (0%).
2. **Drugi team** — niezbędny do T2/blind exchange; brak partnera. Bez niego — autowalidacja.
3. **Panel kalibracyjny** (S3/S5) — **1/≥5 modeli** (Slayer). Brak ≥4 modeli (słaby→mocny) — **blokuje estymację i test rozłączności**.
4. **Overlap embeddingowy** (S2) — n-gram nie łapie parafrazy; dodać warstwę semantyczną.
5. **Dowód rozłączności D1↔D2 (C2/S4)** — pierwsze dane są (macierz 1×2), ale **1 model nie wystarcza**; test wykonalny dopiero na panelu.
6. **Zestawy per wymiar** — **D1, D2 gotowe** (0%). Brakuje **D3–D6**.
7. **Identyfikowalność modelu pomiaru** — potwierdzone, że 1 model nie wystarcza; czy 1PL stabilny przy realnym M → do sprawdzenia na panelu.

## Kryterium obalenia — dwa poziomy
- **C1 (uczciwość):** jeśli „czysty" benchmark daje ten sam ranking co skażony publiczny → przewaga provenance to iluzja. Test: zbiór eval-only + ≥2 modele.
- **C2 (konstrukt):** jeśli w analizie równoległej tylko 1. składowa [model×wymiar] przekracza poziom permutacyjny **oraz** brak istotnych odwróceń → konstrukt jednowymiarowy, D1–D6 upada (procedura: S4).

## Następny krok (priorytet)
Baseline D1+D2 pokazał: **przy jednym modelu wymiary są nierozróżnialne (sufit 9/10)**. Metoda naukowa
wymaga teraz **panelu**, nie kolejnych wymiarów. Priorytet:
1. **Panel modeli** — ≥4 modele obok Slayera (słaby→mocny; lokalne przez LM Studio), przejazd D1+D2
   całym panelem → pierwsza macierz [model × wymiar] z rozrzutem.
2. **Estymacja** (Bradley-Terry + 1PL, bootstrap CI, S5) + **test rozłączności D1↔D2** (S4: istotne
   odwrócenia, analiza równoległa) → pierwsza empiryczna weryfikacja C2.
3. Dalej: zestawy **D3–D6** (wzorzec D1/D2) + rozszerzenie panelu.
Faza **research** po baseline: replikacja, stabilność estymat, wrażliwość na dobór panelu.
