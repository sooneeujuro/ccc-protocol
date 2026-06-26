#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""datalab_harness.py — cost-safe Datalab (Marker) PDF->markdown+images harness.

GUARANTEES (operator: never double-pay, resumable, quality-first):
  - raw-first: the complete Datalab response is saved to raw/<pid>.json before any derive.
  - idempotent: if raw/<pid>.json exists -> NO API call. derive re-runs free from raw.
  - resume: an in-flight request (request_check_url in ledger) is polled, never resubmitted.
  - separation: submit/poll = paid; derive (images/md/manifest) = free, re-runnable.

Datalab Marker API:
  POST https://www.datalab.to/api/v1/marker  (X-Api-Key, multipart: file, output_format, use_llm, ...)
    -> {success, request_id, request_check_url}
  GET <request_check_url> (X-Api-Key) -> {status: processing|complete, markdown, images:{name:b64}, ...}

Env: DATALAB_API_KEY required for submit/poll (NOT for derive).
Run folder (git-excluded; raw contains paper text/images -> never push):
  G:\datalab_runs_v20260616\{RUN_LEDGER.csv, raw\<pid>.json, derived\<pid>\{markdown.md, images\, manifest.csv}}

Usage:
  python datalab_harness.py --jobs jobs.csv --all          # submit->poll->derive (resumable)
  python datalab_harness.py --jobs jobs.csv --derive-only   # free: rebuild from raw only
  jobs.csv columns: pid,pdf_path   (one paper per row)
"""
import os, sys, csv, json, time, base64, hashlib, argparse
from pathlib import Path
try:
    import requests
except Exception:
    requests = None

RUN = Path(r"G:\datalab_runs_v20260616")
RAW = RUN / "raw"; DERIVED = RUN / "derived"; LEDGER = RUN / "RUN_LEDGER.csv"
API = "https://www.datalab.to/api/v1/marker"
KEY = os.environ.get("DATALAB_API_KEY", "")
FIELDS = ["pid", "pdf_path", "pdf_sha256", "options", "request_id", "check_url",
          "submitted_at", "state", "raw_path", "page_count", "note"]

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""): h.update(c)
    return h.hexdigest()

def atomic_write(path, data, mode="w"):
    tmp = Path(str(path) + ".tmp")
    with open(tmp, mode, encoding=None if "b" in mode else "utf-8") as f:
        f.write(data)
    os.replace(tmp, path)

def load_ledger():
    if not LEDGER.exists(): return {}
    return {r["pid"]: r for r in csv.DictReader(open(LEDGER, encoding="utf-8"))}

def save_ledger(d):
    RUN.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(LEDGER) + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader()
        for pid in sorted(d): w.writerow({k: d[pid].get(k, "") for k in FIELDS})
    os.replace(tmp, LEDGER)

def ts(): return time.strftime("%Y-%m-%d %H:%M:%S")

def submit(pid, pdf, led, opts):
    if (RAW / f"{pid}.json").exists():
        print(f"  [{pid}] raw exists -> skip submit (no charge)"); return led
    row = led.get(pid, {})
    if row.get("state") in ("submitted", "polling") and row.get("check_url"):
        print(f"  [{pid}] in-flight ({row['state']}) -> will resume poll, no resubmit"); return led
    if not (requests and KEY):
        print(f"  [{pid}] NO API key/requests -> cannot submit (set DATALAB_API_KEY)"); return led
    with open(pdf, "rb") as fh:
        files = {"file": (Path(pdf).name, fh, "application/pdf")}
        data = {"output_format": "markdown", "use_llm": str(opts.get("use_llm", True)).lower()}
        if opts.get("max_pages"): data["max_pages"] = str(opts["max_pages"])
        r = requests.post(API, headers={"X-Api-Key": KEY}, files=files, data=data, timeout=120)
    j = r.json()
    if not j.get("success"):
        led[pid] = {**row, "pid": pid, "pdf_path": str(pdf), "state": "failed", "note": str(j)[:200]}
        save_ledger(led); print(f"  [{pid}] submit FAIL: {str(j)[:120]}"); return led
    led[pid] = {"pid": pid, "pdf_path": str(pdf), "pdf_sha256": sha(pdf), "options": json.dumps(data),
                "request_id": j.get("request_id", ""), "check_url": j.get("request_check_url", ""),
                "submitted_at": ts(), "state": "submitted", "raw_path": "", "page_count": "", "note": ""}
    save_ledger(led)  # persist request id BEFORE anything else (resume safety)
    print(f"  [{pid}] submitted req={j.get('request_id','')[:12]}")
    return led

def poll_once(pid, led):
    row = led.get(pid, {})
    if (RAW / f"{pid}.json").exists():
        if row.get("state") != "derived": row["state"] = "raw_saved"; led[pid] = row; save_ledger(led)
        return True
    url = row.get("check_url")
    if not (url and requests and KEY): return False
    r = requests.get(url, headers={"X-Api-Key": KEY}, timeout=60); j = r.json()
    st = j.get("status")
    if st == "complete" and j.get("success", True):
        RAW.mkdir(parents=True, exist_ok=True)
        atomic_write(RAW / f"{pid}.json", json.dumps(j, ensure_ascii=False))
        row.update(state="raw_saved", raw_path=str(RAW / f"{pid}.json"), page_count=str(j.get("page_count", "")))
        led[pid] = row; save_ledger(led); print(f"  [{pid}] raw_saved ({j.get('page_count','?')}p)"); return True
    row["state"] = "polling"; led[pid] = row; return False

def derive(pid, led):
    raw = RAW / f"{pid}.json"
    if not raw.exists(): print(f"  [{pid}] no raw -> cannot derive"); return
    j = json.loads(raw.read_text(encoding="utf-8"))
    d = DERIVED / pid.rstrip(" .")  # Windows: 폴더명 trailing space/dot 금지 (raw 조회는 원본 pid 유지)
    (d / "images").mkdir(parents=True, exist_ok=True)
    atomic_write(d / "markdown.md", j.get("markdown", ""))
    imgs = j.get("images", {}) or {}
    rows = []
    for name, b64 in imgs.items():
        try: data = base64.b64decode(b64)
        except Exception: continue
        (d / "images" / name).write_bytes(data)
        rows.append({"datalab_image": name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    with open(d / "manifest.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["datalab_image", "sha256", "bytes"]); w.writeheader(); w.writerows(rows)
    row = led.get(pid, {}); row["state"] = "derived"; led[pid] = row; save_ledger(led)
    print(f"  [{pid}] derived: {len(imgs)} images, md {len(j.get('markdown',''))} chars")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", required=True, help="csv with columns pid,pdf_path")
    ap.add_argument("--all", action="store_true"); ap.add_argument("--derive-only", action="store_true")
    ap.add_argument("--max-pages", type=int, default=0); ap.add_argument("--poll-secs", type=int, default=20)
    ap.add_argument("--max-wait", type=int, default=1800)
    A = ap.parse_args()
    jobs = list(csv.DictReader(open(A.jobs, encoding="utf-8")))
    opts = {"use_llm": True}
    if A.max_pages: opts["max_pages"] = A.max_pages
    led = load_ledger()
    RAW.mkdir(parents=True, exist_ok=True); DERIVED.mkdir(parents=True, exist_ok=True)

    if A.derive_only:
        for jb in jobs: derive(jb["pid"], led)
        print("derive-only done (no API calls)"); return

    if not KEY:
        print("DATALAB_API_KEY not set -> cannot submit/poll. (set env, or use --derive-only).")
        print("Harness ready; provide key + GO to fire.  Jobs:", len(jobs)); return

    print(f"submit {len(jobs)} jobs (idempotent: raw/in-flight skipped)...")
    for jb in jobs: led = submit(jb["pid"], jb["pdf_path"], led, opts)
    print("poll until all raw_saved...")
    t0 = time.time()
    while time.time() - t0 < A.max_wait:
        pending = [jb["pid"] for jb in jobs if not (RAW / f"{jb['pid']}.json").exists()]
        if not pending: break
        for pid in pending: poll_once(pid, led)
        print(f"  pending {len(pending)} ... ({int(time.time()-t0)}s)"); time.sleep(A.poll_secs)
    print("derive (free) ...")
    for jb in jobs: derive(jb["pid"], led)
    done = sum(1 for jb in jobs if (RAW / f"{jb['pid']}.json").exists())
    print(f"DONE: raw_saved {done}/{len(jobs)}. ledger={LEDGER}")

if __name__ == "__main__":
    main()
