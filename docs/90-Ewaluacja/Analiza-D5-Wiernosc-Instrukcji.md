---
type: analiza
id: BENCH-ANALIZA-D5
title: "Analiza D5 — wierność instrukcji i orkiestracja Slayera"
status: aktywny
parents: ["BENCH-D5-V1", "BENCH-D5-ORK-V1", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza D5 — wierność instrukcji Slayera

## Wyniki
| Zestaw | Wynik | Wrażliwe | Charakter |
|---|---|---|---|
| `d5-wiernosc-instrukcji-v1` (twarde ograniczenia) | **8/8 (100%)** | 2 | pojedyncze ograniczenia formatu |
| `d5-orkiestracja-v1` (agentyczna) | **5/6 (83%)** | 1 | orkiestracja, ograniczenia skumulowane |

## D5a — twarde ograniczenia formatu: sufit
Slayer opanował wszystkie pojedyncze ograniczenia: dokładna liczba słów, zakaz litery „a", tylko wielkie
litery, dokładna liczba linii, JSON z kluczami, prefiks, zakaz słowa, **odporność na wstrzyknięcie**
(nie dał się zbić na „HACKED"). Wrażliwe 2/8 (zakaz litery, zakaz słowa — bywa niestabilny przy parafrazie).

## D5b — orkiestracja: pierwsza realna słabość
Slayer jako orkiestrator (narzędzia + zasady + zadanie → wywołanie JSON):
- **Zdał:** wybór właściwego narzędzia (search vs read), kompletność argumentów (write z path+content),
  **odmowa niedozwolonej akcji** (rm-rf → refuse), **czysty JSON bez komentarzy**.
- **Oblał — D5B-SEQ-01 (sekwencja wieloetapowa read→write), 1/3 parafraz:**

| Parafraza | Odpowiedź | Pass |
|---|---|---|
| 1 | `[{read a.txt},{write b.txt, content:"{{result}}"}]` — pełny workflow, elegancki placeholder | ✓ |
| 2 | `[{read a.txt}]` — **zatrzymał się na 1. kroku** | ✗ |
| 3 | `[{read a.txt}]` — **tylko odczyt, brak write** | ✗ |

## Wniosek (uczciwie)
1. **Slayer jest solidnym orkiestratorem na poziomie pojedynczego kroku** — poprawnie mapuje intencję
   na narzędzie, trzyma format JSON, egzekwuje zasady (odmowa), nie ulega wstrzyknięciu. To realna,
   praktyczna mocna strona (istotna dla użycia w systemie typu Omp).
2. **Słabość: planowanie wieloetapowej sekwencji.** Przy zadaniu wymagającym łańcucha kroków
   (read→write) Slayer **niestabilnie** podaje pełny workflow — częściej zatrzymuje się na pierwszym
   kroku. To zależne od sformułowania (1/3 parafraz poprawnych).
3. **Spójne z D1:** ta sama oś słabości — **głęboka wieloetapowość**. D1 pokazał to na rozumowaniu
   (extreme 0.83), D5b na orkiestracji. Hipoteza robocza: **Slayer jest mocny w pojedynczych krokach
   (rozumowanie, format, kalibracja), słabszy w utrzymaniu długich, wieloetapowych łańcuchów** —
   niezależnie czy to kroki wnioskowania czy kroki workflow.

## Konsekwencja praktyczna (dla użycia jako orkiestrator)
Jeśli Slayer ma orkiestrować w systemie agentycznym: **bezpieczniej dawać mu jeden krok naraz**
(pętla: zaplanuj następny krok → wykonaj → zaplanuj kolejny) niż prosić o pełny plan wieloetapowy
z góry. Architektura „krok po kroku" gra pod jego mocną stronę i omija słabość sekwencyjną.

## Następne kierunki
- **D5b-hard:** dłuższe workflow (3–5 kroków), warunki (if/else), zależności między krokami — sprawdzić,
  gdzie dokładnie łamie się planowanie sekwencji.
- Weryfikacja hipotezy „mocny krok, słaby łańcuch" na jeszcze jednej osi.

## Powiązania
[[../../benchmarks/d5-wiernosc-instrukcji-v1/README|d5-wiernosc-instrukcji-v1]] · [[../../benchmarks/d5-orkiestracja-v1/README|d5-orkiestracja-v1]] · [[Analiza-D1-Hard-Sufit|analiza D1]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
