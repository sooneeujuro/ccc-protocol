"""Safe holdout content verification for book sidecar gold.

Reads local book markdown but writes only counts, hashes, booleans, and enum-like
judgments. No source prose, headings, table cells, captions, or resolved values.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

BOOK_ROOT = Path(r"G:\books_v5_out")
SCRIPT_DIR = Path(__file__).resolve().parent
SEGMENT_MANIFEST = SCRIPT_DIR / "BOOK_SEGMENT_MANIFEST_v1_codex.jsonl"
HOLDOUT = SCRIPT_DIR / "BOOK_HOLDOUT_gold_v0.jsonl"
OUT = SCRIPT_DIR / "BOOK_HOLDOUT_VERIFY_v1_codex.safe.json"


PATTERNS = {
    "topic_geochronology": [
        r"\bgeochronolog", r"\bchronometer", r"\bdating\b", r"\bage determination\b",
        r"\bisochron\b", r"\bu[-\s]?pb\b", r"\brb[-\s]?sr\b", r"\bsm[-\s]?nd\b",
    ],
    "topic_radiogenic_decay": [
        r"\bradioactive\b", r"\bradiogenic\b", r"\bdecay\b", r"\bhalf[-\s]?life\b",
        r"\bparent\b", r"\bdaughter\b", r"\batomic\b", r"\bisotope\b",
    ],
    "topic_isotope_fractionation": [
        r"\bfractionation\b", r"\bkinetic isotope\b", r"\bequilibrium isotope\b",
        r"\bd13c\b", r"\bd18o\b", r"\bdelta\b",
    ],
    "topic_equation_of_state": [
        r"\bequation of state\b", r"\bthermodynamic\b", r"\bgibbs\b", r"\bteos\b",
        r"\bequation\b",
    ],
    "topic_noble_gas_solubility": [
        r"\bsolubility\b", r"\bnoble gas\b", r"\bhenry\b", r"\baqueous\b",
        r"\bgas[-\s]?water\b",
    ],
    "method_solubility_model": [
        r"\bsolubility\b", r"\bhenry\b", r"\bmodel\b", r"\baqueous\b",
    ],
    "method_thermodynamic_model": [
        r"\bthermodynamic\b", r"\bequation of state\b", r"\bgibbs\b", r"\bmodel\b",
    ],
    "method_isochron": [
        r"\bisochron\b",
    ],
    "method_sims": [
        r"\bsims\b", r"\bion microprobe\b",
    ],
    "reference_table": [
        r"^\s*\|.*\|\s*$",
    ],
    "equation": [
        r"\$",
    ],
    "solubility_table": [
        r"\bsolubility\b", r"\bhenry\b", r"\bgas[-\s]?water\b", r"\baqueous\b",
    ],
    "thermodynamic_relation": [
        r"\bthermodynamic\b", r"\bequation of state\b", r"\bgibbs\b",
    ],
}


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def sha_prefix(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:16]


def count_patterns(text: str, ids: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for topic_id in ids:
        pats = PATTERNS.get(topic_id, [])
        out[topic_id] = sum(len(re.findall(pat, text, re.IGNORECASE | re.MULTILINE)) for pat in pats)
    return out


def main() -> int:
    segments = {row["segment_id"]: row for row in load_jsonl(SEGMENT_MANIFEST)}
    holdouts = load_jsonl(HOLDOUT)
    rows = []
    for holdout in holdouts:
        seg = segments[holdout["segment_id"]]
        book_dir = BOOK_ROOT / seg["book_slug"]
        md_files = sorted(book_dir.glob("*.md"))
        if not md_files:
            raise RuntimeError(f"missing md for {seg['book_slug']}")
        lines = md_files[0].read_text(encoding="utf-8", errors="replace").splitlines()
        chunk = "\n".join(lines[seg["line_start"]:seg["line_end"]])
        expected = holdout["expected"]
        required_topics = expected.get("topics_norm_required") or []
        soft_topics = expected.get("topics_norm_soft_required") or []
        soft_forbidden_topics = expected.get("topics_norm_soft_forbidden") or []
        required_methods = expected.get("methods_norm_required") or []
        soft_methods = expected.get("methods_norm_soft_required") or []
        required_refs = expected.get("reference_kind_required") or []
        check_ids = sorted(set(
            required_topics + soft_topics + soft_forbidden_topics
            + required_methods + soft_methods + required_refs
            + seg["topics_norm_candidates"] + seg["methods_norm_candidates"] + seg["reference_kind_candidates"]
        ))
        counts = count_patterns(chunk, check_ids)
        topic_required_support = {k: counts.get(k, 0) for k in required_topics}
        topic_soft_required_support = {k: counts.get(k, 0) for k in soft_topics}
        topic_soft_forbidden_support = {k: counts.get(k, 0) for k in soft_forbidden_topics}
        method_required_support = {k: counts.get(k, 0) for k in required_methods}
        method_soft_required_support = {k: counts.get(k, 0) for k in soft_methods}
        ref_required_support = {k: counts.get(k, 0) for k in required_refs}
        rows.append({
            "holdout_id": holdout["holdout_id"],
            "segment_id_hash": sha_prefix(holdout["segment_id"]),
            "book_id_hash": sha_prefix(holdout["book_id"]),
            "segment_line_count": seg["line_count"],
            "page_range": seg["page_range"],
            "segment_method": seg["segment_method"],
            "segment_confidence": seg["segment_confidence"],
            "segment_type": seg["segment_type"],
            "topic_required_support_counts": topic_required_support,
            "topic_soft_required_support_counts": topic_soft_required_support,
            "topic_soft_forbidden_support_counts": topic_soft_forbidden_support,
            "method_required_support_counts": method_required_support,
            "method_soft_required_support_counts": method_soft_required_support,
            "reference_required_support_counts": ref_required_support,
            "candidate_support_counts": counts,
            "topic_required_zero_support_count": sum(1 for v in topic_required_support.values() if v == 0),
            "topic_soft_required_zero_support_count": sum(1 for v in topic_soft_required_support.values() if v == 0),
            "topic_soft_forbidden_positive_count": sum(1 for v in topic_soft_forbidden_support.values() if v > 0),
            "method_required_zero_support_count": sum(1 for v in method_required_support.values() if v == 0),
            "method_soft_required_zero_support_count": sum(1 for v in method_soft_required_support.values() if v == 0),
            "reference_required_zero_support_count": sum(1 for v in ref_required_support.values() if v == 0),
            "chunk_sha256_prefix": sha_prefix(chunk),
        })

    summary = {
        "schema": "book_holdout_verify_v1_codex_safe",
        "holdout_count": len(rows),
        "topic_required_zero_support_total": sum(r["topic_required_zero_support_count"] for r in rows),
        "topic_soft_required_zero_support_total": sum(r["topic_soft_required_zero_support_count"] for r in rows),
        "topic_soft_forbidden_positive_total": sum(r["topic_soft_forbidden_positive_count"] for r in rows),
        "method_required_zero_support_total": sum(r["method_required_zero_support_count"] for r in rows),
        "method_soft_required_zero_support_total": sum(r["method_soft_required_zero_support_count"] for r in rows),
        "reference_required_zero_support_total": sum(r["reference_required_zero_support_count"] for r in rows),
        "raw_text_written": False,
        "heading_text_written": False,
        "table_cell_text_written": False,
        "resolved_numeric_values_written": False,
        "rows": rows,
    }
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "holdout_count": summary["holdout_count"],
        "topic_required_zero_support_total": summary["topic_required_zero_support_total"],
        "topic_soft_required_zero_support_total": summary["topic_soft_required_zero_support_total"],
        "topic_soft_forbidden_positive_total": summary["topic_soft_forbidden_positive_total"],
        "method_required_zero_support_total": summary["method_required_zero_support_total"],
        "method_soft_required_zero_support_total": summary["method_soft_required_zero_support_total"],
        "reference_required_zero_support_total": summary["reference_required_zero_support_total"],
        "sha256_prefix": sha_prefix(OUT.read_text(encoding="utf-8")),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
