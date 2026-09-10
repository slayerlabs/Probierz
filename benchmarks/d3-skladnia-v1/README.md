---
type: benchmark
id: BENCH-D3-SKLADNIA-V1
title: "d3-skladnia-v1 — wymiar D3: składnia / morfoskładnia (pary minimalne)"
status: eval-only
parents: ["BENCH-T4", "BENCH-S4", "BENCH-S5"]
author: Arkadiusz Słota
date: 2026-09-10
---

# d3-skladnia-v1 🇵🇱

> **30 par minimalnych** polskiej morfoskładni z gradientem trudności (poziomy 1–4). Mierzy wymiar
> **D3** konstruktu (patrz [[../../docs/10-Tezy/T4-Dekompozycja-Wymiarow|T4]]): czy model chwyta
> **reguły morfoskładni** (rząd przypadka, zgodę, rodzaj, aspekt), nie powierzchnię leksykalną.
> Wypełnia lukę taksonomii: D3 istnieje w konstrukcie (C2/T4), ale nie miał jeszcze benchmarku
> (są d1/d2/d5/d6). Uzupełnia MultiBLiMP-PL, który pokrywa **tylko** zgodę podmiot–orzeczenie.

> ⚠️ **v1 jest PUBLICZNY = demonstrator/template.** Leży w repo, więc modele trenowane później mogą go
> wchłonąć (AT1: benchmark spala się po ujawnieniu). Traktuj jak **wzór formatu + dowód metody**, NIE
> jak sekretny zestaw do ślepej wymiany — te trzymaj zahashowane przed reveal (`protokol/S1-Commitment-Protokol`).

## Modalność: para minimalna (forced-choice), nie prompt

W przeciwieństwie do d1/d2 (prompt → klasa), D3 to **wybór wymuszony** między dwoma prawie
identycznymi zdaniami: jedno **gramatyczne** (`dobre`), jedno z **jednym błędem** morfoskładni
(`zle`). To celowe — działa dla modeli **bazowych i małych** (w tym byte-level), które nie muszą
umieć wykonywać instrukcji:

- **Wynik itemu:** model przypisuje log-prawdopodobieństwo obu członom; **pass** iff
  `LL(dobre) > LL(zle)` (margines dodatni). **Chance = 0.50.**
- **Wynik zbioru:** accuracy (średnia pass) + per-zjawisko i per-poziom; przy nierównych długościach
  raportuj też margines znormalizowany bajtowo (`LL/len_bajtów`), by odjąć confound długości.
- **Metryka panelowa (S5):** theta IRT per-wymiar zamiast surowego pass-rate (panel ≥5 modeli,
  bootstrap CI) — item najinformatywniejszy przy `theta ≈ b_j`.

## Kontaminacja — semantyka par minimalnych (uwaga admisyjna)

Standardowy `tools/contamination_check.py` (overlap n-gram itemu z treningiem) **nie stosuje się
wprost** do par minimalnych: człon **`dobre`** to poprawna polszczyzna i Z ZAŁOŻENIA występuje w
korpusie (np. `bez wody`) — to nie przeciek, to sedno testu. Właściwy warunek czystości D3:

- człon **`zle`** (niegramatyczny) **nie może** występować w treningu (z konstrukcji nie występuje —
  to forma agramatyczna), oraz
- audyt mierzy overlap **treści par**, nie **szablonu generacji** (Morfeusz/UD) — inaczej fałszywy 0%
  albo fałszywy alarm.

**Admisja D3 do kontraktu Probierza (T1/T2) jest OTWARTA:** pełny audyt prowenancji na
zdekontaminowanym held-oucie + pieczęć wg poprawionej semantyki należą do seamu pomiaru/prowenancji
(nie do tego pliku). Do czasu pieczęci: `status: eval-only`, demonstrator.

## Zakres wymiaru (S4)

D3 obciąża **morfoskładnię**; rozumowanie i znaczenie są **trywialne** (reguła dominującego
obciążenia). Zjawiska pokryte (ortogonalne do zgody podmiot–orzeczenie z MultiBLiMP-PL):

- **Rząd przypadka** (`case-*`): przyimek/czasownik/negacja/liczebnik wymusza przypadek dopełnienia
  (7 przypadków). `dobre` = poprawny przypadek, `zle` = ta sama lema, zły przypadek.
- **Zgoda przymiotnik–rzeczownik** (`agr-adj-*`): rodzaj × liczba × przypadek.
- **Rodzaj w czasie przeszłym** (`past-*`): polski czasownik znaczy rodzaj w formie „l-”; w tym
  **klityka pro-dropowana ↔ orzecznik** (`byłem` vs `byłam` bez rzeczownika-kontrolera) — poza
  zasięgiem benchmarku podmiot–orzeczenie.
- **Aspekt** (`aspekt-*`): `będę`+bezokolicznik wymaga niedokonanego; adverbialia durative/bounded.

## Gradient trudności (S3/T3)

Poziom 1 (rząd/zgoda „podręcznikowa”) → poziom 4 (przypadek w PP, klityka↔orzecznik, aspekt–adverbial).
Poziom to hipoteza; kalibracja empiryczna (`b_j`) po przejeździe panelu 8m/16m/32m/64m/128m (S5).

## Okno bajtowe

Każda para ≤ **32 bajty** UTF-8 (polskie diakrytyki = 2 bajty), krytyczny kontrast w pierwszych
~24 bajtach → działa dla byte-modeli z krótkim oknem bez ucinania kontrastu. Pola `bajty_dobre`,
`bajty_zle` w `eval.jsonl`.

## Skalowanie do tysięcy par

Seed 30 par to demonstrator. Generacja produkcyjna: **Morfeusz 2** (licencja BSD-2, komercyjnie OK,
Kieraś & Woliński 2017) — generator form + szablony ręczne (ścieżka BSD-clean, redystrybuowalna);
**UD Polish-PDB** (CC BY-NC-SA) tylko do minowania szablonów/tagów, bez wysyłania tokenów PDB.
Balans po przypadkach/rodzajach/kierunku aspektu; distractor = edycja jednej cechy (para minimalna,
nie podwójne naruszenie).

## Format `eval.jsonl`

```json
{"id":"MORFO-case-prep-gen-01","wymiar":"D3","poziom_trudnosci":1,"zjawisko":"case-prep-gen","dobre":"bez wody","zle":"bez woda","bajty_dobre":8,"bajty_zle":8,"gate":"NOVELTY_FAIL","contamination_hits":1,"zle_novel":false,"valid_pair":true,"headline_eligible":false}
```

## Flagi admisyjne (gejtowanie) — pola per-item w `eval.jsonl`

Każdy item niesie wynik audytu admisyjnego (źródło: `_heldout/d3_gates.json` + `_heldout/d3_zle_novel.json`, audyt vs `slayer-pl-8x3b` 11.29M docs). Pola:

- `gate` — `ADMIT` | `NOVELTY_FAIL` | `VALIDITY_REVIEW`. `ADMIT` = para ważna i błędna forma nieobecna w treningu. `NOVELTY_FAIL` = błędna forma jednak występuje w treningu (1..10 trafień, szum kierunkowy). `VALIDITY_REVIEW` = >10 trafień, prawdopodobnie gramatyczna w innym czytaniu.
- `contamination_hits` — liczba wystąpień formy `zle` w korpusie treningowym (0 = czysta).
- `zle_novel` — `true` gdy forma `zle` jest NIEobecna w treningu (warunek czystości par minimalnych; `false` = skażona).
- `valid_pair` — `false` tylko dla par udowodnionych jako wadliwe (nie są parą minimalną). Obecnie: `MORFO-case-prep-loc-01` (`w lesie` vs `w las`) — `w las` jest gramatyczne (biernik ruchu), więc oba człony poprawne. Pole `valid_pair_note` podaje powód.
- `headline_eligible` — `true` iff `gate == ADMIT` **oraz** `valid_pair`. To zbiór, na którym liczy się wynik raportowany.

### Zbiór headline (jak liczyć wynik)

- Liczby: `ADMIT` = 23, `NOVELTY_FAIL` = 5, `VALIDITY_REVIEW` = 2; `headline_eligible` = **23**; `valid_pair=false` = 1; skażonych (`zle_novel=false`) = 7.
- **Wynik raportowany (headline) = accuracy na `headline_eligible` (23 par), NIE na wszystkich 30.**
- Naiwne accuracy na surowych 30 par (`acc_all`) jest **nieważne**: zawiera parę wadliwą i skażone. Runner z trybem `--admission` filtruje po `headline_eligible`.
- Rdzeń dyskryminujący (podzbiór `headline_eligible`, na którym metoda odniesienia wypada najsłabiej — rodzina `case-*`) to miejsce, gdzie mierzy się przewaga modelu docelowego (margines nad baseline).
