#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
byte_ppl_w_pl.py - byte-PPL na polskim tekscie W (463 artykuly polskiej Wikipedii) dla modelu przyczynowego HF.

To ten sam pomiar, ktory track.fabryka.ai pokazuje w kolumnie W / byte-PPL PL (pole SDK board_pl/byte_ppl).
Dane pobierane z przypietej rewizji i sprawdzane po sha256:
  SlayerLab/fabryka-track-w-pl  w_final.jsonl  @b25c13a4  sha256 234e7ec2...

Protokol (Glint compute_perplexity, 1:1; funkcja ponizej jest skopiowana bez zmian):
  - tekst = "\\n\\n".join(text artykulow w kolejnosci pliku).strip()   -> 1 431 141 bajtow UTF-8;
  - ids = tokenizer.json (biblioteka tokenizers) .encode(tekst).ids, tak jak jest; id >= rozmiaru slownika odrzucone;
  - okna: chunk = ids[i:i+257] dla i = 0, 256, 512, ...; wejscie chunk[:-1], cele chunk[1:]; kontekst resetowany
    w kazdym oknie; pierwszy token tekstu nigdy nie jest celem; ostatnie okno krotsze, bez dopelniania;
  - token_ppl = exp(suma CE / liczba celow);
  - byte_ppl = token_ppl ** (len(ids) / n_bajtow)   <- w wykladniku WSZYSTKIE tokeny, nie liczba celow.
Kalibracja: SlayerLab/GoLLeM-v6-250M @77d75a2b daje byte_ppl 1.957844 (token_ppl 15.587507, 350 087 tokenow).

Uzycie:
  python byte_ppl_w_pl.py --model REPO --revision PELNY_SHA --out wynik.json            # zwykly model HF
  python byte_ppl_w_pl.py --model C:/sciezka/do/modelu --out wynik.json                 # katalog lokalny (HF format)
  python byte_ppl_w_pl.py --gollem-v6 SlayerLab/GoLLeM-v6-250M --revision 77d75a2b48eaab7aec59816f9849cee75a7bdfc1 \\
         --out kalibracja.json                                                          # kalibracja (loader z repo modelu)
Wymaga: torch, transformers, tokenizers, huggingface_hub.
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

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DANE = ("SlayerLab/fabryka-track-w-pl", "w_final.jsonl", "b25c13a445ba8639759264654f37295ebe08871c",
        "234e7ec21bf2236bc74425591531f2c4772f8c49ff853d57f6fa16f33ee90ac7")
N_ART, N_BAJTOW = 463, 1431141
# Pliki modelu pobierane z Hub: bez pickli i bez kodu autora (kod tylko z --trust-remote-code albo --gollem-v6).
BEZPIECZNE = ["*.json", "*.safetensors", "*.txt", "*.model"]


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def wczytaj_tekst():
    repo, plik, rev, oczekiwane = DANE
    p = hf_hub_download(repo, plik, repo_type="dataset", revision=rev, token=False)
    got = sha256(p)
    if got != oczekiwane:
        raise SystemExit(f"W: sha256 {got} != {oczekiwane}")
    with open(p, encoding="utf-8") as f:
        docs = [json.loads(line) for line in f if line.strip()]
    text = "\n\n".join(d["text"] for d in docs).strip()
    if len(docs) != N_ART or len(text.encode("utf-8")) != N_BAJTOW:
        raise SystemExit(f"W: oczekiwano {N_ART} artykulow i {N_BAJTOW} B tekstu")
    return text, got


def compute_perplexity(logits_fn, tokenizer, text, device, max_length=256):
    # Glint harness (glint_parity_eval.py sha256 d7a38ca0...), bez zmian.
    ids = tokenizer.encode(text).ids
    ids = [i for i in ids if i < tokenizer.get_vocab_size()]
    if len(ids) < 2:
        return float("inf")
    nll = 0.0; n_tokens = 0
    for i in range(0, len(ids) - 1, max_length):
        chunk = ids[i:i + max_length + 1]
        if len(chunk) < 2:
            continue
        inputs = torch.tensor([chunk[:-1]], device=device)
        targets = torch.tensor([chunk[1:]], device=device)
        with torch.no_grad():
            logits = logits_fn(inputs)
        loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), reduction="sum")
        nll += loss.item(); n_tokens += targets.numel()
    return math.exp(nll / n_tokens) if n_tokens > 0 else float("inf")


def wczytaj_model(a):
    if a.gollem_v6:
        d = snapshot_download(a.gollem_v6, revision=a.revision, token=False)
        sys.path.insert(0, d)
        from modeling_gollem_v6 import load_gollem_v6
        model, _ = load_gollem_v6(d, a.device)
        return Tokenizer.from_file(os.path.join(d, "tokenizer.json")), model, lambda ids: model(ids)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if os.path.isdir(a.model):
        d = a.model
    else:
        wzorce = BEZPIECZNE + (["*.py"] if a.trust_remote_code else [])
        d = snapshot_download(a.model, revision=a.revision, allow_patterns=wzorce, token=False)
    tj = os.path.join(d, "tokenizer.json")
    tok = Tokenizer.from_file(tj) if os.path.exists(tj) else AutoTokenizer.from_pretrained(d, use_fast=True).backend_tokenizer
    m = AutoModelForCausalLM.from_pretrained(d, trust_remote_code=a.trust_remote_code, use_safetensors=True,
                                             dtype=torch.float32).eval().to(a.device)
    return tok, m, lambda ids: m(input_ids=ids).logits


def main():
    ap = argparse.ArgumentParser(description="byte-PPL na W (track.fabryka.ai, board_pl/byte_ppl), protokol Glint compute_perplexity")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--model", help="repo HF albo katalog lokalny w formacie HF (AutoModelForCausalLM)")
    g.add_argument("--gollem-v6", help="repo modelu GoLLeM v6 (loader load_gollem_v6 z repo modelu; kalibracja)")
    ap.add_argument("--revision", default=None, help="pelny sha commitu repo HF (zalecane: przypiety)")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--trust-remote-code", action="store_true", help="tylko dla modelu, ktorego kod przejrzales")
    ap.add_argument("--out", required=True, help="plik JSON z wynikiem")
    a = ap.parse_args()

    text, sha = wczytaj_tekst()
    tok, model, fwd = wczytaj_model(a)
    V = tok.get_vocab_size()
    ids = [i for i in tok.encode(text).ids if i < V]
    t = time.time()
    token_ppl = compute_perplexity(lambda x: fwd(x)[..., :V].float(), tok, text, a.device)
    byte_ppl = token_ppl ** (len(ids) / N_BAJTOW)
    res = {"benchmark": "W byte-PPL PL (track.fabryka.ai board_pl/byte_ppl)",
           "protocol": "glint compute_perplexity: okna 256, reset kontekstu; byte_ppl = token_ppl^(tokeny/bajty)",
           "model": a.model or a.gollem_v6, "revision": a.revision, "device": a.device,
           "params": sum(p.numel() for p in model.parameters()),
           "dataset": f"{DANE[0]}/{DANE[1]}@{DANE[2]}", "sha256": sha, "bajty": N_BAJTOW, "tokeny": len(ids),
           "token_ppl": round(token_ppl, 6), "byte_ppl": round(byte_ppl, 6), "sekundy": int(time.time() - t)}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(f"W: byte_ppl {byte_ppl:.6f} (token_ppl {token_ppl:.6f}, {len(ids)} tokenow, {N_BAJTOW} B), {res['sekundy']} s")
    print("zapisano", a.out)


if __name__ == "__main__":
    main()
