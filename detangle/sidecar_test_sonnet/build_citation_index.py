"""build_citation_index.py — corpus citation-graph builder (year-fallback, portable).

Resolves each sidecar's references[] to in-corpus paper_ids via:
  - DOI-exact match, then
  - fuzzy (first-author surname + publication year + title Jaccard >= TH).
Emits the citation graph {corpus, n_papers, doi_index, cites, cited_by}.

WHY THIS VERSION (vs the original corpus-atelier builder):
  1. YEAR FALLBACK — 2026-06+ sidecars carry `year_print` / `year_online` instead of a
     bare `year` key. The original reads only bibliographic.year, so its fuzzy pass
     silently collapsed to 0 matches (article corpus: 1296 linked papers, DOI-only).
     This version falls back to year_print/year_online on BOTH the target-index and the
     reference side, restoring fuzzy → 3316 linked papers (83%) on corpus_20260626.
  2. PORTABLE SIDECAR PATH — reads <root>/sidecars (current bundle layout) and also
     auto-falls back to <root>/article_corpus/sidecars (old layout). No symlink hack.
  3. MULTI-CORPUS TARGET SPACE — pass several sidecar dirs to build one shared target
     index. Use `--sidecars <article_sidecars> <book_sidecars>` to make BOOKS first-class
     citation TARGETS (papers that cite Rudnick&Gao 2003, Faure&Mensing, etc. resolve to
     the book node instead of dangling out-of-corpus).

USAGE:
  python build_citation_index.py CORPUS_ROOT
      # reads CORPUS_ROOT/sidecars, writes CORPUS_ROOT/citation_index.json
  python build_citation_index.py --sidecars DIR1 [DIR2 ...] --out OUT.json [--corpus-label L]
      # explicit dirs; multiple dirs => shared target space (article + book).

No third-party deps (stdlib only). Python 3.8+.
"""
import argparse, json, os, re, sys, unicodedata
from collections import defaultdict

TH = 0.34  # title Jaccard threshold for a fuzzy match
STOP = set("the of a an and or in on for to from with by at as is are study using "
           "based new isotopic isotope".split())


def ndoi(d):
    if not d:
        return ""
    d = str(d).strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    return d.strip().strip(".")


def alow(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()


def surname(a):
    if isinstance(a, list):
        a = a[0] if a else ""
    a = str(a).split(",")[0].strip()
    t = a.split()
    a = t[0] if t else a
    return re.sub(r"[^a-z]", "", alow(a))


def yint(y):
    try:
        return int(str(y)[:4])
    except Exception:
        return None


def bibof(d):
    b = d.get("bibliographic")
    return b if isinstance(b, dict) else {}


def byear(d):  # year fallback — TARGET (in-corpus paper) side
    b = bibof(d)
    return yint(b.get("year") or b.get("year_print") or b.get("year_online") or d.get("year"))


def ryear(r):  # year fallback — REFERENCE side
    return yint(r.get("year") or r.get("year_print") or r.get("year_online"))


def title_of(d):
    return bibof(d).get("title") or d.get("title") or ""


def first_author(d):
    au = bibof(d).get("authors_full") or d.get("authors") or []
    if isinstance(au, list):
        return au[0] if au else ""
    return au if isinstance(au, str) else ""


def toks(t):
    return set(w for w in re.findall(r"[a-z0-9]+", alow(t)) if w not in STOP and len(w) > 2)


def sim(a, b):
    A, B = toks(a), toks(b)
    return (len(A & B) / len(A | B)) if (A and B) else 0.0


def load_sidecars(dirs):
    """Return {paper_id: sidecar_dict}. Keyed by paper_id for global uniqueness across dirs."""
    side = {}
    for sd in dirs:
        if not os.path.isdir(sd):
            print(f"  WARN: sidecar dir not found: {sd}", file=sys.stderr)
            continue
        n = 0
        for fn in os.listdir(sd):
            if not fn.endswith(".json") or fn == "_batch_state.json":
                continue
            try:
                d = json.load(open(os.path.join(sd, fn), encoding="utf-8"))
            except Exception:
                continue
            if isinstance(d, dict):
                pid = d.get("id") or fn[:-5]
                side[pid] = d  # later dir wins on pid collision (dedup)
                n += 1
        print(f"  loaded {n} sidecars from {sd}", file=sys.stderr)
    return side


def resolve_sidecar_dirs(corpus_root):
    for cand in (os.path.join(corpus_root, "sidecars"),
                 os.path.join(corpus_root, "article_corpus", "sidecars")):
        if os.path.isdir(cand):
            return [cand]
    return [os.path.join(corpus_root, "sidecars")]


def build(side, corpus_label):
    # target index
    doi2pid, ay, ptitle = {}, defaultdict(list), {}
    for pid, d in side.items():
        ptitle[pid] = title_of(d)
        dd = ndoi(d.get("doi"))
        if dd:
            doi2pid.setdefault(dd, pid)
        sn, y = surname(first_author(d)), byear(d)
        if sn and y:
            ay[(sn, y)].append(pid)
    # resolve references
    cites = defaultdict(list)
    sd_doi = sd_fz = tot = 0
    for pid, d in side.items():
        refs = d.get("references") or []
        if not isinstance(refs, list):
            continue
        for i, r in enumerate(refs):
            if not isinstance(r, dict):
                continue
            tot += 1
            to = mth = sc = None
            dd = ndoi(r.get("doi"))
            if dd and dd in doi2pid:
                to, mth, sc = doi2pid[dd], "doi", 1.0
            else:
                sn, ry = surname(r.get("authors")), ryear(r)
                cands = ay.get((sn, ry), []) if (sn and ry) else []
                if cands:
                    rt = r.get("title") or ""
                    best, bs = None, 0.0
                    for c in cands:
                        s = sim(rt, ptitle.get(c, ""))
                        if s > bs:
                            bs, best = s, c
                    if best and bs >= TH:
                        to, mth, sc = best, "fuzzy", round(bs, 3)
            if to and to != pid:
                cites[pid].append({"idx": i, "to": to, "method": mth, "score": sc})
                sd_doi += (mth == "doi")
                sd_fz += (mth == "fuzzy")
    cited_by = defaultdict(set)
    for p, lst in cites.items():
        for e in lst:
            cited_by[e["to"]].add(p)
    out = {
        "corpus": corpus_label,
        "n_papers": len(side),
        "doi_index": len(doi2pid),
        "cites": dict(cites),
        "cited_by": {p: sorted(s) for p, s in cited_by.items()},
    }
    return out, tot, sd_doi, sd_fz


def main():
    ap = argparse.ArgumentParser(description="citation-graph builder (year-fallback, portable)")
    ap.add_argument("corpus_root", nargs="?",
                    help="corpus root; reads <root>/sidecars, writes <root>/citation_index.json")
    ap.add_argument("--sidecars", nargs="+",
                    help="explicit sidecar dir(s); multiple => shared target space (article + book)")
    ap.add_argument("--out", help="output path (default <corpus_root>/citation_index.json)")
    ap.add_argument("--corpus-label", default=None, help="value of the output's 'corpus' field")
    a = ap.parse_args()

    if a.sidecars:
        dirs = a.sidecars
        out_path = a.out or "citation_index.json"
        label = a.corpus_label or os.path.dirname(os.path.abspath(out_path))
    elif a.corpus_root:
        dirs = resolve_sidecar_dirs(a.corpus_root)
        out_path = a.out or os.path.join(a.corpus_root, "citation_index.json")
        label = a.corpus_label or a.corpus_root
    else:
        ap.error("give CORPUS_ROOT or --sidecars")

    side = load_sidecars(dirs)
    out, tot, sd_doi, sd_fz = build(side, label)
    json.dump(out, open(out_path, "w", encoding="utf-8"), ensure_ascii=False)
    res = sd_doi + sd_fz
    pw = sum(1 for p in out["cites"] if out["cites"][p])
    print("refs %d | resolved %d (doi %d + fuzzy-title %d) = %.1f%% | papers with link %d (%.1f%%)"
          % (tot, res, sd_doi, sd_fz, 100.0 * res / max(tot, 1), pw, 100.0 * pw / max(len(side), 1)))
    print("wrote %s (%.0f KB)" % (out_path, os.path.getsize(out_path) / 1024.0))


if __name__ == "__main__":
    main()
