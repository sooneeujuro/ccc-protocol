# STATUS — Claude (회사PC, 세션 67522dcd / 이전 a745303e)

last update: 2026-06-16 19:09 (ledger MVP 수렴 + 하트비트 재무장)

## Heartbeat (docs/HEARTBEATS.md adaptive backoff 채택)
- Cadence: **5m 고정**(운영자 지시 2026-06-16, Codex와 동기). 백오프 사다리 폐기 — Claude=병목이라 in-flight 중 늦추면 Codex 멈춤. 이번 라운드는 운영자 수동 wake(자동 타이머 미설정).
- 방금 의미있는 작업 발생(ledger MVP Claude↔Codex 수렴) → quiet_streak 리셋, active 복귀.
- 정지조건: STOP.md 또는 operator 명시 정지. FINAL_SUMMARY는 정지신호 아님.
- ping 규약: 3-quiet due-ping, peer 무응답 반복 시 operator 에스컬레이트(스팸 금지).

## 🆕 Ledger MVP 트랙 (drift-killer, 운영자 발주 2026-06-16)
- **수렴 완료**: Claude(LEDGER_001/003) ↔ Codex(LEDGER_001_REVIEW/002) → 첫 MVP = **migration/apply-state ledger** 만장일치. 아키텍처 LOCK.
- **운영자 Phase 1 GO 받음 → 빌드 완료** (협업모드=Claude 빌드/Codex 검증). manuscript-atelier branch `claude/ledger-migration-apply-state` commit `8a2c51f` (4 files, additive-only, 로컬·미push).
  - 강제체크 green-as-is + pytest 13 passed + 합성드리프트 red 증명. 권고 10건=Phase2 타깃 프리뷰(러너북 :189 오타 포함).
- **Phase 1 클로즈**: Codex `LEDGER_004`=issues_found(3건)→수정 `6a67152`→`LEDGER_005`=**ok**. 잔여 hardening(canonical-path) `efaaf0a` 반영. 전체 production 정적 suite **648 passed**, green-as-is. 3 commits: 8a2c51f/6a67152/efaaf0a.
- **Phase 2 (de-prose) 완료** (운영자 GO): commit `ff19a37` (17 files). 5 SQL헤더+README+claim_client+러너북§1/§6(:189 오타수정) apply-state prose 제거 → APPLY_STATE.json 단일화; 정적테스트 5개 stale-assert 정정; check A2(no-prose,+README)·A3(runbook-ref) **advisory→ENFORCED**; sha256 갱신. 검증: checker PASS(권고 2=by-design A1만), **650 static tests pass**, de-prose grep 0. → migration-apply-state ledger MVP **완성**(Phase1+2).
- Codex `LEDGER_007`=issues_found(2건: claim_client 게이트 0002b 누락 + 체커 출력 cp949 크래시) → **수정 완료** commit `bdd8332`(companion-aware 게이트 + ASCII/reconfigure 출력 + cp949 테스트). checker PASS, 651 tests, cp949 red-path OK. 재검증 `LEDGER_008` 발행.
- Codex `LEDGER_008_..._REREVIEW`=**ok** → **migration/apply-state ledger MVP (Phase 1+2) CLOSED 양측 합의** (`LEDGER_009` 발행). 최종 branch `claude/ledger-migration-apply-state` commits 8a2c51f/6a67152/efaaf0a/ff19a37/bdd8332 (로컬·미push). checker PASS, 651 tests.
- **운영자 게이트**: (1) MVP main 머지 여부(code-only PR 가능). (2) ②live-surface/③decision는 **북극성 미통과로 보류**(운영자·Claude 합의: 인프라위생, 논문 직결 약함).
- **🆕 MVP④ corpus-version binding ledger 설계 착수**(운영자 발의, 북극성 통과 — 초고 인용 재현성): `CORPUS_BINDING.json`(버전 핀 sha1/편수/날짜, 메타만) + per-machine 소스config + 체커(연결 corpus CORPUS_VERSION.json 대조). **실재 드리프트 발견**: `.mcp.json`이 옛 6/02(4470, dedup전) 가리킴 vs 정본 6/12(6/16재빌드, 3903, sha 55522119). 설계안 `inbox_codex/LEDGER_010` 발행 → Codex 검증 대기. 빌드는 수렴 후.
- 하드게이트: live infra/DB/secret/deploy 0, corpus 미터치, manuscript-atelier push 0(로컬 리뷰).

## 🆕 037 dense 트랙 (운영자 인수 지시 → 완료)
- 운영자가 원 dense 세션 확인 후 이 세션에 인수("G만 ㄱㄱ, 레포 사본 플래그만"). Codex 037 verdict 3건 정정 완료(G:\corpus_md_export_20260612, 비-git, 재임베딩 0, 비파괴):
  - manifest+build_bge_m3_dense.py:99 build_mode → full_rebuild_20260616(스크립트는 동적 스탬프). dense_search.py Windows 콘솔 안전화. 정확 smoke(Xu2024 top1 cos 0.826) 기록.
  - 검증: PYTHONIOENCODING 없이 EXITCODE=0 + cos 0.826 재현. G:폴더에 DENSE_METADATA_FIX_20260616.md 타임로그.
  - 레포 사본 manifest(incremental_mellor=옛 mellor 증분)는 무접촉(플래그만, 운영자 ⓐ).
- 발행 `inbox_codex/037B_DENSE_METADATA_FIX_DONE.md` → **Codex `037B_..._VERDICT`=ok**(정확 smoke 독립재현 exit0/cos0.826). → **037 dense 트랙 CLOSED.**

## 현재 트랙 상태
- normalizer: ✅ DONE (75.4%, precision 99.2%). 코드 PR화 미완(manuscript-atelier/tools/corpus-normalize, uncommitted).
- figure refill: ⛔ **source-level BLOCKED** — 잔여 604그림/51편, 이 PC 안전소스 0/50. pilot=충돌붕괴(unsafe). 필요=datalab 머신 per-paper 원본 또는 PDF 재변환. 상세 inbox_codex/021.
- B(sidecar 적용): operator "박아" 대기. PR#15/16 머지 대기.

## 발행 최신: inbox_codex/021 (Codex verdict 대기). 핸드오프: detangle/HANDOFF_NEW_DRIVER_20260616.md (🔴 correction 포함).
