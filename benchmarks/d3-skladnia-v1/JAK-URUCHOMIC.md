# Jak sprawdzić swój model na benchmarku d3-składnia

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

Pary testowe są w pliku `benchmarks/d3-skladnia-v1/eval.jsonl` (30 par). Każda para ma pole `dobre` (zdanie poprawne) i `zle` (zdanie z błędem).

## Krok 2 — policz oceny swojego modelu

Dla każdej z 30 par przepuść przez model osobno tekst z pola `dobre` i tekst z pola `zle`. Dla każdego policz **sumę log-prawdopodobieństwa po znakach** (wyżej = model uważa tekst za bardziej naturalny). To ta sama liczba, którą model daje przy liczeniu BPB.

Zapisz wynik do pliku `moje_oceny.jsonl` — jedna linia na parę, dokładnie w takim formacie:

```
{"id": "MORFO-case-prep-gen-01", "dobre_ll": -12.34, "zle_ll": -15.67}
```

Plik ma mieć 30 linii, a `id` musi być identyczne jak w `eval.jsonl`. To jedyna praca po Twojej stronie — reszta jest gotowa w repo.

## Krok 3 — uruchom program

```
python tools/run_forced_choice.py --eval benchmarks/d3-skladnia-v1/eval.jsonl --scorer logprob --ll-file moje_oceny.jsonl --model twoj-model --outdir wynik/
```

`--ll-file` to Twój plik z kroku 2. Program porówna oceny i zapisze wynik do folderu `wynik/`.

## Krok 4 — odczytaj wynik

Otwórz `wynik/wyniki-twoj-model.json`. Najważniejsze pola:

- `accuracy` — ile procent z 30 par model zrobił dobrze. **0.50 = ślepe zgadywanie.**
- `accuracy_norm` — to samo, ale uczciwie skorygowane o różną długość zdań (to jest właściwa liczba, bo bez tej korekty krótsze zdania wygrywałyby za samą długość, nie za gramatykę).
- `accuracy_ci95` — przedział ufności (zakres niepewności wyniku).
- `per_zjawisko` / `per_poziom` — rozbicie na typy błędów (przypadek, rodzaj, aspekt) i poziomy trudności.

## Krok 5 — wynik na rdzeniu (7 najtrudniejszych par)

Prawdziwy sprawdzian gramatyki to 7 par oznaczonych w `eval.jsonl` polem `"headline_core": true` — tam, gdzie prosta metoda odniesienia (baseline) zawodzi. Accuracy na tych 7 policzysz tak:

```
python -c "import json; core={json.loads(l)['id'] for l in open('benchmarks/d3-skladnia-v1/eval.jsonl',encoding='utf-8') if json.loads(l)['headline_core']}; r=[x for x in json.load(open('wynik/wyniki-twoj-model.json',encoding='utf-8'))['results'] if x['id'] in core]; print('wynik na rdzeniu:', round(sum(x['pass_norm'] for x in r)/len(r),3), 'na', len(r), 'parach')"
```

## Jak sprawdzić, że wyniki się zgadzają

- **Powtarzalność:** dwie osoby liczące oceny tego samego modelu powinny dostać ten sam `accuracy_norm` (z dokładnością do sposobu liczenia log-prawdopodobieństwa). Jeśli się różnią mocno — najpewniej różnie liczycie log-prawdopodobieństwo w kroku 2.
- **Porównanie z baseline:** metoda odniesienia jest już policzona w repo (`benchmarks/d3-skladnia-v1/wyniki-ngram-o4.json`). Jeśli Twój model na rdzeniu (krok 5) bije baseline, który na rdzeniu z definicji zawodzi — to jest sygnał, że model łapie gramatykę.

## Ważne (uczciwie)

7 par w rdzeniu to **za mało na twardy wyrok** „model A lepszy od B" — przedział ufności jest szeroki. To sprawdzian, że pipeline działa i że model łapie kierunek, a nie ostateczna ocena jakości. Twardy werdykt wymaga większego zestawu (co najmniej 85 par w rdzeniu).
