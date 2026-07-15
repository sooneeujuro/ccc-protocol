param(
  [string]$ProjectRoot = ".",
  [Parameter(Mandatory = $true)]
  [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._/-]*$')]
  [string]$ExpectedBranch,
  [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]*$')]
  [string]$Remote = "origin",
  [string]$Message = "",
  [switch]$DryRun,
  [switch]$AllowProtectedBranch,
  [ValidateRange(1024, 1048576)]
  [int64]$MaxFileBytes = 262144,
  [ValidateRange(4096, 4194304)]
  [int64]$MaxSnapshotBytes = 1048576
)

$ErrorActionPreference = "Stop"

$script:exitCode = 0
$script:reason = "ok"
$script:status = "error"
$script:candidateCount = 0
$script:candidateBytes = 0
$script:candidateManifestHash = ""
$script:branchMatch = $false
$script:indexUnchanged = $false
$script:commitCreated = $false
$script:pushAttempted = $false
$script:pushSucceeded = $false
$script:lockStream = $null
$script:lockPath = $null
$script:lockAcquired = $false
$script:root = $null
$script:candidatePaths = @()
$script:stagingAttempted = $false

function Get-Sha256Bytes {
  param([byte[]]$Bytes)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  try {
    return ([System.BitConverter]::ToString($sha.ComputeHash($Bytes))).Replace("-", "").ToLowerInvariant()
  }
  finally {
    $sha.Dispose()
  }
}

function Get-Sha256Text {
  param([string]$Text)
  return Get-Sha256Bytes ([System.Text.Encoding]::UTF8.GetBytes($Text))
}

function Get-FileHashSafe {
  param([string]$LiteralPath)
  if (-not (Test-Path -LiteralPath $LiteralPath -PathType Leaf)) {
    return "absent"
  }
  return Get-Sha256Bytes ([System.IO.File]::ReadAllBytes($LiteralPath))
}

function Stop-Ccc {
  param([string]$Reason, [int]$Code)
  throw [System.InvalidOperationException]::new("CCCFAIL|$Code|$Reason")
}

function Invoke-GitSafe {
  param(
    [string[]]$Arguments,
    [string]$FailureReason = "git_command_failed",
    [switch]$AllowFailure
  )
  $oldPreference = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  try {
    $output = @(& git @Arguments 2>&1)
    $code = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $oldPreference
  }
  if ($code -ne 0 -and -not $AllowFailure) {
    Stop-Ccc $FailureReason 5
  }
  return [pscustomobject]@{ Code = $code; Output = $output }
}

function Test-SecretText {
  param([string]$Text)
  $patterns = @(
    '-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    '(?im)\bAuthorization\s*:\s*Bearer\s+\S+',
    '(?im)\b(?:OPENAI|ANTHROPIC|AWS|GITHUB|SUPABASE|VERCEL|DATABASE|API)[A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)\s*[:=]\s*\S+',
    '\bsk-[A-Za-z0-9_-]{16,}\b',
    '\bgh[pousr]_[A-Za-z0-9]{20,}\b',
    '\bAKIA[A-Z0-9]{16}\b',
    '\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b'
  )
  foreach ($pattern in $patterns) {
    if ($Text -match $pattern) { return $true }
  }
  return $false
}

function Test-AllowedCoordinationPath {
  param([string]$RelativePath)
  $p = $RelativePath.Replace('\', '/')
  if ($p -notmatch '^[A-Za-z0-9_./-]+$' -or $p.Contains('..') -or $p.Contains('//')) {
    return $false
  }
  $patterns = @(
    '^coop/(?:PROTOCOL|SUPERVISOR_POLICY|RUN_STATE|STATUS_codex|STATUS_claude|chat|STOP)\.md$',
    '^coop/\.gitignore$',
    '^coop/operator/commands\.md$',
    '^coop/(?:inbox_codex|inbox_claude|reports)/(?:[A-Za-z0-9][A-Za-z0-9._-]*\.md|\.gitkeep)$',
    '^coop/scratch/(?:[A-Za-z0-9][A-Za-z0-9._-]*\.(?:md|json|jsonl)|\.gitkeep)$'
  )
  foreach ($pattern in $patterns) {
    if ($p -match $pattern) { return $true }
  }
  return $false
}

function Get-CandidateManifest {
  param([string]$RepositoryRoot)

  $staged = Invoke-GitSafe @('-C', $RepositoryRoot, '-c', 'core.quotepath=false', 'diff', '--cached', '--name-only', '--', 'coop') 'git_staged_scan_failed'
  if (@($staged.Output).Count -gt 0) {
    Stop-Ccc 'pre_staged_coop_ambiguous' 3
  }

  $entries = @{}
  $tracked = Invoke-GitSafe @('-C', $RepositoryRoot, '-c', 'core.quotepath=false', 'diff', '--name-status', '--no-renames', 'HEAD', '--', 'coop') 'git_candidate_scan_failed'
  foreach ($lineObject in @($tracked.Output)) {
    $line = [string]$lineObject
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split "`t", 2
    if ($parts.Count -ne 2) { Stop-Ccc 'candidate_path_unparseable' 3 }
    $change = $parts[0]
    $path = $parts[1].Replace('\', '/')
    if ($change -notin @('A', 'M')) { Stop-Ccc 'candidate_change_type_forbidden' 3 }
    $entries[$path] = $change
  }

  $untracked = Invoke-GitSafe @('-C', $RepositoryRoot, '-c', 'core.quotepath=false', 'ls-files', '--others', '--exclude-standard', '--', 'coop') 'git_untracked_scan_failed'
  foreach ($lineObject in @($untracked.Output)) {
    $path = ([string]$lineObject).Replace('\', '/')
    if ([string]::IsNullOrWhiteSpace($path)) { continue }
    $entries[$path] = 'A'
  }

  $rows = @()
  $totalBytes = [int64]0
  $strictUtf8 = [System.Text.UTF8Encoding]::new($false, $true)
  foreach ($path in @($entries.Keys | Sort-Object)) {
    if (-not (Test-AllowedCoordinationPath $path)) {
      Stop-Ccc 'candidate_path_forbidden' 3
    }
    $nativeRelative = $path.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $fullPath = Join-Path $RepositoryRoot $nativeRelative
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
      Stop-Ccc 'candidate_file_missing' 3
    }
    $item = Get-Item -LiteralPath $fullPath -Force
    if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
      Stop-Ccc 'candidate_reparse_forbidden' 3
    }
    if ($item.Length -gt $MaxFileBytes) {
      Stop-Ccc 'candidate_file_too_large' 3
    }
    $totalBytes += [int64]$item.Length
    if ($totalBytes -gt $MaxSnapshotBytes) {
      Stop-Ccc 'candidate_snapshot_too_large' 3
    }
    $bytes = [System.IO.File]::ReadAllBytes($fullPath)
    if ([System.Array]::IndexOf($bytes, [byte]0) -ge 0) {
      Stop-Ccc 'candidate_nul_forbidden' 3
    }
    try {
      $text = $strictUtf8.GetString($bytes)
    }
    catch {
      Stop-Ccc 'candidate_non_utf8_forbidden' 3
    }
    if (Test-SecretText $text) {
      Stop-Ccc 'candidate_secret_detected' 3
    }
    $rows += [pscustomobject]@{
      Path = $path
      Change = $entries[$path]
      Bytes = [int64]$item.Length
      Sha256 = Get-Sha256Bytes $bytes
    }
  }

  $manifestLines = @($rows | ForEach-Object { "$($_.Change)|$($_.Path)|$($_.Bytes)|$($_.Sha256)" })
  $manifestText = $manifestLines -join "`n"
  return [pscustomobject]@{
    Rows = $rows
    Count = $rows.Count
    Bytes = $totalBytes
    Hash = if ($rows.Count -eq 0) { Get-Sha256Text '' } else { Get-Sha256Text $manifestText }
  }
}

function Write-SafeResult {
  $result = [ordered]@{
    schema = 'ccc_snapshot_result_v1'
    status = $script:status
    reason = $script:reason
    dry_run = [bool]$DryRun
    branch_match = [bool]$script:branchMatch
    candidate_count = [int]$script:candidateCount
    candidate_bytes = [int64]$script:candidateBytes
    candidate_manifest_hash = [string]$script:candidateManifestHash
    index_unchanged = [bool]$script:indexUnchanged
    commit_created = [bool]$script:commitCreated
    push_attempted = [bool]$script:pushAttempted
    push_succeeded = [bool]$script:pushSucceeded
  }
  Write-Output ($result | ConvertTo-Json -Compress)
}

$indexPath = $null
$indexHashBefore = 'unknown'
try {
  try {
    $script:root = (Resolve-Path -LiteralPath $ProjectRoot -ErrorAction Stop).Path
  }
  catch {
    Stop-Ccc 'project_root_invalid' 2
  }

  $topResult = Invoke-GitSafe @('-C', $script:root, 'rev-parse', '--show-toplevel') 'git_root_check_failed'
  $top = ([string]@($topResult.Output)[0]).Trim()
  try { $topResolved = (Resolve-Path -LiteralPath $top -ErrorAction Stop).Path } catch { Stop-Ccc 'git_root_invalid' 2 }
  $trimChars = [char[]]@('\', '/')
  if (-not [string]::Equals($topResolved.TrimEnd($trimChars), $script:root.TrimEnd($trimChars), [System.StringComparison]::OrdinalIgnoreCase)) {
    Stop-Ccc 'project_root_not_git_toplevel' 2
  }
  if (-not (Test-Path -LiteralPath (Join-Path $script:root 'coop') -PathType Container)) {
    Stop-Ccc 'coop_missing' 2
  }
  $coopItem = Get-Item -LiteralPath (Join-Path $script:root 'coop') -Force
  if (($coopItem.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
    Stop-Ccc 'coop_reparse_forbidden' 3
  }

  $gitCommonResult = Invoke-GitSafe @('-C', $script:root, 'rev-parse', '--git-common-dir') 'git_common_dir_failed'
  $gitCommon = ([string]@($gitCommonResult.Output)[0]).Trim()
  if (-not [System.IO.Path]::IsPathRooted($gitCommon)) { $gitCommon = Join-Path $script:root $gitCommon }
  try { $gitCommon = (Resolve-Path -LiteralPath $gitCommon -ErrorAction Stop).Path } catch { Stop-Ccc 'git_common_dir_invalid' 2 }
  $script:lockPath = Join-Path $gitCommon 'ccc_snapshot.lock'
  try {
    $script:lockStream = [System.IO.File]::Open($script:lockPath, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
    $script:lockStream.SetLength(0)
    $lockBytes = [System.Text.Encoding]::UTF8.GetBytes("pid=$PID")
    $script:lockStream.Write($lockBytes, 0, $lockBytes.Length)
    $script:lockStream.Flush()
    $script:lockAcquired = $true
  }
  catch [System.IO.IOException] {
    Stop-Ccc 'lock_held' 4
  }

  $indexResult = Invoke-GitSafe @('-C', $script:root, 'rev-parse', '--git-path', 'index') 'git_index_path_failed'
  $indexPath = ([string]@($indexResult.Output)[0]).Trim()
  if (-not [System.IO.Path]::IsPathRooted($indexPath)) { $indexPath = Join-Path $script:root $indexPath }
  $indexHashBefore = Get-FileHashSafe $indexPath

  $branchResult = Invoke-GitSafe @('-C', $script:root, 'symbolic-ref', '--quiet', '--short', 'HEAD') 'detached_head'
  $branch = ([string]@($branchResult.Output)[0]).Trim()
  $script:branchMatch = [string]::Equals($branch, $ExpectedBranch, [System.StringComparison]::Ordinal)
  if (-not $script:branchMatch) { Stop-Ccc 'expected_branch_mismatch' 2 }
  if ($branch -in @('main', 'master') -and -not $AllowProtectedBranch) { Stop-Ccc 'protected_branch_forbidden' 2 }

  $upstreamResult = Invoke-GitSafe @('-C', $script:root, 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{upstream}') 'upstream_missing'
  $upstream = ([string]@($upstreamResult.Output)[0]).Trim()
  if (-not [string]::Equals($upstream, "$Remote/$ExpectedBranch", [System.StringComparison]::Ordinal)) {
    Stop-Ccc 'upstream_branch_mismatch' 2
  }

  $countsResult = Invoke-GitSafe @('-C', $script:root, 'rev-list', '--left-right', '--count', "$upstream...HEAD") 'git_divergence_check_failed'
  $countParts = (([string]@($countsResult.Output)[0]).Trim() -split '\s+')
  if ($countParts.Count -ne 2) { Stop-Ccc 'git_divergence_unparseable' 5 }
  $behind = [int]$countParts[0]
  $ahead = [int]$countParts[1]
  if ($behind -gt 0) { Stop-Ccc 'branch_behind_upstream' 2 }

  $manifest = Get-CandidateManifest $script:root
  $script:candidateCount = $manifest.Count
  $script:candidateBytes = $manifest.Bytes
  $script:candidateManifestHash = $manifest.Hash
  $script:candidatePaths = @($manifest.Rows | ForEach-Object { $_.Path })

  if ($ahead -gt 0) {
    if ($ahead -ne 1 -or $script:candidateCount -ne 0) { Stop-Ccc 'unexpected_local_ahead' 2 }
    $headMessage = Invoke-GitSafe @('-C', $script:root, 'show', '-s', '--format=%B', 'HEAD') 'git_head_message_failed'
    $headBody = (@($headMessage.Output) -join "`n")
    if ($headBody -notmatch '(?m)^CCC-Snapshot: v1$') { Stop-Ccc 'unexpected_local_ahead' 2 }
    if ($DryRun) {
      $script:status = 'dry_run'
      $script:reason = 'pending_snapshot_push'
    }
    else {
      $script:pushAttempted = $true
      $pushRetry = Invoke-GitSafe @('-C', $script:root, 'push', '--porcelain', $Remote, "HEAD:refs/heads/$ExpectedBranch") 'git_push_failed' -AllowFailure
      if ($pushRetry.Code -ne 0) { Stop-Ccc 'git_push_failed' 6 }
      $script:pushSucceeded = $true
      $script:status = 'success'
      $script:reason = 'pending_snapshot_pushed'
    }
  }
  elseif ($script:candidateCount -eq 0) {
    $script:status = if ($DryRun) { 'dry_run' } else { 'noop' }
    $script:reason = 'no_candidate_changes'
  }
  elseif ($DryRun) {
    $script:status = 'dry_run'
    $script:reason = 'candidate_changes_valid'
  }
  else {
    if ([string]::IsNullOrWhiteSpace($Message)) {
      $Message = 'ccc: safe coordination snapshot'
    }
    if ($Message.Length -gt 120 -or $Message -match '[\r\n\x00-\x1F]' -or (Test-SecretText $Message)) {
      Stop-Ccc 'commit_message_forbidden' 3
    }

    $nativePaths = @($script:candidatePaths | ForEach-Object { $_.Replace('/', [System.IO.Path]::DirectorySeparatorChar) })
    $script:stagingAttempted = $true
    $null = Invoke-GitSafe (@('-C', $script:root, 'add', '--') + $nativePaths) 'git_add_failed'
    $commitArgs = @('-C', $script:root, 'commit', '--only', '-m', $Message, '-m', "CCC-Snapshot: v1`nCCC-Candidate-Hash: $($script:candidateManifestHash)", '--') + $nativePaths
    $commitResult = Invoke-GitSafe $commitArgs 'git_commit_failed' -AllowFailure
    if ($commitResult.Code -ne 0) { Stop-Ccc 'git_commit_failed' 5 }
    $script:commitCreated = $true

    $changedResult = Invoke-GitSafe @('-C', $script:root, '-c', 'core.quotepath=false', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD') 'git_commit_scope_check_failed'
    $changed = @($changedResult.Output | ForEach-Object { ([string]$_).Replace('\', '/') } | Where-Object { $_ } | Sort-Object -Unique)
    $expected = @($script:candidatePaths | Sort-Object -Unique)
    if (($changed -join "`n") -ne ($expected -join "`n")) { Stop-Ccc 'commit_scope_mismatch' 5 }

    $script:pushAttempted = $true
    $pushResult = Invoke-GitSafe @('-C', $script:root, 'push', '--porcelain', $Remote, "HEAD:refs/heads/$ExpectedBranch") 'git_push_failed' -AllowFailure
    if ($pushResult.Code -ne 0) { Stop-Ccc 'git_push_failed' 6 }
    $script:pushSucceeded = $true
    $script:status = 'success'
    $script:reason = 'snapshot_committed_and_pushed'
  }

  $indexHashAfter = Get-FileHashSafe $indexPath
  $script:indexUnchanged = [string]::Equals($indexHashBefore, $indexHashAfter, [System.StringComparison]::Ordinal)
  if ($DryRun -and -not $script:indexUnchanged) { Stop-Ccc 'dry_run_index_mutated' 5 }
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
  if ($script:stagingAttempted -and -not $script:commitCreated -and $script:root -and $script:candidatePaths.Count -gt 0) {
    $nativeCleanupPaths = @($script:candidatePaths | ForEach-Object { $_.Replace('/', [System.IO.Path]::DirectorySeparatorChar) })
    $null = Invoke-GitSafe (@('-C', $script:root, 'reset', '-q', 'HEAD', '--') + $nativeCleanupPaths) 'git_cleanup_failed' -AllowFailure
  }
  if ($indexPath -and $indexHashBefore -ne 'unknown') {
    $script:indexUnchanged = [string]::Equals($indexHashBefore, (Get-FileHashSafe $indexPath), [System.StringComparison]::Ordinal)
  }
  if ($script:lockStream) {
    $script:lockStream.Dispose()
    $script:lockStream = $null
  }
  if ($script:lockAcquired -and $script:lockPath -and (Test-Path -LiteralPath $script:lockPath -PathType Leaf)) {
    Remove-Item -LiteralPath $script:lockPath -Force -ErrorAction SilentlyContinue
  }
}

Write-SafeResult
exit $script:exitCode
