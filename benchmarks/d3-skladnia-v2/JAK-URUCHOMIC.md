# Jak sprawdzić swój model na benchmarku d3-składnia-v2

Instrukcja krok po kroku. Benchmark sprawdza, czy model języka polskiego łapie gramatykę: dla każdej pary zdań (jedno poprawne, jedno z jednym błędem) model powinien uznać zdanie poprawne za bardziej prawdopodobne.

## Co jest potrzebne

- Python 3.
- To repozytorium (pobrane przez `git clone`).
- Twój model, który potrafi policzyć prawdopodobieństwo tekstu (to samo, co przy liczeniu BPB / perplexity).

## Krok 1 — pobierz repozytorium

```
git clone https://github.com/slayerlabs/Probierz.git
cd Probierz
```

Pary są w `benchmarks/d3-skladnia-v2/eval.jsonl` (472 pary, z tego **148 w rdzeniu** — pole `headline_core: true`). Każda para ma pole `dobre` (poprawne) i `zle` (z błędem).

## Krok 2 — policz oceny swojego modelu

Dla każdej pary przepuść przez model osobno tekst `dobre` i tekst `zle`. Dla każdego policz **sumę log-prawdopodobieństwa po znakach** (wyżej = bardziej naturalne). To ta sama liczba, którą model daje przy BPB.

Zapisz do pliku `moje_oceny.jsonl` — jedna linia na parę:

```
{"id": "MORFO-case-verb-dat-01", "dobre_ll": -12.34, "zle_ll": -15.67}
```

`id` musi być identyczne jak w `eval.jsonl`. To jedyna praca po Twojej stronie.

## Krok 3 — uruchom program

```
python tools/run_forced_choice.py --eval benchmarks/d3-skladnia-v2/eval.jsonl --scorer logprob --ll-file moje_oceny.jsonl --model twoj-model --outdir wynik/
```

## Krok 4 — odczytaj wynik

Otwórz `wynik/wyniki-twoj-model.json`:

- `accuracy` — procent ze wszystkich par (0.50 = ślepe zgadywanie).
- `accuracy_norm` — skorygowane o różną długość zdań (**właściwa liczba**; bez tej korekty krótsze zdania wygrywałyby za samą długość).
- `accuracy_ci95` — przedział ufności.
- `per_zjawisko` / `per_poziom` — rozbicie na typy błędów i poziomy trudności.

## Krok 5 — wynik na rdzeniu (148 par, które naprawdę różnicują)

Wynik raportowany liczy się na 148 parach oznaczonych `"headline_core": true`:

```
python -c "import json; core={json.loads(l)['id'] for l in open('benchmarks/d3-skladnia-v2/eval.jsonl',encoding='utf-8') if json.loads(l)['headline_core']}; r=[x for x in json.load(open('wynik/wyniki-twoj-model.json',encoding='utf-8'))['results'] if x['id'] in core]; print('wynik na rdzeniu:', round(sum(x['pass_norm'] for x in r)/len(r),3), 'na', len(r), 'parach')"
```

## Jak sprawdzić, że wyniki się zgadzają

- **Powtarzalność:** dwie osoby liczące oceny tego samego modelu powinny dostać ten sam `accuracy_norm`. Jeśli mocno się różnią — różnie liczycie log-prawdopodobieństwo w kroku 2.
- **Porównanie z baseline:** metoda odniesienia jest w repo (`benchmarks/d3-skladnia-v2/wyniki-ngram-o4.json`). Baseline na rdzeniu z definicji zawodzi — jeśli Twój model na rdzeniu bije baseline, to sygnał, że łapie gramatykę.

## Ważne (uczciwie)

- **148 par w rdzeniu przekracza próg ≥85** potrzebny do sensownego porównania A vs B — inaczej niż v1 (7 par). Dla cienkich zjawisk (case-prep-ins = 1 para, case-prep-gen = 2) przedziały per-zjawisko są szerokie; patrz rozbicie `per_zjawisko`.
- v2 jest **publiczny** — model trenowany po jego ujawnieniu może go wchłonąć. Do prawdziwego ślepego testu potrzebna wersja tajna/zahashowana, ujawniana dopiero po pomiarze.
