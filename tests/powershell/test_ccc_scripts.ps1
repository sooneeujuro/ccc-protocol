$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$snapshotScript = Join-Path $repoRoot 'scripts\ccc_push_snapshot.ps1'
$installScript = Join-Path $repoRoot 'scripts\install-ccc.ps1'
$statusScript = Join-Path $repoRoot 'scripts\ccc_status.ps1'
$script:passCount = 0
$script:tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("ccc-powershell-tests-" + [guid]::NewGuid().ToString('N'))

function Assert-True {
  param([bool]$Condition, [string]$Message)
  if (-not $Condition) { throw "ASSERT_TRUE_FAILED: $Message" }
  $script:passCount++
}

function Assert-Equal {
  param($Expected, $Actual, [string]$Message)
  if ($Expected -ne $Actual) { throw "ASSERT_EQUAL_FAILED: $Message expected=[$Expected] actual=[$Actual]" }
  $script:passCount++
}

function Get-Hash {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return 'absent' }
  return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Invoke-Git {
  param([string[]]$Arguments)
  $output = @(& git @Arguments 2>&1)
  if ($LASTEXITCODE -ne 0) { throw 'TEST_GIT_FAILED' }
  return $output
}

function Invoke-GitOne {
  param([string[]]$Arguments)
  $output = @(Invoke-Git $Arguments)
  if ($output.Count -lt 1) { throw 'TEST_GIT_EMPTY' }
  return ([string]$output[0]).Trim()
}

function Invoke-ScriptProcess {
  param([string]$ScriptPath, [string[]]$Arguments)
  $output = @(& pwsh -NoLogo -NoProfile -File $ScriptPath @Arguments 2>&1)
  $code = $LASTEXITCODE
  $text = ($output | ForEach-Object { [string]$_ }) -join "`n"
  $json = $null
  if ($text.TrimStart().StartsWith('{')) {
    try { $json = $text | ConvertFrom-Json } catch { }
  }
  return [pscustomobject]@{ ExitCode = $code; Text = $text; Json = $json }
}

function Write-Utf8 {
  param([string]$Path, [string]$Text)
  $parent = Split-Path -Parent $Path
  if (-not (Test-Path -LiteralPath $parent -PathType Container)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Text, [System.Text.UTF8Encoding]::new($false))
}

try {
  New-Item -ItemType Directory -Path $script:tempRoot -Force | Out-Null
  $remote = Join-Path $script:tempRoot 'remote.git'
  $work = Join-Path $script:tempRoot 'work'
  $null = Invoke-Git @('init', '--bare', $remote)
  $null = Invoke-Git @('clone', $remote, $work)
  $null = Invoke-Git @('-C', $work, 'config', 'user.email', 'ccc-test@example.invalid')
  $null = Invoke-Git @('-C', $work, 'config', 'user.name', 'CCC Test')
  $null = Invoke-Git @('-C', $work, 'checkout', '-b', 'codex/test')

  # Install is exact-manifest, create-missing, and never stages files.
  $install = Invoke-ScriptProcess $installScript @('-ProjectRoot', $work, '-ProtocolRoot', $repoRoot)
  Assert-Equal 0 $install.ExitCode 'fresh install exits zero'
  Assert-True ($null -ne $install.Json) 'fresh install emits JSON only'
  Assert-Equal 'installed' $install.Json.status 'fresh install status'
  Assert-Equal 12 $install.Json.manifest_entry_count 'exact install manifest count'
  Assert-True $install.Json.index_unchanged 'install leaves index unchanged'
  Assert-True (Test-Path -LiteralPath (Join-Path $work 'coop\SUPERVISOR_POLICY.md')) 'supervisor policy installed'
  Assert-True (Test-Path -LiteralPath (Join-Path $work 'coop\scratch\.gitkeep')) 'scratch marker installed'

  $null = Invoke-Git @('-C', $work, 'add', 'coop')
  $null = Invoke-Git @('-C', $work, 'commit', '-m', 'base')
  $null = Invoke-Git @('-C', $work, 'push', '-u', 'origin', 'codex/test')

  # Existing content is preserved even when legacy -Force is passed.
  $runState = Join-Path $work 'coop\RUN_STATE.md'
  $sentinel = 'SENTINEL_PRIVATE_CONTENT_7e91'
  Write-Utf8 $runState $sentinel
  $runStateHash = Get-Hash $runState
  $installAgain = Invoke-ScriptProcess $installScript @('-ProjectRoot', $work, '-ProtocolRoot', $repoRoot, '-Force')
  Assert-Equal 0 $installAgain.ExitCode 'safe force exits zero'
  Assert-Equal 'force_overwrite_disabled' $installAgain.Json.reason 'force cannot overwrite'
  Assert-Equal $runStateHash (Get-Hash $runState) 'existing file preserved'
  Assert-True (-not $installAgain.Text.Contains($sentinel)) 'install output hides content'
  Assert-True (-not $installAgain.Text.Contains($work)) 'install output hides absolute root'
  $null = Invoke-Git @('-C', $work, 'restore', 'coop/RUN_STATE.md')

  # Status is read-only and emits no raw content, filename, or absolute path.
  $privateName = 'SENTINEL_PRIVATE_FILENAME_93bf.md'
  Write-Utf8 (Join-Path $work "coop\inbox_codex\$privateName") $sentinel
  New-Item -ItemType Directory -Path (Join-Path $work 'coop\.ccc\payloads') -Force | Out-Null
  Write-Utf8 (Join-Path $work 'coop\.ccc\payloads\local-only.json') $sentinel
  $indexPath = Invoke-GitOne @('-C', $work, 'rev-parse', '--git-path', 'index')
  if (-not [System.IO.Path]::IsPathRooted($indexPath)) { $indexPath = Join-Path $work $indexPath }
  $indexBeforeStatus = Get-Hash $indexPath
  $headBeforeStatus = Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')
  $status = Invoke-ScriptProcess $statusScript @('-ProjectRoot', $work)
  Assert-Equal 0 $status.ExitCode 'status exits zero'
  Assert-True $status.Json.read_only 'status reports read only'
  Assert-Equal 'unknown_no_machine_linkage' $status.Json.pending_status 'status does not invent pending state'
  Assert-Equal 13 $status.Json.coordination_file_count 'status excludes local supervisor state'
  Assert-True (-not $status.Text.Contains($sentinel)) 'status hides content'
  Assert-True (-not $status.Text.Contains($privateName)) 'status hides filename'
  Assert-True (-not $status.Text.Contains($work)) 'status hides absolute root'
  Assert-Equal $indexBeforeStatus (Get-Hash $indexPath) 'status leaves index unchanged'
  Assert-Equal $headBeforeStatus (Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')) 'status leaves HEAD unchanged'
  Remove-Item -LiteralPath (Join-Path $work "coop\inbox_codex\$privateName") -Force

  # Dry-run must not stage its candidate or disturb unrelated staged work.
  Write-Utf8 (Join-Path $work 'user.txt') 'user staged work'
  $null = Invoke-Git @('-C', $work, 'add', 'user.txt')
  Write-Utf8 (Join-Path $work 'coop\STATUS_codex.md') 'Status: safe candidate'
  $indexBeforeDry = Get-Hash $indexPath
  $stagedBeforeDry = (@(Invoke-Git @('-C', $work, 'diff', '--cached', '--binary')) -join "`n")
  $headBeforeDry = Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')
  $remoteBeforeDry = Invoke-GitOne @('--git-dir', $remote, 'rev-parse', 'refs/heads/codex/test')
  $dry = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
  Assert-Equal 0 $dry.ExitCode ("dry-run exits zero output=" + $dry.Text)
  Assert-Equal 'dry_run' $dry.Json.status 'dry-run status'
  Assert-True $dry.Json.index_unchanged 'dry-run reports immutable index'
  Assert-Equal $indexBeforeDry (Get-Hash $indexPath) 'dry-run raw index hash unchanged'
  Assert-Equal $stagedBeforeDry (@(Invoke-Git @('-C', $work, 'diff', '--cached', '--binary')) -join "`n") 'dry-run staged patch unchanged'
  Assert-Equal $headBeforeDry (Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')) 'dry-run HEAD unchanged'
  Assert-Equal $remoteBeforeDry (Invoke-GitOne @('--git-dir', $remote, 'rev-parse', 'refs/heads/codex/test')) 'dry-run remote unchanged'

  # A real snapshot commits only coop and preserves unrelated staged content.
  $snapshot = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test')
  Assert-Equal 0 $snapshot.ExitCode 'snapshot exits zero'
  Assert-True $snapshot.Json.commit_created 'snapshot creates commit'
  Assert-True $snapshot.Json.push_succeeded 'snapshot pushes'
  $changed = @(Invoke-Git @('-C', $work, 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'))
  Assert-Equal 1 $changed.Count 'snapshot commit has one path'
  Assert-Equal 'coop/STATUS_codex.md' ([string]$changed[0]) 'snapshot commit scope exact'
  $stillStaged = @(Invoke-Git @('-C', $work, 'diff', '--cached', '--name-only'))
  Assert-Equal 1 $stillStaged.Count 'unrelated staged count preserved'
  Assert-Equal 'user.txt' ([string]$stillStaged[0]) 'unrelated staged path preserved'

  # A pre-staged coop file is ambiguous and must block without changing HEAD.
  Write-Utf8 (Join-Path $work 'coop\STATUS_codex.md') 'Status: ambiguous candidate'
  $null = Invoke-Git @('-C', $work, 'add', 'coop/STATUS_codex.md')
  $headAmbiguous = Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')
  $ambiguous = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
  Assert-Equal 3 $ambiguous.ExitCode 'pre-staged coop blocks'
  Assert-Equal 'pre_staged_coop_ambiguous' $ambiguous.Json.reason 'pre-staged reason stable'
  Assert-Equal $headAmbiguous (Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')) 'ambiguous run leaves HEAD'
  $null = Invoke-Git @('-C', $work, 'reset', '-q', 'HEAD', '--', 'coop/STATUS_codex.md')
  $null = Invoke-Git @('-C', $work, 'restore', 'coop/STATUS_codex.md')

  # Wrong branch and held lock fail before mutation.
  Write-Utf8 (Join-Path $work 'coop\STATUS_codex.md') 'Status: branch guard candidate'
  $wrongBranch = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/wrong', '-DryRun')
  Assert-Equal 2 $wrongBranch.ExitCode 'wrong expected branch blocks'
  Assert-Equal 'expected_branch_mismatch' $wrongBranch.Json.reason 'wrong branch reason stable'
  $commonDir = Invoke-GitOne @('-C', $work, 'rev-parse', '--git-common-dir')
  if (-not [System.IO.Path]::IsPathRooted($commonDir)) { $commonDir = Join-Path $work $commonDir }
  $lockPath = Join-Path $commonDir 'ccc_snapshot.lock'
  $lock = [System.IO.File]::Open($lockPath, [System.IO.FileMode]::OpenOrCreate, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
  try {
    $locked = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
    Assert-Equal 4 $locked.ExitCode 'held lock blocks'
    Assert-Equal 'lock_held' $locked.Json.reason 'held lock reason stable'
  }
  finally { $lock.Dispose(); if (Test-Path -LiteralPath $lockPath) { Remove-Item -LiteralPath $lockPath -Force } }
  $null = Invoke-Git @('-C', $work, 'restore', 'coop/STATUS_codex.md')

  # Forbidden type, NUL, and synthetic secret all fail closed without echoing data.
  Write-Utf8 (Join-Path $work 'coop\reports\payload.pdf') 'not really a pdf'
  $forbidden = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
  Assert-Equal 3 $forbidden.ExitCode 'forbidden path blocks'
  Assert-Equal 'candidate_path_forbidden' $forbidden.Json.reason 'forbidden path reason stable'
  Remove-Item -LiteralPath (Join-Path $work 'coop\reports\payload.pdf') -Force

  [System.IO.File]::WriteAllBytes((Join-Path $work 'coop\reports\nul.md'), [byte[]](65, 0, 66))
  $nul = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
  Assert-Equal 3 $nul.ExitCode 'NUL blocks'
  Assert-Equal 'candidate_nul_forbidden' $nul.Json.reason 'NUL reason stable'
  Remove-Item -LiteralPath (Join-Path $work 'coop\reports\nul.md') -Force

  $secret = 'OPENAI_API_KEY=sk-SYNTHETICVALUE1234567890'
  Write-Utf8 (Join-Path $work 'coop\reports\secret.md') $secret
  $secretResult = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test', '-DryRun')
  Assert-Equal 3 $secretResult.ExitCode 'secret blocks'
  Assert-Equal 'candidate_secret_detected' $secretResult.Json.reason 'secret reason stable'
  Assert-True (-not $secretResult.Text.Contains($secret)) 'secret never echoed'
  Remove-Item -LiteralPath (Join-Path $work 'coop\reports\secret.md') -Force

  # Native commit failure returns nonzero and cleans only supervisor staging.
  Write-Utf8 (Join-Path $work 'coop\STATUS_codex.md') 'Status: hook failure candidate'
  $hooks = Join-Path $work '.git\hooks'
  $hookSentinel = 'HOOK_PRIVATE_SENTINEL_125c'
  Write-Utf8 (Join-Path $hooks 'pre-commit') "#!/bin/sh`necho $hookSentinel 1>&2`nexit 17`n"
  $commitFailure = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test')
  Assert-Equal 5 $commitFailure.ExitCode 'native commit failure propagates'
  Assert-Equal 'git_commit_failed' $commitFailure.Json.reason 'commit failure reason stable'
  Assert-True (-not $commitFailure.Text.Contains($hookSentinel)) 'hook stderr hidden'
  $stagedAfterFailure = @(Invoke-Git @('-C', $work, 'diff', '--cached', '--name-only'))
  Assert-Equal 1 $stagedAfterFailure.Count 'only unrelated stage remains after failure'
  Assert-Equal 'user.txt' ([string]$stagedAfterFailure[0]) 'candidate staging cleaned after failure'
  Remove-Item -LiteralPath (Join-Path $hooks 'pre-commit') -Force

  # Push failure leaves one retryable supervisor commit; retry creates no duplicate.
  $prePushSentinel = 'PUSH_PRIVATE_SENTINEL_919a'
  Write-Utf8 (Join-Path $hooks 'pre-push') "#!/bin/sh`necho $prePushSentinel 1>&2`nexit 19`n"
  $headBeforePushFailure = Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')
  $pushFailure = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test')
  Assert-Equal 6 $pushFailure.ExitCode 'native push failure propagates'
  Assert-Equal 'git_push_failed' $pushFailure.Json.reason 'push failure reason stable'
  Assert-True (-not $pushFailure.Text.Contains($prePushSentinel)) 'push stderr hidden'
  $failedCommit = Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')
  Assert-True ($failedCommit -ne $headBeforePushFailure) 'one local snapshot commit retained'
  Remove-Item -LiteralPath (Join-Path $hooks 'pre-push') -Force
  $retry = Invoke-ScriptProcess $snapshotScript @('-ProjectRoot', $work, '-ExpectedBranch', 'codex/test')
  Assert-Equal 0 $retry.ExitCode 'pending push retry succeeds'
  Assert-Equal 'pending_snapshot_pushed' $retry.Json.reason 'retry path identified'
  Assert-Equal $failedCommit (Invoke-GitOne @('-C', $work, 'rev-parse', 'HEAD')) 'retry makes no duplicate commit'

  Write-Output ("PASS assertions=" + $script:passCount)
}
finally {
  if (Test-Path -LiteralPath $script:tempRoot) { Remove-Item -LiteralPath $script:tempRoot -Recurse -Force -ErrorAction SilentlyContinue }
}
