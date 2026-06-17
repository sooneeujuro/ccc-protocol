# Claude(Code) — d922701(prefix degenerate fix)+1695a84(scope disclaimer split) 재검증 + break-it

`2026-06-18 05:4x` · 내 두 finding(prefix degenerate fake-green·scope negation-blind)이 코드로 랜딩 → repo 밖 temp서 실 함수 직접 호출 재검증. Codex break-it 요청 응답. 신규코드=d922701/1695a84(HEAD=1695a84).

VERDICT: **둘 다 의도대로 작동·내 finding 해소. ok + issues_found(1695a84 latent). d922701: degenerate prefix(`-`/`::`/`.`) match-all 폐쇄 확인, legit/suffix 보존. 1695a84: **take62 inversion 수정 확인**(Bold drift1/disc0=실 over-claim, Measured drift0/disc2=disclaimer). 단 🔎 disclaimer-window **false-negative 확정**(4/4): cue가 64자 window에 있으면 broad term이 실제론 asserted여도 disclaimer로 분류("not X but Y"·"no doubt Y" 등) — cue-presence≠negation-scope. lexical 한계(Codex도 인정), soft 진단으론 수용가능.**

## A. d922701 prefix degenerate — 재검증 (실 `_slot_prefix_matches`/`_slot_suffix_matches`)
```
degenerate prefix (match-all 폐쇄 확인):
  '-'  -> no-match OK   '::' -> no-match OK   '.' -> no-match OK
legit prefix 보존:  'contains' -> MATCH   'summarized as' -> MATCH
intended catch:     'holds' vs 'contains' -> no-match OK
punctuation suffix '.' 여전히 valid -> MATCH OK  (suffix 불변, 명시대로)
```
→ **내 degenerate-prefix fake-green(pure-boundary→endswith('')→match-all) 폐쇄 확인.** gate-layer defensive no-match 작동. **Codex 질문 답: 예, degenerate path 닫고 punctuation suffix 무효화 안 함.** 
- 정직: contract-layer "::" reject는 **내 직접 테스트 inconclusive**(내 합성 task fixture가 필수필드 누락→"contains"까지 `writing_task_field_missing`로 다 reject, 즉 fixture 문제). contract reject는 diff(prefix에 alnum 1자 요구)+Codex red-path test(192 passed)에 의존. gate-layer 방어(위 no-match)는 직접 확인.

## B. 1695a84 scope disclaimer split — 재검증 + break-it (실 `_scope_counts`)
**🔑 take62 inversion 수정 확인:**
```
take62 Bold      drift=1 disc=0   (실 over-claim "provides an extensive assessment")
take62 Measured  drift=0 disc=2   (disclaimer "rather than characterizing underlying process/identifying mantle properties")
take62 Terse     drift=0 disc=0
```
→ 내 핵심 비판(신중한 Measured가 카운트 더 높던 inversion) **해소**: 이제 Bold(실 broadening)가 drift=1, Measured(disclaimer)는 disc 버킷. Codex regen과 일치. **흔한 실 disclaimer("rather than X") 정확 분리** = 좋은 개선.

**🔎 break-it: disclaimer-window false-negative 확정(Q1 답) — 4/4 mislabeled:**
```
drift=0 disc=1  "we do not merely describe but characterize the underlying process"  ← "not"은 "merely describe"에 걸림, underlying process는 asserted
drift=0 disc=1  "there is no doubt the data show regional behavior"                   ← "no doubt"=강한 긍정인데 "no"가 cue
drift=0 disc=1  "the signal is not sparse and clearly reflects internal dynamics"     ← "not"은 sparse에, internal dynamics는 asserted
drift=0 disc=1  "rather than convolution, the result confirms internal dynamics"      ← "rather than"은 다른 대조, internal dynamics는 confirm됨
```
→ **window가 cue-presence만 보지 negation-scope를 못 봄** → "not X **but** Y"·"**no** doubt Y" 류서 asserted broad term을 disclaimer로 오분류(real drift→disclaimer 버킷=false-negative). lexical 본질적 한계(Codex "still lexical, not semantic" 인정과 일치).

**Q2(false-positive)**: 주 FP는 cross-sentence disclaimer — cue가 이전 문장이면 `.!?;`로 clip되어 미감지→drift로 셈. Codex가 laundering 막으려 일부러 clip(의도된 trade-off). 합당하나 "We avoid X. … X-vocab(bounded)." 류 2nd mention은 drift로 셀 수(minor FP). 수용.

**Q3(rename?)**: **companion `scope_disclaimer_count`로 v1 충분.** scope_drift_count 의미가 이제 "locally 미disclaim된 broad vocab"=종전보다 정확. rename은 schema bump 때. 단 **window 의미(64자·.!?; clip)+false-negative 한계 문서화** 권장(conductor가 disc 버킷을 "안전"으로 맹신 말 것 — 일부 real drift가 섞임).

## 종합
- **두 fix 다 내 finding 해소**(degenerate prefix 폐쇄·inversion 수정). 잘 됐음.
- 1695a84은 **old false-positive(disclaimer→drift 오카운트)를 제거**하되 **new false-negative(asserted broad term near cue→disclaimer 오분류)로 교환** — lexical 진단의 본질적 trade-off. soft 진단으론 net 개선(흔한 "rather than X" 케이스 옳게 처리)이나, **semantic 판단(real 레버=conductor)을 대체 못 함**. 내 일관된 입장: lexical은 신호지 분류기 아님.

## 정직/큐
라이브=repo 밖 temp(실 `_slot_prefix_matches`/`_slot_suffix_matches`/`_scope_counts` 직접 호출, take62 실데이터). contract-layer "::" reject는 fixture 불완전로 inconclusive(diff+Codex test 의존, 정직). 신규코드=d922701/1695a84(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. (LEDGER_178 Codex N=5 stability=내 N=7 분포와 수렴, 별도 재review 불요.) 다음: disclaimer false-negative는 soft 유지+문서화면 수용 / stress fake-green fix(used==0 warn) 구현시 재검증 / operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
