"""step1-3: 0612 vs 0624 MD prose 비교 → reuse/재추출 분리 + 0624기준 재추출 리스트.
prose-hash = 그림ref 제거 + 공백정규화 후 sha1 (그림격리 차이 무시, 실제 텍스트 차이만 감지)."""
import json, os, glob, re, hashlib, sys
sys.stdout.reconfigure(encoding="utf-8")
A0612 = r"C:\Users\USER\corpus_md_export_20260612\articles"
A0624 = r"G:\corpus_20260624\articles"
QUAR  = r"C:\Users\USER\corpus_md_export_20260612\sidecars_v22_QUARANTINE_oldinput_20260625"
SF    = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"

IMG = re.compile(r"!\[[^\]]*\]\([^)]*\)")          # 그림 markdown(슬러그/해시 파일명 포함)
ALNUM = re.compile(r"[a-z]+")                       # 알파벳 단어만(hex/숫자 토큰=슬러그·해시 오염 배제)
def prose_hash(path):
    try: t = open(path, encoding="utf-8", errors="replace").read()
    except: return None
    t = IMG.sub(" ", t)                             # ① 그림ref 통째 제거(파일명 슬러그/해시 제거)
    words = ALNUM.findall(t.lower())                # ② 알파벳 단어만(혹시 남은 hex/숫자도 배제)
    return hashlib.sha1(" ".join(words).encode("utf-8")).hexdigest()

# 0624 정본: prose_hash -> [filenames]
print("0624 정본 prose 해싱...", flush=True)
h0624 = {}
for f in glob.glob(os.path.join(A0624, "*.md")):
    h = prose_hash(f)
    if h: h0624.setdefault(h, []).append(os.path.basename(f))
print(f"  0624 articles {sum(len(v) for v in h0624.values())} | 고유 prose {len(h0624)}", flush=True)

# done sidecar(2161)의 source(0612 MD) prose
print("done sidecar의 0612 source 해싱...", flush=True)
done_src_hash = {}   # pid -> prose_hash(0612 MD)
covered_hashes = set()
miss_src = 0
for sc in glob.glob(os.path.join(QUAR, "*.json")):
    pid = os.path.basename(sc)[:-5]
    md = os.path.join(A0612, pid + ".md")
    if not os.path.exists(md): miss_src += 1; continue
    h = prose_hash(md)
    done_src_hash[pid] = h
    if h in h0624: covered_hashes.add(h)
print(f"  done {len(done_src_hash)} (source MD 없음 {miss_src})", flush=True)

# 분류
reuse = [pid for pid, h in done_src_hash.items() if h in h0624]       # 0612 MD == 0624 MD = 인벤토리 유효
contaminated = [pid for pid, h in done_src_hash.items() if h not in h0624]  # 0612 MD가 정본에 없음 = 오염우려
# 0624 기준 재추출 대상 = 정본 MD 중 done에 안 잡힌 prose
done_hashes = set(done_src_hash.values())
reextract_0624 = []
for h, names in h0624.items():
    if h not in done_hashes:
        reextract_0624.extend(names)

print(f"\n=== 결과 ===")
print(f"done sidecar {len(done_src_hash)}편:")
print(f"  ① reuse 가능(0612==0624 prose): {len(reuse)}")
print(f"  ② 오염우려(0612 MD가 정본에 없음→재추출): {len(contaminated)}")
print(f"0624 정본 {sum(len(v) for v in h0624.values())}편 중:")
print(f"  covered(done가 커버, reuse): {len(covered_hashes)} 고유")
print(f"  ★재추출 필요(0624에 있는데 sidecar 없음/다름): {len(reextract_0624)}")
json.dump({"reuse": reuse, "contaminated": contaminated, "reextract_0624_mds": reextract_0624},
          open(os.path.join(SF, "MD_VERSION_DIFF.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("→ MD_VERSION_DIFF.json")
