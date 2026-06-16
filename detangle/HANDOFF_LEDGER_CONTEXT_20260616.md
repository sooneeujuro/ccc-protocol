# HANDOFF — drift-killer ledger 트랙 컨텍스트 (2026-06-16, Claude 67522dcd → 다음 세션)

옆 세션이 CCCP 구조개선/ledger 작업을 이어받기 위한 핸드오프. **이 파일 + `MEMORY.md` + `STATUS_claude.md`** 면 재유도 없이 이어감.

## 0. 목표 (북극성)
"무엇이 진짜인가?"를 **기계검증 가능한 state**로 바꿔 prose/live/test 드리프트를 죽인다. 단, **"논문 쓰는 데 실제 도움?"을 통과**해야 함(인프라 위생 자체가 목적 아님).

## 1. 완료된 것
### MVP1 — migration/apply-state ledger ✅ CLOSED (양측 ok)
- branch `claude/ledger-migration-apply-state`, commits `8a2c51f`→`6a67152`→`efaaf0a`→`ff19a37`→`bdd8332`. **로컬·미push**(회사PC).
- `tools/paper-orchestra/queue/migrations/APPLY_STATE.json`(단일진실) + `check_apply_state.py`(강제 E1~E7 + 권고 A1) + generated.md. 5 SQL헤더/README/runbook de-prose 완료. 650+ static tests pass.
- **대기**: 운영자 main 머지 결정만.

### MVP④ — corpus-version binding ledger ⏳ Phase 1 빌드+검증 끝, Codex 검증 대기
- branch `claude/corpus-binding-ledger`, commit `e58e81d` (6 files). **로컬·미push**(회사PC).
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
3. **운영자: corpus-binding Phase 2 GO?** = 67b1 anchor 3곳을 binding 참조로 **실제 교체**(worker가 정본 corpus 거부 안 하게) + DraftEvidenceSearcher/draft-driver에 버전대조 배선 + .mcp.json 타머신 + NAS/web probe(opt-in). **동작 변경이라 별도 GO 필수.**
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
