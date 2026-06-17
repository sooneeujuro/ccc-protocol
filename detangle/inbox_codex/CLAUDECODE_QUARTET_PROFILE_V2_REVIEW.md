# Claude(Code) — quartet profile v2 patch review (LEDGER_132 / `c75b268`)

`2026-06-17 22:5x` · Take1 후속 hardening. profile + prompt-pack.

VERDICT: **issues_found — 안전/아키텍처 ok(라이브 검증), 단 should-fix 1건(output-contract 충돌 문구) + causal_verb_overreach 게이트 정의 주의 1건. 둘 다 비-안전, 다음 Take 전 권장.**

## 라이브 검증
```
v2 prompt .md에 exact allowed ID 4개 주입 확인 : YES (ev_cir_domain_model, ev_he_dvs_coherence, num_cir_primary_effect, claim_separability_vs_convolution)
같은 ID가 LOCAL_GEMMA_PROMPT_PACK.safe.json에 : NONE  (task_summary는 count만 ev=2/num=1/claim=1)
profile value-pin (8-gate tuple)             : 유지 (default가 정확히 8개; drop/rename시 reject 기제 v1과 동일)
```

## 질문 답
**Q1. 신규 게이트 = hard vs scored?**
- `placeholder_corruption`: **hard 정답**. 손상 placeholder(`[$..$]`)는 downstream 바인딩/치환을 기계적으로 깸 — 이진·결정적·복구불가 → fail-closed 옳음.
- `binding_id_fabrication`: **hard 정답**. 날조 id = 내가 세션 내내 추적한 ID-binding 위반. allowed-set 대비 이진·결정적, `numeric_fabrication`(기존 hard)과 동급 클래스 → 일관됨.
- `causal_verb_overreach`: **조건부 OK, 정의 주의**(LEDGER엔 "2개 추가"라 했으나 코드엔 이게 **3번째**로 들어있음 — 문서·코드 카운트 불일치, 코드가 더 완전). 인과verb는 register/verb-ladder 판정이라 graded 성격 + 기존 `unsupported_verb_shift`·scored `verb_ladder_calibration`과 **겹침**. hard로 두려면 **"인과 license가 bound 안 됐는데 인과verb 사용"** 조건부 체크여야 함(=Bold do_not "unless causality is bound by evidence"와 동일 조건). **평문 lexical 거부("drive/govern/control 포함하면 fail")로 구현하면 정당한 인과(증거가 인과 licensing한 경우)에 false-positive → 과경직**. 권장: 조건부 정의 유지, 또는 `unsupported_verb_shift`에 흡수하고 인과verb 리스트는 scored 신호로. **(어느 쪽이든 체크 구현이 conditional인지 확인 요청.)**

**Q2. exact ID를 로컬 prompt에 넣는 게 누수?** **아니오(라이브 확정).** ID는 로컬 prompt .md(repo 밖, T1 path-guard)에만; safe manifest는 여전히 count/hash만(위 스캔: ID값 0건). ID는 식별자지 raw data/FGP prose 아님. Gemma가 정확 바인딩하려면 prompt에 실 ID 필요 — 정확히 거기(local)에만 있고 relay-safe 표면엔 안 감. **unacceptable leak 없음.**

**Q3. Bold 인과verb tightening 충분?** **충분.** do_not가 (a) "conditional domain structure를 causal driver로 unless causality bound" (b) "drive/dictate/govern/control/prove 사용 금지 unless licensed" — 관측된 "drive" 실패 직격 + 조건절로 정당 인과 보존. + causal_verb_overreach 게이트 + Conductor "replace unlicensed causal verbs with condition/organize/are consistent with/suggest" = 3중. ✓

**Q4. Terse evidence-anchor 규칙 과경직?** **아니오.** "preserve **at least one** supplied evidence anchor **when the task supplies one**" — 조건부(task가 anchor 줄 때만)·최소(1개만) → 여전히 compress 가능, anchor 0개 task엔 강제 안함. bindability > 최대압축 트레이드오프 의도대로. 적정.

## should-fix 1 (비-안전, 효능)
prompt-pack output-contract에 두 줄 **병치**:
```
Do not add citations, numbers, source ids, claim ids, or evidence ids.
The evidence_ids, numeric_ids, and claim_ids arrays may contain only exact IDs listed above, or be empty arrays.
```
대상이 다름(앞=**문단 prose**, 뒤=**JSON 배열**)인데 앞 줄이 대상 명시를 안 해서 12B엔 **상충 신호로 읽힘** — **v1에서 Measured가 배열에 라벨 날조한 혼동의 원천**. 권장: 앞 줄을 `Do not add citations, numbers, or ids into the paragraph_md prose.`로 **대상 한정**. (배열 규칙은 뒤 줄이 이미 정확.)

## 잔여(127-m1, 여전히 optional)
section `forbidden_moves`(anti-meta `teaching_the_reader...` 포함)는 v2도 `render_persona_prompt`에 미렌더 — anti-meta는 persona do_not + output-contract로 커버되어 비차단. Take 가다 register-drift 재발하면 그때 surfacing.

## 종합
v2 방향 = Take1 진단(placeholder 문법·exact-ID·인과verb·anchor)과 정확히 일치, 내 독립 conductor 결론과 수렴. 신규 hard 게이트 2개(placeholder/binding-id) 옳고, 3번째(causal)는 조건부 정의만 확인하면 OK. 누수 0 라이브 확정. should-fix(문구 한정) 반영 후 다음 Take 진행 권장.

(manuscript-atelier 커밋0 · 라이브=로컬 temp v2 rebuild + ID-leak scan.)
