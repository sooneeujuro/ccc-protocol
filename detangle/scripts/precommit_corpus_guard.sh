#!/bin/sh
# CCCP de-tangle — 저작권 코퍼스/대용량 산출물 commit 가드 (pre-commit hook).
# 코퍼스 본문·figure·sidecar·대용량 인덱스·백업 잔여물이 staged되면 commit 거부.
# 설치: 각 clone에서  cp precommit_corpus_guard.sh <repo>/.git/hooks/pre-commit && chmod +x ...
#       (git hook은 clone 따라 안 감 → clone마다 설치, 또는 core.hooksPath 공유.)
# 의도적 commit:  ALLOW_CORPUS_COMMIT=1 git commit ...
[ "$ALLOW_CORPUS_COMMIT" = "1" ] && exit 0

staged=$(git diff --cached --name-only --diff-filter=AM)
[ -z "$staged" ] && exit 0

# 차단 패턴 — 위험 디렉터리/확장자에 한정(앱 public 이미지 등 정상자산 오차단 회피).
#  · 코퍼스 본문/노트:  wiki/papers/*.md, wiki/data/, articles/*.md, */corpus/*.{md,jsonl}, sidecars/*.json
#  · figure 파생:       docs/handoffs/**/out|out_raw/, docs/handoffs/**/*.jpg|jpeg
#  · 대용량 인덱스:     */index/*.{npy,pkl,jsonl}, 전역 *.npy|*.pkl
#  · 백업 잔여물:       *.bak.<timestamp>, *.report.json
pattern='(^|/)wiki/papers/.*\.md$|(^|/)wiki/data/|(^|/)articles/.*\.md$|/corpus/.*\.(md|jsonl)$|(^|/)sidecars?/.*\.json$|docs/handoffs/.*/(out|out_raw)/|docs/handoffs/.*\.(jpg|jpeg)$|/index/.*\.(npy|pkl|jsonl)$|\.(npy|pkl)$|\.bak\.[0-9]|\.report\.json$'

hits=$(printf '%s\n' "$staged" | grep -E "$pattern")
if [ -n "$hits" ]; then
  echo "" >&2
  echo "✋ [corpus-guard] 저작권 코퍼스/대용량 산출물이 staged됨 — commit 차단:" >&2
  printf '%s\n' "$hits" | sed 's/^/   /' >&2
  echo "" >&2
  echo "→ git 원격에 올리면 안 됨(저작권/대용량). 'git rm --cached <파일>'로 unstage." >&2
  echo "→ 정말 의도한 거면: ALLOW_CORPUS_COMMIT=1 git commit ..." >&2
  exit 1
fi
exit 0
