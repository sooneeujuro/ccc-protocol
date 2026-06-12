param(
  [string]$ProjectRoot = ".",
  [string]$Message = "",
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path $ProjectRoot
Push-Location $root
try {
  if (-not (Test-Path "coop")) {
    Write-Error "No coop folder found."
  }

  $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
  if (-not $Message) {
    $Message = "ccc: heartbeat snapshot $stamp"
  }

  git status --short
  git add coop

  $pending = git diff --cached --name-only
  if (-not $pending) {
    Write-Host "No coop changes to snapshot."
    exit 0
  }

  if ($DryRun) {
    Write-Host "Dry run. Would commit:"
    $pending
    exit 0
  }

  git commit -m $Message
  git push
}
finally {
  Pop-Location
}

