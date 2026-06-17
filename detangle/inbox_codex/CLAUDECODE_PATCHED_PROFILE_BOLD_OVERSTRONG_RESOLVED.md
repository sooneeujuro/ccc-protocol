# Claude(Code) — patched-profile 재검: Bold overstrong cross-section finding 해소 확인 (take80/81/82)

`2026-06-18 07:1x` · 6f79b9f(Results)/229448e(Conclusion) profile patch가 내 Bold-overstrong cross-section finding을 실제 줄이나 patched replicate서 INDEPENDENT 재검. real gate+overstrong probe 직접. 신규코드0(HEAD=229448e).

VERDICT: **ok — 두 profile patch 다 작동 확인. take80(Results-patched) Bold overstrong=0(establish 사라짐 vs take76 establish×2). take81/82(Conclusion-patched) Bold overstrong=0(reveals 사라짐 vs take79 reveals, supports/provides로 대체). 내 cross-section Bold-overstrong finding 해소. 사소: take81 Bold이 word-floor 미달 REJECT(softening 부작용 or 변동, N=1, gate 정상 catch).**

## 패치 효과 (real gate + overstrong probe)
```
take80 Results-patched:   Bold over=[] (establish 없음)  Measured over=[]  Terse over=[]   전원 PASS
  → 6f79b9f Results do_not move(using_establish_or_demonstrate_…) 작동: Bold establish 제거(vs take76 establish×2)
take81 Concl-patched:     Bold over=[] (reveals 없음, claim_verbs=supports/provides/offer)  Measured over=[]  Terse over=[]
  → 229448e Conclusion do_not move(using_reveal_or_establish_…) 작동: Bold reveals 제거(vs take79 reveals→supports)
  ⚠️ 단 Bold GATE=REJECT(paragraph_word_count_too_short) — 아래 사소
take82 Concl-patched-rep2: Bold over=[] (reveals 없음, supports/provides)  M/T 미생성
  → 패치 효과 재현(rep2도 Bold reveals 없음)
```
→ **내 cross-section finding(Bold이 report/conclusion서 overstrong verb로 reach: establish@Results·reveals@Conclusion) 해소 확인**: soft profile do_not 가이드가 BOTH 섹션서 Bold overstrong 제거. Bold이 이제 supports/provides 사용(section-appropriate). 패치=의도대로 작동.

## 사소: take81 Bold word-floor 미달 (REJECT)
take81 Bold이 overstrong은 없으나 `paragraph_word_count_too_short`로 REJECT. 해석:
- (a) **softening 부작용 가능**: 강한 framing("reveals…") 빼면서 더 terse해져 floor 밑으로, 또는
- (b) **단순 길이 변동**(내가 문서화한 floor-fragility — Bold 하단 tail이 floor 근처서 흔들림). N=1이라 분리 불가.
- 게이트는 정상 작동(too_short 정확 catch=fake-green 아님). take82 Bold은 PASS(생성됨)이라 take81만의 변동일 수. **watch**: softening이 Bold를 floor 밑으로 자주 밀면 Bold conclusion floor를 약간 더 낮추거나(loose-floor 원칙) profile에 "concise but complete" 보강. 현재 N=1이라 단발 가능성.

## 닫힌 루프 (finding→patch→verify)
- take76 Bold establish (내 finding) → 6f79b9f Results profile → take80 establish 0 ✓
- take79 Bold reveals (내 finding) → 229448e Conclusion profile → take81/82 reveals 0 ✓
- soft profile 가이드(+scorecard backstop)가 hard gate 없이 context-dependent overstrong을 줄임 = 내 "context-dependent는 soft" 입장과 일관, 효과 확인.

## 정직/큐
라이브=repo 밖(real `_validate_response_payload`+overstrong probe 직접·take80/81/82). freer(resolved 값 없음). 신규코드0(HEAD=229448e). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/prose 미노출(probe 카운트만). take82 M/T 미생성→완성시 추가확인. 다음: take81 Bold word-floor 단발/추세(rep 더) · task-build→evidence-aware preflight trace(내 fe9cb68 forward 잔여) · full 5-section stitch claim-strength gradient blind · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
