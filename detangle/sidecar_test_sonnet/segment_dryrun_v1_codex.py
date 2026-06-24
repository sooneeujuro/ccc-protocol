"""Book segmentation dry-run v1 (Codex).

Builds relay-safe segment metadata for book-sidecar holdout selection.
No source prose, headings, table cells, equations, or values are written.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

BOOK_ROOT = Path(r"G:\books_v5_out")
SCRIPT_DIR = Path(__file__).resolve().parent
OUT_MANIFEST = SCRIPT_DIR / "BOOK_SEGMENT_MANIFEST_v1_codex.jsonl"
OUT_SUMMARY = SCRIPT_DIR / "BOOK_SEGMENT_SUMMARY_v1_codex.safe.json"
OUT_HOLDOUT = SCRIPT_DIR / "BOOK_HOLDOUT_gold_v0.jsonl"

PROMPT_VERSION = "book_gemma_prompt_codex_v0"
NORMALIZER_VERSION = "book_norm_vocab_codex_v0"
SEGMENT_SCHEMA_VERSION = "book_segment_dryrun_v1_codex"

H12_RE = re.compile(r"^(#{1,2})\s+(.+?)\s*$", re.MULTILINE)
H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
H2_RE = re.compile(r"^##\s+\S", re.MULTILINE)
H3_RE = re.compile(r"^###\s+\S", re.MULTILINE)
TABLE_RE = re.compile(r"^\s*\|.*\|\s*$", re.MULTILINE)


def stable_hash(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:n]


def load_manifest() -> list[dict]:
    rows: list[dict] = []
    with (BOOK_ROOT / "_manifest.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("err"):
                continue
            rows.append(row)
    return rows


def line_offsets(text: str) -> list[int]:
    offsets = [0]
    pos = 0
    for line in text.splitlines(True):
        pos += len(line)
        offsets.append(pos)
    return offsets


def char_to_line(offsets: list[int], char_pos: int) -> int:
    lo, hi = 0, len(offsets) - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if offsets[mid] <= char_pos:
            lo = mid
        else:
            hi = mid - 1
    return lo


def estimated_page_range(line_start: int, line_end: int, total_lines: int, pages: int) -> str:
    if pages <= 0:
        return "unknown"
    total = max(1, total_lines)
    p1 = max(1, min(pages, int(math.floor((line_start / total) * pages)) + 1))
    p2 = max(p1, min(pages, int(math.ceil((line_end / total) * pages))))
    return f"{p1}-{p2}"


def norm_candidates(text: str, method: str, table_ratio: float, eq_count: int) -> dict:
    low = text.lower()
    topics: set[str] = set()
    methods: set[str] = set()
    systems: set[str] = set()
    refs: set[str] = set()
    tags: set[str] = set()

    def has(*patterns: str) -> bool:
        return any(re.search(p, low, re.IGNORECASE) for p in patterns)

    if has(r"\brb[-\s]?sr\b", r"rubidium[-\s]strontium"):
        systems.add("system_rb_sr"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"\bsm[-\s]?nd\b", r"samarium[-\s]neodymium", r"epsilon\s+nd"):
        systems.add("system_sm_nd"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"\bu[-\s]?pb\b", r"\bpb[-\s]?pb\b", r"uranium[-\s]lead", r"zircon"):
        systems.add("system_u_pb"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"\blu[-\s]?hf\b"):
        systems.add("system_lu_hf"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"\bre[-\s]?os\b"):
        systems.add("system_re_os"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"\bk[-\s]?ar\b", r"\bar[-\s]?ar\b", r"40ar\s*/\s*39ar"):
        systems.add("system_k_ar_ar"); topics.add("topic_geochronology"); tags.add("radiogenic")
    if has(r"isochron", r"geochron", r"decay\s+constant", r"radiogenic"):
        topics.add("topic_geochronology"); topics.add("topic_radiogenic_decay"); tags.add("radiogenic")

    if has(r"fractionation", r"kinetic isotope", r"equilibrium isotope"):
        topics.add("topic_isotope_fractionation"); tags.add("stable_fractionation")
    if has(r"d13c", r"delta\s*13c", r"carbon isotope"):
        systems.add("system_c_isotopes"); tags.add("stable_fractionation")
    if has(r"d18o", r"delta\s*18o", r"oxygen isotope", r"hydrogen isotope", r"\bdd\b", r"delta\s*d"):
        systems.add("system_o_h_isotopes"); tags.add("stable_fractionation")
    if has(r"d34s", r"delta\s*34s", r"sulfur isotope"):
        systems.add("system_s_isotopes"); tags.add("stable_fractionation")
    if has(r"d15n", r"delta\s*15n", r"nitrogen isotope"):
        systems.add("system_n_isotopes"); tags.add("stable_fractionation")

    if has(r"\btims\b", r"thermal ionization"):
        methods.add("method_tims"); tags.add("method")
    if has(r"\bsims\b", r"ion microprobe"):
        methods.add("method_sims"); tags.add("method")
    if has(r"mc[-\s]?icp[-\s]?ms", r"multi[-\s]?collector"):
        methods.add("method_mc_icp_ms"); tags.add("method")
    if has(r"\bicp[-\s]?ms\b"):
        methods.add("method_icp_ms"); tags.add("method")
    if has(r"\birms\b", r"isotope ratio mass spectrometry"):
        methods.add("method_irms"); tags.add("method")
    if has(r"noble gas mass spectrom", r"static noble gas"):
        methods.add("method_noble_gas_ms"); tags.add("method")
    if has(r"laser ablation", r"\bla[-\s]?icp[-\s]?ms\b"):
        methods.add("method_laser_ablation"); tags.add("method")
    if has(r"fluorination"):
        methods.add("method_fluorination"); tags.add("method")
    if has(r"step heating", r"incremental heating"):
        methods.add("method_step_heating"); tags.add("method")
    if has(r"ion exchange", r"chromatograph"):
        methods.add("method_ion_exchange"); tags.add("method")
    if has(r"mixing model", r"endmember", r"binary mixing"):
        methods.add("method_mixing_model")
    if has(r"isochron"):
        methods.add("method_isochron")

    if has(r"hydrothermal", r"geothermal"):
        topics.add("topic_hydrothermal_fluids")
    if has(r"mantle", r"morb", r"oib"):
        topics.add("topic_mantle_isotopes")
    if has(r"contamination", r"assimilation"):
        topics.add("topic_crustal_contamination")

    if method == "table_dense" or table_ratio >= 0.30 or has(r"reference table", r"constant", r"standard", r"calibration"):
        refs.add("reference_table"); tags.add("reference_table")
    if has(r"solubility", r"henry", r"gas[-\s]?water", r"aqueous solution"):
        topics.add("topic_noble_gas_solubility")
        methods.add("method_solubility_model")
        refs.add("solubility_table")
        tags.add("solubility")
    if has(r"equation of state", r"\bteos\b", r"thermodynamic", r"gibbs") or eq_count >= 50:
        topics.add("topic_equation_of_state")
        methods.add("method_thermodynamic_model")
        refs.add("equation")
        refs.add("thermodynamic_relation")
        tags.add("equation")
    if has(r"property table"):
        refs.add("property_table"); tags.add("reference_table")

    return {
        "topics_norm_candidates": sorted(topics),
        "methods_norm_candidates": sorted(methods),
        "isotope_systems_norm_candidates": sorted(systems),
        "reference_kind_candidates": sorted(refs),
        "selection_tags": sorted(tags),
    }


def make_segment(
    *,
    book_id: str,
    slug: str,
    segment_index: int,
    segment_type: str,
    segment_method: str,
    segment_confidence: str,
    md_quality: str,
    page_range: str,
    total_pages: int,
    line_start: int,
    line_end: int,
    total_lines: int,
    text: str,
    heading_level: int | None,
    heading_text: str,
) -> dict:
    seg_text = "\n".join(text.splitlines()[line_start:line_end])
    table_rows = len(TABLE_RE.findall(seg_text))
    eq_markers = seg_text.count("$")
    line_count = max(1, line_end - line_start)
    table_ratio = table_rows / line_count
    cands = norm_candidates(seg_text, segment_method, table_ratio, eq_markers)
    return {
        "schema": "book_segment_manifest_v1",
        "segment_schema_version": SEGMENT_SCHEMA_VERSION,
        "prompt_version": PROMPT_VERSION,
        "normalizer_version": NORMALIZER_VERSION,
        "book_id": book_id,
        "book_slug": slug,
        "segment_id": f"{book_id}::seg_{segment_index:03d}",
        "segment_index": segment_index,
        "segment_type": segment_type,
        "segment_method": segment_method,
        "segment_confidence": segment_confidence,
        "md_quality": md_quality,
        "page_range": page_range,
        "page_range_estimated": True,
        "total_pages": total_pages,
        "line_start": line_start,
        "line_end": line_end,
        "line_count": line_count,
        "table_row_count": table_rows,
        "equation_marker_count": eq_markers,
        "heading_level": heading_level,
        "heading_hash": stable_hash(heading_text.strip()) if heading_text.strip() else "",
        **cands,
    }


def segment_book(row: dict) -> list[dict]:
    slug = row["slug"]
    book_id = f"book_{slug}"
    book_dir = BOOK_ROOT / slug
    md_files = sorted(book_dir.glob("*.md"))
    if not md_files:
        return []
    text = md_files[0].read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    total_lines = max(1, len(lines))
    total_pages = int(row.get("pages") or row.get("images") or 0)

    h1 = len(H1_RE.findall(text))
    h2 = len(H2_RE.findall(text))
    h3 = len(H3_RE.findall(text))
    h12 = h1 + h2
    table_rows = len(TABLE_RE.findall(text))
    table_ratio = table_rows / total_lines
    eq_count = text.count("$")

    if table_ratio >= 0.30:
        md_quality = "table_weak"
        method = "table_dense"
        seg_type = "reference_table_group"
        conf = "medium"
    elif h12 >= 5:
        md_quality = "ok"
        method = "heading"
        seg_type = "chapter_or_section"
        conf = "high"
    elif h12 >= 3:
        md_quality = "heading_weak"
        method = "heading"
        seg_type = "section"
        conf = "medium"
    else:
        md_quality = "heading_weak"
        method = "fixed_window"
        seg_type = "page_window"
        conf = "low"

    offsets = line_offsets(text)
    segments: list[dict] = []
    if method == "heading":
        matches = list(H12_RE.finditer(text))
        bounds: list[tuple[int, int, int, str]] = []
        for i, m in enumerate(matches):
            start = char_to_line(offsets, m.start())
            end_char = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            end = max(start + 1, char_to_line(offsets, end_char))
            level = len(m.group(1))
            heading_text = m.group(2)
            bounds.append((start, end, level, heading_text))
        for idx, (start, end, level, heading_text) in enumerate(bounds):
            page_range = estimated_page_range(start, end, total_lines, total_pages)
            stype = "chapter" if level == 1 else "section"
            segments.append(make_segment(
                book_id=book_id, slug=slug, segment_index=idx, segment_type=stype,
                segment_method=method, segment_confidence=conf, md_quality=md_quality,
                page_range=page_range, total_pages=total_pages, line_start=start,
                line_end=end, total_lines=total_lines, text=text,
                heading_level=level, heading_text=heading_text,
            ))
    else:
        window_pages = 25 if method == "table_dense" else 15
        seg_count = max(1, math.ceil(max(1, total_pages) / window_pages))
        for idx in range(seg_count):
            start = int((idx / seg_count) * total_lines)
            end = int(((idx + 1) / seg_count) * total_lines)
            if idx == seg_count - 1:
                end = total_lines
            page_start = idx * window_pages + 1
            page_end = min(total_pages, (idx + 1) * window_pages) if total_pages else 0
            page_range = f"{page_start}-{page_end}" if total_pages else "unknown"
            segments.append(make_segment(
                book_id=book_id, slug=slug, segment_index=idx, segment_type=seg_type,
                segment_method=method, segment_confidence=conf, md_quality=md_quality,
                page_range=page_range, total_pages=total_pages, line_start=start,
                line_end=max(start + 1, end), total_lines=total_lines, text=text,
                heading_level=None, heading_text="",
            ))

    for seg in segments:
        seg["book_h1_count"] = h1
        seg["book_h2_count"] = h2
        seg["book_h3_count"] = h3
        seg["book_table_ratio"] = round(table_ratio, 4)
        seg["book_equation_marker_count"] = eq_count
    return segments


def pick_holdout(segments: list[dict]) -> list[dict]:
    chosen: list[dict] = []
    used: set[str] = set()

    def select(slot: str, predicate, expected) -> None:
        for seg in segments:
            if seg["segment_id"] in used:
                continue
            if predicate(seg):
                expected_obj = expected(seg) if callable(expected) else expected
                used.add(seg["segment_id"])
                chosen.append({
                    "holdout_id": slot,
                    "book_id": seg["book_id"],
                    "segment_id": seg["segment_id"],
                    "segment_manifest_version": SEGMENT_SCHEMA_VERSION,
                    "expected": expected_obj,
                })
                return
        raise RuntimeError(f"no segment matched {slot}")

    select("H1", lambda s: s["segment_confidence"] == "high",
           {"copied_fields_exact": True, "content_type_any": ["explanation", "mixed"],
            "topics_norm_required": [], "methods_norm_required": [],
            "reference_kind_required": [], "locator_required": False,
            "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H2", lambda s: "radiogenic" in s["selection_tags"] and s["segment_confidence"] == "high",
           {"copied_fields_exact": True, "topics_norm_required": ["topic_geochronology"],
            "methods_norm_required": [], "isotope_systems_norm_required": [],
            "reference_kind_required": [], "locator_required": False,
            "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H3", lambda s: "stable_fractionation" in s["selection_tags"] and s["segment_confidence"] == "high",
           {"copied_fields_exact": True, "topics_norm_required": ["topic_isotope_fractionation"],
            "methods_norm_required": [], "isotope_systems_norm_required": [],
            "reference_kind_required": [], "locator_required": False,
            "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H4", lambda s: bool(s["methods_norm_candidates"]) and s["segment_confidence"] == "high",
           lambda s: {"copied_fields_exact": True, "topics_norm_required": [],
                      "methods_norm_required": [s["methods_norm_candidates"][0]],
                      "reference_kind_required": [], "locator_required": False,
                      "value_extracted_must_all_be_false": True,
                      "numeric_value_string_count_must_be_zero": True,
                      "production_allowed": True})
    select("H5", lambda s: s["segment_method"] == "table_dense",
           {"copied_fields_exact": True, "content_type_any": ["reference_table", "mixed"],
            "topics_norm_required": [], "methods_norm_required": [],
            "reference_kind_required": ["reference_table"], "locator_required": True,
            "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H6", lambda s: "equation" in s["selection_tags"],
           {"copied_fields_exact": True, "topics_norm_required": ["topic_equation_of_state"],
            "methods_norm_required": [], "reference_kind_required": ["equation"],
            "locator_required": True, "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H7", lambda s: "solubility" in s["selection_tags"],
           {"copied_fields_exact": True, "topics_norm_required": ["topic_noble_gas_solubility"],
            "methods_norm_required": ["method_solubility_model"],
            "reference_kind_required": ["solubility_table"],
            "locator_required": True, "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": True})
    select("H8", lambda s: s["segment_confidence"] != "high",
           {"copied_fields_exact": True, "topics_norm_required": [],
            "methods_norm_required": [], "reference_kind_required": [],
            "locator_required": False, "value_extracted_must_all_be_false": True,
            "numeric_value_string_count_must_be_zero": True,
            "production_allowed": False})
    return chosen


def main() -> int:
    all_segments: list[dict] = []
    for row in load_manifest():
        all_segments.extend(segment_book(row))
    all_segments.sort(key=lambda s: (s["book_id"], s["segment_index"]))

    OUT_MANIFEST.write_text(
        "".join(json.dumps(seg, ensure_ascii=True, sort_keys=True) + "\n" for seg in all_segments),
        encoding="utf-8",
    )
    holdout = pick_holdout(all_segments)
    OUT_HOLDOUT.write_text(
        "".join(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n" for row in holdout),
        encoding="utf-8",
    )

    by_method: dict[str, int] = {}
    by_conf: dict[str, int] = {}
    by_quality: dict[str, int] = {}
    by_tag: dict[str, int] = {}
    for seg in all_segments:
        by_method[seg["segment_method"]] = by_method.get(seg["segment_method"], 0) + 1
        by_conf[seg["segment_confidence"]] = by_conf.get(seg["segment_confidence"], 0) + 1
        by_quality[seg["md_quality"]] = by_quality.get(seg["md_quality"], 0) + 1
        for tag in seg["selection_tags"]:
            by_tag[tag] = by_tag.get(tag, 0) + 1

    summary = {
        "schema": "book_segment_summary_v1_codex_safe",
        "book_count": len({seg["book_id"] for seg in all_segments}),
        "segment_count": len(all_segments),
        "segment_manifest_sha256_prefix": stable_hash(OUT_MANIFEST.read_text(encoding="utf-8")),
        "holdout_gold_sha256_prefix": stable_hash(OUT_HOLDOUT.read_text(encoding="utf-8")),
        "method_counts": dict(sorted(by_method.items())),
        "confidence_counts": dict(sorted(by_conf.items())),
        "md_quality_counts": dict(sorted(by_quality.items())),
        "selection_tag_counts": dict(sorted(by_tag.items())),
        "holdout_count": len(holdout),
        "holdout_ids": [row["holdout_id"] for row in holdout],
        "raw_text_written": False,
        "heading_text_written": False,
        "table_cell_text_written": False,
        "resolved_numeric_values_written": False,
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
