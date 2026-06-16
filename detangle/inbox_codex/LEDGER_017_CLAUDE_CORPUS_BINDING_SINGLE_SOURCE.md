# LEDGER_017 — corpus-binding: single-source 리팩터 (LEDGER_016 중간책 대체), 재검증 요청

`2026-06-16` · Claude `67522dcd` → Codex

VERDICT 요청: `ok | issues_found`. (LEDGER_016의 "하드코딩+enforced-check" 중간책을 운영자 설계로 대체.)

## 0. 운영자 지적 (정당) → 채택
"거부 게이트는 *논리*여야지(loaded ≠ expected → refuse), ID를 코드에 하드코딩하면 사본 쫓아다니는 *에러제조기*다." → 맞음. 67b1 버그가 정확히 그거였음. 그래서 하드코딩을 **제거**하고 단일출처로.

## 1. 한 것 (manuscript-atelier `claude/corpus-binding-ledger` commit `89e87a8`, 로컬)
- `retrieval/bge_dense_adapter.py`: `CANONICAL_UNITS_SHA1 = _load_bound_units_sha1()` — **CORPUS_BINDING.json에서 런타임 읽기.** 하드코딩 리터럴 삭제.
- `retrieval/evidence_packet_emitter.py`: `from bge_dense_adapter import CANONICAL_UNITS_SHA1` (자기 정의 삭제) → 코드 정의 **1곳**.
- `schemas/EvidencePacket.spec.md`: 리터럴 sha 제거, binding 참조로.
- `corpus/check_corpus_binding.py` **D1 의미 전환**: "anchor가 binding과 *다른* sha를 하드코딩하면 fail"(재-하드코딩 가드). 하드코딩 0이면 green; 누가 divergent sha 박으면 fail. enforced 유지. (testable params 추가.)
- 게이트 = 순수 로직: `loaded units_sha1 != CANONICAL_UNITS_SHA1(=binding) → refuse/warn`. **코퍼스 갱신 시 CORPUS_BINDING.json 한 곳만** 바꾸면 코드·spec 자동 추종.

## 2. 검증 (재현)
```
python -c "...; import bge_dense_adapter as m; print(m.CANONICAL_UNITS_SHA1)"   # 55522119... (binding에서 로드)
python tools/paper-orchestra/corpus/check_corpus_binding.py                      # PASS (D1: 하드코딩 0)
python -m pytest .../nas-worker/production/tests .../corpus/tests .../retrieval/tests -q   # 787 passed
grep -rn "[0-9a-f]\{40\}" retrieval/*.py schemas/EvidencePacket.spec.md   # 코드/spec에 리터럴 40-hex 0 (binding/CORPUS_VERSION에만)
```
- 신규 테스트: `test_anchors_read_from_binding_no_hardcode`(드리프트 0 + enforced 확인) + `test_d1_catches_hardcoded_divergent_sha`(가짜 stray sha 박으면 적발).
- import-time binding 읽기 OK(테스트들이 importlib로 로드 → 787 green). emitter가 상수 import도 OK.

## 3. 적대검증 요청
- (a) 코드/spec에 하드코딩 sha 0 + CANONICAL이 binding서 로드 + 787 재현?
- (b) D1이 재-하드코딩(divergent sha) 잡나?
- (c) 게이트 로직(loaded != binding → refuse) 의도대로?
- (d) import-time binding 읽기 우려 있나(없으면 ImportError로 시끄럽게 실패=의도)?
- (e) 하드게이트: corpus 본문/index 미커밋·미push.

## 다음
ok면 corpus-binding 종료(단일출처 완성). 잔여=D3(draft default, advisory) + 머지 운영자 게이트. Codex 작업 운영자가 멈춤 상태 — 재개 시 이거 검증.
