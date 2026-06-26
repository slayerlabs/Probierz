"""contamination_check.py — audyt kontaminacji eval ↔ trening (n-gramowy overlap).

Teza (T1): „dane od zera" NIE wystarczy — trzeba ZMIERZYĆ, że zbiór eval nie przecieka
do treningu. Bez tego benchmark jest skażony i mierzy zapamiętywanie, nie zdolność.

Metoda: n-gramowy overlap (jak dedup GPT-3 / Llama, n=13) + flaga near-verbatim (overlap≈1).
To dokładnie ten sam mechanizm n-gram co w `micro-models`: n-gram = detektor DOSŁOWNEJ pamięci.
Tam mierzył kompresję języka; tu wykrywa, czy item eval był „widziany" w treningu.

Wynik: % itemów eval skażonych (overlap > próg) + najgorsze przypadki. Benchmark jest „czysty"
DOPIERO gdy audyt to potwierdzi (provenance to teza; ten skrypt to dowód).

Użycie:
  python contamination_check.py --train ../../datasets/seed_500_training_final.jsonl \
                                --eval  ../../datasets/test_verification.jsonl
  python contamination_check.py --train trening.jsonl --eval kandydat.jsonl --n 13 --prog 0.5
"""
import argparse, json, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def load_items(path):
    """JSONL -> lista stringów (znane pola lub fallback: wszystkie pola tekstowe); .txt -> cały plik."""
    items = []
    KNOWN = ("prompt", "response", "text", "input", "output", "spec", "pytanie", "zadanie")
    if path.endswith(".jsonl"):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            parts = [str(o[k]) for k in KNOWN if o.get(k)]
            if not parts:                       # nieznany schemat -> wszystkie pola tekstowe
                parts = [str(v) for v in o.values() if isinstance(v, str)]
            if parts:
                items.append("\n".join(parts))
    else:
        items.append(open(path, encoding="utf-8").read())
    return items


def tokens(s):
    return re.findall(r"\w+", s.lower(), flags=re.UNICODE)


def ngrams(toks, n):
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)} if len(toks) >= n else set()


def score_item(toks, train_ng, n):
    """(frakcja, trafienia, total, najdłuższy_span_tokenów) lub None gdy < n tokenów.
    Span = najdłuższy ciągły fragment itemu pokryty n-gramami treningu (łapie wtopione kopie)."""
    if len(toks) < n:
        return None
    windows = [tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)]
    flags = [w in train_ng for w in windows]
    hits = sum(flags)
    longest = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        if cur > longest:
            longest = cur
    span = longest + n - 1 if longest else 0
    return hits / len(windows), hits, len(windows), span


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True, help="korpus treningowy (jsonl/txt)")
    ap.add_argument("--eval", required=True, help="kandydat na benchmark (jsonl/txt)")
    ap.add_argument("--n", type=int, default=13, help="długość n-gramu (Llama-style=13)")
    ap.add_argument("--prog", type=float, default=0.5, help="próg frakcji n-gramów = skażony")
    ap.add_argument("--span", type=int, default=None,
                    help="próg najdłuższego wspólnego spanu (tokeny); domyślnie =n (any-match: dowolne trafienie n-gramu flaguje)")
    ap.add_argument("--top", type=int, default=5, help="ile najgorszych pokazać")
    args = ap.parse_args()
    span_prog = args.span if args.span is not None else args.n

    train_items = load_items(args.train)
    eval_items = load_items(args.eval)

    train_ng = set()
    for t in train_items:
        train_ng |= ngrams(tokens(t), args.n)
    print(f"trening: {len(train_items)} itemów, {len(train_ng):,} unikalnych {args.n}-gramów")
    print(f"eval:    {len(eval_items)} itemów\n")

    scored, skipped = [], 0
    for i, e in enumerate(eval_items):
        r = score_item(tokens(e), train_ng, args.n)
        if r is None:
            skipped += 1
            continue
        frac, hits, total, span = r
        scored.append((frac, hits, total, span, i))

    if not scored:
        print("brak itemów eval z >= n tokenami — zmniejsz --n."); return 1

    # skażony: frakcja > prog LUB najdłuższy span >= span_prog (any-match / wtopiona kopia — fix Xaviera)
    contaminated = [s for s in scored if s[0] > args.prog or s[3] >= span_prog]
    any_match = [s for s in scored if s[1] >= 1]
    near_verbatim = [s for s in scored if s[0] >= 0.99]
    mean = sum(s[0] for s in scored) / len(scored)
    max_span = max(s[3] for s in scored)

    print(f"=== AUDYT KONTAMINACJI (n={args.n}, próg-frakcji={args.prog}, próg-spanu={span_prog} tok) ===")
    print(f"  scoringowanych itemów:     {len(scored)} ({skipped} pominiętych: < {args.n} tokenów)")
    print(f"  średnia frakcja n-gram:    {mean:.3f}")
    print(f"  any-match (≥1 {args.n}-gram):  {len(any_match)} ({100*len(any_match)/len(scored):.1f}%)  ← łapie wtopione kopie")
    print(f"  najdłuższy wspólny span:   {max_span} tokenów")
    print(f"  near-verbatim (frakcja≈1): {len(near_verbatim)}")
    print(f"  SKAŻONE (frakcja>{args.prog} LUB span≥{span_prog}): {len(contaminated)} ({100*len(contaminated)/len(scored):.1f}%)")

    if contaminated:
        print(f"\n  najgorsze {min(args.top, len(contaminated))} (wg spanu):")
        for frac, hits, total, span, idx in sorted(contaminated, key=lambda s: (s[3], s[0]), reverse=True)[:args.top]:
            print(f"    item #{idx}: span {span} tok, frakcja {frac:.2f} ({hits}/{total} {args.n}-gramów)")

    print("\n=== WERDYKT ===")
    if not contaminated:
        print(f"  ✓ CZYSTY: 0% skażonych (brak frakcji>{args.prog} i brak spanu≥{span_prog} tok). Nadaje się na benchmark.")
        return 0
    print(f"  ✗ SKAŻONY: {100*len(contaminated)/len(scored):.1f}% itemów przecieka (frakcja LUB wtopiony span) — USUŃ przed użyciem.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
