# 밤샘 자율운영 (Claude 회사PC, 2026-06-15 23:2x~)

운영자: **전권 위임** ("손 안 댈래, 끝까지 굴려"). 모니터: GitHub issue#1 + 이 브랜치. 정지: `coop/STOP.md` 또는 `detangle/STOP.md` 한 줄.

## 안전 계약 (이걸 어기면 멈춤)
1. **비파괴 우선** — 모든 파괴/force-push/삭제 *전에* `git bundle` 풀백업. 복구경로 없으면 그 단계 보류.
2. **Codex 게이트** — 비가역 단계(history rewrite·freeze·클론삭제·deploy) 전에 `inbox_codex/`로 검증요청 → VERDICT=ok 받고만 실행. issues_found/blocked면 보류+보고.
3. **예산 하드캡 $60** (Claude API $100 중). B1 재추출만 과금. 캡 도달 시 자동중단. 탐지기-우선이라 멀쩡한 편 재추출 0(중복작업 회피).
4. **STOP 감시 + 로깅** — 매 단계 RUN_STATE 로그 + 콘솔 보고. STOP 발견 시 즉시 정지 + FINAL_SUMMARY.
5. **history rewrite(force-push)** = 최고위험. 풀백업 + Codex green 둘 다 통과해야 실행. 하나라도 안 되면 staged로 두고 운영자 인계(나머지 완료한 채).

## 작업 큐 (순서)
| # | 단계 | 위험 | 게이트 |
|---|---|---|---|
| 1 | **B1 탐지기** (현 corpus 008 결함 잔존 탐지, 무료·로컬) | 🟢 read-only | 없음 |
| 2 | B1 타깃 재추출 (결함 있을 때만, Sonnet, 캡$60) + 검증 | 🟡 과금 | 예산캡 |
| 3 | 축 A 가드 적용 (repo gitignore+pre-commit hook) | 🟢 가역 커밋 | Codex spot |
| 4 | 클론 .env.local 백업 → Cursor/codes 정리 + worktree prune | 🟠 삭제 | 백업+Codex |
| 5 | PR#14 머지 + sink-hardening→main + Vercel deploy | 🟠 외부 | Codex+backup |
| 6 | history rewrite(geochem 코퍼스 purge) → GCA freeze | 🔴 비가역 | 풀백업+Codex green (실패시 staged 인계) |

## 진행 로그 (append-only)
- 23:2x — 밤샘런 시작. OVERNIGHT_RUN 작성, 콘솔 공지. Step1(탐지기) 착수.
