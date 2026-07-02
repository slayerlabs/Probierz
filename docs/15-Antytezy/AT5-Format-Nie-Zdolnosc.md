---
type: antyteza
id: BENCH-AT5
title: "Benchmark mierzy format i artefakt promptu, nie zdolność"
status: w-dyskusji
parents: ["BENCH-C2", "BENCH-T5"]
author: Arkadiusz Słota
date: 2026-07-02
---

# AT5 — Pomiar wrażliwości na format zamiast kompetencji (steelman)

## Najmocniejsza wersja
Pass/fail z rubryki (T5) formalnie przypomina pomiar zdolności, lecz może rejestrować **wrażliwość na
powierzchnię promptu** — zmienną odrębną od kompetencji językowej:

1. **Wrażliwość na sformułowanie promptu.** Ta sama zdolność daje pass albo fail zależnie od
   sformułowania polecenia, kolejności przykładów, obecności instrukcji „rozwiąż krokowo", nagłówków,
   języka polecenia. Pomiar rejestruje reakcję modelu na konwencję promptowania autora, nie jego
   zdolność. Inny zespół z inną konwencją uzyska inny ranking; brak niezmienniczości oznacza brak
   pomiaru konstruktu.
2. **Parsowanie jako ukryty warunek zaliczenia.** Rubryka weryfikuje wyjście automatycznie, co wymusza
   format (JSON, „Odpowiedź: X", bloki kodu). Model kompetentny, lecz rozwlekły, uzyska fail na etapie
   parsowania; model niekompetentny, lecz zgodny formalnie, uzyska pass. Pomiar rejestruje wówczas
   formatowanie, nie treść — łączy D5 (wierność instrukcji) z pozostałymi wymiarami.
3. **Skróty i artefakty datasetu.** Modele wykorzystują regularności statystyczne: pozycję poprawnej
   odpowiedzi, jej długość, słowa-klucze w dystraktorach, styl poprawnej odpowiedzi. Wysoki wynik może
   wynikać z eksploatacji regularności zestawu, nie z rozumienia.
4. **Bias grader-a LLM.** Jeśli grader-em jest LLM, preferuje odpowiedzi we własnym stylu i jest
   podatny na iniekcję instrukcji. Wysoka zgodność między-graderami może wynikać ze **wspólnego biasu
   dwóch graderów tej samej rodziny**, nie z trafności rubryki.

## Konsekwencja, jeśli prawdziwa
Wyniki Probierza są **nieidentyfikowalne**: nie da się rozdzielić, jaka część pass-rate to zdolność, a
jaka to zgodność z formatem lub artefaktem. Ranking modeli odpowiada wtedy na pytanie „który model
lepiej pasuje do przyjętej konwencji", nie „który model językowy jest lepszy". Podważa to
interpretowalność wyniku (cel C2).

## Czego wymaga, by ją odeprzeć (środki zaradcze do wpisania w S4/S5)
- **Test niezmienniczości promptu:** każdy item w ≥3 parafrazach polecenia; zdolność liczona jako
  statystyka odporna na parafrazę (np. mediana), a **wariancja po parafrazie raportowana osobno jako
  wskaźnik wrażliwości** (sygnał dla D5, nie szum).
- **Rozdział formatu od treści:** tolerancyjne parsowanie plus osobny wymiar „wierność formatu" (D5),
  aby błąd formatu nie był klasyfikowany jako błąd rozumowania (D1). Fail z powodu formatu →
  taksonomia `format`, nie `błędny-plan`.
- **Kontrola skrótów:** itemy z permutacją kolejności odpowiedzi i wariantami dystraktorów; jeśli
  wynik zależy od permutacji, item mierzy skrót i podlega odrzuceniu (spójne z panelem kalibracyjnym S3).
- **Grader trust-minimized:** ≥2 graderów **różnego pochodzenia** (człowiek + LLM lub dwie różne
  rodziny modeli); rozbieżność kieruje item do ręcznego audytu. Wykluczony pojedynczy grader LLM tej
  samej rodziny co model oceniany (spójne ze ślepym audytem, M4).

## Powiązania
parent: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · kontra dla: [[../10-Tezy/T5-Falsyfikowalna-Rubryka|T5]] · rozstrzyga: [[../25-Syntezy/S4-Taksonomia-Wymiarow|S4]] · pomiar: [[../25-Syntezy/S5-MIRT-Panel|S5]]
