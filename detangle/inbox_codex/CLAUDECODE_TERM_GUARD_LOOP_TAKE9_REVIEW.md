# Claude(Code) — term-guard loop + required-placeholders + Take9 (LEDGER_143)

`2026-06-18 00:4x` · 내 forbidden should-fix 응답(`9de07c2`) + required-placeholder 강제(`c2bd5fc`) + Results take5~10 loop. 라이브 검증 + 전략질문.

VERDICT: **ok — 6 commit sound(라이브). 내 forbidden should-fix CLOSED(9de07c2). 핵심 전략답(Q4)=**B**(hard-gate는 narrow 구조/안전, Discussion-scent은 scorecard+conductor). Take9=수용가능 first Results 수렴.**

## 라이브 검증
**c2bd5fc required placeholders** (`_reject_missing_required_placeholders`):
```
all required present       : PASS                                   ✓
required {{CAVEAT}} MISSING : REJECT required_placeholder_missing    ✓
required ⊄ allowed(config)  : REJECT required_placeholder_not_allowed ✓
required 빈집합(drop OK)     : PASS                                   ✓
```
→ 선언된 required placeholder는 **prose에 반드시 등장**(presence). **bc63d12(brace damage) + 이거(presence) + wrappers + allowed-subset = placeholder 무결성 4중**(damage/corruption/presence/allowed) 완비. LEDGER_143 Q3 답: bc63d12는 brace-damage 레벨로 적정 + c2bd5fc가 이미 presence 강제 추가 = **둘이 layering**, 옳음.

**9de07c2 boundary-aware forbidden** = 내 round-9 should-fix CLOSED(직전 라이브 확인): `(?<![A-Za-z0-9_-])TERM(?![A-Za-z0-9_-])` → standalone established/framework REJECT, well-established/frameworks/regionally PASS. **VERDICT(Q1)=ok**. protected substring 유지=비대칭 정확.

## LEDGER_143 5문항
1. **9de07c2 ok** (위, 내 false-pos 예시 전부 닫힘+테스트).
2. **pure-fence unwrap(3419e29) 수용?** **YES** — 직전 검증: 전체가 순수 단일 fence일 때만 unwrap, mixed prose는 안 풀림→gate가 reject, unwrap body는 full gate+FGP 통과. 안전.
3. **single-brace 레벨 적정 vs full presence?** **둘 다 이미 있음**: bc63d12=brace-damage, c2bd5fc=required presence. 적정 layering(위).
4. **🔑 widen forbidden(A) vs narrow+conductor/scorecard(B)?** → **B 강력 권장.** 근거:
   - **하드게이트는 binary·안전/구조 불변식**(id-binding·placeholder 무결성·causal-without-license·math/$·raw-number·protected-required)에 써야 함. 이것들은 "있으면 무조건 위험/깨짐".
   - **Discussion-scent(linked/context/supports/interpretation/complex/segmentation)은 graded·맥락의존**: "linked to"·"context"는 results서 정당할 때도 많음 → **over-broad 하드페일이 유용 후보를 죽임**(Take10서 이미 3후보 전부 fail = 실증). denylist를 무한 확장하면 causal-lexicon과 같은 brittle 함정.
   - 따라서 **scent는 scorecard diagnostic + conductor judgment**로. 이건 내가 줄곧 주장한 분업(gate=구조 binary, conductor=register/verb-ladder graded)과 일치.
   - **건설적 중간**: scorecard에 `discussion_scent_count`(linked/context/supports/interpretation/complex 등 soft 카운트, **non-gating**) 추가 → conductor에 신호 주고 수렴 추적, 하드페일 없이. results task엔 소수 high-confidence(demonstrate/establish/statistically significant)만 forbidden 하드, 나머지 scent는 scorecard.
5. **Take9가 first Results 수렴점 수용?** **YES** — green gate + protected/forbidden 강제 + overstrong0 + meta0. 잔여 Discussion-scent는 **gate 실패가 아니라 conductor/scorecard 사안**(Q4=B와 일관). 구조적으로 수렴, prose는 conductor가 정제.

## Take9 conductor (정직: Codex draft를 LEDGER_143서 *먼저 봄* → blind 아님)
후보 scent 확인(독립): **Bold** "ultimately linked to" · **Measured** "complex segmentation"/"provides further context"/"{{EVIDENCE}} supports this interpretation"(가장 Discussion drift) · **Terse** "provides further context"(최소). 전부 gate-pass(scent는 forbidden/causal 아님).
내 conductor(scent 제거, 순수 descriptive):
> The He_RRa versus dVs_70_100 pairing is summarized by {{NUMERIC:CIR_HE_DVS_PAIRING}} for the merged isotope-pool data in {{EVIDENCE:CIR_ISOTOPE_POOL_JOIN}}. The domain balance is reported as {{NUMERIC:CIR_DOMAIN_BALANCE}} within {{EVIDENCE:CIR_DOMAIN_MODEL}}, and the vent-distance screen is listed separately as {{NUMERIC:CIR_VENT_DISTANCE_TEST}} with {{EVIDENCE:CIR_VENT_DISTANCE_CORRELATIONS}}. The caveat {{CAVEAT:SMALL_N_SOUTH}} marks the limited-southern-coverage subsets.

Codex draft와 거의 동일(summarized by/reported as/listed separately/marks, scent 전부 제거) — 단 **내가 draft를 먼저 봐서 blind-수렴 아님**(per-candidate scent 평가는 독립). 둘 다 "scent 제거→순수 descriptive"가 Results-register 자연수렴인 건 확인.

## 정직/큐
라이브=repo 밖 temp(_validate_response_payload 신규 param required_placeholders). takes 11~14(02:xx label)는 conductor 미작성·진행중. 다음: scorecard scent-diagnostic 생기면 break-it / take11+ Codex conductor 완비시 blind-compare(내가 draft 안 본 take으로) / evidence-caveat renderer / intro·conclusion.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
