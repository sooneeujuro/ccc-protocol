# Claude(Code) — b3b73a2 discriminating_v2 rubric + DRY-gap fix break-it (LEDGER_230)

`2026-06-18 15:2x` · ma 신규커밋 b3b73a2(discriminating tournament rubric) break-it. 실 함수 import·실행 검증. LEDGER_229(R4 stop)/230(rubric equipment) 정렬 확인.

VERDICT: **ok — 🟢 내 DRY갭 finding CLOSED(검증)·discriminating_v2(0-3) 메타데이터 contract clean·hard gates 불변·내 2-run+M1~M4 권고 반영. + LOW 3(설계 노트, 블로커 아님).**

## A. 🟢 DRY갭 CLOSED (내 e5214cf finding) — 검증
- runner `_FORBIDDEN_BLIND_STRINGS = ("prompt_pack_dir","prompt_packs.local") + tuple(_RELAY_FORBIDDEN_VARIANT_TERMS)` (prepare서 import). 정확히 내가 권고한 single-source 파생.
- 실행 검증: `_RELAY_FORBIDDEN_VARIANT_TERMS`(18 토큰)가 **18 variant_id(round1 9+evolved 9) 전부 커버**(UNCOVERED=NONE). runner forbidden=20개(compression_guard 등 evolved 포함 확인). → evolved run scoring self-check가 이제 evolved 라벨 잡음. 닫힘.

## B. discriminating_v2 (0-3) — clean
- `SCORING_RUBRICS={standard_v1(0-2, 보존), discriminating_v2(0-3)}`. `--scoring-rubric` CLI choices 검증, default standard_v1(기존 계약 무변). 잘못된 id→`gemma_prompt_tournament_scoring_rubric_invalid`.
- dv2 6축: claim_altitude_two_sided·bound_tightness·caveat_survival·register_fit·protected_preservation·conciseness. **hard_gates==standard_v1(불변)** 검증 → 안전 무손상.
- selection_rule="..._then_two_run_reproducibility"(내 2-run 게이트 반영), task_pressure_profile="M1_overreach..M4_register"(내 M1~M4 반영), judge_notes("3은 merely-safe보다 강할 때만"·"overclaim/vagueness 둘다 0"·"near-miss protected drift는 gate 못잡으면 hard fail"). 채점 지침으로 적절.
- rubric은 blind_manifest `blind_scoring`에 `**dict(scoring_rubric)`로 주입=메타데이터(코드 강제 아님, 채점은 Claude). `_assert_blind_manifest_is_blind` 통과(값/경로/라벨 없음).
- tests 80 passed(+6).

## C. LOW 설계 노트 (블로커 아님)
1. **2nd-order DRY(latent)**: `_RELAY_FORBIDDEN_VARIANT_TERMS`는 아직 `VARIANT_PRESETS`와 별개 수기 리스트. 현재 18=18 일치하나, 3번째 preset 추가 시 relay 수기 갱신 안 하면 갭 재발. 완전 single-source는 relay를 `[v.variant_id for p in VARIANT_PRESETS.values() for v in p]`(+필요시 bare 토큰)에서 파생. (보고한 runner↔prepare 갭은 닫힘. 이건 한 단계 더.)
2. **evidence_binding 축 누락**: 내 스펙의 evidence_binding(각 claim이 licensing datum에 명시 결박됐나)이 dv2에 없음 — Codex는 bound_tightness(claim 강도 vs bound 분리)로 대체. bound_tightness도 좋은 변별축이나 **차원이 다름**(binding=claim↔evidence 결박, tightness=bound 폭). harder task의 M2 약-evidence가 binding을 직접 시험하니 **evidence_binding 추가 고려** 권고(또는 채점시 내가 bound_tightness에 흡수). 선택.
3. **spread-shadow(defense)**: `**dict(scoring_rubric)`가 `variant_mapping_withheld`/`reveal_file` 뒤에 spread — 현재 rubric dict에 그 키 없어 안전하나, 미래 rubric이 그 키 가지면 안전 플래그 덮어씀. assert-no-overlap 한 줄 권고(defense-in-depth).
4. **N=8 미반영**: 내 noise-reduction N=8은 runtime `--repetitions` 파라미터(rubric 메타 아님). harder run은 `--repetitions 8`로 명시 실행해야 R1~3의 N5 flip 노이즈 줄임.

## D. 다음 (분업)
- **Codex**: LEDGER_230 "next"대로 **harder task instantiation**(M1 over-reach미끼·M2 약-evidence·M3 protected near-miss·M4 register압박, 값 포함 RESOLVED·value relay 아님). 그 task + `--scoring-rubric discriminating_v2` + `--repetitions 8`로 45→72-run(9 variant×8). 2-run(×2) 재현성.
- **Claude(나)**: harder task landing시 채점 Workflow를 dv2로 갱신(schema enum [0,1,2,3]·6축·rubric 프롬프트에 dv2 judge_notes+harder task 컨텍스트·cand 0-3 스케일 cand=median−λvar−μ(3−worst)·2nd-judge on <3·detector RD/라벨). cross-check→채점→2-run 재현성·spread(vs R1~3 0.07~0.19) 비교→점수만 노트.
- **operator**: harder task 난도/값 승인 + GO.

## 정직/큐
라이브=b3b73a2 실 import·`_RELAY`/runner forbidden/dv2 hard_gates 실행 검증(값 미노출). 신규코드=b3b73a2(HEAD). manuscript-atelier 커밋0. ccc file-specific add. 다음: harder task 빌드 대기→내 dv2 채점장비 갱신→새 run 채점. 060329Z(R4)는 미완=채점 안 함(LEDGER_229와 일치).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출.)
