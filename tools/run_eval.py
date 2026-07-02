"""run_eval.py — przejazd modelu przez zestaw eval + ocena deterministyczna.

Realizuje pomiar wg dokumentow Probierza:
- odpytuje model na KAZDEJ parafrazie polecenia (AT5: test niezmienniczosci promptu),
- weryfikuje odpowiedz koncowa deterministycznie wzgledem `odpowiedz_kanoniczna` (T5),
- liczy wynik itemu jako statystyke odporna (mediana pass po parafrazach) + wariancje (wrazliwosc),
- zapisuje odpowiedzi surowe do audytu (grader trybu awarii = osobny krok, S3/S4).

Odpornosc na przerwanie: zapis INKREMENTALNY po kazdym itemie (checkpoint) + WZNAWIANIE
(pomija itemy juz obecne w pliku --out). Wolne endpointy (Slayer ~40s/wywolanie) nie traca postepu.

Typy odpowiedzi (T5):
- "liczba": porownanie numeryczne z tolerancja formatu.
- "kanoniczny_tekst": jesli item ma `klasy_odpowiedzi` (zamkniety zbior, np. tak/nie/nie wiadomo),
  wykrywana jest KLASA wybrana przez model (najdluzsza pasujaca fraza wygrywa, by 'nie wiadomo'
  nie bylo mylone z 'nie'); inaczej dopasowanie frazy kanonicznej jako slowa.

NIE klasyfikuje automatycznie trybu awarii (wymaga >=2 graderow roznego pochodzenia, S4) —
zapisuje surowe wyjscia do reczej/pol-automatycznej klasyfikacji.

Uzycie:
  python run_eval.py --eval ../benchmarks/d2-semantyka-v1/eval.jsonl \
    --base-url http://127.0.0.1:8799/v1 --model slayer-v49-qwen3.5-27b \
    --api-key "$SLAYER_API_KEY" --out wyniki-slayer-d2.json
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

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
            with urllib.request.urlopen(req, timeout=180) as r:
                j = json.loads(r.read().decode("utf-8"))
                return j["choices"][0]["message"]["content"]
        except Exception as e:
            last = e
            time.sleep(1.5 * (attempt + 1))
    return f"__ERROR__: {last}"


def extract_answer(text):
    """Wyciaga wartosc po 'WYNIK:'; fallback: ostatnia niepusta linia."""
    if text is None:
        return ""
    m = list(re.finditer(r"WYNIK:\s*(.+)", text, flags=re.IGNORECASE))
    if m:
        return m[-1].group(1).strip().rstrip(".").strip()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return lines[-1] if lines else ""


def normalize_num(s):
    s = s.replace(",", ".")
    m = re.search(r"-?\d+(?:\.\d+)?", s)
    return float(m.group(0)) if m else None


def normalize_text(s):
    return re.sub(r"\s+", " ", s.strip().lower()).rstrip(".")


def detect_class(answer, klasy):
    """Wykrywa, ktora KLASE z zamknietego zbioru wybral model.
    Najdluzsza pasujaca fraza wygrywa (np. 'nie wiadomo' > 'nie'), by uniknac
    falszywych trafien podlancuchow. Zwraca znormalizowana klase lub None."""
    na = normalize_text(answer)
    hits = []
    for k in klasy:
        nk = normalize_text(k)
        if re.search(r"\b" + re.escape(nk) + r"\b", na):
            hits.append(nk)
    if not hits:
        return None
    return max(hits, key=len)  # najdluzsza pasujaca klasa


def judge(answer, kanon, typ, klasy=None):
    """Deterministyczny pass/fail wg typu odpowiedzi (T5)."""
    if typ == "liczba":
        a, k = normalize_num(answer), normalize_num(kanon)
        if a is None or k is None:
            return False
        return abs(a - k) < 1e-6
    # kanoniczny_tekst
    if klasy:
        chosen = detect_class(answer, klasy)
        return chosen is not None and chosen == normalize_text(kanon)
    na, nk = normalize_text(answer), normalize_text(kanon)
    return nk == na or re.search(r"\b" + re.escape(nk) + r"\b", na) is not None


def item_level(it):
    """Elastyczny odczyt poziomu trudnosci (rozne wymiary: poziom_krokow / poziom_trudnosci)."""
    for key in ("poziom_krokow", "poziom_trudnosci", "poziom"):
        if key in it:
            return it[key]
    return None


def default_classes(it):
    """Zbior klas odpowiedzi: jawne pole `klasy_odpowiedzi` albo heurystyka dla typowych
    odpowiedzi zamknietych (tak/nie/nie wiadomo/niejednoznaczne)."""
    if it.get("klasy_odpowiedzi"):
        return it["klasy_odpowiedzi"]
    kanon = normalize_text(it["odpowiedz_kanoniczna"])
    closed = {"tak", "nie", "nie wiadomo", "niejednoznaczne", "burmistrz", "demonstranci"}
    if kanon in closed:
        # domyslny zbior klas tak/nie/nie wiadomo/niejednoznaczne + wariant kanonu
        base = ["nie wiadomo", "niejednoznaczne", "tak", "nie"]
        return base if kanon in {"tak", "nie", "nie wiadomo", "niejednoznaczne"} else None
    return None


def score_item(it, base_url, model, api_key, max_tokens, temperature):
    kanon, typ = it["odpowiedz_kanoniczna"], it["typ_odpowiedzi"]
    klasy = default_classes(it)
    per_para = []
    for p in it["spec_parafrazy"]:
        raw = call_model(base_url, model, api_key, SYSTEM, p, max_tokens, temperature)
        ans = extract_answer(raw)
        per_para.append({"prompt": p, "raw": raw, "answer": ans, "pass": judge(ans, kanon, typ, klasy)})
    passes = [x["pass"] for x in per_para]
    pass_rate = sum(passes) / len(passes)
    return {
        "id": it["id"], "poziom": item_level(it),
        "pass_median": pass_rate >= 0.5,
        "pass_rate_parafraz": round(pass_rate, 3),
        "wrazliwosc_parafraza": 0 if all(passes) or not any(passes) else 1,
        "kanon": kanon, "typ": typ, "per_parafraza": per_para,
    }


def build_summary(model, eval_path, items, results):
    n = len(results)
    npass = sum(r["pass_median"] for r in results)
    return {
        "model": model, "eval": eval_path, "n_items": len(items), "n_scored": n,
        "pass_median_count": npass,
        "pass_median_rate": round(npass / n, 3) if n else 0,
        "items_wrazliwe": sum(r["wrazliwosc_parafraza"] for r in results),
    }


def save(out_path, model, eval_path, items, results):
    payload = {"summary": build_summary(model, eval_path, items, results), "results": results}
    json.dump(payload, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


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

    results, done = [], set()
    if os.path.exists(args.out):
        try:
            prev = json.load(open(args.out, encoding="utf-8"))
            results = prev.get("results", [])
            done = {r["id"] for r in results}
            if done:
                print(f"Wznawianie: {len(done)} itemow juz zrobionych, pomijam.")
        except Exception:
            pass

    for it in items:
        if it["id"] in done:
            continue
        r = score_item(it, args.base_url, args.model, args.api_key, args.max_tokens, args.temperature)
        results.append(r)
        save(args.out, args.model, args.eval, items, results)  # CHECKPOINT po kazdym itemie
        print(f"  {r['id']} (poz. {r['poziom']}): pass={r['pass_median']} "
              f"({sum(x['pass'] for x in r['per_parafraza'])}/{len(r['per_parafraza'])} parafraz)"
              + ("  [WRAZLIWY na parafraze]" if r["wrazliwosc_parafraza"] else ""))

    save(args.out, args.model, args.eval, items, results)
    print("\n=== PODSUMOWANIE ===")
    print(json.dumps(build_summary(args.model, args.eval, items, results), ensure_ascii=False, indent=2))
    print(f"\nZapisano: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
