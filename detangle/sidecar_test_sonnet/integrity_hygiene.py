# -*- coding: utf-8 -*-
"""③④⑤ 위생: INTEGRITY.json 생성 + CORPUS_VERSION 키보강·절대경로제거 + manifest units_path 상대화."""
import os, json, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = sys.argv[1] if len(sys.argv) > 1 else r"G:\corpus_20260626"
IDX = os.path.join(ROOT, "index")
def sha1f(p):
    h = hashlib.sha1()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

cvp = os.path.join(ROOT, "CORPUS_VERSION.json")
cv = json.load(open(cvp, encoding="utf-8"))
units = os.path.join(IDX, "retrieval_units.jsonl")
usha = sha1f(units)
ucount = cv.get("retrieval_units")

# ③ INTEGRITY.json (배포 자동검증용)
integ = {
    "units_count": ucount,
    "units_sha1": usha,
    "bm25_doc_count": ucount,            # bm25 indexed over retrieval_units (1:1)
    "embedding_rows": cv.get("dense_embedding_count"),
    "embedding_dim": cv.get("dense_embedding_dim"),
    "built_at": cv.get("updated_by_codex_at"),
    "corpus_version": cv.get("corpus_version"),
}
json.dump(integ, open(os.path.join(ROOT, "INTEGRITY.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ⑤ CORPUS_VERSION 키보강 + ④ 절대경로 제거
cv["corpus_version_date"] = cv.get("corpus_version")
cv["corpus_units_sha1"] = usha
cv["integrity"] = "INTEGRITY.json"
cv["citation_index"] = "citation_index.json"
cv["pdf_manifest"] = "pdf_manifest.json"
cv["sidecar_year_normalized"] = True
removed = [k for k in ("c_drive_clone", "g_drive_canonical") if k in cv]
for k in removed: cv.pop(k)
json.dump(cv, open(cvp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ④ manifest units_path 상대화 (그 키만 안전하게)
mp = os.path.join(IDX, "embeddings_bge_m3.manifest.json")
mfix = []
if os.path.exists(mp):
    m = json.load(open(mp, encoding="utf-8"))
    for k, v in list(m.items()):
        if isinstance(v, str) and ("\\" in v or (len(v) > 2 and v[1] == ":")):
            base = os.path.basename(v.replace("\\", "/"))
            m[k] = "index/" + base if base.endswith((".jsonl", ".npy", ".pkl")) else base
            mfix.append(k)
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

print(f"③ INTEGRITY.json: units_sha1={usha[:16]}… / units={ucount} / emb={integ['embedding_rows']}x{integ['embedding_dim']} / built_at={integ['built_at']}")
print(f"⑤ CORPUS_VERSION +keys: corpus_version_date={cv['corpus_version_date']}, corpus_units_sha1, integrity, citation_index, pdf_manifest, sidecar_year_normalized")
print(f"④ 절대경로 제거: CORPUS_VERSION {removed} / manifest units-keys {mfix}")
