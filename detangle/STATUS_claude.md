# STATUS — Claude (회사PC, a745303e)

last update: 2026-06-16 10:33 (figure source-block 확정 후)

## Heartbeat (docs/HEARTBEATS.md adaptive backoff 채택)
- Quiet backoff: interval=10m, quiet_streak=0/3, next quiet level=30m → 90m(ScheduleWakeup 상한 60m로 캡).
- 방금 의미있는 작업 발생(figure source-block 증명 + 핸드오프 교정) → quiet_streak 리셋, active 복귀.
- 정지조건: STOP.md 또는 operator 명시 정지. FINAL_SUMMARY는 정지신호 아님.
- ping 규약: 3-quiet due-ping, peer 무응답 반복 시 operator 에스컬레이트(스팸 금지).

## 현재 트랙 상태
- normalizer: ✅ DONE (75.4%, precision 99.2%). 코드 PR화 미완(manuscript-atelier/tools/corpus-normalize, uncommitted).
- figure refill: ⛔ **source-level BLOCKED** — 잔여 604그림/51편, 이 PC 안전소스 0/50. pilot=충돌붕괴(unsafe). 필요=datalab 머신 per-paper 원본 또는 PDF 재변환. 상세 inbox_codex/021.
- B(sidecar 적용): operator "박아" 대기. PR#15/16 머지 대기.

## 발행 최신: inbox_codex/021 (Codex verdict 대기). 핸드오프: detangle/HANDOFF_NEW_DRIVER_20260616.md (🔴 correction 포함).
