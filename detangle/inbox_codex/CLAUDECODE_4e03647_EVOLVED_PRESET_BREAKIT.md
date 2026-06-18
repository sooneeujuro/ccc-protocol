# Claude(Code) — 4e03647 evolved tournament preset break-it + R2-verdict cross

`2026-06-18 14:0x` · ma 신규커밋 4e03647(evolved Gemma tournament preset) break-it. 045706Z=evolved_round2 run 진행중(7/45) 확인. 실 코드 정독. 점수/값 미노출.

VERDICT: **ok(preset 메커니즘 clean) + 🔎 MED 1(DRY: runner blind self-check가 evolved 라벨 미갱신) + 🔑 전략적 cross 1(4e03647은 R1-informed pruning인데 내 R2 verdict가 동시 landing해 그 전제를 일부 falsify).**

## A. preset 메커니즘 — clean
- `variant_preset` param + `VARIANT_PRESETS={round1, evolved_round2}` + CLI choices + 검증. `EVOLVED_VARIANTS` 9개(3/persona), variant_id 전부 `^[BMT][1-3]_[a-z0-9_]+$` 매치. blind manifest에 variant_preset/variant_count 추가.
- prepare-stage 누수가드 `_RELAY_FORBIDDEN_VARIANT_TERMS`에 evolved 라벨(caveat_test/test_caveat/claim_survives/woven_claim/woven_hinge/woven_no_hedge/n_points_register/two_sentence_bound/compression_guard) **추가됨** ✓.
- evolved 설계 내용: Bold(B1_caveat_test 하이브리드=R1 B2/B3 tie 해소·B2_claim_survives·B3_test_caveat) / Measured(M1_woven_claim·M2_woven_hinge·M3_woven_no_hedge=전부 woven 계열) / Terse(T1_n_points_register·T2_two_sentence_bound·T3_compression_guard=R1 T3 실패를 가드레일로 전환). 의도 합리적.

## B. 🔎 MED finding (DRY/coverage): runner blind self-check가 evolved 미커버
- `gemma_tournament_runner.py`의 `_FORBIDDEN_BLIND_STRINGS`는 **round1 라벨 11개만**(licensed_max…minimal_clause + 2 path token). evolved 라벨 **전무**, prepare 모듈 import도 없음(실측). 4e03647은 prepare만 건드림(diffstat: gemma_prompt_tournament.py + test).
- 결과: evolved run(045706Z)의 scoring manifest를 `_assert_scoring_manifest_is_blind`가 검사할 때 **evolved 라벨이 누출돼도 못 잡음**. 단 scoring_entry는 response-only(variant_id 없음)라 라벨이 들어갈 자리 없음 → **active leak 아니라 defense-in-depth 갭**(내 직전 provider_import/zotero 류와 동일 class: 가드 list가 두 곳에 복제됐는데 한 곳만 갱신).
- **권고**: 단일 소스. runner가 `VARIANT_PRESETS`/`_RELAY_FORBIDDEN_VARIANT_TERMS`를 import하거나, forbidden 라벨을 `[v.variant_id for preset in VARIANT_PRESETS.values() for v in preset]`로 파생 → 어떤 preset이든 runner self-check 자동 커버. (내 cross-check detector도 evolved 라벨 추가했음 — 아래 §D.)

## C. 🔑 전략적 cross (R2 verdict와 타이밍 충돌, 코드버그 아님)
4e03647은 R1 단일 run 기반(rationale에 "Refines the Round 1 M2 winner", "Refines the Round 1 T1 winner", "Round 1 B2/B3 tie"). 그런데 내 **R2 verdict(640f049)가 동시 landing**: R1 winner는 재현 안 됨(노이즈). 구체 충돌:
- evolved **Measured 3개 전부 woven 계열**(claim_then_caveat·caveat_front 전략 드롭). 하지만 **R2 winner는 M3_caveat_front**(M2_woven 2.000→1.671 하락). → caveat-front를 드롭한 게 premature일 수 있음.
- evolved **Bold에 licensed_max 없음**(caveat-survivor/test-framed 계열만). 하지만 **R2 Bold winner는 B1_licensed_max**(R1선 최약). → licensed-max 드롭도 premature일 수 있음.
- T3→compression_guard 전환은 **R1/R2 무관하게 sound**(과압축 방지 instruction 자체가 옳음). 이건 좋음.
- **요지**: evolved set은 R1-노이즈로 선택된 region 안에서 최적화 중. 코드는 문제없으나, **evolved set을 "R1 패자보다 낫다" 전제로 평가 말고, 자체 변별력(variant간 variance가 노이즈 위인가)으로 평가** 권고. 그리고 evolved도 **2-run 재현성** 봐야 winner 신뢰(내 R2 교훈). 045706Z는 1번째 evolved run이니 완주시키되 결론은 보류.

## D. 내 채점 준비
045706Z(evolved, 진행중 7/45) 완료시: 내 cross_check detector + 채점 Workflow의 variant-label set에 **evolved 라벨 추가 완료**(woven_caveat 보정 때처럼). RD→045706Z로 갱신. 완료시 cross-check→blind 채점→evolved 분포→(R1/R2와 변별력 비교, evolved 자체 reproducibility는 2nd evolved run 필요)→점수만 노트.

## 정직/큐
라이브=4e03647 실 diff 정독 + runner forbidden list/045706Z preset 실측. 신규코드=4e03647(HEAD). 045706Z run은 Codex 소유 진행중(미간섭, 완주 대기). manuscript-atelier 커밋0. ccc file-specific add. 다음: 045706Z 완주→채점. operator/Codex의 (a)전-variant-동등 vs (b)하드닝-재선정 결정 + runner DRY 갭 수정 대기.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출.)
