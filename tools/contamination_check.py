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
    """JSONL {prompt,response,text} -> lista stringów; .txt -> cały plik jako 1 item."""
    items = []
    if path.endswith(".jsonl"):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            parts = [str(o[k]) for k in ("prompt", "response", "text", "input", "output") if o.get(k)]
            if parts:
                items.append("\n".join(parts))
    else:
        items.append(open(path, encoding="utf-8").read())
    return items


def tokens(s):
    return re.findall(r"\w+", s.lower(), flags=re.UNICODE)


def ngrams(toks, n):
    return {tuple(toks[i:i + n]) for i in range(len(toks) - n + 1)} if len(toks) >= n else set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", required=True, help="korpus treningowy (jsonl/txt)")
    ap.add_argument("--eval", required=True, help="kandydat na benchmark (jsonl/txt)")
    ap.add_argument("--n", type=int, default=13, help="długość n-gramu (Llama-style=13)")
    ap.add_argument("--prog", type=float, default=0.5, help="próg overlapu = skażony")
    ap.add_argument("--top", type=int, default=5, help="ile najgorszych pokazać")
    args = ap.parse_args()

    train_items = load_items(args.train)
    eval_items = load_items(args.eval)

    # indeks n-gramów treningu
    train_ng = set()
    for t in train_items:
        train_ng |= ngrams(tokens(t), args.n)
    print(f"trening: {len(train_items)} itemów, {len(train_ng):,} unikalnych {args.n}-gramów")
    print(f"eval:    {len(eval_items)} itemów\n")

    scored = []          # (overlap, hit, total, idx)
    skipped = 0
    for i, e in enumerate(eval_items):
        eg = ngrams(tokens(e), args.n)
        if not eg:
            skipped += 1
            continue
        hit = sum(1 for g in eg if g in train_ng)
        scored.append((hit / len(eg), hit, len(eg), i))

    if not scored:
        print("brak itemów eval z >= n tokenami — zmniejsz --n."); return 1

    contaminated = [s for s in scored if s[0] > args.prog]
    near_verbatim = [s for s in scored if s[0] >= 0.99]
    mean = sum(s[0] for s in scored) / len(scored)

    print(f"=== AUDYT KONTAMINACJI (n={args.n}, próg={args.prog}) ===")
    print(f"  scoringowanych itemów:     {len(scored)} ({skipped} pominiętych: < {args.n} tokenów)")
    print(f"  średni overlap n-gram:     {mean:.3f}")
    print(f"  skażone (>{args.prog}):          {len(contaminated)} ({100*len(contaminated)/len(scored):.1f}%)")
    print(f"  near-verbatim (≈1.0):      {len(near_verbatim)} ({100*len(near_verbatim)/len(scored):.1f}%)")

    if contaminated:
        print(f"\n  najgorsze {min(args.top, len(contaminated))}:")
        for ov, hit, tot, idx in sorted(contaminated, reverse=True)[:args.top]:
            print(f"    item #{idx}: overlap {ov:.2f} ({hit}/{tot} {args.n}-gramów w treningu)")

    print("\n=== WERDYKT ===")
    if not contaminated:
        print(f"  ✓ CZYSTY: 0% itemów powyżej progu — eval nie przecieka do treningu. Nadaje się na benchmark.")
        return 0
    else:
        print(f"  ✗ SKAŻONY: {100*len(contaminated)/len(scored):.1f}% itemów przecieka — USUŃ je przed użyciem jako eval.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
