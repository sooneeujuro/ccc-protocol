# Claude(Code) — Draft writing preflight exporter break-it (LEDGER_116 / `8333086`)

`2026-06-17 22:1x` · Draft Workspace -> writing-runner 다리(MVP B 슬라이스).

VERDICT: **ok — exporter sound. ID-binding seam이 구조적으로 닫힘(라이브 확정).**

## 라이브 break-it (repo_root=REAL로 scratch 아티팩트 제거 후)
- **ID 존재증명(핵심)**: `allowed_claim_ids=["claim_001"]`(bundle 실재) → **OK**; `["claim_999_FAKE"]`(날조) → **REJECT `selected_id_missing`** ✅. → operator가 준 ID가 *bundle에 실재함을 증명*한 뒤에만 통과. **이게 내가 CIR/Kim2024 리뷰에서 지목한 "최종 인용이 prose `(저자,연도)` 텍스트매칭이 아니라 ID-bind여야 한다"의 구조적 구현.** 날조 ID는 task에 못 들어감.
- **prose 비누수**: 생성 payload 전체 = `schema/draft_id/workspace_status(enum)/booleans/allowed_*_ids/blocked_*/source_role_kinds(enum)/ready_for_task_builder/generated_from(sha256)/bundle(sha256)`. **40+자 string은 manifest_sha256(64hex) 하나뿐 = prose/snippet/title/manuscript/path 0** ✅. (초기 leak=YES는 내 휴리스틱이 sha256을 prose로 오탐한 false-positive, 정밀 walk로 정정.)
- **require_decomposition 게이트**: 유효 decomposition 없으면(또는 generated stale) `draft_context_check_failed` fail-closed ✅.

## Codex 테스트 커버 (확인)
- `test_writing_task_preflight_exports_bundle_validated_ids`(happy) · `test_writing_task_preflight_requires_decomposition`(게이트) · **`test_writing_task_preflight_rejects_missing_bundle_id`(날조 ID 거부 = 핵심)** ✅.

## 의미 (큰 그림)
이 exporter는 **Draft Workspace의 검증된 decomposition → writing-runner의 ID-bound preflight**로 변환하는 다리. 핵심 성질 = (1) bundle ID 실존 증명(날조/텍스트매칭 차단) (2) prose-free(ids/enums/hash only) (3) decomposition 선결. **이번 세션 내내 추적한 "citation/claim이 텍스트가 아니라 ID로 묶여야 한다"가 코드로 닫힘.** decomposition family(role/figure/stats) + 이 preflight = MVP B bridge의 안전 코어 견고.

## 정직 메모
scratch REPO_ROOT 오계산으로 처음 check_failed 아티팩트 → repo_root=REAL 넘겨 해소(진짜 버그 아님). 라이브 repro 로컬 `.scratch/preflight-gate`. preflight-surface 체커(draft_context의 optional closed-shape)는 closed-key/enum/sha 검증한다는 LEDGER 설명 + 기존 패턴 신뢰로 깊은 dup-key repro는 생략(필요시 다음 라운드).

(manuscript-atelier 커밋0 · 라이브=로컬.)
