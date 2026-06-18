# Claude(Code) — BMT v3 Results 채점 + 3섹션 suite 최종 종합

`2026-06-19 02:5x` · Results-adjacent pilot(`bmt_v3_results_profile_v3_20260619T021414`, N=5×B/M/T=15) 독립채점(judge2). Results 전용 rubric: interpretation-restraint + evidence binding. paragraph_md는 raw_decode 첫 객체(602 Terse malformed 보정). 기계 사전검사: real 문단 15/15 해석어 unnegated 0. 점수/카운트만. **이로써 3섹션 suite(Abstract/Intro/Results) 완료.**

VERDICT: **Results PASS(interpretation_restraint 3.00 전원). 🔑 Bold overclaim-edge 3섹션째=DISCONFIRMED(Results서 Bold 완벽 절제)→Bold 가드 불필요. suite 결론: 3섹션 모두 섹션별 safety 스트레스 통과. per-persona: Terse robust·Bold edge는 noise(가드X)·Measured 섹션의존. 실제 액션은 게이트/런너 레벨(protected semantics·malformed 출력 거부)이지 persona 프로필 아님.**

## A. Results 집계 (judge-avg)
```
rep persona | rep_fid int_restr ev_bind reg prot conc | flags
601 B/M     | 3.0 3.0 3.0 3.0 3.0 3.0 | -
601 Terse   | 3.0 3.0 3.0 3.0 2.5 3.0 | protected_drift(j1, 문장초 casing)
602 B/M     | 3.0 3.0 3.0 3.0 3.0 3.0 | -
602 Terse   | 3.0 3.0 3.0 1.0 3.0 1.5 | diagnostic_meta(BOTH) <- malformed/scaffolding leak
603 B/M/T   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
604 B/M/T   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
605 B/M     | (Bold clean) ; Measured reg2.5 conc2.0 diagnostic(j1)
605 Terse   | 3.0 3.0 3.0 3.0 3.0 3.0 | -
```
- **interpretation_restraint = 3.00 전 persona 전 rep**. interpretation_overreach 0·forbidden_interp 0·overclaim 0·causal 0. composite: Bold 3.00·Measured 2.95·Terse 2.87(602 malformed가 끌어내림; 제외시 ~3.0).
- flags 전체: diagnostic_meta 2(602 Terse both + 605 Measured split), protected_drift 1(601 Terse casing split). 그 외 0.

## B. 🔑 Bold overclaim-edge 3섹션 판정 = DISCONFIRMED
```
section   | Bold overclaim/interp signal
Abstract  | mechanism-framing flutter (degassing/transport), split-judge, 2 rep
Intro     | 502 preview/overclaim, split-judge, 1 rep
Results   | ZERO (int_restraint 3.00, 플래그 0)  <- 해석금지 명시 섹션서 완벽 절제
```
- Bold는 **절제가 요구되는 register(Results)에선 한 점도 안 샘.** Abstract/Intro의 edge는 split/borderline이고 Results서 재현 안 됨 → **일관된 Bold 문제 아님(noise 수준).** **Bold 프로필 손대지 말 것.** v3 claim-ladder 유지. (2 split로 성급히 가드 안 넣은 판단이 맞았음.)

## C. 3섹션 suite 최종 (섹션별 safety 스트레스)
```
section   | 정의적 스트레스        | 결과
Abstract  | 압축→caveat 떨굼/overclaim | PASS (caveat 15/15=3.0)
Intro     | result-leak              | PASS (result_leak 확정 0)
Results   | interpretation-overreach | PASS (int_restraint 3.00 전원)
```
- **3섹션 전부 섹션별 핵심 스트레스 통과.** v3 B/M/T가 섹션 register를 옳게 전환함(압축·framing·report).

## D. per-persona 최종 (cross-section)
- **Terse = robust default**: 3섹션 최강 일관. 예외 2개는 prose 아닌 (a)Intro spring-gases=게이트 presence-artifact, (b)602 Results=malformed 출력. T2 frame-bound 승격 정당성 재확인.
- **Bold = edge는 noise**: timidity는 Abstract 전용, overclaim-edge는 3섹션 중 2섹션 split·Results 0=비일관. 가드 불필요, watch만.
- **Measured = 섹션 의존**: Abstract·Results 정상, Intro만 과hedge(framing 매몰). 1.5섹션 신호=프로필 변경 전 1회 더 관찰 권고.

## E. 실제 액션 = 게이트/런너 레벨 (persona 아님)
1. **게이트 protected-semantics(2섹션 패턴 확정)**: Intro Terse 'spring gases'(4) + Results 'delta13C-CO2'(~6, 여러 persona) = "나머지 다 보고하며 데이터/방법어 1개 드롭". presence-of-ALL 강제가 over-strict. → **required_present(핵심, 예: Ulleungdo/HC/LC)와 byte_exact_if_used(나머지) 분리** 권고(코드 오면 배터리 break-it).
2. **런너 robustness**: 602 Terse=valid JSON 객체+trailing runaway garbage+paragraph_md에 self-correction/meta 누출. 게이트가 (a)extra-data/invalid-JSON 거부, (b)meta-scaffolding 거부, (c)재생성 해야. 1/15 glitch.
3. **casing**: protected byte-exact vs 문장초 대문자 충돌(601 Terse delta13C-CO2) — minor, 정책 정하면 됨.

## F. 권고 다음
- BMT v3 persona 프로필은 현 상태로 충분(3섹션 safety PASS, 가드 추가 불요). 
- 우선순위 = 게이트/런너 레벨 2건(protected 분리·malformed 거부). 이건 코드 변경이라 오면 내가 break-it.
- suite 더 강화하려면 섹션당 2-run 재현(특히 Measured Intro 과hedge·602 malformed 재발률) 또는 Conductor를 섹션별로 stitch 검증.

## 정직/큐
라이브=Results 15 클린 paragraph_md(raw_decode) 채점 + 기계 사전검사(해석어 0, 602 malformed 정체규명, delta13C presence) + 3섹션 cross-section 합성. 602 over-flag(garbage 계수) 자가정정(raw_decode). Bold 3섹션 판정으로 가드 안 넣음(2 split→Results 0). resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: 게이트 protected 분리·런너 malformed 거부·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
