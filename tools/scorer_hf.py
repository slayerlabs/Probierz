# -*- coding: utf-8 -*-
"""
scorer_hf.py — policzy oceny (log-likelihood) DOWOLNEGO gotowego modelu Hugging Face
dla par z eval.jsonl i zapisze plik --ll-file, ktory potem czyta run_forced_choice.py.

Uzycie:
  python tools/scorer_hf.py --model <id-lub-sciezka-HF> --eval benchmarks/d3-skladnia-v2/eval.jsonl --out moje_oceny.jsonl
  python tools/run_forced_choice.py --eval benchmarks/d3-skladnia-v2/eval.jsonl --scorer logprob --ll-file moje_oceny.jsonl --model <nazwa> --outdir wynik/

Dziala z KAZDYM modelem AutoModelForCausalLM (GPT, Llama, Qwen, Bielik, nasze 8m/16m/32m, ...).
Liczy sume log-prawdopodobienstwa tekstu (teacher forcing). Wyzej = model uwaza tekst za bardziej naturalny.
"""
import argparse, json, math
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def total_ll(model, tok, text, device):
    ids = tok(text, return_tensors="pt").input_ids.to(device)
    if ids.shape[1] < 2:                       # za krotkie na warunkowanie
        ids = torch.cat([torch.tensor([[tok.bos_token_id or tok.eos_token_id or 0]], device=device), ids], dim=1)
    with torch.no_grad():
        logits = model(ids).logits             # [1, T, V]
    logp = torch.log_softmax(logits[:, :-1, :].float(), dim=-1)
    tgt = ids[:, 1:]                            # nastepny token
    ll = logp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1).sum().item()
    return ll                                  # log-likelihood (natural log), wyzej=lepiej

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="HF model id albo lokalna sciezka")
    ap.add_argument("--eval", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--device", default="cpu", help="cpu albo cuda")
    ap.add_argument("--dtype", default="float32", choices=["float32","float16","bfloat16"])
    a = ap.parse_args()
    dtype = getattr(torch, a.dtype)
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, torch_dtype=dtype).to(a.device).eval()
    items = [json.loads(l) for l in open(a.eval, encoding="utf-8") if l.strip()]
    n = 0
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        for it in items:
            d = total_ll(model, tok, it["dobre"], a.device)
            z = total_ll(model, tok, it["zle"], a.device)
            f.write(json.dumps({"id": it["id"], "dobre_ll": round(d, 4), "zle_ll": round(z, 4)}, ensure_ascii=False) + "\n")
            n += 1
    print(f"OK: policzono {n} par -> {a.out} (model={a.model})")

if __name__ == "__main__":
    main()
