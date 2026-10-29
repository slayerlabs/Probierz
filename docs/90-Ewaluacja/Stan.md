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
| Metoda uczciwości pomiaru | C1 + [[../metoda/Kontaminacja-i-wymiana\|kontaminacja i wymiana]] + [[../metoda/Trudnosc-i-taksonomia-awarii\|trudność i taksonomia awarii]] | opisana; każde założenie ma zapisane kryterium obalenia |
| Benchmark `csharp-solid-v1` | **CZYSTY 0%** | 15 itemów adwersarialnych SOLID; audyt vs seed_500 = 0% |
| Review Xaviera (2026-06-26) | wdrożony | fix any-match/span + protokół „trust-minimized"; patrz [[Review-Xavier]] |
| Benchmark `d1-rozumowanie-v1` | **CZYSTY 0%** | 10 itemów rozumowania wieloetapowego (gradient 2–6 kroków); audyt = 0% (span 0 tok) |
| Benchmark `d2-semantyka-v1` | **CZYSTY 0%** | 10 itemów semantyki (negacja/kwantyfikatory/scope/presupozycja/implikatura/koreferencja); audyt = 0% |
| Runner `tools/run_eval.py` | działa | przejazd OpenAI-compat + ocena deterministyczna + test parafraz; checkpoint per item + wznawianie; grader wykrywa klasę odpowiedzi (najdłuższa fraza) |
| Baseline D1 — Slayer v49 | **zmierzony (1 model)** | 9/10 pass; 1 wrażliwy; patrz „Baseline D1/D2" |
| Baseline D2 — Slayer v49 | **zmierzony (1 model)** | 9/10 pass; 2 wrażliwe; fail = koreferencja |

## ✓ Warstwa konstruktu i modelu pomiaru (2026-07-02, rozpisane + recenzja wewnętrzna)
> Odpowiada na pytanie „**co** mierzymy i **jak** to formalizujemy", logicznie poprzedzające dobór zadań.
> Status: opisane, z kryteriami obalenia; przeszło recenzję wewnętrzną.

| Element | Stan | Zawartość |
|---|---|---|
| **Warstwa 1 — Konstrukt** | rozpisana + zrecenzowana | [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej\|C2]] cel; [[../metoda/Wymiary-i-rubryka\|wymiary D1–D6]]; [[../metoda/Wymiary-i-rubryka\|deterministyczna rubryka]] rubryka; [[../metoda/Wymiary-i-rubryka\|ryzyko jednego czynnika ogólnego]] czynnik g; [[../metoda/Wymiary-i-rubryka\|test parafraz]] format vs zdolność; [[../metoda/Wymiary-i-rubryka\|kryterium rozłączności]] taksonomia + demarkacja + warunek obalenia |
| **Warstwa 2 — Model pomiaru** | rozpisana + zrecenzowana | [[../metoda/Model-pomiaru-IRT\|model pomiaru]] rodzina IRT; [[../metoda/Model-pomiaru-IRT\|założenia modelu pomiaru]] nietrafność 2PL przy małym panelu; [[../metoda/Model-pomiaru-IRT\|model pomiaru]] Rasch/1PL + Bradley-Terry + bootstrap CI |

### Recenzja wewnętrzna (2026-07-02) — wdrożona
- **[KRYT.] 2PL nieidentyfikowalny przy panelu 5–12 modeli** → model pomiaru: 1PL/Rasch domyślny + Bradley-Terry; założenia modelu pomiaru + tabela bilansu.
- **[KRYT.] próg „90% wariancji" arbitralny** → analiza równoległa Horna.
- **[IST.] słabe „pojedyncze odwrócenie"** → istotne odwrócenie (CI bootstrap).
- **[IST.] zazębianie wymiarów** → kryterium demarkacji kryterium rozłączności + kandydaci D7/PL.

### Baseline D1 + D2 — Slayer v49 (pierwszy węzeł panelu)
Model: **Slayer v49** (proxy lokalny). Ocena deterministyczna, 3 parafrazy/item.

| Wymiar | Pass (mediana) | Wrażliwe | Fail |
|---|---|---|---|
| **D1** rozumowanie | 9/10 (0.90) | 1 | `D1-L4-02` pułapka brzegowa (nie wylać 45 l z 30 l), 1/3 |
| **D2** semantyka | 9/10 (0.90) | 2 | `D2-L4-03` koreferencja (Winograd), **0/3 twardy fail** |

**Interpretacja (uczciwie):**
- **Sygnał jakościowy trafny:** faile są tam, gdzie miały być — D1 pęka na ograniczeniu fizycznym,
  D2 na koreferencji zaimka (znana trudność LLM) i implikaturze. Gradient trudności działa: poziomy
  1–3 przechodzą, faile na poziomie 4.
- **9/10 na OBU wymiarach = sufit dla jednego modelu.** Slayer nie różnicuje wymiarów przy tej
  trudności → **nie da się jeszcze wykonać testu rozłączności D1↔D2** (istotne odwrócenie
  wymaga pary modeli o rozjeżdżających się wynikach). To empiryczne potwierdzenie ryzyko jednego czynnika ogólnego: rozłączność
  jest własnością **panelu**, nie pojedynczego modelu.
- Estymacja $\theta$ / Rascha / Bradleya-Terry'ego oraz analiza równoległa **wstrzymane** do panelu —
  z jednym modelem parametry i składowe nieidentyfikowalne.
- Wniosek operacyjny: **kolejne wymiary bez panelu nie zwiększają mocy dowodowej** — priorytetem staje
  się zebranie panelu ≥5 modeli i przejazd D1+D2 wszystkimi.

## ✓ Warstwa leaderboard + metryka BPB (2026-09-11)
> Dokumenty: [[../metoda/Metryka-BPB-i-leaderboard|metryka BPB, confound tokenizera i bramka leaderboardu]] · [[../20-Decyzje/D-DEC3-Leaderboard-Eksperymentalny|DEC3]]

| Element | Stan | Dowód |
|---|---|---|
| Benchmark `d3-skladnia-v2` | CZYSTY, 148 rdzeń | 472 par (Morfeusz 2), 3 sita; skan 11.29M docs |
| Benchmark `d3-skladnia-v3` | CZYSTY, 273 rdzeń | skala v2, ta sama metoda + sita |
| Metryka **BPB** (tokenizer-fair) | działa | `bpb_scorer.py`; held-out 300 docs/153 583 B; round-trip 100%/0 UNK |
| Metryka **margin** (ciągła d3) | działa | większa moc niż accuracy (paired-bootstrap) |
| **Panel: 5 modeli zmierzonych** | GoLLeM-45M/110M-v2/v3, Slayer-110M, Polock-125M | BPB + d3 (acc+margin) + 95% CI |
| Komórka (110M, 32000) | **rozstrzygnięta** | v3<Slayer<v2 (paired-bootstrap; BPB i margin; rdzeń 148 i 273); `caveat:single-seed` |
| Leaderboard + gate | DEC3 | fabryka-track `leaderboard-d3`; INDISTINGUISHABLE-GATE; `results/` + SHA256 piny |

**Rusza otwarte (§ poniżej):**
- Panel ≥5 (poz. 3): **5 modeli zmierzonych** — ale różne tokenizery → atrybucja tylko w komórce kontrolowanej; byte-modele fabryki (jedna skala) czekają na loader BDH.
- Wymiary (poz. 6): **D3-składnia gotowe** (v2+v3); zostają D4–D6.

**Otwarte w tej warstwie:** Gate 1 (≥3 seedy treningowe → poziom recepty) na RunPod; loader byte-modeli fabryki (arch. BDH, vocab 256); rotacja rdzenia sterowana saturacją (`acc_core < ~0.9`).

## ○ Otwarte (kryteria sukcesu C1 + C2)
1. ~~Brak czystego eval-only~~ → **trzy czyste zestawy:** `csharp-solid-v1`, `d1-rozumowanie-v1`, `d2-semantyka-v1` (0%).
2. **Drugi team** — niezbędny do ślepa wymiana/blind exchange; brak partnera. Bez niego — autowalidacja.
3. **Panel kalibracyjny** — **1/≥5 modeli** (Slayer). Brak ≥4 modeli (słaby→mocny) — **blokuje estymację i test rozłączności**.
4. **Overlap embeddingowy** — n-gram nie łapie parafrazy; dodać warstwę semantyczną.
5. **Dowód rozłączności D1↔D2** — pierwsze dane są (macierz 1×2), ale **1 model nie wystarcza**; test wykonalny dopiero na panelu.
6. **Zestawy per wymiar** — **D1, D2 gotowe** (0%). Brakuje **D3–D6**.
7. **Identyfikowalność modelu pomiaru** — potwierdzone, że 1 model nie wystarcza; czy 1PL stabilny przy realnym M → do sprawdzenia na panelu.

## Kryterium obalenia — dwa poziomy
- **C1 (uczciwość):** jeśli „czysty" benchmark daje ten sam ranking co skażony publiczny → przewaga provenance to iluzja. Test: zbiór eval-only + ≥2 modele.
- **C2 (konstrukt):** jeśli w analizie równoległej tylko 1. składowa [model×wymiar] przekracza poziom permutacyjny **oraz** brak istotnych odwróceń → konstrukt jednowymiarowy, D1–D6 upada (procedura: kryterium rozłączności).

## Następny krok (priorytet)
Baseline D1+D2 pokazał: **przy jednym modelu wymiary są nierozróżnialne (sufit 9/10)**. Metoda naukowa
wymaga teraz **panelu**, nie kolejnych wymiarów. Priorytet:
1. **Panel modeli** — ≥4 modele obok Slayera (słaby→mocny; lokalne przez LM Studio), przejazd D1+D2
   całym panelem → pierwsza macierz [model × wymiar] z rozrzutem.
2. **Estymacja** (Bradley-Terry + 1PL, bootstrap CI) + **test rozłączności D1↔D2** (istotne
   odwrócenia, analiza równoległa) → pierwsza empiryczna weryfikacja C2.
3. Dalej: zestawy **D3–D6** (wzorzec D1/D2) + rozszerzenie panelu.
Faza **research** po baseline: replikacja, stabilność estymat, wrażliwość na dobór panelu.
