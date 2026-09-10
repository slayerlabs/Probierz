
"""run_forced_choice.py - runner par minimalnych (forced-choice) dla byte-LM. Probierz d3-skladnia.
Wynik itemu: pass iff LL(dobre) > LL(zle) (rownowaznie bits(dobre) < bits(zle)). chance=0.50.
Raportuje tez margines znormalizowany bajtowo (bits/len) - odejmuje confound dlugosci.
Scorery:
  --scorer ngram --fit <txt> --maxorder K [--panel]  : bajtowy n-gram add-alpha, fit z korpusu; panel = rzedy 1..K.
  --scorer logprob --ll-file <jsonl>                 : zewnetrzny model; jsonl {"id":..,"dobre_ll":..,"zle_ll":..} (LL, wyzej=lepiej).
Wyjscie: wyniki-<model>.json (summary/per_zjawisko/per_poziom/results) w katalogu --outdir.
"""
import argparse, json, math, os, random, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

def fit_ngram(path, maxo):
    data=open(path,"rb").read()
    ctx=[dict() for _ in range(maxo+1)]; jnt=[dict() for _ in range(maxo+1)]
    p1=p2=p3=p4=0; have=0
    for b in data:
        c=0; ctx[0][c]=ctx[0].get(c,0)+1; jnt[0][b]=jnt[0].get(b,0)+1
        if have>=1 and maxo>=1:
            c=p1; ctx[1][c]=ctx[1].get(c,0)+1; jnt[1][c*256+b]=jnt[1].get(c*256+b,0)+1
        if have>=2 and maxo>=2:
            c=p1+256*p2; ctx[2][c]=ctx[2].get(c,0)+1; jnt[2][c*256+b]=jnt[2].get(c*256+b,0)+1
        if have>=3 and maxo>=3:
            c=p1+256*p2+65536*p3; ctx[3][c]=ctx[3].get(c,0)+1; jnt[3][c*256+b]=jnt[3].get(c*256+b,0)+1
        if have>=4 and maxo>=4:
            c=p1+256*p2+65536*p3+16777216*p4; ctx[4][c]=ctx[4].get(c,0)+1; jnt[4][c*256+b]=jnt[4].get(c*256+b,0)+1
        p4=p3;p3=p2;p2=p1;p1=b; have=min(have+1,4)
    return ctx,jnt

def bits(s, o, ctx, jnt, alpha=0.05, V=256):
    D=s.encode("utf-8"); tot=0.0; p1=p2=p3=p4=0; i=0
    for b in D:
        ou=min(i,o)
        if ou==0: c=0
        elif ou==1: c=p1
        elif ou==2: c=p1+256*p2
        elif ou==3: c=p1+256*p2+65536*p3
        else: c=p1+256*p2+65536*p3+16777216*p4
        num=jnt[ou].get(c*256+b,0)+alpha; den=ctx[ou].get(c,0)+alpha*V
        tot += -math.log2(num/den)
        p4=p3;p3=p2;p2=p1;p1=b; i+=1
    return tot, len(D)

def score_items(items, scorefn):
    res=[]
    for it in items:
        bd,ld=scorefn(it["dobre"]); bz,lz=scorefn(it["zle"])
        # bits: lower=better -> LL(dobre)>LL(zle) == bd<bz
        margin=bz-bd                     # raw (bits), >0 = correct
        mnorm=(bz/lz)-(bd/ld)            # per-byte, >0 = correct
        res.append({"id":it["id"],"zjawisko":it["zjawisko"],"poziom":it["poziom_trudnosci"],
                    "bits_dobre":round(bd,3),"bits_zle":round(bz,3),
                    "margin_bits":round(margin,3),"margin_norm":round(mnorm,4),
                    "pass":bool(bd<bz),"pass_norm":bool(mnorm>0)})
    return res

def boot_ci(passes, iters=2000, seed=7):
    R=random.Random(seed); n=len(passes); vals=[]
    for _ in range(iters):
        s=sum(passes[R.randrange(n)] for _ in range(n)); vals.append(s/n)
    vals.sort(); return round(vals[int(0.025*iters)],3), round(vals[int(0.975*iters)],3)

def group_rate(res, key):
    g={}
    for r in res: g.setdefault(r[key],[]).append(1 if r["pass"] else 0)
    return {str(k):{"n":len(v),"acc":round(sum(v)/len(v),3)} for k,v in sorted(g.items())}

def summarize(res, model, evalpath):
    passes=[1 if r["pass"] else 0 for r in res]
    accn=sum(1 for r in res if r["pass_norm"])/len(res)
    lo,hi=boot_ci(passes)
    return {"summary":{"model":model,"eval":evalpath,"n_items":len(res),"chance":0.5,
                       "accuracy":round(sum(passes)/len(res),3),"accuracy_ci95":[lo,hi],
                       "accuracy_norm":round(accn,3)},
            "per_zjawisko":group_rate(res,"zjawisko"),"per_poziom":group_rate(res,"poziom"),
            "results":res}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--eval",required=True); ap.add_argument("--scorer",choices=["ngram","logprob"],default="ngram")
    ap.add_argument("--fit"); ap.add_argument("--maxorder",type=int,default=4); ap.add_argument("--order",type=int)
    ap.add_argument("--alpha",type=float,default=0.05); ap.add_argument("--ll-file")
    ap.add_argument("--model",default=None); ap.add_argument("--outdir",default=".")
    ap.add_argument("--panel",action="store_true")
    a=ap.parse_args()
    items=[json.loads(l) for l in open(a.eval,encoding="utf-8") if l.strip()]
    os.makedirs(a.outdir,exist_ok=True); panel={}
    if a.scorer=="logprob":
        ll={j["id"]:j for j in (json.loads(l) for l in open(a.ll_file,encoding="utf-8") if l.strip())}
        def sf(s, _id=None): raise RuntimeError("logprob uses precomputed")
        res=[]
        for it in items:
            j=ll[it["id"]]; bd=-j["dobre_ll"]; bz=-j["zle_ll"]
            res.append({"id":it["id"],"zjawisko":it["zjawisko"],"poziom":it["poziom_trudnosci"],
                        "bits_dobre":round(bd,3),"bits_zle":round(bz,3),"margin_bits":round(bz-bd,3),
                        "margin_norm":None,"pass":bool(bd<bz),"pass_norm":bool(bd<bz)})
        out=summarize(res,a.model or "logprob",a.eval)
        json.dump(out,open(os.path.join(a.outdir,f"wyniki-{out['summary']['model']}.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print(json.dumps(out["summary"],ensure_ascii=False)); return
    ctx,jnt=fit_ngram(a.fit,a.maxorder)
    orders=range(1,a.maxorder+1) if a.panel else [a.order or a.maxorder]
    for o in orders:
        res=score_items(items, lambda s,o=o: bits(s,o,ctx,jnt,a.alpha))
        model=f"ngram-o{o}"
        out=summarize(res,model,a.eval)
        json.dump(out,open(os.path.join(a.outdir,f"wyniki-{model}.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        panel[model]=out["summary"]
        print(f"{model}: acc={out['summary']['accuracy']} CI={out['summary']['accuracy_ci95']} acc_norm={out['summary']['accuracy_norm']}")
    if a.panel:
        json.dump(panel,open(os.path.join(a.outdir,"panel-summary.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
        print("PANEL_DONE chance=0.50")

if __name__=="__main__": main()
