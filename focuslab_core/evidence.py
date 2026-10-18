"""Small local lexical evidence retrieval (BM25-style, no external service)."""
import json, math, re
from collections import Counter
from .config import EVIDENCE_PATH

def tokenize(text):
    return re.findall(r"[a-z0-9]+", str(text).lower())

def load_entries(path=EVIDENCE_PATH):
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    if not isinstance(entries, list): raise ValueError("Evidence must be a list")
    ids = [e.get("id") for e in entries]
    if any(not x for x in ids) or len(ids) != len(set(ids)): raise ValueError("Evidence IDs must be present and unique")
    return entries

def retrieve_evidence(query, k=3, entries=None):
    entries = entries if entries is not None else load_entries()
    q = tokenize(query)
    if not q: return []
    docs=[]
    for entry in entries:
        passages = entry.get("passages") or [entry.get("summary", "")]
        text = " ".join([entry.get("title", ""), entry.get("summary", ""), *passages])
        toks = tokenize(text); docs.append((entry, toks, Counter(toks)))
    avgdl = sum(len(t) for _,t,_ in docs) / max(1,len(docs)); N=len(docs); df=Counter()
    for _, toks, _ in docs: df.update(set(toks))
    scored=[]
    for entry,toks,tf in docs:
        score=0.0
        for term in q:
            freq=tf[term]
            if not freq: continue
            idf=math.log(1+(N-df[term]+0.5)/(df[term]+0.5))
            denom=freq+1.5*(1-0.75+0.75*len(toks)/max(avgdl,1))
            score += idf*(freq*2.5/denom)
        if score > 0: scored.append((score,entry))
    scored.sort(key=lambda x:(-x[0],x[1]["id"]))
    return [{"id":e["id"],"title":e["title"],"sourceUrl":e["sourceUrl"],"summary":e["summary"],"passage":(e.get("passages") or [e["summary"]])[0],"limitations":e.get("limitations", ""),"score":round(s,4)} for s,e in scored[:max(0,k)]]

def validate_evidence_ids(ids, entries=None):
    known={e["id"] for e in (entries if entries is not None else load_entries())}
    if any(i not in known for i in ids): raise ValueError("Unknown evidence ID")
    return list(dict.fromkeys(ids))
