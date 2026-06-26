# -*- coding: utf-8 -*-
"""0626 정본 빌드 (복제 0624->0626 완료 후 실행). 결정론적 $0.
 1) helium 19편: flat article + slug폴더(md+그림) + STEM_TO_SLUG 갱신
 2) sidecar 4014 정렬통합 -> 0626\sidecars\ (exact->rmap->norm->jaccard, 못잡으면 _orphan_no_article\)
 3) helium sidecar 19 -> 0626\sidecars\
 4) 리포트 + 검증
"""
import os, sys, json, re, shutil, hashlib
sys.stdout.reconfigure(encoding="utf-8")

BASE     = r"G:\corpus_20260626"
ART      = os.path.join(BASE, "articles")
IDX      = os.path.join(BASE, "index")
SIDE_OUT = os.path.join(BASE, "sidecars")
ORPHAN   = os.path.join(SIDE_OUT, "_orphan_no_article")
SIDE_SRC = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical"
RMAP_F   = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\SIDECAR_RENAME_MAP.json"
HELI_ART = r"G:\corpus_helium_add_20260626\articles"
HELI_SIDE= r"G:\corpus_helium_add_20260626\sidecars_final"
DERIVED  = r"G:\datalab_runs_v20260616\derived"
S2S      = os.path.join(IDX, "STEM_TO_SLUG.json")
REPORT   = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\BUILD_0626_REPORT.json"

assert os.path.isdir(ART), "0626\\articles 없음 (복제 미완)"
assert os.path.isdir(IDX), "0626\\index 없음 (복제 미완)"

# ---------- 1. helium 통합 ----------
s2s = json.load(open(S2S, encoding="utf-8"))
heli = [f[:-3] for f in os.listdir(HELI_ART) if f.endswith(".md")]
hn = himg = 0
for pp in heli:
    src_md = os.path.join(HELI_ART, pp + ".md")
    shutil.copy2(src_md, os.path.join(ART, pp + ".md"))          # flat view (검색/인덱스)
    slug = "helium_" + hashlib.md5(pp.encode("utf-8")).hexdigest()[:10]
    sd = os.path.join(BASE, slug); os.makedirs(sd, exist_ok=True)
    shutil.copy2(src_md, os.path.join(sd, slug + ".md"))          # slug 폴더 (그림뷰)
    dimg = os.path.join(DERIVED, pp.rstrip(" ."), "images")
    if os.path.isdir(dimg):
        for img in os.listdir(dimg):
            shutil.copy2(os.path.join(dimg, img), os.path.join(sd, img)); himg += 1
    s2s[pp] = slug; hn += 1
json.dump(s2s, open(S2S, "w", encoding="utf-8"), ensure_ascii=False)
print(f"[1] helium: {hn}편 flat+slug, 그림 {himg}장, STEM_TO_SLUG +{hn}")

# ---------- 2. 매칭 인덱스 ----------
art_set = set(f[:-3] for f in os.listdir(ART) if f.endswith(".md"))
def norm(s): return re.sub(r"[^a-z0-9가-힣]", "", s.lower())
art_norm = {}
for p in art_set:
    n = norm(p)
    if n and n not in art_norm: art_norm[n] = p
def toks(s): return [t for t in re.split(r"[^a-z0-9가-힣]+", s.lower()) if len(t) >= 3]
art_tok = {p: set(toks(p)) for p in art_set}
rmap = json.load(open(RMAP_F, encoding="utf-8")) if os.path.exists(RMAP_F) else {}

def years(s): return set(re.findall(r"(?:19|20)\d{2}", s))
def jaccard_best(spid):
    st = set(toks(spid)); tk = toks(spid)
    if not tk: return None
    a0 = tk[0]; sy = years(spid); best=None; bj=0.0
    for p, pt in art_tok.items():
        if a0 not in pt: continue
        py = years(p)
        if sy and py and not (sy & py): continue   # 연도 둘다 있는데 불일치 = 다른 논문/판 → 매핑 금지
        u = len(st | pt)
        if not u: continue
        j = len(st & pt) / u
        if j > bj: bj=j; best=p
    return best if bj >= 0.40 else None

# ---------- 3. sidecar 정렬통합 ----------
if os.path.isdir(SIDE_OUT): shutil.rmtree(SIDE_OUT)   # 재실행 멱등: 기존 sidecars 초기화
os.makedirs(SIDE_OUT, exist_ok=True); os.makedirs(ORPHAN, exist_ok=True)
n_exact=n_rmap=n_norm=n_jac=n_orph=0; orphans=[]; jacmap=[]
for fn in sorted(os.listdir(SIDE_SRC)):
    if not fn.endswith(".json"): continue
    spid = fn[:-5]; dest=None
    if spid in art_set: dest=spid; n_exact+=1
    elif spid in rmap and rmap[spid] in art_set: dest=rmap[spid]; n_rmap+=1
    elif norm(spid) in art_norm: dest=art_norm[norm(spid)]; n_norm+=1
    else:
        jb = jaccard_best(spid)
        if jb: dest=jb; n_jac+=1; jacmap.append((spid, jb))
    if dest:
        shutil.copy2(os.path.join(SIDE_SRC, fn), os.path.join(SIDE_OUT, dest + ".json"))
    else:
        shutil.copy2(os.path.join(SIDE_SRC, fn), os.path.join(ORPHAN, fn)); n_orph+=1; orphans.append(spid)

# ---------- 4. helium sidecar ----------
hs=0
for fn in os.listdir(HELI_SIDE):
    if fn.endswith(".json"):
        shutil.copy2(os.path.join(HELI_SIDE, fn), os.path.join(SIDE_OUT, fn)); hs+=1

# ---------- 5. 리포트/검증 ----------
side_n = len([f for f in os.listdir(SIDE_OUT) if f.endswith(".json")])
print(f"[3] sidecar: exact {n_exact} / rmap {n_rmap} / norm {n_norm} / jaccard {n_jac} / orphan {n_orph}")
print(f"[4] helium sidecar: {hs}")
print(f"    sidecars\\ 총 json = {side_n} (orphan 별도 {n_orph})")
print(f"\n[jaccard 자동매핑 {n_jac}건 — 확인]")
for s,d in jacmap: print(f"   {s[:44]}  ->  {d[:44]}")
print(f"\n[orphan {n_orph}편 — article 없음, _orphan_no_article\\ 보존]")
for o in orphans: print(f"   {o[:64]}")
# 검증: sidecars\ pid ⊆ art pid?
side_pids = set(f[:-5] for f in os.listdir(SIDE_OUT) if f.endswith(".json"))
notin = side_pids - art_set
print(f"\n[검증] sidecars\\ 중 article 없는 pid = {len(notin)} (0이어야 정상)")
for x in list(notin)[:10]: print("   !!", x[:60])
json.dump({"counts":{"exact":n_exact,"rmap":n_rmap,"norm":n_norm,"jaccard":n_jac,"orphan":n_orph,"helium":hs,"sidecars_total":side_n},
           "orphans":orphans,"jaccard":jacmap,"sidecar_not_in_articles":list(notin)},
          open(REPORT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n리포트 저장: {REPORT}")
