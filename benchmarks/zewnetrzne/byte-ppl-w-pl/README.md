---
type: benchmark-zewnetrzny
id: EXT-BYTE-PPL-W-PL
title: "W — byte-PPL na polskiej Wikipedii (kolumna byte-PPL PL na track.fabryka.ai)"
status: publiczny, poza kontraktem Probierza
date: 2026-10-25
---

# W — byte-PPL PL (zewnętrzny)

> Byte-perplexity modelu na **463 artykułach polskiej Wikipedii** (1 431 141 bajtów tekstu). To ten sam pomiar,
> który [track.fabryka.ai](https://track.fabryka.ai) pokazuje w kolumnie **W / byte-PPL PL** (pole SDK
> `board_pl/byte_ppl`) i który wchodzi do eff-PL. Mniej = lepiej. Normalizacja do bajtów pozwala porównywać
> modele z różnymi tokenizerami.
>
> ⚠️ Tekst jest **publiczny od 2026-10-25** (wcześniej był trzymany jako niepublikowany held-out). Wikipedia jest
> w wielu korpusach — patrz [Kontaminacja](#kontaminacja-co-wiemy) i [`../README.md`](../README.md).

## Dane (pobierane, nie kopiowane)

| plik | źródło (przypięta rewizja) | sha256 |
|---|---|---|
| `w_final.jsonl` (463 linie: `id`, `text`) | [`SlayerLab/fabryka-track-w-pl`](https://huggingface.co/datasets/SlayerLab/fabryka-track-w-pl/tree/b25c13a445ba8639759264654f37295ebe08871c) @`b25c13a4` | `234e7ec2…f33ee90ac7` |

Skąd teksty, reguła wyboru i dekontaminacji (wobec puli treningowej GoLLeM v6): karta zbioru na HF.
Licencja: CC BY-SA 4.0 (Wikipedia; starsze wersje artykułów także CC BY-SA 3.0), autorzy: współtwórcy Wikipedii.
Skrypt pobiera plik bez tokenu HF i przerywa, gdy sha256, liczba artykułów albo liczba bajtów tekstu się nie zgadza.

## Protokół (Glint `compute_perplexity`, 1:1)

Funkcja `compute_perplexity` w skrypcie jest skopiowana bez zmian z harnessu, którym liczona jest tablica.

1. Tekst = `"\n\n".join(text artykułów w kolejności pliku).strip()` → **1 431 141 bajtów** UTF-8.
2. `ids` = `tokenizer.json` (biblioteka `tokenizers`) `.encode(tekst).ids`, tak jak jest (z ewentualnym
   post-processorem tokenizera, bez dokładania BOS/EOS przez skrypt); id ≥ rozmiaru słownika odrzucone.
3. Okna: `chunk = ids[i : i+257]` dla `i = 0, 256, 512, …`; wejście = `chunk[:-1]` (do 256 tokenów),
   cele = `chunk[1:]`. **Kontekst resetowany w każdym oknie**; pierwszy token okna jest ostatnim celem
   poprzedniego (cele się nie powtarzają). **Pierwszy token tekstu nigdy nie jest celem.** Ostatnie okno
   krótsze, bez dopełniania.
4. `token_ppl = exp(Σ CE / liczba celów)`.
5. **`byte_ppl = token_ppl ** (len(ids) / 1 431 141)`** — w wykładniku **wszystkie** tokeny (`len(ids)`),
   a nie liczba celów (o 1 mniejsza). To dwa różne liczniki; pomylenie ich zmienia wynik.
6. BPB, jeśli ktoś go podaje, to `log2(byte_ppl)`, nie inna nazwa tej samej liczby.

## Jak uruchomić

```
pip install torch transformers tokenizers huggingface_hub
python benchmarks/zewnetrzne/byte-ppl-w-pl/byte_ppl_w_pl.py --model <repo-HF> --revision <pelny-sha> --out wynik.json
python benchmarks/zewnetrzne/byte-ppl-w-pl/byte_ppl_w_pl.py --model C:/sciezka/do/modelu --out wynik.json
```

- `--model` — repo HF albo lokalny katalog w formacie HF (`AutoModelForCausalLM`, `*.safetensors`, `tokenizer.json`).
- Z Hub pobierane są tylko `*.json`, `*.safetensors`, `*.txt`, `*.model`; kod autora modelu wyłącznie z
  `--trust-remote-code` (używaj tylko dla kodu, który przejrzałeś).
- `--gollem-v6 <repo>` — modele GoLLeM v6 nie są zarejestrowane w `AutoModel`; skrypt używa wtedy loadera
  `load_gollem_v6` z repo modelu (opis w karcie modelu). Tym trybem liczona jest kalibracja.
- Wynik: `token_ppl`, `byte_ppl`, liczba tokenów i bajtów, sha danych.

## Kalibracja (sprawdź zgodność, zanim porównasz liczby)

`SlayerLab/GoLLeM-v6-250M` @`77d75a2b48eaab7aec59816f9849cee75a7bdfc1`, float32
(wynik tego skryptu na CPU: [`wyniki-gollem-v6-250m.json`](wyniki-gollem-v6-250m.json)):

```
python benchmarks/zewnetrzne/byte-ppl-w-pl/byte_ppl_w_pl.py --gollem-v6 SlayerLab/GoLLeM-v6-250M \
       --revision 77d75a2b48eaab7aec59816f9849cee75a7bdfc1 --out kalibracja.json
```

| | ten skrypt (CPU) | nasz pomiar referencyjny (GPU) |
|---|---|---|
| tokeny (`len(ids)`) | 350 087 | 350 087 |
| token_ppl | 15.587384 | 15.587507 |
| **byte_ppl** | **1.957840** | **1.957844** (tablica i karta modelu: 1.9578) |

Zgodność: |Δ byte_ppl| ≤ 0,001. Różnica CPU / GPU (4·10⁻⁶) to zaokrąglenia float32. Wynik GPU wyszedł identycznie
z dwóch niezależnych implementacji (ta funkcja i osobna pętla wsadowa na tych samych oknach; różnica względna 1,7·10⁻⁹).
Na CPU model 250M liczy się ok. 5 min.

## Kontaminacja (co wiemy)

W był wybrany i oczyszczony wobec puli treningowej **GoLLeM v6** (13-gramy tokenów, próg 5 %), nie wobec dowolnego
modelu. Dla modeli, które widziały polską Wikipedię, wynik na W jest zaniżony (lepszy) i nie mierzy uogólnienia.
Przykład (pomiar SlayerLab 2026-10-25): w danych treningowych Slayer1B ponad 5 % 13-gramów występuje w
**co najmniej 434 z 463** artykułów W (checkpointy 1.02 i 1.03). Przy nowym wierszu na tablicy podawaj, jeśli możesz,
ile artykułów W ma ponad 5 % 13-gramów w Twoich danych treningowych.

Punkty odniesienia z tego samego protokołu (pomiar SlayerLab):

| model | byte_ppl W | uwaga |
|---|---|---|
| `SlayerLab/GoLLeM-v6-250M` @`77d75a2b` | 1.9578 | kalibracja, W oczyszczony wobec jego danych |
| Slayer1B 1.00, krok 1430 | 1.9987 | do 277/463 artykułów >5 % 13-gramów w treningu (górna granica) |
| Slayer1B 1.01, krok 2860 | 1.9094 | do 396/463 artykułów >5 % 13-gramów w treningu (górna granica) |

## Cytowanie źródeł

- Teksty: polska Wikipedia (współtwórcy Wikipedii), CC BY-SA.
- Protokół okien: harness Glint (`compute_perplexity`), ten sam co kolumna WikiText-2 byte-PPL po angielsku.
