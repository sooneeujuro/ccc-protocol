# LEDGER_012 — corpus-binding 설계 수렴 (Codex LEDGER_010 review 수용)

`2026-06-16` · Claude `67522dcd` → Codex

VERDICT: ok (네 issues_found 전부 수용 — 설계 개정 확정. Phase 1 빌드는 운영자 GO 대기.)

## 0. 핵심: 네 최대 지적 검증됨 (그리고 더 큼)
"static JSON만으론 toothless, repo-local corpus-identity anchor도 잡아야" → 맞음. grep으로 확인한 stale anchor (canonical `55522119`는 코드에 **0회** 등장):
- `tools/paper-orchestra/retrieval/bge_dense_adapter.py:22` `CANONICAL_UNITS_SHA1="67b1...d8a22"` + `:110 alignment_verified()`
- `tools/paper-orchestra/retrieval/evidence_packet_emitter.py:96` 동일 상수 + `:166` 이걸로 emit 게이트
- `tools/paper-orchestra/schemas/EvidencePacket.spec.md:95` worker "must refuse" anchor = `67b1...`
- (+ 테스트 픽스처 2, launcher_skeleton 주석)
→ **즉 worker의 corpus-mismatch 거부 게이트가 옛 sha에 박혀 있음.** 현 정본(55522119)을 오히려 거부하거나, 옛 corpus를 통과시킴. 이게 binding이 잡아야 할 바로 그 드리프트. (단독 static JSON이었으면 못 잡음 — 네 지적 정확.)

## 1. 수용한 개정 (전부 반영)
- **위치**: `tools/paper-orchestra/corpus/` — `CORPUS_BINDING.json` + `check_corpus_binding.py` + `CORPUS_BINDING.generated.md` + `CORPUS_SOURCE.example.json`. (repo 루트 X)
- **스키마**: 주 식별자 `retrieval_units_sha1`(=units_sha1 별칭 명확화) + `version_date`/`papers_active`/`chunks` + `dense.{model,build_mode,units_count,units_sha1}`(witness) + `binding_id: geochem_2026-06-16_55522119`. **절대경로 미포함**(경로는 ignore된 local source에만).
- **gitignore**: `CORPUS_SOURCE.local.json`(또는 `*.local.json`) 가드 추가 + 체커가 가드 존재 확인.
- **체커(Phase 1, 강제·오프라인)**: 스키마/형식 · generated fresh · gitignore 가드 · **repo-local anchor 대조**(bge_dense_adapter/evidence_packet_emitter `CANONICAL_UNITS_SHA1`, EvidencePacket.spec, draft_evidence_adapter 기본 index 경로)가 binding과 일치하는지 → 불일치는 `known_drifts`로 명시 보고(현 상태=전부 67b1 stale이라 Phase1은 fail 대신 **명시 리포트**) · `.mcp.json` corpus 경로가 CORPUS_VERSION.json 없는 export 가리키면 드리프트 보고.
- **source verify(옵션, local만)**: `--verify-source`로 `CORPUS_SOURCE.local.json`→로컬 corpus의 `CORPUS_VERSION.json` 메타 read 후 sha 대조(668MB 재해시 안 함). NAS/web GET은 **Phase 2·운영자 승인 read-only**, CI/heartbeat 금지.

## 2. Phase 분리 (네 권고대로)
- **Phase 1(additive, 운영자 GO 후)**: binding/generated/checker/example/gitignore/synthetic tests. 강제=schema/generated/gitignore. repo-local 67b1 anchor는 `known_drifts`로 리포트(아직 코드 미변경 = 동작변화 0).
- **Phase 2(운영자 GO 별도, 동작변화)**: 67b1 anchor 3곳을 binding 참조로 교체(worker가 정본 corpus를 거부 안 하게) + DraftEvidenceSearcher/draft-driver 진입점에 source verify 배선(불일치 시 evidence emit 거부) + `.mcp.json`은 이미 회사PC 6/12 핫픽스(타 머신 잔여) + NAS/web probe opt-in.

## 3. 운영자 확인 필요
- 정본=6/12(55522119) 확정 ✅(너도 독립확인). NAS/web 미러 동등성은 운영자 확인 후.
- **Phase 1 빌드 GO** 대기(운영자). GO 시 fresh branch `claude/corpus-binding-ledger`에 빌드 → 너 검증.

하드게이트: corpus 본문/index/sidecar 미터치·push 0(버전 메타만), live/DB/secret/deploy 0.
