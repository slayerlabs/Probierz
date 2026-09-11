---
type: decyzja
id: BENCH-DEC3
title: "Decyzja — leaderboard eksperymentalny fabryki: BPB-primary + gate S7"
status: przyjeta
parents: ["BENCH-S7"]
author: Arkadiusz Słota
date: 2026-09-11
---

# DEC3 — Protokół leaderboardu dla modeli fabryki

## Kontekst
Fabryka.ai używa JEDNEGO tokenizera bajtowego (UTF-8, vocab 256) dla wszystkich modeli i rozmiarów (weryfikacja z kodu: `hf_publish.py`, `training.py`). To znaczy: **wewnątrz fabryki confound tokenizera znika z definicji** → porównania są czyste po samym rozmiarze/treningu.

## Decyzja
Przyjmujemy protokół [[../25-Syntezy/S7-Leaderboard-BPB-Gate|S7]] jako **eksperymentalny leaderboard fabryki**:
- **BPB-primary** (jedna skala, dowolny model) + **mean margin** (confirming, moc) + **accuracy** (pomocnicza).
- **INDISTINGUISHABLE-GATE** obowiązkowy: brak gołych rankingów, A>B tylko przy CI paired-delta rozłącznych, badge:confound między komórkami.
- **Zakres = reżim mały/średni**, granica przez **saturację** (`acc_core < ~0.9`), nie sztywny próg parametrów. Dla base do ~125M w pełni użyteczny (empiria: 8M–110M na 0.4–0.7).
- Osobny od produktowego leaderboardu `track.fabryka.ai`.

## Otwarte (warunki podniesienia wniosku)
- **Gate 1 (≥3 seedy treningowe)** — do przejścia z „checkpoint-ordering" na „recepta X > Y". Trening na RunPod (nie lokalne 3090; potwierdzone 2026-09-11).
- **Loader byte-modeli fabryki** (arch. BDH, vocab 256) — żeby ranking BPB objął realne modele fabryki (ta sama skala z definicji), nie tylko modele subword (GoLLeM/Slayer).

## Prowieniencja
`leaderboard-d3` @ fabryka-track; `results/` z SHA256 pinami (reprodukcja z bajtów).

---
parent: [[../25-Syntezy/S7-Leaderboard-BPB-Gate|S7]] · [[D-DEC2-Fokus-Na-Slayerze|DEC2]] · [[../90-Ewaluacja/Stan|Stan]]
