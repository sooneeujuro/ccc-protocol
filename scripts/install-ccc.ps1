param(
  [Parameter(Mandatory = $true)]
  [string]$ProjectRoot,
  [string]$ProtocolRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path,
  [switch]$Force
)

$ErrorActionPreference = "Stop"
$script:exitCode = 0
$script:status = 'error'
$script:reason = 'internal_error'
$script:createdCount = 0
$script:unchangedCount = 0
$script:preservedConflictCount = 0
$script:manifestHash = ''
$script:indexUnchanged = $false
$script:lockStream = $null
$script:lockPath = $null
$script:lockAcquired = $false

$manifest = @(
  '.gitignore',
  'PROTOCOL.md',
  'SUPERVISOR_POLICY.md',
  'RUN_STATE.md',
  'chat.md',
  'STATUS_claude.md',
  'STATUS_codex.md',
  'operator/commands.md',
  'inbox_claude/.gitkeep',
  'inbox_codex/.gitkeep',
  'reports/.gitkeep',
  'scratch/.gitkeep'
)

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

function Get-FileHashSafe {
  param([string]$LiteralPath)
  if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) { return 'absent' }
  return Get-Sha256Bytes ([System.IO.File]::ReadAllBytes($LiteralPath))
}

function Stop-Ccc {
  param([string]$Reason, [int]$Code)
  throw [System.InvalidOperationException]::new("CCCFAIL|$Code|$Reason")
}

function Invoke-GitSafe {
  param([string[]]$Arguments, [string]$FailureReason)
  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $output = @(& git @Arguments 2>&1)
    $code = $LASTEXITCODE
  }
  finally { $ErrorActionPreference = $oldPreference }
  if ($code -ne 0) { Stop-Ccc $FailureReason 5 }
  return [pscustomobject]@{ Output = [object[]]$output }
}

function Test-SecretText {
  param([string]$Text)
  $patterns = @(
    '-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    '(?im)\bAuthorization\s*:\s*Bearer\s+\S+',
    '(?im)\b(?:OPENAI|ANTHROPIC|AWS|GITHUB|SUPABASE|VERCEL|DATABASE|API)[A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*\S+',
    '\bsk-[A-Za-z0-9_-]{16,}\b',
    '\bgh[pousr]_[A-Za-z0-9]{20,}\b',
    '\bAKIA[A-Z0-9]{16}\b'
  )
  foreach ($pattern in $patterns) { if ($Text -match $pattern) { return $true } }
  return $false
}

function Write-SafeResult {
  $result = [ordered]@{
    schema = 'ccc_install_result_v1'
    status = $script:status
    reason = $script:reason
    manifest_entry_count = $manifest.Count
    created_count = $script:createdCount
    unchanged_count = $script:unchangedCount
    preserved_conflict_count = $script:preservedConflictCount
    manifest_hash = $script:manifestHash
    force_overwrite_performed = $false
    index_unchanged = [bool]$script:indexUnchanged
  }
  Write-Output ($result | ConvertTo-Json -Compress)
}

$indexPath = $null
$indexHashBefore = 'unknown'
try {
  try { $root = (Resolve-Path -LiteralPath $ProjectRoot -ErrorAction Stop).Path }
  catch { Stop-Ccc 'project_root_invalid' 2 }
  try { $protocol = (Resolve-Path -LiteralPath $ProtocolRoot -ErrorAction Stop).Path }
  catch { Stop-Ccc 'protocol_root_invalid' 2 }

  $topResult = Invoke-GitSafe @('-C', $root, 'rev-parse', '--show-toplevel') 'git_root_check_failed'
  $top = ([string](@($topResult.Output)[0])).Trim()
  try { $topResolved = (Resolve-Path -LiteralPath $top -ErrorAction Stop).Path }
  catch { Stop-Ccc 'git_root_invalid' 2 }
  $trimChars = [char[]]@('\', '/')
  if (-not [string]::Equals($topResolved.TrimEnd($trimChars), $root.TrimEnd($trimChars), [System.StringComparison]::OrdinalIgnoreCase)) {
    Stop-Ccc 'project_root_not_git_toplevel' 2
  }

  $template = Join-Path $protocol 'templates\coop'
  if (-not (Test-Path -LiteralPath $template -PathType Container)) { Stop-Ccc 'template_root_missing' 2 }
  $templateItem = Get-Item -LiteralPath $template -Force
  if (($templateItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { Stop-Ccc 'template_reparse_forbidden' 3 }

  $gitCommonResult = Invoke-GitSafe @('-C', $root, 'rev-parse', '--git-common-dir') 'git_common_dir_failed'
  $gitCommon = ([string](@($gitCommonResult.Output)[0])).Trim()
  if (-not [System.IO.Path]::IsPathRooted($gitCommon)) { $gitCommon = Join-Path $root $gitCommon }
  try { $gitCommon = (Resolve-Path -LiteralPath $gitCommon -ErrorAction Stop).Path }
  catch { Stop-Ccc 'git_common_dir_invalid' 2 }
  $script:lockPath = Join-Path $gitCommon 'ccc_install.lock'
  try {
    $script:lockStream = [System.IO.File]::Open($script:lockPath, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    $script:lockAcquired = $true
  }
  catch [System.IO.IOException] { Stop-Ccc 'lock_held' 4 }

  $indexResult = Invoke-GitSafe @('-C', $root, 'rev-parse', '--git-path', 'index') 'git_index_path_failed'
  $indexPath = ([string](@($indexResult.Output)[0])).Trim()
  if (-not [System.IO.Path]::IsPathRooted($indexPath)) { $indexPath = Join-Path $root $indexPath }
  $indexHashBefore = Get-FileHashSafe $indexPath

  $sourceRows = @()
  $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
  foreach ($relative in $manifest) {
    $source = Join-Path $template ($relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { Stop-Ccc 'template_manifest_incomplete' 3 }
    $item = Get-Item -LiteralPath $source -Force
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { Stop-Ccc 'template_file_reparse_forbidden' 3 }
    if ($item.Length -gt 262144) { Stop-Ccc 'template_file_too_large' 3 }
    $bytes = [System.IO.File]::ReadAllBytes($source)
    if ([System.Array]::IndexOf($bytes, [byte]0) -ge 0) { Stop-Ccc 'template_nul_forbidden' 3 }
    try { $text = $strictUtf8.GetString($bytes) }
    catch { Stop-Ccc 'template_non_utf8_forbidden' 3 }
    if (Test-SecretText $text) { Stop-Ccc 'template_secret_detected' 3 }
    $sourceRows += [pscustomobject]@{ Relative = $relative; Source = $source; Bytes = $bytes; Sha256 = Get-Sha256Bytes $bytes }
  }
  $script:manifestHash = Get-Sha256Text ((@($sourceRows | ForEach-Object { "$($_.Relative)|$($_.Sha256)" }) | Sort-Object) -join "`n")

  $target = Join-Path $root 'coop'
  if (Test-Path -LiteralPath $target) {
    $targetItem = Get-Item -LiteralPath $target -Force
    if (($targetItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) { Stop-Ccc 'coop_reparse_forbidden' 3 }
    if (-not $targetItem.PSIsContainer) { Stop-Ccc 'coop_not_directory' 3 }
  }
  else {
    New-Item -ItemType Directory -Path $target -ErrorAction Stop | Out-Null
  }

  foreach ($row in $sourceRows) {
    $destination = Join-Path $target ($row.Relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar))
    $parent = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $parent -PathType Container)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    if (Test-Path -LiteralPath $destination) {
      $destinationItem = Get-Item -LiteralPath $destination -Force
      if ($destinationItem.PSIsContainer -or (($destinationItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0)) {
        Stop-Ccc 'destination_type_conflict' 3
      }
      $destinationHash = Get-FileHashSafe $destination
      if ([string]::Equals($destinationHash, $row.Sha256, [System.StringComparison]::Ordinal)) { $script:unchangedCount++ }
      else { $script:preservedConflictCount++ }
      continue
    }
    $tempName = ".ccc-install-$([guid]::NewGuid().ToString('N')).tmp"
    $tempPath = Join-Path $parent $tempName
    try {
      [System.IO.File]::WriteAllBytes($tempPath, $row.Bytes)
      Move-Item -LiteralPath $tempPath -Destination $destination -ErrorAction Stop
      $script:createdCount++
    }
    finally {
      if (Test-Path -LiteralPath $tempPath -PathType Leaf) { Remove-Item -LiteralPath $tempPath -Force -ErrorAction SilentlyContinue }
    }
  }

  $script:indexUnchanged = [string]::Equals($indexHashBefore, (Get-FileHashSafe $indexPath), [System.StringComparison]::Ordinal)
  if (-not $script:indexUnchanged) { Stop-Ccc 'install_index_mutated' 5 }
  $script:status = if ($script:preservedConflictCount -gt 0) { 'installed_with_preserved_conflicts' } elseif ($script:createdCount -gt 0) { 'installed' } else { 'noop' }
  $script:reason = if ($Force -and $script:preservedConflictCount -gt 0) { 'force_overwrite_disabled' } elseif ($script:preservedConflictCount -gt 0) { 'existing_content_preserved' } else { 'ok' }
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
finally {
  if ($indexPath -and $indexHashBefore -ne 'unknown') {
    $script:indexUnchanged = [string]::Equals($indexHashBefore, (Get-FileHashSafe $indexPath), [System.StringComparison]::Ordinal)
  }
  if ($script:lockStream) { $script:lockStream.Dispose(); $script:lockStream = $null }
  if ($script:lockAcquired -and $script:lockPath -and (Test-Path -LiteralPath $script:lockPath -PathType Leaf)) {
    Remove-Item -LiteralPath $script:lockPath -Force -ErrorAction SilentlyContinue
  }
}

Write-SafeResult
exit $script:exitCode
