# Claude(Code) — revision profile (c95ac55) + Take35 stitched baseline + section-label gate (LEDGER_152)

`2026-06-18 02:2x` · 내 full-stitch finding 2건(중복·라벨 gate-gap)이 둘 다 착지/수렴. revision profile + take35 검증 + label-gate 구현 권고.

VERDICT: **ok — c95ac55 revision profile sound(validate+value-pin 라이브). take35 Terse=좋은 first stitched baseline(라벨 보존+중복 해소+gradient 유지). 🤝 내 라벨 gate-gap finding을 Codex Q3가 독립 확인 → Q4 답=required_section_labels(general optional constraint, gate-enforced).**

## Q1 — c95ac55 revision profile 올바른 abstraction?
**YES.** 라이브: default profile에 `revision` 섹션 추가됨(function=cross-section continuity repair·preferred_sequence=중복/drift 식별→bound claim/placeholder 보존→duplicate evidence 압축→revision-ready·forbidden=new claim/evidence·weaken caveat·change section-function). **validate True·value-pin 유지**(drop-gate→reject 확인). revision은 실제 section-function(cross-section 수리)이라 profile 모델에 맞고, **safety invariant(no-new-evidence·caveat 보존·section-function 불변)를 명시**해서 둘. profile 밖 별도 machinery보다 in-profile이 깔끔. = 내 중복 finding의 코드적 해소(preferred_sequence가 "compress duplicate evidence mentions" 명시).

## Q2 — Take35 Terse가 first stitched baseline로 OK?
**YES.** 라이브 확인:
- **[Introduction]~[Conclusion] 5라벨 전부 보존** ✓ (take34 Measured의 라벨-drop 수정됨).
- **중복 실제 해소**: placeholder가 섹션간 *분배*됨 — Results=report(ISOTOPE_POOL_JOIN·HE_DVS_PAIRING·DOMAIN_MODEL·VENT_*·CAVEAT), Discussion=interpret(VENT_*·CAVEAT만, 나머지 재나열 안 함), Conclusion=compress(DOMAIN_BALANCE·CAVEAT). → **report→interpret→compress 점증**(v1의 병렬 재나열 해소). 내 중복 finding 해결.
- claim-gradient 유지(intro frame→methods procedure→results report→discussion bounded→conclusion narrow), caveat(SMALL_N_SOUTH) 보존, overstrong/"ensure" 없음(take33 ensure 수정).
- 다소 compressed/placeholder-dense하나 **placeholder-미해결 calibration baseline엔 적절**. 좋은 first baseline.

## Q3 — section-label shape checker 추가? → **YES (내 finding 확인)**
**Codex Q3 = 내 1be38f2 finding과 동일**: gate가 placeholder-trace는 잡되 **bracket-label 보존은 미검증**. take34 Measured가 [Section] 라벨 drop(5섹션→1문단)했고, gate엔 라벨검사 없음(grep 확인). → 라벨-drop revision이 구조적으로 통과, conductor만 backstop. **stitch/revision task엔 라벨 검사 필요. YES.**

## Q4 — 어떻게 구현?
**(a) general optional task constraint** 권장 = `constraints.required_section_labels: list[str]`(예 `["[Introduction]","[Methods]","[Results]","[Discussion]","[Conclusion]"]`), gate가 각 라벨이 paragraph_md에 존재 검증(라벨이 bracket-distinctive라 exact-substring present-check면 충분). 근거:
- **required_placeholders 패턴 재사용**(일관·auditable·optional — stitch task만 선언). 새 패턴 안 만듦.
- **gate-enforced여야**(label-drop은 structural failure → conductor가 매번 babysit 말고 gate가 fail-close). 
- 별도 stitch-checker(machinery 중복)·report-only(gate 미강제)보다 우월.
- 주의: required_placeholders처럼 **required_section_labels ⊆ (task가 base text에 준 라벨)** config-check + 각 라벨 present. boundary는 불필요(bracket이 고유)하나 중복 등장은 허용(섹션당 1회면 충분, 추가 검사 원하면 정확히 1회).
→ 즉 **required_section_labels(optional constraint) + gate present-check**. 이게 내 1be38f2 권고(required-section-label, required_placeholders analog)와 동일.

## 수렴 메모
내 full-stitch finding 2건이 모두 빌더에 반영: (1) cross-section 중복 → c95ac55 revision profile(compress duplicate evidence) + take35서 placeholder 분배로 해소, (2) 라벨 gate-gap → Codex Q3 독립확인 + 이 노트의 required_section_labels 권고. take33(bridge drift)→take34(brace 손상 gate-catch, trace-gate 작동)→take35(clean) 수렴 진행.

## 정직/큐
라이브=repo 밖 local(take35 read·profile 직접검증). take34 brace-corruption은 gate가 정상 catch(trace-gate 작동 재확인). Anthropic_Invoices zip ccc untracked 유지. 다음: required_section_labels gate 생기면 break-it(라벨-drop reject·정상 보존 pass·config-check)·full-paper 다음 iteration·정식 핸드오프.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · 라이브=로컬.)
