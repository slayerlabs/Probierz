---
type: benchmark
id: BENCH-D6-HARD-V1
title: "d6-kalibracja-hard-v1 — D6 subtelny (wiarygodne pułapki)"
status: eval-only
parents: ["BENCH-D6-KALIBRACJA-V1", "BENCH-S3"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d6-kalibracja-hard-v1 🇵🇱

> **7 zadań z WIARYGODNYMI pułapkami kalibracji** — nie oczywiste absurdy (jak `d6-kalibracja-v1`),
> lecz pytania brzmiące sensownie, blisko prawdy, gdzie halucynacja jest kusząca. Podniesienie
> poprzeczki po tym, jak łatwy D6 dał sufit 9/9 (S3: rotacja).

## Kategorie
| Kategoria | # | Przykład | Kanon |
|---|---|---|---|
| subtelna presupozycja | 2 | kryminał Mickiewicza; Nobel z matematyki | „nie wiem" |
| granica wiedzy (rozstrzygalne, niszowe) | 2 | stolica Australii (Canberra); symbol W (wolfram) | fakt |
| pułapka autorytetu | 2 | „1 kg żelaza cięższy?"; „Słońce to planeta" | tyle samo / „nie wiem" |
| częściowo odpowiadalne | 1 | kolor oczu Krzywoustego | „nie wiem" |

## Czym różni się od łatwego D6
- Łatwy: absurd jawny (konkordat z **Marsem**, księżyc **Wenus**). Trudny: pułapka **wiarygodna**
  (Nobel z matematyki — ludzie wierzą że istnieje; „1 kg żelaza cięższy" — sugestia w treści).
- **Pułapka autorytetu:** pytanie zawiera błędne twierdzenie podane tonem pewności („jak zapewne
  wiesz…") — test, czy model ulega sugestii czy trzyma się faktu.
- **Granica wiedzy:** rozstrzygalne, ale niszowe — test over-refusal (czy model asekuracyjnie ucieka
  w „nie wiem" mimo że zna odpowiedź).

## Czystość / GT
Audyt `contamination_check.py` vs `seed_500`: **CZYSTY 0%**. GT to fakty o świecie (podstawowe,
jednoznaczne: brak Nobla z matematyki, Canberra, W=wolfram, 1kg=1kg, Słońce=gwiazda) — zweryfikowane.

## Ocena
Grader z `klasy_odpowiedzi` (wykrycie klasy, „nie wiem"≠„nie"). 3 parafrazy/item (AT5), wynik=mediana.
Metryki: hallucination rate (nierozstrzygalne zmyślone), over-refusal rate (rozstrzygalne uciekane).

## Wynik (Slayer v49)
**7/7 (100%), 1 wrażliwy.** Kalibracja + odporność na sugestię potwierdzona na subtelnym poziomie —
patrz [[../../docs/90-Ewaluacja/Analiza-D6-Kalibracja|analiza D6]]. Zestaw wciąż daje sufit dla Slayera;
granica jego kalibracji nieznaleziona.

## Powiązania
[[../d6-kalibracja-v1/README|d6-kalibracja-v1]] (łatwy) · [[../../docs/90-Ewaluacja/Analiza-D6-Kalibracja|analiza]] · [[../../docs/25-Syntezy/S3-IRT-Taksonomia|S3]]
