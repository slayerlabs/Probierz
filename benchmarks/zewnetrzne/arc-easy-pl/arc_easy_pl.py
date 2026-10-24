#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arc_easy_pl.py - ARC-Easy-PL (polskie tlumaczenia testu ARC-Easy) dla dowolnego modelu przyczynowego HF.

To ten sam pomiar, ktory SlayerLab podaje jako os K (eff-PL) w kartach modeli GoLLeM.
Dane pobierane z przypietych rewizji i sprawdzane po sha256, wiec kazdy liczy na tych samych bajtach:
  EU20   Eurolingua/arcx                  arc_easy_PL_test.jsonl             @f2e35fbe  (glowne)
  ddudek ddudek/ai2_arc_translated_pol    ARC-Easy/test-00000-of-00001.parquet @e61110df (kontrolne)
Oba maja te same 2376 id i answerKey co allenai/ai2_arc ARC-Easy test @210d026f.

Protokol (Glint evaluate_arc_easy, 1:1):
  - zero-shot, bez szablonu: kandydat = pytanie + " " + odpowiedz;
  - wynik odpowiedzi = LL(pytanie + " " + odpowiedz) - LL(pytanie), suma log-prob tokenow;
  - argmax, BEZ normalizacji dlugosci; miara = trafnosc (acc), losowo ok. 25 %;
  - tokenizacja: tokenizer.json (biblioteka tokenizers) .encode(tekst).ids, tak jak jest, z ewentualnym
    post-processorem tokenizera; id >= rozmiaru slownika odrzucone; przyciecie do 256 tokenow;
    tekst krotszy niz 2 tokeny dostaje -inf.
Kalibracja: SlayerLab/GoLLeM-45M-PL @1b1791fc daje EU20 31.57, ddudek 31.73 (README obok).

Uzycie:
  python arc_easy_pl.py --model SlayerLab/GoLLeM-45M-PL --revision 1b1791fcd67727920db39bcf1e7022ce7a209e12 --out wynik.json
  python arc_easy_pl.py --model C:/sciezka/do/mojego/modelu --out wynik.json        # katalog lokalny (HF format)
Wymaga: torch, transformers, tokenizers, huggingface_hub, pyarrow.
"""
import argparse
import hashlib
import json
import math
import os
import sys
import time

os.environ.pop("HF_TOKEN", None)
os.environ["HF_HUB_DISABLE_IMPLICIT_TOKEN"] = "1"

import torch  # noqa: E402
import torch.nn.functional as F  # noqa: E402
from huggingface_hub import hf_hub_download, snapshot_download  # noqa: E402
from tokenizers import Tokenizer  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

N = 2376
MAX_LEN = 256
DANE = {
    "EU20": ("Eurolingua/arcx", "arc_easy_PL_test.jsonl", "f2e35fbebdb572a9653eda706b00083b0892ed43",
             "c6732eeba3b2f3cfda95d65d42fb9d4e0f10edc1b9e6c8582d46c069b6706186"),
    "ddudek": ("ddudek/ai2_arc_translated_pol", "ARC-Easy/test-00000-of-00001.parquet",
               "e61110df4097ca5f5284a62e60d01d8f80d15069",
               "f4f30341da404f5d5134ab38e25a55cc9267fdaccb42584607e2830d21bdb934"),
}
# Pliki modelu pobierane z Hub: bez pickli i bez kodu autora (kod tylko z --trust-remote-code).
BEZPIECZNE = ["*.json", "*.safetensors", "*.txt", "*.model"]


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def wczytaj_dane(nazwa):
    repo, plik, rev, oczekiwane = DANE[nazwa]
    p = hf_hub_download(repo, plik, repo_type="dataset", revision=rev, token=False)
    got = sha256(p)
    if got != oczekiwane:
        raise SystemExit(f"{nazwa}: sha256 {got} != {oczekiwane}")
    if plik.endswith(".jsonl"):
        with open(p, encoding="utf-8") as f:
            rows = [json.loads(line) for line in f if line.strip()]
    else:
        import pyarrow.parquet as pq
        rows = pq.read_table(p).to_pylist()
    if len(rows) != N or len({r["id"] for r in rows}) != N:
        raise SystemExit(f"{nazwa}: oczekiwano {N} unikalnych id, jest {len(rows)}")
    return rows, got


def wczytaj_model(model, revision, trust_remote_code):
    if os.path.isdir(model):
        d = model
    else:
        wzorce = BEZPIECZNE + (["*.py"] if trust_remote_code else [])
        d = snapshot_download(model, revision=revision, allow_patterns=wzorce, token=False)
    tj = os.path.join(d, "tokenizer.json")
    tok = Tokenizer.from_file(tj) if os.path.exists(tj) else AutoTokenizer.from_pretrained(d, use_fast=True).backend_tokenizer
    m = AutoModelForCausalLM.from_pretrained(d, trust_remote_code=trust_remote_code, use_safetensors=True,
                                             dtype=torch.float32).eval()
    return tok, m


def log_probs(logits_fn, tok, V, texts, device, batch_size):
    """Suma log-prob tokenow kazdego tekstu (bez pierwszego tokenu, ktory jest tylko kontekstem)."""
    all_ids = []
    for t in texts:
        ids = [i for i in tok.encode(t).ids if i < V][:MAX_LEN]
        all_ids.append(ids)
    out = [-float("inf")] * len(all_ids)
    with torch.inference_mode():
        for start in range(0, len(all_ids), batch_size):
            idx = [j for j in range(start, min(start + batch_size, len(all_ids))) if len(all_ids[j]) >= 2]
            if not idx:
                continue
            seqs = [all_ids[j] for j in idx]
            T = max(len(s) for s in seqs) - 1
            inp = torch.zeros((len(seqs), T), dtype=torch.long)
            tgt = torch.zeros((len(seqs), T), dtype=torch.long)
            mask = torch.zeros((len(seqs), T), dtype=torch.bool)
            for b, s in enumerate(seqs):
                inp[b, :len(s) - 1] = torch.tensor(s[:-1])
                tgt[b, :len(s) - 1] = torch.tensor(s[1:])
                mask[b, :len(s) - 1] = True
            inp, tgt, mask = inp.to(device), tgt.to(device), mask.to(device)
            lp = F.log_softmax(logits_fn(inp), dim=-1)
            g = lp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1)
            g[~mask] = 0.0
            for j, v in zip(idx, g.sum(dim=-1).tolist()):
                out[j] = v
    return out


def ocen(logits_fn, tok, V, rows, device):
    wyniki = {}
    for ex in rows:
        q, ch = ex["question"], ex["choices"]
        lps = log_probs(logits_fn, tok, V, [q + " " + t for t in ch["text"]], device, batch_size=4)
        lpq = log_probs(logits_fn, tok, V, [q], device, batch_size=128)[0]
        best = max(range(len(lps)), key=lambda j: lps[j] - lpq)
        wyniki[ex["id"]] = int(ch["label"][best] == ex["answerKey"])
    return wyniki


def main():
    ap = argparse.ArgumentParser(description="ARC-Easy-PL (EU20 + ddudek), protokol Glint evaluate_arc_easy")
    ap.add_argument("--model", required=True, help="repo HF albo katalog lokalny w formacie HF")
    ap.add_argument("--revision", default=None, help="pelny sha commitu repo HF (zalecane: przypiety)")
    ap.add_argument("--zestawy", default="EU20,ddudek", help="lista z: EU20, ddudek")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--trust-remote-code", action="store_true", help="tylko dla modelu, ktorego kod przejrzales")
    ap.add_argument("--out", required=True, help="plik JSON z wynikiem")
    a = ap.parse_args()

    zestawy = [z.strip() for z in a.zestawy.split(",") if z.strip()]
    for z in zestawy:
        if z not in DANE:
            raise SystemExit(f"nieznany zestaw {z}; dostepne: {', '.join(DANE)}")
    dane = {z: wczytaj_dane(z) for z in zestawy}

    tok, model = wczytaj_model(a.model, a.revision, a.trust_remote_code)
    model.to(a.device)
    V = tok.get_vocab_size()

    def logits_fn(ids):
        return model(input_ids=ids).logits[..., :V].float()

    se0 = math.sqrt(0.25 * 0.75 / N)
    res = {"benchmark": "ARC-Easy-PL", "protocol": "glint evaluate_arc_easy: LL(q+' '+c)-LL(q), argmax, bez normalizacji dlugosci",
           "model": a.model, "revision": a.revision, "params": sum(p.numel() for p in model.parameters()),
           "vocab": V, "device": a.device, "n": N, "se_przy_losowym": round(100 * se0, 2), "zestawy": {}}
    for z, (rows, sha) in dane.items():
        t = time.time()
        items = ocen(logits_fn, tok, V, rows, a.device)
        acc = 100 * sum(items.values()) / N
        repo, plik, rev, _ = DANE[z]
        res["zestawy"][z] = {"acc": round(acc, 2), "dataset": f"{repo}/{plik}@{rev}", "sha256": sha,
                             "sekundy": int(time.time() - t), "items": items}
        print(f"{z}: acc {acc:.2f} % ({sum(items.values())}/{N}), {int(time.time() - t)} s", flush=True)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("zapisano", a.out)


if __name__ == "__main__":
    main()
