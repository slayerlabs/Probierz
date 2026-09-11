# -*- coding: utf-8 -*-
"""
bpb_scorer.py — bits-per-byte DOWOLNEGO modelu HF na wspolnym held-oucie.
BPB = tokenizer-fair: mianownik = BAJTY surowego tekstu (nie tokeny) -> jedna skala dla kazdego vocab.

Uzycie:
  python tools/bpb_scorer.py --model <id> --heldout heldout_bpb_sample.jsonl [--device cpu]
Wypisuje: BPB (bits/bajt), nizej=lepiej. Model losowy bajtowy = 8.0.
"""
import argparse, json, math
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--heldout", required=True)
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--dtype", default="float32")
    ap.add_argument("--max-tokens", type=int, default=1024)
    a = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(a.model)
    model = AutoModelForCausalLM.from_pretrained(a.model, dtype=getattr(torch, a.dtype)).to(a.device).eval()
    docs = [json.loads(l)["text"] for l in open(a.heldout, encoding="utf-8") if l.strip()]
    total_nats = 0.0; total_bytes = 0
    for text in docs:
        ids = tok(text, return_tensors="pt").input_ids[:, :a.max_tokens].to(a.device)
        if ids.shape[1] < 2:
            continue
        with torch.no_grad():
            logits = model(ids).logits
        logp = torch.log_softmax(logits[:, :-1, :].float(), dim=-1)
        tgt = ids[:, 1:]
        nats = logp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1).sum().item()   # sum log P (nats)
        total_nats += nats
        total_bytes += len(text.encode("utf-8"))
    bpb = -total_nats / math.log(2) / total_bytes
    print(json.dumps({"model": a.model, "bpb": round(bpb, 4), "docs": len(docs), "bytes": total_bytes}, ensure_ascii=False))

if __name__ == "__main__":
    main()
