param(
  [Parameter(Mandatory=$true)]
  [string]$ProjectRoot,

  [string]$ProtocolRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [switch]$Force
)

$ErrorActionPreference = "Stop"

$project = Resolve-Path $ProjectRoot
$template = Join-Path $ProtocolRoot "templates\coop"
$target = Join-Path $project "coop"

if ((Test-Path $target) -and -not $Force) {
  Write-Host "coop already exists: $target"
  Write-Host "Use -Force to merge template files."
  exit 0
}

New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Path (Join-Path $template "*") -Destination $target -Recurse -Force:$Force

Write-Host "Installed CCC coop template:"
Write-Host "  $target"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Edit coop/RUN_STATE.md"
Write-Host "  2. Tell both agents to read coop/PROTOCOL.md"
Write-Host "  3. Configure heartbeats"

