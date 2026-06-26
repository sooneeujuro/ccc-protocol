"""확정 누락 리스트: 전 풀의 본문 H1 제목이 정본 '본문 content'에 있나(파일명 무시, 한글 포함).
없는 것만 = 진짜 누락. 출처 MD경로 + DOI 부착."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"G:\corpus_20260624\articles"
POOLS = {
 "Q_dup20260602": r"G:\corpus_md_export_20260602\articles\_duplicates_quarantine",
 "Q_newdup20260609": r"G:\corpus_md_export_20260602\_renewal_20260609\_new_dup_quarantine",
 "Q_20260612": r"G:\corpus_md_export_20260612\quarantine",
 "v20260602": r"G:\corpus_md_export_20260602\articles",
 "v20260610": r"G:\corpus_md_export_20260610\articles",
 "v20260612": r"G:\corpus_md_export_20260612\articles",
 "Atelier_pilot": r"G:\Atelier_Handoff_2026-05-19_full_corpus\article_corpus\pilot",
 "PaperAtelier": r"G:\Paper_Atelier\datalab\pilot",
}
NOISE = re.compile(r"^(article|articles|volcanology|geochemistry|chemical geodynamics|earth sciences|"
   r"index|preface|references|acknowledg|abstract|introduction|chapter\s*\d*|epsl|scientific reports|"
   r"technical reports|unknown|references and notes|geochemical perspectives|nature|science|supplement|"
   r"\d+|\W*)$", re.I)
TOK = re.compile(r"[가-힣a-z0-9]{2,}")
STOP = set("the of and in a to for on with from by an at as is are this".split())
DOIre = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def h1(path, n=1800):
    try: t = open(path, encoding="utf-8", errors="replace").read(n)
    except: return ""
    m = re.search(r"^#\s+(.+)$", t, re.M); return (m.group(1) if m else "").strip()
def toks(s): return frozenset(x for x in TOK.findall(s.lower()) if x not in STOP and not x.isdigit())

# 정본 content 인덱스 (head 4500자 = 제목+초록, 한글포함)
print("정본 content 인덱스...", flush=True)
heads = []; inv = {}
for f in glob.glob(os.path.join(CORPUS, "*.md")):
    try: t = open(f, encoding="utf-8", errors="replace").read(4500)
    except: continue
    tk = toks(t); i = len(heads); heads.append((os.path.basename(f), tk))
    for w in tk: inv.setdefault(w, []).append(i)
print(f"  정본 {len(heads)}편\n", flush=True)

def present(cand):
    if len(cand) < 4: return (0.0, None)
    c = {}
    for w in cand:
        for i in inv.get(w, []): c[i] = c.get(i,0)+1
    best = (0.0, None)
    for i, sh in sorted(c.items(), key=lambda x:-x[1])[:30]:
        ov = len(cand & heads[i][1]) / len(cand)   # 후보 제목어가 정본 doc head에 얼마나 들어있나
        if ov > best[0]: best = (ov, heads[i][0])
        if best[0] >= 0.9: break
    return best

missing = {}
for name, d in POOLS.items():
    if not os.path.isdir(d): continue
    for f in glob.glob(os.path.join(d, "*.md")):
        ti = h1(f)
        if not ti or NOISE.match(ti): continue
        cand = toks(ti)
        if len(cand) < 4: continue
        ov, cm = present(cand)
        if ov < 0.85:
            key = " ".join(sorted(cand))[:60]
            if key not in missing:
                # DOI 시도
                try: full = open(f, encoding="utf-8", errors="replace").read(6000)
                except: full = ""
                dm = DOIre.search(full)
                missing[key] = {"title": ti[:90], "pools": [name], "src": f,
                                "doi": (dm.group(0) if dm else ""), "best_ov": round(ov,2), "near": cm}
            elif name not in missing[key]["pools"]:
                missing[key]["pools"].append(name)

ms = sorted(missing.values(), key=lambda x:-x["best_ov"])
print(f"=== 정본 본문에 없음(확정 누락 후보): {len(ms)} ===\n")
for m in ms:
    print(f"  ✗ {m['title']}")
    print(f"     pools={m['pools']} doi={m['doi'] or '없음'} (정본최근접 ov={m['best_ov']}: {m['near']})")
json.dump(ms, open(r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\DEFINITIVE_MISSING.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n→ DEFINITIVE_MISSING.json ({len(ms)}편)")
