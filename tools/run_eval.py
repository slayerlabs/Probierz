"""run_eval.py — przejazd modelu przez zestaw eval + ocena deterministyczna.

Realizuje pomiar wg dokumentow Probierza:
- odpytuje model na KAZDEJ parafrazie polecenia (AT5: test niezmienniczosci promptu),
- weryfikuje odpowiedz deterministycznie (T5),
- liczy wynik itemu jako statystyke odporna (mediana pass po parafrazach) + wariancje (wrazliwosc),
- zapisuje odpowiedzi surowe do audytu.

Typy odpowiedzi (typ_odpowiedzi):
- "liczba": porownanie numeryczne z tolerancja formatu (extract po 'WYNIK:').
- "kanoniczny_tekst": dopasowanie do `klasy_odpowiedzi` (najdluzsza fraza) lub frazy kanonicznej.
- "programowa": weryfikacja SUROWEJ odpowiedzi predykatem z pola `regula` {pred, arg}. Uzywane dla
  D5 (wiernosc instrukcji) - grader sprawdza format programowo (liczba slow, brak znaku, JSON, ...).
  Nie uzywa 'WYNIK:'; system prompt neutralny (model ma wykonac polecenie doslownie).

Odpornosc: checkpoint per item + wznawianie (pomija itemy z pliku --out).

Uzycie:
  python run_eval.py --eval <zestaw>/eval.jsonl --base-url <url> --model <id> --out wyniki.json
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SYSTEM_SOLVER = ("Jesteś precyzyjnym solverem. Rozwiąż zadanie krok po kroku, a na końcu podaj "
                 "wynik końcowy w osobnej linii dokładnie w formacie: WYNIK: <odpowiedź>")
# Dla typu 'programowa' (D5): model ma wykonac polecenie DOSLOWNIE, bez doklejania 'WYNIK:'.
SYSTEM_INSTRUCT = ("Jesteś asystentem wykonującym polecenia dokładnie. Wykonaj polecenie użytkownika "
                   "ściśle według podanych ograniczeń formatu. Zwróć wyłącznie żądaną treść, bez "
                   "komentarzy, wyjaśnień ani dodatkowego tekstu.")


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
    na = normalize_text(answer)
    hits = []
    for k in klasy:
        nk = normalize_text(k)
        if re.search(r"\b" + re.escape(nk) + r"\b", na):
            hits.append(nk)
    if not hits:
        return None
    return max(hits, key=len)


# ---- Predykaty D5 (typ 'programowa') — weryfikacja formatu na SUROWEJ odpowiedzi ----
def _clean(raw):
    """Odpowiedz oczyszczona: bez otaczajacych bialych znakow i ewentualnych ogranicznikow ```."""
    t = (raw or "").strip()
    t = re.sub(r"^```[a-zA-Z]*\n?", "", t)
    t = re.sub(r"\n?```$", "", t)
    return t.strip()


def _words(t):
    return re.findall(r"\b[\wąćęłńóśźżÀ-ÿ]+\b", t, flags=re.UNICODE)


def pred_exact_word_count(raw, arg):
    return len(_words(_clean(raw))) == int(arg)

def pred_max_word_count(raw, arg):
    return len(_words(_clean(raw))) <= int(arg)

def pred_forbidden_char(raw, arg):
    return arg.lower() not in _clean(raw).lower()

def pred_forbidden_word(raw, arg):
    return re.search(r"\b" + re.escape(arg.lower()), _clean(raw).lower()) is None

def pred_uppercase_only(raw, arg):
    t = _clean(raw)
    letters = [c for c in t if c.isalpha()]
    return len(letters) > 0 and all(c.isupper() for c in letters)

def pred_exact_line_count(raw, arg):
    lines = [l for l in _clean(raw).splitlines() if l.strip()]
    return len(lines) == int(arg)

def pred_starts_with(raw, arg):
    return _clean(raw).startswith(arg)

def pred_ends_with(raw, arg):
    return _clean(raw).rstrip().endswith(arg)

def pred_contains_not(raw, arg):
    return arg.lower() not in _clean(raw).lower()

def pred_contains(raw, arg):
    return arg.lower() in _clean(raw).lower()

def pred_json_has_keys(raw, arg):
    t = _clean(raw)
    m = re.search(r"\{.*\}", t, flags=re.DOTALL)
    if not m:
        return False
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return False
    return isinstance(obj, dict) and all(k in obj for k in arg)

def pred_regex(raw, arg):
    return re.search(arg, _clean(raw)) is not None

def _extract_json(raw):
    """Wyciaga pierwszy obiekt {...} lub tablice [...] z odpowiedzi (toleruje ``` i tekst)."""
    t = _clean(raw)
    m = re.search(r"(\{.*\}|\[.*\])", t, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def pred_json_tool_is(raw, arg):
    """JSON obiekt z polem tool == arg."""
    o = _extract_json(raw)
    return isinstance(o, dict) and str(o.get("tool", "")).strip().lower() == str(arg).lower()


def pred_json_tool_args(raw, arg):
    """JSON tool==arg['tool'] ORAZ args zawiera wszystkie arg['keys']."""
    o = _extract_json(raw)
    if not isinstance(o, dict):
        return False
    if str(o.get("tool", "")).strip().lower() != str(arg["tool"]).lower():
        return False
    a = o.get("args")
    return isinstance(a, dict) and all(k in a for k in arg["keys"])


def pred_json_only_tool(raw, arg):
    """CALA odpowiedz (po oczyszczeniu) parsuje sie jako JSON obiekt z tool==arg (zero tekstu poza)."""
    t = _clean(raw)
    try:
        o = json.loads(t)
    except Exception:
        return False
    return isinstance(o, dict) and str(o.get("tool", "")).strip().lower() == str(arg).lower()


def pred_json_seq_order(raw, arg):
    """Tablica JSON obiektow; sekwencja pol 'tool' zawiera arg jako podciag w kolejnosci."""
    o = _extract_json(raw)
    if not isinstance(o, list) or not o:
        return False
    tools = [str(x.get("tool", "")).strip().lower() for x in o if isinstance(x, dict)]
    # arg musi wystapic jako podciag zachowujacy kolejnosc
    it = iter(tools)
    return all(any(t == want.lower() for t in it) for want in arg)


def pred_json_seq_len_order(raw, arg):
    """Tablica JSON o DOKLADNEJ dlugosci arg['len'] i dokladnej sekwencji tool==arg['order']."""
    o = _extract_json(raw)
    if not isinstance(o, list):
        return False
    tools = [str(x.get("tool", "")).strip().lower() for x in o if isinstance(x, dict)]
    want = [w.lower() for w in arg["order"]]
    return len(tools) == int(arg["len"]) and tools == want


def pred_json_seq_dep(raw, arg):
    """Sekwencja tool w kolejnosci arg['order']; jesli ref_in_last, ostatni krok ma w args
    referencje do wczesniejszego wyniku (placeholder {{...}}, 'step', 'result', '$')."""
    o = _extract_json(raw)
    if not isinstance(o, list) or not o:
        return False
    tools = [str(x.get("tool", "")).strip().lower() for x in o if isinstance(x, dict)]
    it = iter(tools)
    if not all(any(t == w.lower() for t in it) for w in arg["order"]):
        return False
    if arg.get("ref_in_last"):
        last = o[-1]
        blob = json.dumps(last.get("args", {}), ensure_ascii=False).lower()
        return bool(re.search(r"\{\{.*\}\}|step|result|wynik|\$", blob))
    return True


def pred_json_seq_no_tool(raw, arg):
    """Sekwencja tool == arg['order'] (podciag w kolejnosci) ORAZ zaden krok nie uzywa arg['forbidden']."""
    o = _extract_json(raw)
    if not isinstance(o, list) or not o:
        return False
    tools = [str(x.get("tool", "")).strip().lower() for x in o if isinstance(x, dict)]
    if arg["forbidden"].lower() in tools:
        return False
    it = iter(tools)
    return all(any(t == w.lower() for t in it) for w in arg["order"])


PREDICATES = {
    "exact_word_count": pred_exact_word_count,
    "max_word_count": pred_max_word_count,
    "forbidden_char": pred_forbidden_char,
    "forbidden_word": pred_forbidden_word,
    "uppercase_only": pred_uppercase_only,
    "exact_line_count": pred_exact_line_count,
    "starts_with": pred_starts_with,
    "ends_with": pred_ends_with,
    "contains_not": pred_contains_not,
    "contains": pred_contains,
    "json_has_keys": pred_json_has_keys,
    "regex": pred_regex,
    "json_tool_is": pred_json_tool_is,
    "json_tool_args": pred_json_tool_args,
    "json_only_tool": pred_json_only_tool,
    "json_seq_order": pred_json_seq_order,
    "json_seq_len_order": pred_json_seq_len_order,
    "json_seq_dep": pred_json_seq_dep,
    "json_seq_no_tool": pred_json_seq_no_tool,
}


def check_predicate(raw, regula):
    fn = PREDICATES.get(regula.get("pred"))
    if fn is None:
        return False
    try:
        return bool(fn(raw, regula.get("arg")))
    except Exception:
        return False


def judge(answer, kanon, typ, klasy=None):
    """Deterministyczny pass/fail dla typow 'liczba' i 'kanoniczny_tekst' (T5)."""
    if typ == "liczba":
        a, k = normalize_num(answer), normalize_num(kanon)
        if a is None or k is None:
            return False
        return abs(a - k) < 1e-6
    if klasy:
        chosen = detect_class(answer, klasy)
        return chosen is not None and chosen == normalize_text(kanon)
    na, nk = normalize_text(answer), normalize_text(kanon)
    return nk == na or re.search(r"\b" + re.escape(nk) + r"\b", na) is not None


def item_level(it):
    for key in ("poziom_krokow", "poziom_trudnosci", "poziom"):
        if key in it:
            return it[key]
    return None


def default_classes(it):
    if it.get("klasy_odpowiedzi"):
        return it["klasy_odpowiedzi"]
    kanon = normalize_text(it.get("odpowiedz_kanoniczna", ""))
    closed = {"tak", "nie", "nie wiadomo", "niejednoznaczne", "burmistrz", "demonstranci"}
    if kanon in closed:
        base = ["nie wiadomo", "niejednoznaczne", "tak", "nie"]
        return base if kanon in {"tak", "nie", "nie wiadomo", "niejednoznaczne"} else None
    return None


def score_item(it, base_url, model, api_key, max_tokens, temperature):
    typ = it["typ_odpowiedzi"]
    per_para = []
    if typ == "programowa":
        regula = it["regula"]
        for p in it["spec_parafrazy"]:
            raw = call_model(base_url, model, api_key, SYSTEM_INSTRUCT, p, max_tokens, temperature)
            ok = check_predicate(raw, regula)
            per_para.append({"prompt": p, "raw": raw, "answer": _clean(raw), "pass": ok})
        kanon = f"{regula.get('pred')}:{regula.get('arg')}"
    else:
        kanon = it["odpowiedz_kanoniczna"]
        klasy = default_classes(it)
        for p in it["spec_parafrazy"]:
            raw = call_model(base_url, model, api_key, SYSTEM_SOLVER, p, max_tokens, temperature)
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
        save(args.out, args.model, args.eval, items, results)
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
