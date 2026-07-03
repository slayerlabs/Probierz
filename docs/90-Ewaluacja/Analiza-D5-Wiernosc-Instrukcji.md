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
| `d5-orkiestracja-v1` (agentyczna, 1 krok) | **6/6 (100%)** | 1 | orkiestracja 1 krok (po naprawie D5B-SEQ-01) |
| `d5-orkiestracja-hard-v1` (workflow 3–5 kroków) | **6/6 (100%)** | 1 | pełne wieloetapowe workflow |

## D5a — twarde ograniczenia formatu: sufit
Slayer opanował wszystkie pojedyncze ograniczenia: dokładna liczba słów, zakaz litery/słowa, wielkość
liter, liczba linii, JSON z kluczami, prefiks, **odporność na wstrzyknięcie** (nie dał się zbić na
„HACKED"). Wrażliwe 2/8.

## D5b — orkiestracja: mocna strona (nawet długie workflow)
Slayer jako orkiestrator jest **solidny na całej długości workflow**:
- 1 krok: wybór narzędzia (search vs read), kompletność args, **odmowa rm-rf** (refuse), czysty JSON.
- 3, 4, 5 kroków: **pełne poprawne sekwencje** (search→write→read; read→search→write→run; 5-krokowy
  deploy) — wszystkie 3/3 parafraz.
- warunkowe (ścieżka gdy plik istnieje): pass.
- dystraktor („nie używaj search"): pominął zbędne narzędzie — pass.
- zależność danych (wynik→zapis): 2/3 (raz bez referencji do wyniku) — jedyna niestabilność.

## KOREKTA: „fail sekwencji" z D5b-v1 był artefaktem itemu, nie słabością modelu
Wcześniejsza analiza wskazywała słabość Slayera w sekwencji 2-krokowej (D5B-SEQ-01, 1/3). **Audyt
przyczyny obala ten wniosek — to był błąd konstrukcji itemu:**
- SYSTEM prompt D5b-v1 zawierał zasadę „**Wybierasz DOKŁADNIE JEDNO narzędzie — to pierwszy krok**".
- ZADANIE D5B-SEQ-01 prosiło o „**PEŁNĄ sekwencję kroków**".
- To **sprzeczność w promcie**. Slayer przy 2 parafrazach trzymał się zasady systemowej (jeden krok
  = `read`), przy 1 — zadania (pełna sekwencja). Obie reakcje są racjonalne wobec sprzecznej instrukcji.
- Gdy instrukcje są **spójne** (D5b-hard: SYSTEM „podaj PEŁNY plan"), Slayer planuje 3–5 kroków bezbłędnie.

**Wniosek metodologiczny:** to znalezisko o **nas**, nie o modelu — item z wewnętrznie sprzecznym
promptem nie mierzy zdolności, tylko którą sprzeczną instrukcję model wybierze. D5B-SEQ-01 oznaczony
jako wadliwy (patrz niżej); wynik nie liczy się jako słabość Slayera.

## Zrewidowany wniosek o Slayerze (uczciwie)
1. **Wierność instrukcji to mocna strona Slayera** — zarówno twarde ograniczenia formatu (8/8), jak i
   orkiestracja wieloetapowa (workflow 3–5 kroków, warunki, dystraktor, odmowa). Praktycznie: **nadaje
   się na orkiestratora** w systemie agentycznym, również do planów wieloetapowych z góry.
2. **Hipoteza „mocny krok, słaby łańcuch" — ODRZUCONA dla orkiestracji.** Slayer planuje pełne
   sekwencje. (Dla D1-rozumowania słabość głębi pozostaje — ale to inna oś: głębia wnioskowania ≠
   długość planu narzędziowego.)
3. Jedyna realna niestabilność: **zależność danych między krokami** (referencja wyniku kroku N w kroku
   M) — 2/3. Wart osobnego, celowanego testu.

## Działania naprawcze
- **D5B-SEQ-01:** wadliwy (sprzeczny prompt) — do usunięcia lub naprawy (usunąć zasadę „jedno
  narzędzie" z SYSTEM albo przeformułować zadanie na 1 krok). Wynik z niego wykluczony z wniosków.
- **Lekcja ogólna:** przy itemach orkiestracji SYSTEM i ZADANIE muszą być spójne co do „jeden krok vs
  pełny plan". Dodać do reguł konstrukcji zestawów.

## Następne kierunki
- **Zależność danych** — celowany zestaw (przepływ wyniku między krokami, wiele referencji) — jedyna
  wykryta niestabilność orkiestracyjna.
- D1 pozostaje osią, gdzie Slayer realnie się łamie (głęboka wieloetapowość wnioskowania).

## Powiązania
[[../../benchmarks/d5-wiernosc-instrukcji-v1/README|d5-wiernosc-instrukcji-v1]] · [[../../benchmarks/d5-orkiestracja-v1/README|d5-orkiestracja-v1]] · [[../../benchmarks/d5-orkiestracja-hard-v1/README|d5-orkiestracja-hard-v1]] · [[Analiza-D1-Hard-Sufit|analiza D1]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]]
