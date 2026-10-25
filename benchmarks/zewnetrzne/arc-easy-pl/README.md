---
type: benchmark-zewnetrzny
id: EXT-ARC-EASY-PL
title: "ARC-Easy-PL — polskie tłumaczenia testu ARC-Easy (zestaw zewnętrzny)"
status: publiczny, poza kontraktem Probierza
date: 2026-10-24
---

# ARC-Easy-PL (zewnętrzny)

> Polskie tłumaczenie testu **ARC-Easy** (AI2 Reasoning Challenge, pytania wyboru z wiedzy szkolnej):
> **2376 pytań**, 3–5 odpowiedzi, zgadywanie ≈ 25 %. To ten sam pomiar, który SlayerLab podaje jako
> **oś K (eff-PL)** w kartach modeli GoLLeM. Na leaderboardzie track.fabryka.ai jest to kolumna
> **ARC-Easy-PL** we wpisach właścicieli modeli (`board_pl/arc_easy`). Natywna automatyczna
> ewaluacja PL serwera liczy obecnie MultiBLiMP; angielski `allenai/ai2_arc` to osobna oś EN.
> [Jedna mapa danych, skryptów i protokołów leaderboardu](https://github.com/slayerlabs/fabryka-track/blob/main/docs/leaderboard-benchmarks.md).
>
> ⚠️ Zestaw publiczny, **kontaminacja niekontrolowana** — patrz [`../README.md`](../README.md).

## Dane (pobierane, nie kopiowane)

| zestaw | rola | źródło (przypięta rewizja) | sha256 pliku |
|---|---|---|---|
| **EU20** | główny | [`Eurolingua/arcx`](https://huggingface.co/datasets/Eurolingua/arcx/blob/f2e35fbebdb572a9653eda706b00083b0892ed43/arc_easy_PL_test.jsonl) `arc_easy_PL_test.jsonl` @`f2e35fbe` | `c6732eeb…6706186` |
| **ddudek** | kontrolny | [`ddudek/ai2_arc_translated_pol`](https://huggingface.co/datasets/ddudek/ai2_arc_translated_pol/tree/e61110df4097ca5f5284a62e60d01d8f80d15069/ARC-Easy) `ARC-Easy/test-00000-of-00001.parquet` @`e61110df` | `f4f30341…bdb934` |

Oba to niezależne tłumaczenia tego samego splitu **test** ARC-Easy, po **2376 pytań** (te same `id` i `answerKey` co
`allenai/ai2_arc` ARC-Easy test @`210d026f`). Licencja obu: **CC BY-SA 4.0** (jak oryginał ARC).
Skrypt pobiera pliki z tych rewizji bez tokenu HF i przerywa, gdy sha256 lub liczba pytań się nie zgadza.

**Który zestaw jest „nasz”:** oś K w kartach GoLLeM (eff-PL) to **EU20**. ddudek liczymy obok jako kontrolę
(różnica EU20 − ddudek mówi, ile wyniku zależy od tłumaczenia). Skrypt domyślnie liczy oba.

Pola rekordu (identyczne w obu): `question` (tekst), `choices.text` (lista odpowiedzi), `choices.label`
(etykiety — zwykle `A`–`D`, w części pytań `1`–`4`, jak w oryginale), `answerKey` (etykieta poprawnej).
Trafienie = etykieta wybranej odpowiedzi równa `answerKey`; etykiet nie mapujemy ani nie przepisujemy.

## Protokół (Glint `evaluate_arc_easy`, 1:1)

Dla każdej odpowiedzi `a` z `choices.text` liczymy dwa teksty, **dosłownie** (bez żadnego prefiksu typu
„Pytanie:/Odpowiedź:”, bez przykładów, bez nowej linii; jedyny łącznik to jedna spacja doklejona przed odpowiedzią):

```
pelny  = question + " " + a
pytanie = question
wynik(a) = LL(pelny) − LL(pytanie)
```

- `LL(t)` = suma log-prawdopodobieństw tokenów `t` od drugiego tokenu (teacher forcing); oba teksty tokenizowane
  **osobno i w całości**, więc na granicy pytanie / odpowiedź liczy się tokenizacja całego `pelny`;
- wybór = argmax `wynik(a)`, **bez normalizacji długości** (ani znakami, ani bajtami, ani tokenami);
  przy remisie wygrywa pierwsza odpowiedź; miara = trafność (%) na 2376 pytaniach;
- tokenizacja: `tokenizer.json` modelu (biblioteka `tokenizers`), `.encode(tekst).ids` tak jak jest.
  **Sami nie doklejamy BOS/EOS** — pojawią się tylko, jeśli dodaje je post-processor tokenizera modelu;
  id spoza słownika odrzucone, przycięcie do 256 tokenów.

Reguła punktacji odpowiada `acc` (nie `acc_norm`) z lm-evaluation-harness, ale **szablon jest inny**:
lm-eval `arc_easy` używa `Question: {q}\nAnswer: {a}`, my samego `{q} {a}`. Liczby z lm-eval (ani `acc`,
ani `acc_norm`) nie są więc wprost porównywalne z tymi. Jeśli Twoje ustawienie daje na modelu
kalibracyjnym (niżej) te same liczby, liczymy tak samo.

## Jak uruchomić

```
pip install torch transformers tokenizers huggingface_hub pyarrow
python benchmarks/zewnetrzne/arc-easy-pl/arc_easy_pl.py --model <repo-HF> --revision <pelny-sha> --out wynik.json
python benchmarks/zewnetrzne/arc-easy-pl/arc_easy_pl.py --model C:/sciezka/do/modelu --out wynik.json
```

- `--model` — repo HF albo lokalny katalog w formacie HF (`config.json`, `*.safetensors`, `tokenizer.json`).
- Z Hub pobierane są tylko `*.json`, `*.safetensors`, `*.txt`, `*.model`; kod autora modelu wyłącznie z
  `--trust-remote-code` (używaj tylko dla kodu, który przejrzałeś).
- `--zestawy EU20` liczy sam zestaw główny (połowa czasu).
- Wynik: `acc` na każdy zestaw + `items` (0/1 na `id`, bez treści pytań). Na CPU model 42M liczy jeden
  zestaw ok. 5 min.

## Kalibracja (sprawdź zgodność, zanim porównasz liczby)

`SlayerLab/GoLLeM-45M-PL` @`1b1791fcd67727920db39bcf1e7022ce7a209e12`, CPU, float32
(wynik: [`wyniki-gollem-45m-pl.json`](wyniki-gollem-45m-pl.json)):

| zestaw | ten skrypt | nasz pomiar referencyjny (GPU) |
|---|---|---|
| EU20 | **31.61** (751 / 2376) | 31.57 (750 / 2376) |
| ddudek | **31.73** (754 / 2376) | 31.73 (754 / 2376) |

Jedyna różnica to pytanie `NYSEDREGENTS_2015_8_24`: w EU20 odpowiedzi C i D mają **identyczny tekst**
(„Ziemi jednokrotny obrót”), więc wyniki są równe i o trafieniu decyduje rozstrzygnięcie remisu; na GPU
różnice zaokrągleń w ostatnim bicie mogą je odwrócić. Takich pytań z powtórzoną odpowiedzią jest
**6 w EU20** (w 3 powtórzona jest poprawna) i **1 w ddudek**, więc same te pytania mogą zmienić wynik
o ok. 0,25 pp (6 / 2376). To nie jest ogólna granica różnic CPU / GPU: inne pytania z bliskimi wynikami
też mogą się odwrócić; w naszej kalibracji odwróciło się tylko to jedno.

Punkty odniesienia z tego samego protokołu (pomiar SlayerLab, 2026-09, GPU):

| model (rewizja) | EU20 | ddudek |
|---|---|---|
| `radlab/polish-gpt2-small` @`2cc7cf9f` | 47.31 | 46.80 |
| `SlayerLab/GoLLeM-45M-PL` @`1b1791fc` | 31.57 | 31.73 |
| `Maggio33/GoLLeM-110M-PL` @`8749fd4a` | 30.89 | 32.28 |

Błąd standardowy przy zgadywaniu: √(0,25·0,75/2376) ≈ 0,89 pp.

## Kontaminacja (co wiemy)

To publiczny tekst z internetu — każdy korpus webowy może go zawierać. W korpusie treningowym
GoLLeM v4 znaleźliśmy **14 pytań** testu EU20; w karcie GoLLeM v6 podajemy dlatego obok pełnego wyniku
wariant „PL clean” na 2362 pytaniach. Pełny wynik z tego skryptu to zawsze 2376 pytań.

## Cytowanie źródeł

- Thellmann i in., *Towards Cross-Lingual LLM Evaluation for European Languages*, 2024,
  [arXiv:2410.08928](https://arxiv.org/abs/2410.08928) — zestaw `Eurolingua/arcx`.
- Clark i in., *Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge*, 2018,
  [arXiv:1803.05457](https://arxiv.org/abs/1803.05457) — oryginalny ARC.
- `ddudek/ai2_arc_translated_pol` — tłumaczenie ARC na polski (Hugging Face, CC BY-SA 4.0).
