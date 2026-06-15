# RUN_STATE

<!-- Machine-readable header: heartbeats/audits parse these exact keys. -->
status: active
phase: cccp-bootstrap-complete
task: 양쪽 에이전트 부팅 완료. 첫 협업 작업 대기 (후보=lazy verification 정보층).
project: manuscript-atelier
coop_root: ccc-protocol/runs/manuscript-atelier/coop  (★작업 repo 밖. work=manuscript-atelier, 조정+로그=여기)
operator: 김희준
started: 2026-06-15T06:53Z
last_claude_heartbeat: 2026-06-15T06:53Z
last_codex_heartbeat: 2026-06-15T06:53Z (operator-relay, VERDICT: ok)

## Current Objective
manuscript-atelier corpus의 정확도·완결성 보강 작업을 CCCP로 협업. 현 1순위 후보 =
**lazy verification 정보층**(검색 hit 시 답하는 LLM이 full MD 읽는 김에 measured-vs-cited
판정→sidecar `verifications` 누적). 설계 메모: memory `project_lazy_verification_enrichment.md`
+ repo `docs/handoffs/company_computer_handoff_20260615.md`.

## Heartbeats
- Codex interval: 미정 (operator가 다음 run 시작 시 설정). recurring 보장 불가 시 명시할 것.
- Claude interval: 대화형(이 세션). 백그라운드 작업은 platform이 자동 재호출.
- Quiet backoff ladder: 10m → 30m → 90m (3회 연속 quiet마다 승급).
- ★Codex가 옛 ad-hoc 감사 루프 2개(PID 3660 autonomous_run / 29188 reader_ux) 종료함 — brittle keyword-STOP 제거됨.

## Write Scope
- Allowed: coop/ (+ task가 명시한 경로만: NAS sidecars / C:\Users\soone\geochemistry-analyzer-git / nas-worker).
- Forbidden: 그 외. 논문본문·코퍼스·대용량·secret은 coop/에 절대 금지(경로로 참조).

## API / Cost Policy
- 유료 실행(datalab/API)은 operator GO. 예산 상한 없음(master_backlog 06-14)이나 이중지출 회피 + batch_id·누계 기록.
- Approval required: push/merge/deploy/reindex/install/delete/off-machine send/secrets (하드게이트).

## GitHub Snapshot Policy
- ccc-protocol 보완본: PR #3 (github.com/sooneeujuro/ccc-protocol) — 머지는 operator.
- 이 coop/는 manuscript-atelier 레포에 설치됨. 커밋/스냅샷은 operator 판단(coop/*.md·inbox·reports·소형 ledger만, payload 금지).

## Pending Decisions (operator)
- lazy verification 착수 GO? (만들 것 3개: sidecar `verifications` 필드 / `record_verification` MCP툴 / senpAI 프롬프트 1줄 — ②③ 라이브게이트)
- Fischer CO 논문 올바른 PDF 제공.
- German·LeeSC 라이브 reindex GO (staging 검증완료).
- 집PC 커밋 머지: A3/A6/B8(ma `6f36b77`), A4/A5(geochem `b05dfb62`).
- A7 중복 삭제 GO (26그룹/27편, Gehler suppl 보존).

## Standing Audit
태스크 없을 때: STOP 확인 → inbox 확인 → 최근 산출물 검증(sha1/diff/count로, 키워드매치 금지) → 변화/운영자 주의 필요분만 보고.
