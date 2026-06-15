# TASK 002 — Codex 검증: corpus 가드 (pre-commit hook + repo별 gitignore)

발행: 회사PC Claude → Codex. 채널: ccc-protocol `coop/detangle-20260615`. 보고: `inbox_claude/002_GUARD_VERIFY_VERDICT.md` (VERDICT ok/issues_found/blocked). push 전 `git pull --rebase origin coop/detangle-20260615`.

## 배경
축 A = "코퍼스가 git에 *새로* 안 들어가게". Claude가 가드 작성: `scripts/precommit_corpus_guard.sh` + `GUARD_DEPLOY.md`(repo별 gitignore). 너는 이게 **잘 잡고(코퍼스) 안 막나(정상자산)** 독립 검증.

## 검증 항목 (전부 read-only)
1. **잡는가 (true positive)**: hook regex가 다음을 차단하나? — `docs/handoffs/fig_refill_20260613/out/*.jpg`, `wiki/papers/*.md`, `*/corpus/*.jsonl`, `index/*.npy`, `*.bak.20260518_*`, `*.report.json`. (실제 경로 샘플로 `printf | grep -E` 돌려 확인.)
2. **오차단 (false positive) — 핵심**: 각 repo에서 가드가 **정상 파일을 막진 않나** 확인:
   - `geochemistry-analyzer`: `public/**/*.jpg|png` 같은 앱 자산, `tools/geochem-stats/index/variable-vocabulary.json`(빌드 의존 — **절대 막으면 안 됨**)이 패턴에 안 걸리나?
   - `sooneeujuro-web`: `public/`·fixture 이미지가 안 걸리나?
   - `manuscript-atelier`: 정상 docs(.md)·샘플 패킷이 안 걸리나? (가드는 `docs/handoffs/**/out*`·`*.jpg` 한정이라 일반 .md는 통과해야 함.)
3. **gitignore 정확성**: `GUARD_DEPLOY.md`의 repo별 패치가 (a) 위험만 덮고 (b) `variable-vocabulary.json`을 `!`로 제외 유지하나? geochem은 이미 tracked라 ignore만으론 부족(history rewrite 필요)함을 확인.
4. (선택) 더 잡아야 할 코퍼스 패턴 / 빼야 할 과잉 패턴 제안.

## 제약 (CCCP)
- read-only. 실제 commit/hook 설치/repo 변경 금지(검증만). geochem-analyzer에 커밋 금지. 코퍼스 remote push 금지.
- 보고는 `inbox_claude/002_GUARD_VERIFY_VERDICT.md` 한 파일. 오차단 발견 시 구체적 파일경로로.
