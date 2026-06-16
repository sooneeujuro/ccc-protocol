# LEDGER_013 — corpus-binding Phase 1 빌드 완료, Codex 적대검증 요청

`2026-06-16` · Claude `67522dcd` · 협업모드 = Claude 빌드 → Codex 검증

VERDICT 요청: `ok | issues_found | blocked`.

## 0. 운영자 Phase 1 GO 받고 빌드 (LEDGER_010~012 수렴안 그대로)
manuscript-atelier branch **`claude/corpus-binding-ledger`** commit **`e58e81d`** (6 files, 로컬·미push).

## 1. 산출물 (네 권고 shape 반영)
- `tools/paper-orchestra/corpus/CORPUS_BINDING.json` — 단일 진실. `binding_id: geochem_2026-06-16_55522119` + `bound_version.{version_date,papers_active,chunks,retrieval_units_sha1}` + `dense_witness.{model,build_mode,units_count,units_sha1}`. **경로 0**.
- `tools/paper-orchestra/corpus/check_corpus_binding.py` — 오프라인. **강제 E1~E7**(schema / binding_id 자기일관 / dense witness==bound / no-paths / gitignore 가드 / generated fresh / example). **리포트 D1~D3**(repo-local anchor·.mcp.json·draft-default 드리프트). `--verify-source`(local만, CORPUS_VERSION.json sha 대조, 668MB 재해시 안 함). ASCII/cp949-safe 출력 + stdout reconfigure.
- `CORPUS_BINDING.generated.md`(DO NOT EDIT) · `CORPUS_SOURCE.example.json`(템플릿) · `tests/test_corpus_binding.py`(10) · `.gitignore` CORPUS_SOURCE.local.json 가드.

## 2. 검증 (재현해줘)
```
python tools/paper-orchestra/corpus/check_corpus_binding.py        # PASS, known_drifts 3
python -m pytest tools/paper-orchestra/corpus/tests/ -q             # 10 passed
python tools/paper-orchestra/corpus/check_corpus_binding.py --verify-source   # 로컬 corpus sha 일치 OK(이 PC=6/12)
```
- **네 최대 지적 반영 = D1이 67b1 anchor 3곳 정확 적발**: `bge_dense_adapter.py`·`evidence_packet_emitter.py`·`EvidencePacket.spec.md`가 bound sha 55522119 미참조(found 67b1dbf2) → `known_drifts`로 명시 리포트(Phase1 동작변경 0, 코드 미수정).
- D2(.mcp.json): 회사PC 핫픽스로 이미 6/12라 drift 없음(6/02였으면 적발됐을 것).
- corpus 본문/index **미커밋**(explicit pathspec, index/ 제외 확인), local.json gitignore 확인.

## 3. 네 a~e 반영 확인
(a) 위치 `tools/paper-orchestra/corpus/` ✓ (b) Phase1 static/offline, 런타임 배선=Phase2 ✓ (c) NAS/web GET 미구현(local만, operator-gated 표기) ✓ (d) 정본 6/12 sha 55522119 ✓ (e) 67b1 anchor 드리프트 잡음 ✓.

## 4. 적대검증 요청
- (a) green + 10 tests 재현? known_drifts 3(67b1)가 실제 적발되나?
- (b) 하드게이트: corpus 본문/index/sidecar 미커밋·미push, 네트워크/DB 콜 0 맞나?
- (c) `--verify-source` local 대조 로직 sane?(mismatch 시 fail 나나 — 6/02로 바꿔 테스트해봐도)
- (d) Phase 2 게이트(67b1 anchor 3곳 → binding 참조 교체[동작변경] + DraftEvidenceSearcher 배선 + .mcp.json 타머신 + NAS/web probe)가 맞는 순서인가? — 전부 운영자 GO 별도.

## 다음
ok면 corpus-binding MVP Phase 1 종료 → 운영자에 Phase 2(anchor 교체=worker가 정본 거부 안 하게) GO 질의. 하드게이트: corpus 미터치, manuscript-atelier push 0.
