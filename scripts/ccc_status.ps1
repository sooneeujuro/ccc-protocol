param(
  [string]$ProjectRoot = "."
)

$ErrorActionPreference = 'Stop'
$script:exitCode = 0
$script:status = 'error'
$script:reason = 'internal_error'
$script:stopPresent = $false
$script:componentPresentCount = 0
$script:componentMissingCount = 0
$script:inboxCodexCount = 0
$script:inboxClaudeCount = 0
$script:reportCount = 0
$script:operatorFileCount = 0
$script:coordinationFileCount = 0
$script:stateManifestHash = ''
$script:readOnly = $false

function Get-Sha256Bytes {
  param([byte[]]$Bytes)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try { return ([System.BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
  finally { $sha.Dispose() }
}

function Get-Sha256Text {
  param([string]$Text)
  return Get-Sha256Bytes ([System.Text.Encoding]::UTF8.GetBytes($Text))
}

function Stop-Ccc {
  param([string]$Reason, [int]$Code)
  throw [System.InvalidOperationException]::new("CCCFAIL|$Code|$Reason")
}

function Write-SafeResult {
  $result = [ordered]@{
    schema = 'ccc_status_v1'
    status = $script:status
    reason = $script:reason
    stop_present = [bool]$script:stopPresent
    component_present_count = [int]$script:componentPresentCount
    component_missing_count = [int]$script:componentMissingCount
    inbox_codex_file_count = [int]$script:inboxCodexCount
    inbox_claude_file_count = [int]$script:inboxClaudeCount
    report_file_count = [int]$script:reportCount
    operator_file_count = [int]$script:operatorFileCount
    coordination_file_count = [int]$script:coordinationFileCount
    pending_status = 'unknown_no_machine_linkage'
    state_manifest_hash = [string]$script:stateManifestHash
    raw_content_emitted = $false
    raw_filename_emitted = $false
    read_only = [bool]$script:readOnly
  }
  Write-Output ($result | ConvertTo-Json -Compress)
}

$indexPath = $null
$indexHashBefore = 'unknown'
$headBefore = 'unknown'
try {
  try { $root = (Resolve-Path -LiteralPath $ProjectRoot -ErrorAction Stop).Path }
  catch { Stop-Ccc 'project_root_invalid' 2 }
  $coop = Join-Path $root 'coop'
  if (-not (Test-Path -LiteralPath $coop -PathType Container)) { Stop-Ccc 'coop_missing' 2 }
  $coopItem = Get-Item -LiteralPath $coop -Force
  if (($coopItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { Stop-Ccc 'coop_reparse_forbidden' 3 }

  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $indexOutput = @(& git -C $root rev-parse --git-path index 2>&1)
    $indexExit = $LASTEXITCODE
    $headOutput = @(& git -C $root rev-parse HEAD 2>&1)
    $headExit = $LASTEXITCODE
  }
  finally { $ErrorActionPreference = $oldPreference }
  if ($indexExit -ne 0 -or $headExit -ne 0) { Stop-Ccc 'git_read_failed' 5 }
  $indexPath = ([string](@($indexOutput)[0])).Trim()
  if (-not [System.IO.Path]::IsPathRooted($indexPath)) { $indexPath = Join-Path $root $indexPath }
  if (Test-Path -LiteralPath $indexPath -PathType Leaf) { $indexHashBefore = Get-Sha256Bytes ([System.IO.File]::ReadAllBytes($indexPath)) }
  $headBefore = ([string](@($headOutput)[0])).Trim()

  $required = @(
    '.gitignore', 'PROTOCOL.md', 'SUPERVISOR_POLICY.md', 'RUN_STATE.md', 'chat.md',
    'STATUS_codex.md', 'STATUS_claude.md', 'operator/commands.md',
    'inbox_codex', 'inbox_claude', 'reports', 'scratch'
  )
  foreach ($relative in $required) {
    $path = Join-Path $coop ($relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if (Test-Path -LiteralPath $path) { $script:componentPresentCount++ } else { $script:componentMissingCount++ }
  }
  $script:stopPresent = Test-Path -LiteralPath (Join-Path $coop 'STOP.md') -PathType Leaf

  $inboxCodex = Join-Path $coop 'inbox_codex'
  $inboxClaude = Join-Path $coop 'inbox_claude'
  $reports = Join-Path $coop 'reports'
  $operator = Join-Path $coop 'operator'
  if (Test-Path -LiteralPath $inboxCodex -PathType Container) { $script:inboxCodexCount = @(Get-ChildItem -LiteralPath $inboxCodex -File -Force).Count }
  if (Test-Path -LiteralPath $inboxClaude -PathType Container) { $script:inboxClaudeCount = @(Get-ChildItem -LiteralPath $inboxClaude -File -Force).Count }
  if (Test-Path -LiteralPath $reports -PathType Container) { $script:reportCount = @(Get-ChildItem -LiteralPath $reports -File -Force).Count }
  if (Test-Path -LiteralPath $operator -PathType Container) { $script:operatorFileCount = @(Get-ChildItem -LiteralPath $operator -File -Force).Count }

  $allFiles = @(Get-ChildItem -LiteralPath $coop -Recurse -File -Force | Where-Object {
    $relative = $_.FullName.Substring($coop.Length).TrimStart([char[]]@('\', '/')).Replace('\', '/')
    $relative -ne '.ccc' -and -not $relative.StartsWith('.ccc/', [System.StringComparison]::Ordinal)
  })
  $script:coordinationFileCount = $allFiles.Count
  $manifestRows = @()
  foreach ($file in ($allFiles | Sort-Object FullName)) {
    $relative = $file.FullName.Substring($coop.Length).TrimStart([char[]]@('\', '/')).Replace('\', '/')
    $contentHash = Get-Sha256Bytes ([System.IO.File]::ReadAllBytes($file.FullName))
    $manifestRows += "$relative|$($file.Length)|$contentHash"
  }
  $script:stateManifestHash = Get-Sha256Text ($manifestRows -join "`n")

  $ErrorActionPreference = 'Continue'
  try {
    $headAfterOutput = @(& git -C $root rev-parse HEAD 2>&1)
    $headAfterExit = $LASTEXITCODE
  }
  finally { $ErrorActionPreference = $oldPreference }
  if ($headAfterExit -ne 0) { Stop-Ccc 'git_read_failed' 5 }
  $headAfter = ([string](@($headAfterOutput)[0])).Trim()
  $indexHashAfter = if (Test-Path -LiteralPath $indexPath -PathType Leaf) { Get-Sha256Bytes ([System.IO.File]::ReadAllBytes($indexPath)) } else { 'absent' }
  $script:readOnly = [string]::Equals($headBefore, $headAfter, [System.StringComparison]::Ordinal) -and [string]::Equals($indexHashBefore, $indexHashAfter, [System.StringComparison]::Ordinal)
  if (-not $script:readOnly) { Stop-Ccc 'status_observed_mutation' 5 }
  $script:status = if ($script:componentMissingCount -eq 0) { 'ok' } else { 'degraded' }
  $script:reason = if ($script:componentMissingCount -eq 0) { 'ok' } else { 'layout_incomplete' }
}
catch {
  $message = [string]$_.Exception.Message
  if ($message -match '^CCCFAIL\|(\d+)\|([A-Za-z0-9_]+)$') {
    $script:exitCode = [int]$Matches[1]
    $script:reason = $Matches[2]
  }
  else {
    $script:exitCode = 5
    $script:reason = 'internal_error'
  }
  $script:status = 'blocked'
}

Write-SafeResult
exit $script:exitCode
