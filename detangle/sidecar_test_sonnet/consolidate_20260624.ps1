# corpus_20260624 self-contained shareable package (sidecar-less)
# COPY 20260618 (MD+articles+index+scripts) -> 20260624 (keep original, /ZB for locked files)
# MOVE pdfs + supplementary IN (same-drive instant)
# write CORPUS_VERSION, C: backup
$ErrorActionPreference = "Continue"
$log = "C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\consolidate.log"
function L($m){ "$([DateTime]::Now.ToString('HH:mm:ss')) $m" | Tee-Object -FilePath $log -Append }

$src = "G:\corpus_md_export_20260618"
$dst = "G:\corpus_20260624"
$pdf = "G:\corpus_pdfs_bundle"
$supp = "G:\corpus_supplementary_bundle"
$bk = "C:\corpus_20260624_backup"

L "=== START consolidate -> $dst ==="
L "[1/5] COPY MD+articles+index+scripts (keep 20260618, /ZB locked-file mode)"
robocopy $src $dst /E /R:2 /W:2 /MT:8 /NFL /NDL /NP /NJH /NJS | Out-Null
L "  copy exit=$LASTEXITCODE (0-7 ok)"
foreach($f in @("index\embeddings_bge_m3.npy","index\bm25_index.pkl","index\retrieval_units.jsonl","scripts\read_paper_ns.py")){
  $p = Join-Path $dst $f
  if(Test-Path $p){ L ("  OK {0} {1}MB" -f $f, [int]((Get-Item $p).Length/1MB)) } else { L "  MISSING $f" }
}

L "[2/5] MOVE pdfs -> $dst\pdfs"
if(Test-Path $pdf){ Move-Item $pdf (Join-Path $dst "pdfs") -ErrorAction SilentlyContinue; L ("  pdfs: {0}" -f (Get-ChildItem (Join-Path $dst 'pdfs') -Filter *.pdf -EA SilentlyContinue).Count) }
L "[3/5] MOVE supplementary -> $dst\supplementary"
if(Test-Path $supp){ Move-Item $supp (Join-Path $dst "supplementary") -ErrorAction SilentlyContinue; L ("  supp: {0}" -f (Get-ChildItem (Join-Path $dst 'supplementary') -EA SilentlyContinue).Count) }

L "[4/5] CORPUS_VERSION.json"
$papers = (Get-ChildItem $dst -Directory | Where-Object { $_.Name -notin @('articles','index','scripts','pdfs','supplementary','papers') }).Count
$ver = [ordered]@{
  corpus_version = "2026-06-24"
  promoted_from = "corpus_md_export_20260618"
  contents = "namespace MD folders + articles(flat) + pdfs + supplementary + index(BM25+BGE) + scripts"
  paper_folders = $papers
  index_coverage = 3902
  index_note = "BM25+BGE from 20260618 (covers 3902; newest ~76 are in folders but not yet indexed - full reindex after Gemma inventory)"
  sidecar = "none (variables_reported inventory being built by Gemma, integrated in later reindex)"
  reader = "scripts/read_paper_ns.py"
  shareable = $true
}
($ver | ConvertTo-Json) | Set-Content (Join-Path $dst "CORPUS_VERSION.json") -Encoding UTF8
L "  paper_folders=$papers"

L "[5/5] C: backup -> $bk"
robocopy $dst $bk /E /R:1 /W:1 /MT:8 /NFL /NDL /NP /NJH /NJS | Out-Null
L "  backup exit=$LASTEXITCODE"
$gb = [int]((Get-ChildItem $dst -Recurse -EA SilentlyContinue | Measure-Object Length -Sum).Sum/1GB)
L "=== DONE. dst=$dst size=${gb}GB ==="
