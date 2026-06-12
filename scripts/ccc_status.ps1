param(
  [string]$ProjectRoot = "."
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path $ProjectRoot
$coop = Join-Path $root "coop"

if (-not (Test-Path $coop)) {
  Write-Error "No coop folder found at $coop"
}

Write-Host "CCC status for $root"
Write-Host ""

$stop = Join-Path $coop "STOP.md"
Write-Host ("STOP: " + (Test-Path $stop))

foreach ($name in @("RUN_STATE.md", "STATUS_codex.md", "STATUS_claude.md")) {
  $path = Join-Path $coop $name
  if (Test-Path $path) {
    Write-Host ""
    Write-Host "== $name =="
    Get-Content $path -TotalCount 80
  }
}

Write-Host ""
Write-Host "== Recent chat =="
$chat = Join-Path $coop "chat.md"
if (Test-Path $chat) {
  Get-Content $chat -Tail 20
}

Write-Host ""
Write-Host "== Pending inbox files =="
foreach ($dir in @("inbox_codex", "inbox_claude", "operator")) {
  $path = Join-Path $coop $dir
  if (Test-Path $path) {
    Write-Host "-- $dir"
    Get-ChildItem $path -File | Sort-Object LastWriteTime -Descending | Select-Object -First 20 Name,LastWriteTime
  }
}

