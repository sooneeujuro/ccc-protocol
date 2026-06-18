# Claude(Code) — BMT v3 Intro 섹션 채점 + Abstract와 cross-section 합성

`2026-06-19 02:0x` · BMT v3 Intro pilot(`bmt_v3_intro_profile_v3_20260619T012344`, N=5×B/M/T=15, profile v3) 독립채점(judge2, repo-밖 클린 paragraph_md). Intro 전용 rubric: result-leak avoidance + framing + safety. 기계 사전검사(result-term/diagnostic grep)=0/15 리터럴. 점수/카운트만.

VERDICT: **Intro PASS. result_leak 확정 0(15개 다 발견 미리말 안 함), framing 강함, safety 클린. Cross-section 신호: Terse=robust default(양섹션 3.0), Bold=timidity는 Abstract전용이나 overclaim-edge가 2섹션 재현, Measured=Intro서 과hedge로 aim 매몰. → Bold 진짜 리스크는 timidity 아닌 overclaim-edge(v3 claim-ladder는 엉뚱한 곳 겨냥).**

## A. Intro 집계 (judge-avg)
```
rep persona | fram leak_avoid scope reg prot conc | flags
501 Bold    | 3.0 3.0 3.0 3.0 3.0 2.5 | -
501 Measured| 2.0 3.0 3.0 3.0 3.0 2.0 | -
501 Terse   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
502 Bold    | 3.0 2.5 2.5 2.5 3.0 2.0 | overclaim(j2)  <- 미리-성공 암시
502 Measured| 2.5 3.0 3.0 3.0 3.0 2.0 | -
502 Terse   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
503 B/M/T   | 3.0 3.0 3.0 3.0 3.0 3.0 | - (전부)
504 Bold    | 3.0 3.0 3.0 3.0 3.0 3.0 | -
504 Measured| 2.0 3.0 3.0 2.5 3.0 2.0 | -  <- 과hedge framing 약화
504 Terse   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
505 B/M/T   | 3.0 3.0 3.0 3.0 3.0 2~3 | -
```
- result_leak_avoidance: Bold 2.90·Measured 3.00·Terse 3.00. **result_leak 확정 0**(유일 flag=502 Bold overclaim split). protected 15/15·causal 0·meta 0·new_number 0·예산 15/15·게이트 fail 0.
- framing_strength: Bold 3.00·Terse 3.00·**Measured 2.50**(2.0 ×2). composite: Terse 3.00>Bold 2.87>Measured 2.77.

## B. 🔑 Cross-section 합성 (Abstract v3 + Intro)
```
persona | Abstract(claim_alt/comp) | Intro(framing/comp) | 신호
Terse   | 3.00 / 3.00              | 3.00 / 3.00         | robust default, 양섹션 클린
Bold    | 2.50 / 2.70 (timid)      | 3.00 / 2.87         | timidity=Abstract전용; overclaim-edge 2섹션 재현
Measured| 2.80 / 2.78              | 2.50 / 2.77 (과hedge)| 섹션의존: Abs OK, Intro aim 매몰
```
- **Bold**: Abstract선 timid(claim 2.50)였지만 Intro framing은 3.0=섹션별로 다름. 그러나 **overclaim-edge는 두 섹션 다 출현**: Abstract 502/403의 mechanism-framing(degassing/transport) flutter + Intro 502의 "방법이 clear signature 낸다" 미리-성공 암시. 둘 다 split(미확정)이나 **같은 방향이 반복** = Bold의 일관된 리스크.
- **Measured**: Abstract 정상, Intro선 과hedge가 aim을 매몰(framing 2.0 ×2). Measured의 caveat-우선 스타일이 framing-우선 섹션(Intro)선 약점.
- **Terse**: 양 섹션 최강·클린. T2 frame-bound 기본 승격의 정당성 재확인.

## C. 함의 / 권고
1. **Bold v3 claim-ladder는 엉뚱한 곳 겨냥**: timidity는 Abstract 전용 증상이고, 섹션 가로질러 반복되는 건 **overclaim-edge**(mechanism/preview). Bold 튜닝하려면 claim-ladder보다 **overclaim/preview 경계 강화**가 우선(do_not: "method가 성공/signature를 낸다고 미리 말하지 말 것", "degassing/transport를 bounded pathway로"). 단 둘 다 split=미확정이라 **3번째 섹션(Results-adjacent)서 또 나오면 확정** 후 손대기 권고(단발로 프로필 안 건드림).
2. **Measured Intro 과hedge**: 1섹션 신호. framing-우선 섹션 가드(do: "aim을 한 문장으로 분명히, hedge는 aim 뒤") 후보지만 역시 재현 확인 후.
3. **Terse**: 손대지 말 것(양섹션 최강).
4. Intro 자체는 PASS — result-leak 0, framing 강, safety 클린.

## D. 다음
- **Results-adjacent(interpretation-overreach)** = 3번째이자 마지막 섹션. 이걸로 suite 완성 + Bold overclaim-edge가 3섹션째 재현되는지(=확정 trigger) 확인. rubric: interpretation_overreach 플래그(report 자리서 causal/significance 해석?)+evidence_binding.

## 정직/큐
라이브=Intro 클린 paragraph_md 15개 채점(judge2, repo-밖) + 기계 result-leak 사전검사(0/15 리터럴) + Abstract와 cross-section 합성. resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: Results-adjacent 섹션·Bold overclaim-edge 3섹션 확인·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
