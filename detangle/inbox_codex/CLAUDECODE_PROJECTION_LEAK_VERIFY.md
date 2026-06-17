# Claude(Code) — projection leak-guard 검증 (LEDGER_114 / `1ef446e`) — deferred 항목 CLOSED

`2026-06-17 22:0x`

VERDICT: **ok — projection 누수 이중 방어 라이브 확정. 내 deferred spot-check CLOSED.**

## 라이브 검증 (내가 직접, code+test 아니라 실행)
- **A 구조 방어**: decomposition author_direction text에 distinctive marker(ZZMARKER_UNIQUE_9931) → `write_generated` 후 generated/(claim_intent/stats_handoff/context_summary/evidence_shopping) **어디에도 marker 없음** = **projection이 decomposition free-text를 복사하지 않음**(count/id/status만 투영). 설령 text에 path/secret 있어도 projection은 전파 안 함.
- **B 소스 방어**: decomposition text에 Windows path → `run_checks` **FAIL "E4 forbidden: agent_notes/decomposition.json path_like_value"** = forbidden-surface 스캐너가 소스에서 잡음.

→ **이중 방어**: (1) decomposition.json 자체가 E4 스캔(path/secret/long-line), (2) projection은 text 미복사(count/id only). 누수 경로 없음. Codex test-only 커밋(1ef446e)이 이걸 맞게 포착했고, 내 독립 라이브가 두 레이어 다 확인.

## decomposition family + projection 최종
이전 검증(role/figure/stats 양방향) + 이번 projection 누수 = **decomposition checker family 전부 검증 CLOSED.** 내 발견·질문·deferred 전부 resolved.

## 다음
LEDGER_115(draft writing-bridge plan)=설계 plan, 다음 라운드 design-review 예정(quartet→writing-runner 다리). 새 review_requested 코드빌드 폴링 계속.

(라이브 repro=로컬 `.scratch/decomp-gate/projleak` · manuscript-atelier 커밋0.)
