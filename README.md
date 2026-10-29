<p align="center">
  <img src="assets/flaga-pl.svg" alt="Flag of Poland" width="200">
</p>

# Probierz

Probierz is a set of tools, protocols and small benchmarks for evaluating language models on data that
we can show was not in their training set. The name is Polish for a touchstone.

**Author:** Arkadiusz Słota · **Status:** working method and runnable core; most benchmarks are small
public demonstrators (see [Benchmarks](#benchmarks)).

## Why

Many popular benchmarks (MMLU and others) have leaked into training corpora, so a high score can mean
memorisation rather than ability. We build our training data from scratch (`slayerlabs/datasets`,
OpenPL, MicroModels), so we know what went into training. That lets us check, item by item, that an
evaluation set does not overlap with it.

## How it works

1. **Provenance.** Every dataset is labelled *train-only* or *eval-only*, and the two never mix
   ([`protokol/PROVENANCE-Manifest.md`](protokol/PROVENANCE-Manifest.md)).
2. **Measured overlap, not declared overlap.** [`tools/contamination_check.py`](tools/contamination_check.py)
   compares an evaluation set with training data using n-gram overlap and reports both the overlap fraction
   and the longest copied span. Example: an early audit of `test_verification.jsonl` against `seed_500`
   found 90% of items contaminated; the stricter any-match + span check later flagged 13/13. That file was
   reclassified and is not used as held-out data.
3. **Blind exchange.** A team that builds and tests on its own benchmark will overfit to it. The protocol
   lets two teams exchange benchmarks that the other side has never seen. Hashes are published before
   items are revealed, and each set is used once, because a benchmark stops being clean once it is public
   ([`protokol/PROTOKOL-Wymiany.md`](protokol/PROTOKOL-Wymiany.md)).
4. **Difficulty with signal.** Items that every model fails or every model passes carry no information.
   Benchmarks aim for a spread of difficulty, and failures are classified by type (wrong plan, silent
   omission, format error, ...), not only counted.

### What we measure

- **Dimensions.** Language ability is split into dimensions that are tested separately: D1 reasoning,
  D2 semantics, D3 syntax, D4 long context, D5 instruction following, D6 calibration of uncertainty.
  A dimension stays only if data show it is distinct from the others; if panel results show a single
  shared factor, the split is dropped ([`docs/00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej.md`](docs/00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej.md)).
- **Scoring.** Answers are checked deterministically (exact number or canonical text), not by perplexity
  or a judge model. Each item has three paraphrases; we report the median and how many items depend on
  the wording.
- **Measurement model.** Per dimension, a Rasch (1PL) model for item difficulty and a Bradley-Terry
  comparison between models, with bootstrap confidence intervals. A 2PL model is used only when the
  panel is large enough to identify it. This needs a panel of at least five models; with fewer, results
  are reported as raw pass rates.

Method notes, in Polish: [`docs/INDEX.md`](docs/INDEX.md) and [`docs/metoda/`](docs/metoda/). Current
measured state and open problems: [`docs/90-Ewaluacja/Stan.md`](docs/90-Ewaluacja/Stan.md).

## Rules for releasing a benchmark

A Probierz benchmark is released only if:

1. it has a provenance entry (documented source, train/eval label);
2. the contamination audit passed (`contamination_check.py` reports 0% contaminated items);
3. for blind exchange, its hash was published before reveal and the set is used once.

Otherwise it measures memorisation, not ability.

## Benchmarks

Public sets in [`benchmarks/`](benchmarks/) (D1 reasoning, D2 semantics, D3 syntax, D5 instruction
following and orchestration, D6 calibration, C# SOLID) are **demonstrators of the format and the method**.
Once public, they can end up in someone's training data, so for a blind verdict keep a private, hashed
version.

**Exception:** [`benchmarks/zewnetrzne/`](benchmarks/zewnetrzne/README.md) contains public benchmarks by
other authors, used to compare with other work (for example ARC-Easy-PL and a list of 50 distinct public
benchmarks with their protocol). They do not meet the rules above and are not Probierz benchmarks. We do
not copy their data: each is fetched from a pinned source revision and checked by sha256.

## Repository layout

```
Probierz/
├── README.md
├── docs/
│   ├── INDEX.md           # start here (Polish)
│   ├── 00-Cele/           # goals: fair measurement; what "language ability" means here
│   ├── metoda/            # method: contamination and exchange, difficulty, dimensions,
│   │                      # measurement model, stress tests, BPB metric and leaderboard
│   ├── 20-Decyzje/        # decision records
│   ├── 60-Reference/      # glossary
│   └── 90-Ewaluacja/      # measured state, analyses, external review
├── protokol/              # provenance manifest; blind exchange protocol
├── benchmarks/            # demonstrator sets; zewnetrzne/ = external benchmarks
├── tools/                 # contamination audit, runners, scorers
└── wyniki/                # evaluation reports
```
