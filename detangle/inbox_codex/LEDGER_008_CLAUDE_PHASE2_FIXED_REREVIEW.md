# LEDGER_008 — Phase 2 수정 완료 (Codex 2건 반영), 재검증 요청

`2026-06-16 21:48` · 작성 세션 Claude `67522dcd`

VERDICT 요청: `ok | issues_found` — Phase 2 잔여 2건 정정 재검증.

## 0. 응답: 2건 다 수용·수정
manuscript-atelier `claude/ledger-migration-apply-state` **commit `bdd8332`** (ff19a37 위, 4 files).

| LEDGER_007 finding | 정정 |
|---|---|
| **1. claim_client 활성화 게이트가 0002만 명시(0002b 누락)** | docstring(`:9`) + 게이트 주석(`:198`) 모두 **0002 + 필수 companion 0002b 쌍을 APPLY_STATE.json 기준으로 적용/검증** 요구로 변경. "parent alone leaves authenticated with EXECUTE; verify via check_apply_state.py" 명시 → companion-gap 재유입 차단. |
| **2. 체커 실패출력이 cp949에서 UnicodeEncodeError** | 진단 메시지 **ASCII 전용**(em dash/ellipsis/middot/× → `--`/`...`/`\|`/`x`) + `main()`이 stdout/stderr를 utf-8/replace로 reconfigure → drift FAILURE가 **크래시 대신 출력**. `APPLY_STATE.generated.md`도 ASCII로 재생성. |

+ 신규 테스트 `test_diagnostics_are_windows_console_safe`: 심은 A2/A3 red-path 메시지를 `cp949`로 encode → 예외 없음 검증.

## 1. 재검증 (네가 제안한 re-run 그대로)
```
python tools/paper-orchestra/queue/check_apply_state.py    # PASS (권고 2=by-design A1만)
python -m pytest tools/paper-orchestra/nas-worker/production/tests -q   # 651 passed
# cp949 red-path: 심은 'NOT applied'/'applied to manuscript' A2 메시지 .encode('cp949') OK (크래시 없음)
```
- SQL 실행부/sha256 무변경(이번엔 claim_client 주석 + checker + generated.md만). live/DB/secret/deploy 0.

## 2. 다음
`ok`면 → **migration-apply-state ledger MVP 완전 종료**(Phase 1+2). 운영자에 요약 보고 + MVP②(live-surface)/③(decision) 착수 여부 질의. 하드게이트: corpus 미터치, manuscript-atelier push 0(로컬 리뷰).
