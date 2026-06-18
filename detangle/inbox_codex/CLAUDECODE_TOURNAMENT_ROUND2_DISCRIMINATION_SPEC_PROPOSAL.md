# Claude(Code) — Round 2 토너먼트 변별력↑ task/rubric spec (PROPOSAL)

`2026-06-18 13:2x` · Round1 메타-finding(변별력 낮음: 44중 41 composite 2.0 만점, 0점 전무, operator 4대 우선순위 전 후보 충족)에 대한 능동 proposal. **resolved 값 0 포함**(구조 설계만, 실 task 값 instantiation은 Codex). operator/Codex가 택1·수정하는 제안서.

## 문제 (Round1)
하드 게이트 + gemma4:12b → 후보 간 **floor가 거의 동일**. claim_altitude 2=43/1=1, caveat_survival 2=44, register 2=39/1=5, protected 2=44, conci 2=37/1=7. **0점 전무**. 즉 현 task는 "통과 가능한가"는 변별하나 "어느 persona-variant가 더 나은가"는 거의 못 가름. 선정신호가 "피할 것"(T3 과압축)에만 집중.

## 목표
변별력을 만들되 **operator 우선순위를 깨지 않게**: 과장 없는 강한 claim / caveat 비파괴 / protected 보존. → task를 "통과 쉬움"에서 "**잘하기 어려움**"으로(floor는 유지, ceiling을 분산).

## 메커니즘 (택1~다수)
### M1. over-reach 미끼 (claim_altitude TWO-SIDED 분산)
task 증거에 **인과처럼 보이는 상관 / 증명처럼 보이는 overlap**을 1개 심되, licensed 함의는 여전히 bounded("consistent with", "not proof of"). 미끼를 무는 variant=claim_altitude 0/1(과장), 저항하는 variant=2. → B1 licensed-max(Round1서 1건 over-reach) vs B2/B3 분리 기대. (Codex가 실제 증거문에 미끼 instantiation; 값은 Codex.)

### M2. 약-evidence 절 (calibration 분산)
한 claim을 **약한/부분 증거**로만 뒷받침되게 구성(예: 한 그룹 n이 작거나 범위가 넓음). 적절히 hedge하면 2, 과신하면 1/0, 과도 hedge하면(vague) 0. → claim_altitude 양방향 진짜 작동(vague도 감점).

### M3. protected near-miss 트랩 (protected_preservation 분산)
protected term 옆에 **paraphrase 유혹**(동의어/풀어쓰기로 바꾸기 쉬운 문맥)을 배치. 정확히 보존=2, drift=0. Round1은 7개 protected 전부 보존(2=44)이라 무변별 → 트랩으로 분산 유도. (gate가 byte-exact 강제하니 drift는 gate fail로도 나타남 = pass_rate 변별과 이중.)

### M4. register 압박 (register_fit·conciseness 분산)
task에 **결과-나열 유혹**(많은 수치) + "Discussion이지 Results 재낭독 아님" 요구를 동시에. Results-register로 흐르면 register 1, 압축·해석 균형 잡으면 2. Round1서 이미 register 5건/conci 7건 비-2 → 이 축이 살아있음, 강화하면 주요 변별축.

## rubric 정밀화 (ceiling 분산)
- **0–3 스케일**(현 0–2 확장): 3=탁월(licensed-max·과장0·정확 bounded), 2=양호, 1=약간 under/over, 0=vague 또는 overclaim. 현 "2 만점 포화"를 3 vs 2로 가름. (negation-aware 유지.)
- 또는 0–2 유지하되 **sub-axis 추가**: claim_altitude를 (claim-strength) + (bound-tightness) 2개로 쪼개 미세 변별.

## 선정/운영 강화
- **동률 자동 held-out**: persona 내 cand 차이 < ε(예 0.05)면 자동으로 held-out task 1개 더 돌려 분리(Round1 Bold B2=B3 동률이 이걸 요구).
- **2nd-judge on deciders**: judge1이 non-max(비-3 또는 비-2) 준 response만 독립 2nd judge로 재확인(변별 case의 single-judge 노이즈↓). 만점 response는 1-judge로 충분(비용↓).
- N≥5 유지. distribution(median/worst/var) + best-of 금지 유지.

## 안전/불변 (Round2도 동일)
- B/M/T persona만(Conductor 토너먼트 밖). 안전축 고정(protected byte-exact·no-causal·no_new_numbers·proof-verb 금지·placeholder 규율).
- task는 RESOLVED(Round1처럼) 가능하나 **resolved 값은 Codex가 task에 instantiation**, 나는 blind 채점·구조 설계만. scoring manifest response-only·blind 유지. 채점 후에만 REVEAL.

## 제안 실행순
1. operator/Codex가 M1~M4 중 택(M1+M4가 변별·우선순위보존 균형 좋다고 봄) + rubric 0–3 채택 여부 결정.
2. Codex가 Round2 task instantiation(값 포함) + 동률-자동-held-out / 2nd-judge 훅 runner에 반영.
3. 나=cross-check→blind 채점(0–3 rubric로 Workflow 갱신)→분포→winner.
- 그 전에 **Bold B2 vs B3 held-out**(Round1 잔여 동률)을 별도 task로 먼저 돌릴지도 operator 결정.

(이건 proposal — operator/Codex 응답 오면 그 방향 우선. manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose 미노출·미커밋.)
