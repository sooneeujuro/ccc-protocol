# LEDGER_016 — corpus-binding Phase 2 빌드 완료 (운영자 GO), Codex 적대검증 요청

`2026-06-16` · Claude `67522dcd` · 협업모드 = Claude 빌드 → Codex 검증

VERDICT 요청: `ok | issues_found`.

## 0. 운영자 GO("다 바꿔") → Phase 2 빌드
manuscript-atelier `claude/corpus-binding-ledger` **commit `047a653`** (e58e81d→c7a7bcd 위, 7 files). 로컬·미push.

긴급도 사전평가: 게이트가 하드거부 아니라 플래그(`alignment_status`)였고 호출처가 smoke/test뿐이라 데이터위험 0 — 그래도 정본 인식하도록 교체.

## 1. 한 것 (옛 67b1 → 정본 55522119)
- **3 anchor sha 교체**: `retrieval/bge_dense_adapter.py:22`, `retrieval/evidence_packet_emitter.py:96` `CANONICAL_UNITS_SHA1` `67b1...`→`55522119...`; `schemas/EvidencePacket.spec.md:95` alignment anchor 동일 + SSOT를 옛 handoff→`CORPUS_BINDING.json`으로 재지정. + `retrieval/README.md`·emitter docstring 정정.
- **D1 advisory→ENFORCED**: `check_corpus_binding.py`가 이제 repo-local anchor가 binding sha와 다르면 **빌드 fail**(재드리프트 봉쇄). anchors 지금 일치 → green.
- `generated.md`는 D3만 남김(여전히 커밋코드만으로 재현). D2 런타임전용 유지.

## 2. 검증 (재현해줘)
```
grep -rn 67b1dbf2 tools/paper-orchestra --include=*.py --include=*.md | grep -v docs/handoffs   # → 0 (handoff만 남김=역사기록)
python tools/paper-orchestra/corpus/check_corpus_binding.py     # PASS (D1 enforced, anchors==bound; known_drifts 1=D3)
python -m pytest tools/paper-orchestra/nas-worker/production/tests tools/paper-orchestra/corpus/tests tools/paper-orchestra/retrieval/tests -q   # 787 passed
```
- 신규 테스트: `test_anchors_now_match_binding`(드리프트 0) + `test_d1_anchor_mismatch_is_enforced`(binding sha 흔들면 errors로 — 권고 아님).
- 67b1 픽스처 테스트들(test_bge_dense_adapter/evidence_packet_emitter/bm25_retrieval_client)은 상수 참조라 새 sha로 자동 통과(787 green).

## 3. 남긴 것 (의도적)
- **D3(draft_evidence_adapter repo-local 기본 index) = advisory 유지.** 이건 sha 플립이 아니라 운영적 이슈(repo-local corpus/index가 옛 incremental_mellor 미러). 절대경로 하드코딩 없이 고치려면 adapter에 binding-정렬 검증을 배선해야 함 → 별도 후속(운영자 판단). 지금 enforced로 올리면 빌드 깨지므로 리포트만.

## 4. 적대검증 요청
- (a) live 67b1 0 + checker PASS + 787 재현?
- (b) D1 enforced 실제 작동(binding/anchor 흔들면 fail)?
- (c) worker가 이제 정본 corpus(55522119)를 "verified"로 인식하나(옛 67b1로 거부 안 함)?
- (d) D3 advisory 유지 타당한가, 아니면 지금 enforce할 방법 제안?
- (e) 하드게이트: corpus 본문/index 미커밋·미push, 네트워크/DB 0.

## 다음
ok면 corpus-binding Phase 2 종료. 잔여=D3 후속 + 머지(MVP1+corpus-binding) 운영자 게이트. (운영: 자동폴링/Workflow OFF, 비용캡 $500 도달, 수동 wake.)
