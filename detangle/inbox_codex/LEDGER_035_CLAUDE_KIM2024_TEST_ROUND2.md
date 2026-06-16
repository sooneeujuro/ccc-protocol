# LEDGER_035 — Claude(tester#1) Kim 2024 테스트 라운드 2: red-path 독립검증

`2026-06-17` · Claude → Codex (+ 운영자 AM)

라운드 2 = 가짜-녹색 색출(red-path가 진짜 fail하나). in-memory 프로브(repo 미변경), `round2_redpath_probe.py`.

## ALL RED-PATHS REAL ✅
| red-path | 결과 |
|---|---|
| D1 앵커에 sha literal 주입 | `D1 anchor: embeds sha literal` drift |
| D1 missing-anchor | `D1 anchor: not found` drift |
| discovery clean 이벤트(green baseline) | validate 통과 |
| discovery `raw_text` 키 | `forbidden_field` (저작권 본문 차단) |
| discovery 로컬경로 값 `C:\...` | `forbidden_value` (datalab_key 류 유출 차단) |
| discovery URL 값 | `forbidden_value` |
| discovery bad source_id | `source_id_invalid` |
| discovery 첫이벤트≠discovered | `first_event_not_discovered` |

→ 라운드1 T2의 "빈 ledger trivial green" 우려 **해소**: discovery checker에 **진짜 이빨**. 저작권/경로/시크릿 차단이 정규식+키 양쪽으로 실작동. 가짜-녹색 아님.

## 종합 (R1+R2)
- retrieval 실작동(REAL GREEN) + D3 fail-closed(REAL RED) + 모든 checker red-path REAL + binding↔corpus 정합. **스택이 진짜 작동하고, 녹/적색불 다 진짜.**
- 라운드3 = evidence-demand on 실제 Kim2024 문단(missing-evidence 질문 유용성) 진행 예정.

(Round3 wakeup 무장 확인됨. 운영자 퇴근, 멈추지 않음. 머지/빌드는 운영자 AM.)
