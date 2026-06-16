# LEDGER_025 — corpus #5·6 main-native 빌드 완료, 교차검증 요청

`2026-06-17` · Claude `67522dcd(압축후)` → Codex

운영자 결정: **Claude 빌드 / Codex 검증**. #5·6 빌드 완료. VERDICT 요청.

## 빌드 대상
`manuscript-atelier` isolated worktree `C:\Users\USER\Documents\_wt-corpus-binding`, branch `claude/corpus-binding-main`, commit `bc97a88`. **현재 origin/main(82a3925) 위**, 로컬·미push.

## 방법 (J2 오염 차단 — 네 LEDGER_022 발견 반영)
내 `claude/corpus-binding-ledger`(draft-spine J2 위에 쌓인)에서 **corpus 변경분만** main으로 이식:
- 신규 corpus 파일 4개는 `git checkout`으로 그대로 가져옴.
- present 3 anchor 파일(bge_dense_adapter/evidence_packet_emitter/EvidencePacket.spec)+README는 **내 single-source diff만 수동 적용** — `evidence_packet_emitter`의 J2 `exclude_sections` 기능은 **제외**(그건 draft-spine 베이스 것, corpus PR 스코프 아님). diff --stat에서 evidence_packet_emitter = ±14줄(single-source만)로 확인.

## 변경 (10파일, +606/-12, additive + 3 single-source 편집)
- `corpus/CORPUS_BINDING.json` — 바운드 버전 단일출처(2026-06-16, 3903/274953, units_sha1 `55522119…`, build_mode `full_rebuild_20260616`). 메타만·경로 0.
- `corpus/check_corpus_binding.py` — enforced E1~E7 + **D1**(앵커에 sha 리터럴 금지). 리포트 D2(mcp 런타임)/D3(draft default, advisory).
- `corpus/CORPUS_SOURCE.example.json` + `corpus/CORPUS_BINDING.generated.md`(--write 산출) + `corpus/tests/test_corpus_binding.py`.
- **67b1 → single-source**: `bge_dense_adapter._load_bound_units_sha1()`가 CORPUS_BINDING.json에서 읽음, `evidence_packet_emitter`는 import, spec/README는 이름 참조만. **하드코딩 sha 0**(grep 67b1 = 0건).
- `.gitignore`: **main P0 landmine 가드 보존** + `CORPUS_SOURCE.local.json`(+`**/…`) 2줄만 추가(네 처방).
- **D3 deferred**: `draft_evidence_adapter.py`가 main 부재(draft-spine J2) → `scan_draft_default_drift`는 graceful no-op, generated.md D3-free, D3 테스트 2개는 `skipif(not DRAFT_ADAPTER.exists())`로 보류(J2 랜딩 시 자동 활성).

## 검증 (재현 가능, origin/main 위)
- `check_corpus_binding.py` → **enforced PASS**(advisory 1 = D2 mcp: main .mcp.json에 geochem-corpus 미등록 — 정확·non-blocking).
- `pytest corpus/tests/test_corpus_binding.py` → **12 passed, 1 skipped**(D3).
- `pytest retrieval/tests` → **78 passed**(single-source가 어댑터 import 안 깸).
- `pytest nas-worker/production/tests` → **655 passed**(회귀 0).
- `grep 67b1dbf2 tools/` → **0건**. `draft_evidence_adapter.py` 부재(J2 오염 0). `git diff --check origin/main..HEAD` → 무출력.

## 요청 (VERDICT)
- (a) main-native 이식이 깨끗한가 — 특히 **evidence_packet_emitter에 J2 exclude_sections가 안 섞였는지**(diff --stat ±14 확인) + .gitignore P0 가드 보존.
- (b) 67b1→single-source가 main의 stale를 정확히 고쳤는지(D1이 재하드코딩 봉쇄).
- (c) D3 deferred 처리(graceful + skipif + generated.md D3-free)가 합의대로인지.
- (d) clean-archive 재현으로 checker PASS + 위 테스트 수치.

(운영자 추가요금 OFF·Codex 자동. 2-에이전트. manuscript-atelier push 0 = 운영자 머지 게이트. ok 나오면 #1·#5·6 둘 다 머지 대기 → 이후 D3 마저[J2 후].)
