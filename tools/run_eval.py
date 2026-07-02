"""run_eval.py — przejazd modelu przez zestaw eval + ocena deterministyczna.

Realizuje pomiar wg dokumentow Probierza:
- odpytuje model na KAZDEJ parafrazie polecenia (AT5: test niezmienniczosci promptu),
- weryfikuje odpowiedz koncowa deterministycznie wzgledem `odpowiedz_kanoniczna` (T5),
- liczy wynik itemu jako statystyke odporna (mediana pass po parafrazach) + wariancje (wrazliwosc),
- zapisuje odpowiedzi surowe do audytu (grader trybu awarii = osobny krok, S3/S4).

NIE klasyfikuje automatycznie trybu awarii (to wymaga >=2 graderow roznego pochodzenia, S4) —
zapisuje surowe wyjscia do reczej/pol-automatycznej klasyfikacji.

Model: dowolny endpoint OpenAI-compatible (chat/completions). Dla Slayera uzyj proxy:
  --base-url http://127.0.0.1:8799/v1  --model slayer-v49-qwen3.5-27b

Uzycie:
  python run_eval.py --eval ../benchmarks/d1-rozumowanie-v1/eval.jsonl \
    --base-url http://127.0.0.1:8799/v1 --model slayer-v49-qwen3.5-27b \
    --api-key "$SLAYER_API_KEY" --out wyniki-slayer-d1.json
"""
import argparse, json, re, sys, time, urllib.request, urllib.error

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SYSTEM = ("Jesteś precyzyjnym solverem. Rozwiąż zadanie krok po kroku, a na końcu podaj "
          "wynik końcowy w osobnej linii dokładnie w formacie: WYNIK: <odpowiedź>")


def call_model(base_url, model, api_key, system, user, max_tokens=1024, temperature=0.0, retries=3):
    url = base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": max_tokens, "temperature": temperature, "stream": False,
    }
    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as r:
                j = json.loads(r.read().decode("utf-8"))
                return j["choices"][0]["message"]["content"]
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    return f"__ERROR__: {last}"


def extract_answer(text):
    """Wyciaga wartosc po 'WYNIK:'; fallback: ostatnia liczba/linia."""
    if text is None:
        return ""
    m = list(re.finditer(r"WYNIK:\s*(.+)", text, flags=re.IGNORECASE))
    if m:
        return m[-1].group(1).strip().rstrip(".").strip()
    # fallback: ostatnia niepusta linia
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[-1] if lines else ""


def normalize_num(s):
    """Do porownania numerycznego: wyciaga pierwsza liczbe (kropka/przecinek dziesietny)."""
    s = s.replace(",", ".")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def normalize_text(s):
    return re.sub(r"\s+", " ", s.strip().lower()).rstrip(".")


def judge(answer, kanon, typ):
    """Deterministyczny pass/fail wg typu odpowiedzi (T5)."""
    if typ == "liczba":
        a, k = normalize_num(answer), normalize_num(kanon)
        if a is None or k is None:
            return False
        return abs(a - k) < 1e-6
    else:  # kanoniczny_tekst
        na, nk = normalize_text(answer), normalize_text(kanon)
        # pass gdy kanon wystepuje jako slowo/fraza w odpowiedzi (tolerancja rozwlesklosci)
        return nk == na or re.search(r"\b" + re.escape(nk) + r"\b", na) is not None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", required=True)
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--api-key", default="")
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--temperature", type=float, default=0.0)
    args = ap.parse_args()

    items = [json.loads(l) for l in open(args.eval, encoding="utf-8") if l.strip()]
    results = []
    n_pass_median = 0

    for it in items:
        paras = it["spec_parafrazy"]
        kanon = it["odpowiedz_kanoniczna"]
        typ = it["typ_odpowiedzi"]
        per_para = []
        for p in paras:
            raw = call_model(args.base_url, args.model, args.api_key, SYSTEM, p,
                             args.max_tokens, args.temperature)
            ans = extract_answer(raw)
            ok = judge(ans, kanon, typ)
            per_para.append({"prompt": p, "raw": raw, "answer": ans, "pass": ok})
        passes = [x["pass"] for x in per_para]
        pass_rate = sum(passes) / len(passes)
        pass_median = pass_rate >= 0.5  # statystyka odporna: wiekszosc parafraz
        wrazliwosc = 0 if all(passes) or not any(passes) else 1  # rozjazd miedzy parafrazami
        if pass_median:
            n_pass_median += 1
        results.append({
            "id": it["id"], "poziom_krokow": it["poziom_krokow"],
            "pass_median": pass_median, "pass_rate_parafraz": round(pass_rate, 3),
            "wrazliwosc_parafraza": wrazliwosc, "kanon": kanon, "typ": typ,
            "per_parafraza": per_para,
        })
        print(f"  {it['id']} (L{it['poziom_krokow']}): pass={pass_median} "
              f"({sum(passes)}/{len(passes)} parafraz)"
              + ("  [WRAZLIWY na parafraze]" if wrazliwosc else ""))

    summary = {
        "model": args.model, "eval": args.eval, "n_items": len(items),
        "pass_median_count": n_pass_median,
        "pass_median_rate": round(n_pass_median / len(items), 3) if items else 0,
        "items_wrazliwe": sum(r["wrazliwosc_parafraza"] for r in results),
    }
    out = {"summary": summary, "results": results}
    json.dump(out, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("\n=== PODSUMOWANIE ===")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"\nZapisano: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
