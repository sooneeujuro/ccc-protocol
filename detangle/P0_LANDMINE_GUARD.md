# P0 — ma 워킹트리 저작권 코퍼스 215MB 노출 가드 (LANDMINE)

발견: 홈PC 감사(`reports/HOME_AUDIT_RESULT.md` §LANDMINE). 위험: 홈PC `manuscript-atelier`에서 `git add -A && push` 한 방이면 **저작권 figure 4,171 + paper MD 1,444 (≈215MB)** 가 public `manuscript-atelier.git`으로 유출.

## 즉시 가드 — `.gitignore` 추가 패치 (manuscript-atelier)
아래를 `manuscript-atelier/.gitignore` 끝에 추가:
```gitignore
# --- 저작권 코퍼스/figure 파생물: 절대 추적 금지 (P0 LANDMINE 2026-06-15) ---
docs/handoffs/**/out/
docs/handoffs/**/out_raw/
docs/handoffs/**/*.jpg
docs/handoffs/**/*.jpeg
# 논문 본문/그림 파생 일반 차단 (handoff scratch)
docs/handoffs/**/*.png
```
> `*.docx`/`*.pdf` 전역 차단은 정당한 문서까지 막을 수 있어 보류 — 필요시 운영자 판단.

## 적용 (운영자 게이트 — 어느 것이든)
1. **회사PC(권장, 전파용)**: 위 패치를 `manuscript-atelier`에 추가 → **main으로 PR 머지**. main에 들어가야 모든 브랜치(senpai-design 포함)가 다음 머지/리베이스 때 보호받음.
2. **홈PC(즉효)**: 자기 `senpai-design` 브랜치 `.gitignore`에 위 패치를 **명시적 path-add 커밋**(절대 `git add -A` 말 것)으로 추가.
3. 둘 다 하면 안전망 이중.

## 실물 out* 처분 (별개, 운영자 확인)
- `docs/handoffs/fig_refill_20260613/out/` + `out_raw/` 는 **NAS 통합본(fig root 4,001 이월완료)의 잔여물일 가능성**(홈PC 메모) → 운영자 확인 후 **NAS 이동 또는 삭제**. gitignore는 "새로 안 들어가게", 처분은 "있는 거 치우기" — 둘 다 필요.

## (선택) pre-commit 가드 — 사고 원천차단
전 repo `.git/hooks/pre-commit`에 staged 경로가 코퍼스 패턴(`wiki/papers/|*.jpg|*.npy|*.pkl|docs/handoffs/**/out`)이면 commit 거부. (축 A에서 전 repo 공통 가드로 정식화 예정.)

## 상태
- 가드 패치·지침 작성 완료(이 문서). **실제 .gitignore 커밋은 운영자 GO 게이트**(deploy repo).
- 그 전까지 **홈PC ma에서 `git add -A` 절대 금지** — 회사PC Claude 권고, 홈PC 감사도 동일 권고.
