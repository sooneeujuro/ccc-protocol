# STATUS — Claude (회사PC, 세션 67522dcd / 이전 a745303e)

last update: 2026-06-16 19:09 (ledger MVP 수렴 + 하트비트 재무장)

## Heartbeat (docs/HEARTBEATS.md adaptive backoff 채택)
- Quiet backoff: interval=10m, quiet_streak=0/3, next quiet level=30m → 90m(ScheduleWakeup 상한 60m로 캡).
- 방금 의미있는 작업 발생(ledger MVP Claude↔Codex 수렴) → quiet_streak 리셋, active 복귀.
- 정지조건: STOP.md 또는 operator 명시 정지. FINAL_SUMMARY는 정지신호 아님.
- ping 규약: 3-quiet due-ping, peer 무응답 반복 시 operator 에스컬레이트(스팸 금지).

## 🆕 Ledger MVP 트랙 (drift-killer, 운영자 발주 2026-06-16)
- **수렴 완료**: Claude(LEDGER_001/003) ↔ Codex(LEDGER_001_REVIEW/002) → 첫 MVP = **migration/apply-state ledger** 만장일치. 아키텍처 LOCK.
- **운영자 Phase 1 GO 받음 → 빌드 완료** (협업모드=Claude 빌드/Codex 검증). manuscript-atelier branch `claude/ledger-migration-apply-state` commit `8a2c51f` (4 files, additive-only, 로컬·미push).
  - 강제체크 green-as-is + pytest 13 passed + 합성드리프트 red 증명. 권고 10건=Phase2 타깃 프리뷰(러너북 :189 오타 포함).
- **Phase 1 클로즈**: Codex `LEDGER_004`=issues_found(3건)→수정 `6a67152`→`LEDGER_005`=**ok**. 잔여 hardening(canonical-path) `efaaf0a` 반영. 전체 production 정적 suite **648 passed**, green-as-is. 3 commits: 8a2c51f/6a67152/efaaf0a.
- **다음 = 운영자 Phase 2(de-prose) GO 게이트** (운영자에 에스컬레이트 + `LEDGER_006` 발행). GO 전 구현 0.
- 하드게이트: live infra/DB/secret/deploy 0, corpus 미터치, manuscript-atelier push 0(로컬 리뷰).

## 현재 트랙 상태
- normalizer: ✅ DONE (75.4%, precision 99.2%). 코드 PR화 미완(manuscript-atelier/tools/corpus-normalize, uncommitted).
- figure refill: ⛔ **source-level BLOCKED** — 잔여 604그림/51편, 이 PC 안전소스 0/50. pilot=충돌붕괴(unsafe). 필요=datalab 머신 per-paper 원본 또는 PDF 재변환. 상세 inbox_codex/021.
- B(sidecar 적용): operator "박아" 대기. PR#15/16 머지 대기.

## 발행 최신: inbox_codex/021 (Codex verdict 대기). 핸드오프: detangle/HANDOFF_NEW_DRIVER_20260616.md (🔴 correction 포함).
