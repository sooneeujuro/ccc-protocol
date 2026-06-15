<#
.SYNOPSIS
  De-tangle 1단계: 로컬 git 클론들의 미push 작업 read-only 감사.
  origin에 안 올라간 커밋 / 미커밋 / 코퍼스 건드림 여부를 markdown 리포트로 출력.
.NOTES
  비파괴. git fetch(읽기) 외엔 working tree/원격 변경 없음. push/commit/delete 일절 안 함.
.LIMITATION (2026-06-15 홈PC 발견 — 재사용 전 수정 권장)
  `rev-list --count <b> --not --remotes=origin` 은 "origin ref에 없는 커밋"만 셈 →
  origin tip이 등가작업으로 전진(분기)한 경우 **diverged-duplicate를 "미push"로 오판**.
  "push 안전 여부"를 정확히 보려면 브랜치별로 추가:
    git rev-list --left-right --count <local>...<origin-counterpart>   # ahead/behind
    git merge-base --is-ancestor <local> origin/<b> && echo FF가능      # superseded 판정
  (현 스크립트는 미push '후보'만 출력 — diverged 여부는 별도 확인 필요.)
#>
param(
  [string[]]$RepoPaths = @(
    'C:\Users\soone\geochemistry-analyzer-git',
    'C:\Users\soone\Documents\manuscript-atelier'
  ),
  [string]$OutFile = "$PSScriptRoot\..\reports\HOME_AUDIT_RESULT.md"
)

# origin에도 있으면 push된 것. 아래 패턴이 미push 커밋에 잡히면 '코퍼스/저작권 → push 금지' 플래그.
$corpusRegex = 'wiki/papers/|wiki/data/|articles/|sidecar|datalab/|corpus/|\.docx$|\.pdf$|\.xlsx$|\.csv$|\.npy$|\.pkl$'

function GitR {
  param([string]$Repo, [Parameter(ValueFromRemainingArguments = $true)] $a)
  & git -C $Repo @a
}

$L = New-Object System.Collections.Generic.List[string]
$L.Add('VERDICT: <ok | issues_found | blocked>   # 보고 시 채울 것')
$L.Add('')
$L.Add('# 홈PC 미push 감사 (read-only)')
$L.Add("- 생성: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  | machine: $env:COMPUTERNAME / $env:USERNAME")
$L.Add('')

foreach ($repo in $RepoPaths) {
  $L.Add('---')
  $L.Add("## repo: ``$repo``")
  if (-not (Test-Path (Join-Path $repo '.git'))) {
    $L.Add("- ❌ git repo 아님/없음 — 경로 교정 필요 (`git -C <후보> remote get-url origin`으로 확인)")
    $L.Add('')
    continue
  }

  & git -C $repo fetch origin --prune *> $null
  if ($LASTEXITCODE -ne 0) { $L.Add('- ⚠️ fetch 실패(offline?) — 아래 미push는 마지막 fetch 기준') } else { $L.Add('- fetch OK') }

  $origin = (GitR $repo remote get-url origin) 2> $null
  $cur = GitR $repo branch --show-current
  $head = GitR $repo rev-parse --short HEAD
  $L.Add("- origin: $origin")
  $L.Add("- HEAD: $head on '$cur'")
  $L.Add('')
  $L.Add('### 브랜치별 미push 커밋 (origin 어느 ref에도 없는 것)')
  $L.Add('')
  $L.Add('| branch | 미push 커밋수 | 코퍼스 건드림? |')
  $L.Add('|---|---|---|')

  $branches = GitR $repo for-each-ref --format='%(refname:short)' refs/heads/
  $detail = New-Object System.Collections.Generic.List[string]
  foreach ($b in $branches) {
    $cnt = (GitR $repo rev-list --count $b --not --remotes=origin).Trim()
    $files = GitR $repo log $b --not --remotes=origin --name-only --pretty=format:
    $hits = @($files | Where-Object { $_ -match $corpusRegex } | Select-Object -Unique)
    $flag = if ($hits.Count -gt 0) { "⚠️ YES ($($hits.Count) files)" } else { 'code-only' }
    $L.Add("| $b | $cnt | $flag |")
    if ([int]$cnt -gt 0) {
      $detail.Add('')
      $detail.Add("#### $b — 미push 커밋 $cnt개")
      $detail.Add('```')
      $detail.Add((GitR $repo log $b --not --remotes=origin --pretty=format:'%h %ai %s'))
      $detail.Add('```')
      if ($hits.Count -gt 0) {
        $detail.Add('**⚠️ 코퍼스/저작권 건드린 파일 (push 금지, 보고만):**')
        $detail.Add('```')
        $detail.Add(($hits -join "`n"))
        $detail.Add('```')
      }
    }
  }
  $L.Add('')
  $L.Add('### 미push 커밋 상세')
  foreach ($d in $detail) { $L.Add($d) }

  $L.Add('')
  $L.Add('### 작업트리 미커밋')
  $porc = GitR $repo status --porcelain
  if ($porc) { $L.Add('```'); foreach ($p in $porc) { $L.Add($p) }; $L.Add('```') } else { $L.Add('- clean') }

  $L.Add('')
  $L.Add('### worktree 목록')
  $L.Add('```')
  $L.Add((GitR $repo worktree list))
  $L.Add('```')
  $L.Add('')
}

$dir = Split-Path $OutFile
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
($L -join "`r`n") | Set-Content -Path $OutFile -Encoding utf8
Write-Host "리포트 작성됨: $OutFile`n"
$L -join "`n" | Write-Host
