# HANDOFF — drift-killer ledger 트랙 컨텍스트 (2026-06-16, Claude 67522dcd → 다음 세션)

옆 세션이 CCCP 구조개선/ledger 작업을 이어받기 위한 핸드오프. **이 파일 + `MEMORY.md` + `STATUS_claude.md`** 면 재유도 없이 이어감.

## 0. 목표 (북극성)
"무엇이 진짜인가?"를 **기계검증 가능한 state**로 바꿔 prose/live/test 드리프트를 죽인다. 단, **"논문 쓰는 데 실제 도움?"을 통과**해야 함(인프라 위생 자체가 목적 아님).

## 1. 완료된 것
### MVP1 — migration/apply-state ledger ✅ CLOSED (양측 ok)
- branch `claude/ledger-migration-apply-state`, commits `8a2c51f`→`6a67152`→`efaaf0a`→`ff19a37`→`bdd8332`. **로컬·미push**(회사PC).
- `tools/paper-orchestra/queue/migrations/APPLY_STATE.json`(단일진실) + `check_apply_state.py`(강제 E1~E7 + 권고 A1) + generated.md. 5 SQL헤더/README/runbook de-prose 완료. 650+ static tests pass.
- **대기**: 운영자 main 머지 결정만.

### MVP④ — corpus-version binding ledger ✅ Phase 1 CLOSED (양측 ok, Codex LEDGER_014)
- branch `claude/corpus-binding-ledger`, commits `e58e81d`(빌드) + `c7a7bcd`(E6 재현성+D3 fix). **로컬·미push**(회사PC).
- `tools/paper-orchestra/corpus/CORPUS_BINDING.json`(binding_id `geochem_2026-06-16_55522119`, 경로0) + `check_corpus_binding.py`(강제 E1~E7, 리포트 D1~D3) + generated.md + example + tests(10) + `.gitignore` 가드.
- 목적: 초고가 기계 간 이동 시 corpus 버전 불일치(인용 재현 깨짐) 차단.
- **검증됨**: checker PASS, 10 tests, `--verify-source`로 이 PC corpus(6/12) sha 일치 OK.
- **핵심 발견(D1이 적발)**: worker corpus-거부 게이트가 옛 sha `67b1...`에 하드코딩 — 3곳: `tools/paper-orchestra/retrieval/bge_dense_adapter.py:22`, `evidence_packet_emitter.py:96`, `schemas/EvidencePacket.spec.md:95`. 정본 `55522119`는 코드에 0회. → known_drifts로 리포트만(Phase1 동작변경 0).
- **대기**: Codex `LEDGER_013` 검증 → ok면 운영자 Phase 2 GO 질의.

### 037 dense 트랙 ✅ CLOSED + .mcp.json 핫픽스
- G:\corpus_md_export_20260612 manifest/build script build_mode→full_rebuild_20260616, dense_search.py Windows-safe. Codex 037B ok.
- **`.mcp.json` geochem-corpus 6/02→6/12 재등록 완료(회사PC, 미커밋 워킹트리 변경).** ⚠️ 홈/노트북은 각자 .mcp.json 동일 수정 필요(binding MVP가 코드로 강제 예정).

## 2. 다음 결정/작업 (대기 중)
1. **Codex `LEDGER_013` 검증** (corpus-binding Phase 1) — 아직 안 옴.
2. **운영자: MVP1 main 머지?** (code-only PR 가능, 게이트)
3. **corpus-binding Phase 2 — ✅ 완료, single-source (commits `047a653`→`89e87a8`, 로컬).** worker corpus-게이트가 옛 67b1 하드코딩이던 걸: 코드가 `CANONICAL_UNITS_SHA1 = _load_bound_units_sha1()`로 **CORPUS_BINDING.json에서 런타임 읽기**(하드코딩 0, 운영자 설계). emitter는 import, spec은 참조. D1=재-하드코딩 가드(enforced). 게이트=순수로직(loaded != bound → refuse). **코퍼스 갱신 시 CORPUS_BINDING.json 한 곳만.** live 리터럴 sha 0, checker PASS, **787 tests**. Codex 검증(`LEDGER_017`, LEDGER_016 대체) 대기. **잔여 = (b) D3(draft_evidence_adapter repo-local 기본 index)=advisory 유지(운영적 후속) + (d) .mcp.json 타머신 + NAS/web probe.** 아래 원래 스펙 참고.
   - (원래 GO 스펙, 긴급도 낮음 — 게이트가 플래그라 데이터위험 0) (게이트가 하드거부 아니라 플래그 `bge_alignment_verified`/`alignment_status`만 찍음 + 호출처는 smoke/test뿐 라이브 루프 아님 + .mcp.json 핫픽스로 실제 corpus는 이미 정본 6/12라 "틀린 데이터" 위험 0, 보수적 실패). → **옆 세션이 싸게 처리 권장**(이 Opus 세션 비용). **스펙(아래) 그대로 실행 → Claude 빌드→Codex 검증.**
   - **(a) 67b1 → 55522119 교체 3곳**: `tools/paper-orchestra/retrieval/bge_dense_adapter.py:22` `CANONICAL_UNITS_SHA1`, `evidence_packet_emitter.py:96` 동일 상수, `schemas/EvidencePacket.spec.md:95` refusal anchor. (값 교체 + binding 참조 주석. 더 견고히 하려면 CORPUS_BINDING.json에서 로드.)
   - **(b) draft 기본 index**: `retrieval/draft_evidence_adapter.py:50` `_INDEX_DIR`(repo-local corpus/index = 옛 incremental_mellor) → bound corpus 가리키게/검증 추가.
   - **(c) 재발방지**: `check_corpus_binding.py`의 D1(anchor)·D3(draft-default)를 **advisory→enforced 승격**(이제 값 맞으니 fail 0, 이후 또 어긋나면 빌드 fail). 관련 테스트(67b1 픽스처들: `test_bge_dense_adapter_synthetic.py`, `test_evidence_packet_emitter_synthetic.py`, `test_bm25_retrieval_client_synthetic.py`) 동반 갱신.
   - **(d) 선택/후속**: DraftEvidenceSearcher/draft-driver 진입점에 `--verify-source` 배선, `.mcp.json` 타머신, NAS/web probe(opt-in, 운영자-게이트).
   - 검증: 전체 production 정적 suite + corpus tests green, checker green(D1/D3 이제 PASS).
4. ②live-surface/③decision ledger = **북극성 미통과로 보류**(인프라위생). ②의 §0 데이터노출은 별도 일회성 보안수정.

## 3. 정본/주소 (CORPUS_SSOT.md가 단일 진실)
- 정본 corpus = **`G:\corpus_md_export_20260612`** (ver 2026-06-16, 3903편, units 274,953, sha1 `55522119bdd5767957879420b13563eb7c3109ef`). 폴더명≠버전 주의(C:에 6/12명 사본 2벌 = 옛 스냅샷).
- NAS = `100.108.229.47`(tailnet) `/volume2/manuscript_atelier`, reader :8765 / MCP :8766.
- 협업노트: `detangle/inbox_codex/LEDGER_001~013`(Claude→Codex), `detangle/inbox_claude/LEDGER_*`(Codex→Claude).

## 4. 하드게이트 (불변)
corpus 본문/index/sidecar/wiki/그림 **git push 0**(버전 메타만 OK). manuscript-atelier 코드 **로컬 유지**(머지는 운영자 GO). live infra/DB/secret/deploy 0.

## 5. 🔴 비용 교훈 (이 세션 $480 태움 — 반드시 승계)
- **거대 Opus 세션을 워치독 타이머로 자동폴링 금지** — wake마다 1M 컨텍스트 재처리 = 돈 줄줄. 폴링은 LLM 없이/싼 모델/수동으로.
- **Workflow·멀티에이전트는 routine에 쓰지 말 것**(서브에이전트 10개 = 한 방에 수십 달러). 진짜 큰 설계/리뷰일 때만.
- Opus(프런티어)는 **실제 빌드/설계** 때만. 코디네이션(inbox 확인·간단 ack)은 cheap 모델/수동.
- 오늘 운영: **운영자 수동 wake**, 자동 타이머 OFF, Workflow OFF.
- 상세: 메모리 `feedback_cccp_poll_tight_when_bottleneck` (+ 폴링은 5m 고정, fiddly 숫자 금지).
