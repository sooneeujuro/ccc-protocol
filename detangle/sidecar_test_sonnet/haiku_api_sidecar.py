"""19편 helium 논문 Haiku verbatim 사이드카 (직접 Anthropic API = 콘솔 prepaid).
키는 env ANTHROPIC_API_KEY(런타임 registry 주입). 표준 api.anthropic.com 명시(게이트웨이 우회).
입력=datalab derived markdown.md, 출력=격리 sidecars_haiku/. idempotent."""
import os, json, csv, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not KEY:
    print("ERROR: ANTHROPIC_API_KEY 없음 (PowerShell로 registry서 주입 필요)"); sys.exit(1)
DERIVED = r"G:\datalab_runs_v20260616\derived"
OUT = r"G:\corpus_helium_add_20260626\sidecars_haiku"
JOBS = r"C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\jobs_helium.csv"
os.makedirs(OUT, exist_ok=True)
pids = [r["pid"] for r in csv.DictReader(open(JOBS, encoding="utf-8"))]

INSTR = """You replicate a metadata "sidecar" (JSON) for ONE geochemistry paper, matching a corpus schema. Output ONLY the JSON object (no prose, no markdown fence).
Extract (verbatim where the text gives them; null or [] if genuinely absent — DO NOT invent):
{
 "doi": "<doi or null>",
 "bibliographic": {"authors_full":["Surname, I."],"title":"","journal":"","volume":"","issue":"","pages":"","year_print":null,"year_online":null,"publisher":null},
 "abstract_raw": "<abstract verbatim or null>",
 "conclusions_raw": "<conclusions/summary verbatim or null>",
 "classification": {"type":"<gas|petrology|both|other>","confidence":0.0,"evidence":["short reason"]},
 "geography": {"country":null,"region":null,"specific_location":null,"coordinates_approx":[],"tectonic_setting":null},
 "analytical": {"instruments":[{"category":"","raw_verbatim":""}],"labs":[{"name":"","full_name":""}],"standards":[{"name":"","used_for":""}]},
 "variables_measured": [{"id":"","raw_label":"","unit":null,"phase":null}],
 "figure_summaries": [{"id":"","caption_verbatim":""}],
 "page_anchors": {"<Section>":1},
 "references": [{"raw_id":"","raw_text":""}],
 "schema_version": "v2.1",
 "extraction_meta": {"extraction_model":"claude-haiku-4-5","via":"direct_api","source_corpus":"helium_add_20260626"}
}
classification.type: gas=noble gas/volatile/fluid; petrology=rocks/minerals/elements; both; other=methods/review/geophysics/theory.
PAPER TEXT:
"""

def call(pid, md):
    payload = {"model": "claude-haiku-4-5", "max_tokens": 16000,
               "messages": [{"role": "user", "content": f'The "id" field must be exactly: {pid}\n\n' + INSTR + md[:600000]}]}
    req = urllib.request.Request("https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={"x-api-key": KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        resp = json.loads(r.read().decode("utf-8"))
    return "".join(b.get("text", "") for b in resp.get("content", []) if b.get("type") == "text")

ok = fail = skip = 0
for pid in pids:
    pid = pid.rstrip(" .")  # derive가 폴더명 sanitize했으므로 동일 정규화 (trailing space/dot)
    outp = os.path.join(OUT, pid + ".json")
    if os.path.exists(outp): skip += 1; continue
    mdp = os.path.join(DERIVED, pid, "markdown.md")
    if not os.path.exists(mdp): print(f"  no md: {pid[:45]}"); fail += 1; continue
    md = open(mdp, encoding="utf-8", errors="replace").read()
    try:
        text = call(pid, md)
        try: obj = json.loads(text)
        except json.JSONDecodeError: obj = json.JSONDecoder().raw_decode(text.strip().lstrip("`json").strip())[0]
        obj["id"] = pid
        json.dump(obj, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        ok += 1
        print(f"  ok {ok}: {pid[:42]} ({len(obj.get('variables_measured') or [])}var/{len(obj.get('references') or [])}ref)")
    except Exception as e:
        fail += 1; print(f"  FAIL {pid[:42]}: {str(e)[:70]}")
print(f"\ndone: ok {ok} / fail {fail} / skip {skip} / 출력 {OUT}")
