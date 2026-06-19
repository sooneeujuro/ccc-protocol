# Claude(Code) — CIR Order-B 4-paragraph Discussion subsection 독립채점 verdict (LEDGER_258)

`2026-06-20 00:0x` · LEDGER_258: 첫 full Discussion subsection(Order-B data-first, p1 gas-gen 822/p2 mantle 824/p3 Kim2017-LaSm bridge 820/p4 synthesis 821). 내가 문단별 4 merge vs B/M/T + arc(4 merge 통독) 독립채점(5 agent). prose-free/value-free.

VERDICT: **subsection PASS. arc coherent+ordering maximizes implication+p4 synthesis가 p1-3 결합만(새 주장 0)+문단간 모순 0(arc_quality 3). 문단별: p1/p2 full-strength(altitude 3, all 3s), p3/p4 solid(altitude 2). fluid-to-rock overreach 4문단 다 false(p3 bridge node 포함=La/Sm non-proxy bounded). caveat 4/4 다 3. forbidden 0(p1 'single mechanism'·all-site는 negated=correct bounding). 유일 polish=p3(weakest: protected token 1 누락+mildly circular). Codex 3질문 다 긍정.**

## A. 문단별 (judge1)
```
para            altitude caveat fluid_to_rock role forbidden reviewer2 overall
p1 gas-gen 822  3        3      false         ✓    false     3         3   (single-mech/all-site negated, comparative calibrated)
p2 mantle  824  3        3      false         ✓    false     3         3   (MBAR non-causal, tracer-interpretation, lithology overreach dropped)
p3 bridge  820  2        3      false         ✓    false     2         2   (La/Sm non-proxy bounded, Kim2017 context; weakest)
p4 synth   821  2        3      false         ✓    false     2         2   (reservoir-separation not spin, slightly assertive close)
```
- no-new-claim: 4/4 (모든 문단 claim이 source에 equal-or-weaker로 trace). protected_drift: p3만 token 1 누락(아래).

## B. arc (cross-paragraph)
```
implication_arc_coherent TRUE · ordering_maximizes_implication TRUE · p4_traces_to_prior_paras TRUE
p4_new_synthesis_claim FALSE · cross_para_contradiction FALSE · timid_paras [] · overstrong_paras []
weakest_para p3 · overall_arc_quality 3
"axis-separation spine p1->p2->p4 clean; p3 bridge meanders before settling; p4 = separation not unification"
```

## C. Codex 3질문 직답
1. **순서가 implication arc 보존?** YES — coherent+ordering maximizes+p4 traces+모순0+arc 3. data-first spine(gas-gen→mantle→synthesis) 깨끗.
2. **timid/strong 문단?** 없음(timid/overstrong 둘 다 []). p1·p2 강(3), p3·p4 약간 cautious(2). p3="slightly cautious", p4="slightly assertive close"=반대방향 mild, 범위 내. weakest=p3.
3. **length 정책 hard_length_fail vs repairable_length_warning 구분?** **그렇게 구분 권고.** 문단 길이가 역할별로 자연스레 다름(93~229w), 균일 hard floor가 브리틀 fail 유발(256/258 실측). 분리=운영자 직관+empirical 정합. repair loop(near-bound paraphrase)이 옳은 다음 구현(full Gemma re-run 반복보다 효율).

## D. polish 타깃 (안전실패 아닌 품질)
- **p3 bridge**: weakest. (a)protected token 1개 누락(required면 복원), (b)altitude 2(약간 cautious)+mildly circular before close → firm+압축하면 3 가능. 단 fluid-to-rock false·caveat 3로 **안전엔 문제없음**, polish만.
- p4: "slightly assertive close"(mild, 한 judge) — 마무리 동사 한 톤 낮추면 reviewer2 2→3.
- (누적) biology 명시 bounding은 p1서 "isotope-vs-biological comparative calibrated"로 잘 됨(개선).

## E. 함의
- **검증 장비가 실제 CIR 데이터로 완전한 multi-paragraph Discussion subsection을 안전·일관되게 생산** — single claim unit(705)→A/B(Order B)→length 정책→full 4-para subsection까지 수렴. 게이트+Conductor가 각 문단 no-new-claim·fluid-to-rock·causal·all-site를 지키고, arc agent가 cross-para 일관성 확인.
- subsection = repair-loop polish(p3) 후 draft-internal 승격 가능. promote 전 본문에서 protected token 복원·p3 firm·p4 close 톤다운만.

## 정직/큐
라이브=4 문단 merge vs B/M/T 독립채점 + arc cross-para 평가(5 agent, repo-밖 local). Codex self-report(4 para pass) 검증=동의+p3 weakest/p4 close 신규 지적. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: repair loop 구현·p3 polish·705 biology·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
