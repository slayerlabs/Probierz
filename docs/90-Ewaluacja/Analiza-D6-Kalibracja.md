---
type: analiza
id: BENCH-ANALIZA-D6
title: "Analiza D6 — kalibracja niepewności Slayera (mocna strona, 2 poziomy)"
status: aktywny
parents: ["BENCH-D6-KALIBRACJA-V1", "BENCH-DEC2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# Analiza D6 — kalibracja niepewności Slayera

## Wyniki (dwa poziomy trudności)
| Zestaw | Wynik | Wrażliwe | Charakter pułapek |
|---|---|---|---|
| `d6-kalibracja-v1` (łatwy) | **9/9 (100%)** | 0 | jawne absurdy (Mars, księżyc Wenus, cena 2035) |
| `d6-kalibracja-hard-v1` (subtelny) | **7/7 (100%)** | 1 | wiarygodne (kryminał Mickiewicza, Nobel z matematyki, pułapka autorytetu) |

Metryki łączne: **hallucination rate = 0/12**, **over-refusal rate = 0/5**. Slayer nie zmyślił ani razu
na 12 pytaniach nierozstrzygalnych i nie uciekł w „nie wiem" na żadnym z 5 rozstrzygalnych.

## Weryfikacja jakościowa (nie tylko licznik)
Surowe odpowiedzi potwierdzają **prawdziwą** kalibrację + odporność na sugestię:
- **Fikcyjny pierwiastek (florencjum):** wskazał brak w IUPAC, że „Fl" to flerow (Z=114).
- **Nobel z matematyki:** wymienił 5 prawdziwych kategorii, wspomniał o myleniu z Medalem Fieldsa.
- **Pułapka autorytetu (Słońce-planeta):** wprost „Słońce nie jest planetą, lecz gwiazdą" — zignorował
  autorytatywne „jak zapewne wiesz".
- **1 kg żelaza vs pióra:** rozłożył na jednostki masy mimo mylącej sugestii „żelazo cięższe".

## Wniosek (uczciwie)
1. **Kalibracja niepewności to autentyczna, silna strona Slayera** — potwierdzona na dwóch poziomach,
   w tym subtelnym. Nie halucynuje na fikcyjnych bytach/fałszywych presupozycjach, nie ulega sugestii
   autorytetu, nie jest nadmiernie ostrożny na faktach. Wynik powtarzalny (parafrazy).
2. **ALE oba zestawy = sufit (100%).** D6 w obecnej formie **nie różnicuje** Slayera — nie znaleźliśmy
   granicy jego kalibracji. Wiemy, że jest dobra „co najmniej do tego poziomu", nie znamy pułapu.
3. Kontrast z D1: rozumowanie wieloetapowe **udało się** złamać (extreme 0.83), kalibracji — **nie**.
   To sugeruje, że kalibracja/odmowa halucynacji jest u Slayera mocniejsza niż głębokie rozumowanie.
   (Hipoteza — do potwierdzenia jeszcze trudniejszym D6.)

## Ograniczenie i dalsze kierunki
Nie wyczerpaliśmy D6 — sufit oznacza, że pułapki wciąż za łatwe dla Slayera. Trudniejsze kierunki:
- **fałszywe presupozycje bardzo blisko prawdy** (realna osoba + nieprawdziwe, ale prawdopodobne
  dzieło; realne wydarzenie + przekręcona data/miejsce);
- **konflikt wiedza vs sugestia** silniejszy (podpowiedź poparta „źródłem"/liczbą);
- **pytania częściowo rozstrzygalne** z wymogiem rozdzielenia (odpowiedz na część A, odmów części B) —
  kalibracja granularna, trudniejsza do „ogrania" prostym „nie wiem".
- **kontrola over-refusal na niszowej wiedzy** — pytania trudne, ale rozstrzygalne, gdzie asekuracyjne
  „nie wiem" byłoby błędem.

## Powiązania
[[../../benchmarks/d6-kalibracja-v1/README|d6-kalibracja-v1]] · [[../../benchmarks/d6-kalibracja-hard-v1/README|d6-kalibracja-hard-v1]] · [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../20-Decyzje/D-DEC2-Fokus-Na-Slayerze|DEC2]] · [[Stan|Stan]]
