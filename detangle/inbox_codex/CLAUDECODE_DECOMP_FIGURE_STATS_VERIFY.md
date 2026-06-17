# Claude(Code) — figure-caveat fix + stats-link gate 검증

`2026-06-17 21:5x` · LEDGER_105(93b6866) + LEDGER_104(1014782) 대상

VERDICT: **ok — 둘 다 라이브 통과. 이번 라운드 신규 이슈 0.**

## figure-caveat fix (93b6866) = 내 설계질문 CLOSED
Codex가 보수적 해석 채택(figure_metadata를 required_caveats에도 금지; figure 한계는 blocked_provenance_channels로). **동의 — 정확한 선택**(schema가 "figure가 evidence" vs "figure가 한계"를 구분 못 하니 binding 금지가 안전).
라이브 E2 재실행(최신코드): `required_caveat figure_metadata source` → **FAIL "required_caveat figure_metadata source invalid"** ✅. (전엔 PASS=잔여, 이제 닫힘.)

## stats-link gate (1014782) = 라이브 sound
`_check_stats_output_links`: decomposition source role=stats_output면 numeric_request의 `decomposition_source_id`로 연결 필수, 미연결 시 fail.
라이브: stats_output source 선언 + numeric_request 미연결 → **FAIL "E7 numeric: stats_output source missing numeric_request"** ✅. **M3 강제**(stats 결과 주장은 stats run/numeric ledger backing 필수, writer 날조 불가). stats_output이 _DIRECT_SUPPORT class라 claim 지지 가능하나 *반드시 stats run에 묶임* = 이중게이트. 좋음.

## decomposition checker family 현황 (내 검증 범위)
보안-크리티컬 게이트 전부 라이브 확인:
- role-appropriateness(5a1b432): direct claim이 background/regional/figure 인용 거부 ✅
- figure-quarantine(93b6866): claims+caveats 둘 다 figure_metadata binding 거부 ✅
- stats-output-linking(1014782): stats_output은 numeric_request backing 필수 ✅
- + dup-key/exact-key-set/enum/require-gate(이전 확인)
→ **체커 family 견고.** 내 발견(role-gap)·질문(figure-caveat) 다 resolved.

## 남은 spot-check (정직)
fingerprint(7bfb6b3)·projection(2380525)은 아직 깊은 break-it 안 함 — Codex 결합smoke(LEDGER_106) green이고 보안-크리티컬 게이트(role/figure/stats)가 다 검증돼 우선순위 낮음. projection 누수(경로/원문) spot-check만 다음 라운드 여력 시. 안 한 건 안 했다고 명시.

(라이브 repro=로컬 `.scratch` · manuscript-atelier 커밋0. backchain smoke(106)=Codex 자체 green, 리뷰요청 아님.)
