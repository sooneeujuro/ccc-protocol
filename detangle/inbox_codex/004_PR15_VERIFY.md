# TASK 004 — Codex 검증: ma PR#15 corpus verification policy (+ 회사PC 추가분)

발행: 회사PC Claude → Codex. 보고: `inbox_claude/004_PR15_VERIFY_VERDICT.md` (VERDICT). push 전 `git pull --rebase origin coop/detangle-20260615`.

## 대상
manuscript-atelier **PR#15** (`docs/corpus-verification-policy`, base main). 노트북 작성 + 회사PC가 추가분 push(`5a05c2f`).
- `gh pr diff 15 --repo sooneeujuro/manuscript-atelier` 또는 브랜치 pull로 확인.
- 파일: `docs/design/corpus_verification_policy_v0.md` + 신규 `docs/design/verification_protocols.json` + `senpai.md` 패치.

## 검증 항목 (read-only, 머지 금지)
1. **(A)/(B) 구분 건전성**: corpus-provenance(A, 허용) vs student-claim 인증(B, RIL 금지) 구분이 일관되나? senpai.md 패치가 (A)를 허용하면서 (B)를 확실히 막나? "툴 없으면 능력 날조 금지" 가드 충분?
2. **§0.5 정규화 전제**: "verifications가 variable_id 안정키로 매칭 → 73% raw_label_only면 헛매칭 → 정규화(VP-NORM-1) 선행 필수" 논리 타당? raw_label_snapshot 보완이 충분/부족?
3. **protocol registry**(`verification_protocols.json`): 스키마 일관? VP-NORM-1/VP-CVM-1/VP-CERT-1의 code/purpose/known_limits 적절? `verifications[].protocol` + `meta.protocols` 참조가 registry와 정합? 재인증 추적성(버전 bump+태그보존) 설계 견고?
4. **데이터모델 안전**: additive(원본 미덮음)·인접파일·CAS·dedup·server-stamp·false-positive 가드가 v0.1로 충분한가? 빠진 위험?
5. **모순/갭**: PR이 자기 §7(흩어진 조각)을 제대로 통합했나? 남은 모순?

## 제약
read-only. PR 머지/코드변경 금지. 보고는 `inbox_claude/004_PR15_VERIFY_VERDICT.md`. 이슈는 구체적 파일:줄/섹션으로.
