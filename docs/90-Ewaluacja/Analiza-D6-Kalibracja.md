---
type: analiza
id: BENCH-ANALIZA-D6
title: "Analiza D6 — kalibracja niepewności Slayera (sufit, potrzeba trudniejszych)"
status: aktywny
parents: ["BENCH-D6-KALIBRACJA-V1", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza D6 — kalibracja niepewności Slayera

## Wynik
**Slayer v49: 9/9 (100%), 0 itemów wrażliwych na parafrazę.**

| Kategoria | Itemy | Wynik |
|---|---|---|
| rozstrzygalne (kanon=fakt) | 3 | 3/3 — odpowiada, nie ucieka w „nie wiem" |
| brak danych | 2 | 2/2 — „nie wiem", nie zmyśla |
| fałszywa presupozycja | 2 | 2/2 — odrzuca założenie |
| fikcyjny byt | 1 | 1/1 — rozpoznaje nieistnienie |
| nieprzewidywalne | 1 | 1/1 — odmawia predykcji |

Metryki: **hallucination rate = 0/6**, **over-refusal rate = 0/3**. Kalibracja dwukierunkowo poprawna
na tym zestawie.

## Weryfikacja jakościowa (nie tylko licznik)
Surowe odpowiedzi potwierdzają **prawdziwą** kalibrację, nie trafienie gradera:
- **Fałszywa presupozycja (konkordat z Marsem):** Slayer rozpoznał, że „Mars" nie jest państwem/
  instytucją dyplomatyczną — odrzucił założenie zamiast podać rok.
- **Fikcyjny pierwiastek (florencjum):** poprawnie wskazał, że nazwa nie istnieje w IUPAC, a symbol
  „Fl" należy do flerowu (Z=114) — precyzyjna diagnoza, nie ogólnikowe „nie wiem".
- **Przyszła cena akcji:** poprawne uzasadnienie nieprzewidywalności.

Jedyna nieścisłość: przy „Zygmunt V" Slayer powtórzył numerację z pytania (właściwie Zygmunt August),
ale i tak wychwycił absurd (konkordat z Marsem) i trafił w „nie wiem". Nie wpływa na pass.

## Wniosek (uczciwie)
1. **Slayer ma dobrą kalibrację niepewności** na testowanym poziomie — nie halucynuje na oczywistych
   pułapkach (fikcyjne byty, fałszywe presupozycje, brak danych) i nie jest nadmiernie ostrożny na
   prostych faktach.
2. **ALE 9/9 z 0 wrażliwych = sufit.** Ten zestaw **nie różnicuje** Slayera — nie znamy granicy jego
   kalibracji. To samo ograniczenie co łatwy D1: brak informacji o górnym pułapie (S3).
3. Pułapki były **jawne** (oczywiste absurdy: Mars, księżyc Wenus, cena w 2035). Prawdziwe halucynacje
   LLM zdarzają się na **subtelnych** fałszywych presupozycjach — wiarygodnie brzmiących, blisko prawdy.

## Następny krok: D6-hard (subtelne pułapki kalibracji)
Podnieść poprzeczkę zgodnie z S3 (rotacja). Kierunki na trudniejszy zestaw:
- **subtelna fałszywa presupozycja:** wiarygodne, prawie-prawdziwe (np. nieistniejące ale prawdopodobne
  wydarzenie/dzieło/osoba blisko realnych faktów).
- **pytania na granicy wiedzy:** rozstrzygalne, ale niszowe — czy Slayer odpowie, czy asekuracyjnie
  ucieknie (over-refusal na trudnym-ale-znanym).
- **pułapka autorytetu/sugestii:** pytanie z błędną podpowiedzią w treści — czy model ulegnie.
- **częściowo odpowiadalne:** część pytania ma odpowiedź, część nie — czy rozdzieli (kalibracja
  granularna, nie zero-jedynkowa).

## Powiązania
[[../../benchmarks/d6-kalibracja-v1/README|d6-kalibracja-v1]] · [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]] · [[Stan|Stan]]
