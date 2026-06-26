"""구조적 해결: 정본 각 파일의 '본문출처' 메타(제목·DOI·저자줄)를 manifest로.
파일명은 불투명 ID(그림슬러그와 묶임)로 두고, 조회/갭점검은 이 manifest로. 결정론적 $0."""
import os, re, glob, json, sys
sys.stdout.reconfigure(encoding="utf-8")
CORPUS = r"G:\corpus_20260624\articles"
DOIre = re.compile(r"10\.\d{4,9}/[A-Za-z0-9._;()/:+\-]+")
def clean_title(s):
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)   # [text](url) -> text
    s = re.sub(r"https?://\S+", "", s)
    s = re.sub(r"<[^>]+>", "", s)                     # <sub> 등
    s = re.sub(r"\(#[^)]*\)|\[|\]", "", s)
    return re.sub(r"\s+", " ", s).strip()

man = []; n_title = n_doi = 0
for f in sorted(glob.glob(os.path.join(CORPUS, "*.md"))):
    try: t = open(f, encoding="utf-8", errors="replace").read(4000)
    except: continue
    # H1 = 본문 제목 (노이즈 H1은 다음 H1로 폴백)
    h1s = re.findall(r"^#\s+(.+)$", t, re.M)
    title = ""
    for h in h1s:
        c = clean_title(h)
        if len(re.findall(r"[가-힣a-z]{3,}", c.lower())) >= 3 and not re.match(
           r"^(article|chapter|index|abstract|introduction|references|scientific|technical)\b", c, re.I):
            title = c; break
    if not title and h1s: title = clean_title(h1s[0])
    dm = DOIre.search(t)
    doi = re.sub(r"[).,;\]>]+$", "", dm.group(0)) if dm else ""
    if title: n_title += 1
    if doi: n_doi += 1
    man.append({"file": os.path.basename(f), "title": title, "doi": doi})

json.dump(man, open(r"G:\corpus_20260624\CORPUS_MANIFEST.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"정본 {len(man)}편 → CORPUS_MANIFEST.json (G:\\corpus_20260624\\)")
print(f"  본문제목 추출: {n_title} ({100*n_title//len(man)}%)")
print(f"  본문 DOI 추출: {n_doi} ({100*n_doi//len(man)}%)")
print("\n=== 샘플 5 (파일명 != 제목인 케이스 위주) ===")
shown = 0
for m in man:
    if shown >= 6: break
    if not m["file"][:6].lower() in m["title"].lower().replace(" ","")[:6] or m["file"].startswith("1-s2"):
        print(f"  파일: {m['file'][:45]}")
        print(f"   제목: {m['title'][:70]}")
        print(f"   DOI : {m['doi'] or '없음'}\n"); shown += 1
