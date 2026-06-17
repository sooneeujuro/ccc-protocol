# Claude(Code) — paragraph_word_count gate (2c23479) break-it + real-run evidence

`2026-06-18 04:1x` · 신규 코드 우선. `constraints.paragraph_word_count {min,max}` 게이트 라이브 break-it(repo 밖 temp, 실제 `_WORD_RE` 복제) + take53/54 freer 실런 word-count(카운트만, prose/값 미echo).

VERDICT: **issues_found(비-안전, 설계긴장) — 게이트는 기계적으로 건전(char class가 hyphen/slash/colon/dot 포함 → 화학식·복합어 `143Nd/144Nd`·`mid-ocean-ridge`·`mg/L`를 whitespace와 동일하게 1단어로 셈 = 좋은 설계). 단 🔑 **단일 task-level band를 Bold/Measured/Terse에 일률 적용 → persona 길이변이(=diversity의 한 축)와 직접 충돌**. 실런이 확증: band {90,130}=40단어폭인데 baseline 자연 persona spread=46단어(>band폭). + 사소 latent: apostrophe/em-dash over-count.**

## 1. 기계검증 (라이브, 실제 `_WORD_RE` 복제)
char class `[A-Za-z0-9][A-Za-z0-9_:/^.-]*` 가 hyphen/slash/colon/dot/caret/underscore 포함 → **복합어·화학식·비율·범위가 whitespace 카운트와 일치**(내 초기 "복합어 undercount" 가설은 **틀림**, 확인):
```
plain prose                       ws=18 regex=18  Δ0
geochem compounds(143Nd/144Nd,mg/L,mid-ocean-ridge) ws=16 regex=16  Δ0   ← 좋은 설계
isotope ratios/ranges(0.512-0.513,10-20 km)         ws=15 regex=15  Δ0
section labels [Introduction]..                     ws=5  regex=5   Δ0
```
→ 복합어 처리는 의도적이고 정확. malformed-config 검증(min<1·max<min·max>1000·bool)도 적절.

## 2. 🔑 핵심: 단일 floor vs persona diversity (실런 확증)
**take53/54 freer 실런 per-persona regex word count(카운트만):**
```
take53 (freer baseline) : Bold=56  Measured=102 Terse=90  spread=46
take54 (freer FGP)      : Bold=95  Measured=94  Terse=95  spread= 1
band(둘 다 동일)        : {min:90, max:130}  = 40단어 폭
```
- **band 폭(40) < baseline 자연 persona 길이 spread(46)**. 즉 band가 persona 다양성보다 좁음 → 세 persona 자연길이를 동시에 못 담음. **baseline Bold=56은 min=90 미달 → 일률 floor면 reject**(too_short). 내 합성 Terse 예측이 **실 데이터로 확증**(짧게 쓰는 persona는 런마다 다르나 — 여기선 Bold — 일률 floor가 그 persona를 친다).
- take54 FGP는 95/94/95로 **길이변이 거의 소멸(spread 1)**. (FGP 때문인지 band 압력인지 N=1이라 분리 불가 — 아래 정직 캐비엇. 단 어느 쪽이든 band가 persona 길이축을 짓누르는 방향.)
- → **over-constraint→homogenization 명제(persona-collapse)의 새 인스턴스.** freer 프롬프트가 복원한 variance(spread 337 char)를 **band가 너무 좁으면 길이축에서 되돌린다.** Terse는 설계상 짧음 — Bold 길이에 맞춘 floor는 Terse(또는 그 런의 최단 persona)를 false-reject하거나 padding으로 내몬다(=다른 경로의 collapse). 

## 3. word count는 development의 blunt proxy
README 의도="freer가 under-developed paragraph로 collapse하는 것 방지". 단 word count는 **길이**지 development가 아님 — Codex 자신의 too_long 테스트가 "synthetic filler prose"로 max 초과 증명 = padding이 길이를 채움. floor로서 1문장 degenerate collapse는 잡지만 "충분히 전개됨"은 보증 못 함. **degenerate-collapse FLOOR로는 OK, "development band"로는 과대해석 금지.**

## 4. 사소 latent (whitespace 대비 over-count)
char class에 apostrophe·em-dash(—,U+2014) 없음 → 분할:
```
possessives/contractions("ridge's","doesn't","mantle's") ws=14 regex=19  Δ+5
em-dash 무공백절("inference—bounded—remains")              ws=13 regex=15  Δ+2
```
→ 소유격/축약·무공백 em-dash 많은 절에서 regex가 whitespace보다 **over-count**. 작고 latent(tight max 근처서만 too_long 위험). 정식 prose엔 축약 드물어 영향 미미. (원하면 prefix처럼 normalize, 단 우선순위 낮음.)

## 권고
1. **쓸 거면 loose degenerate-collapse FLOOR로**(예: min~30, max 넉넉 ~180-200). 40폭 band는 자연 persona spread(46)보다 좁아 clip/converge 강제. **Bold 길이에 calibrate 금지.**
2. 또는 **per-persona band**(Terse 낮은 floor / Bold 높은) — 길이 shaping이 진짜 목표면. 현재는 task-level 단일 필드 = 일률.
3. degenerate collapse만 막고 "development"는 scorecard(diagnostic counts)·conductor 판단에 맡길 것. word floor는 length proxy.

## 정직/큐
라이브=repo 밖 temp(`_WORD_RE` 복제 + malformed-config 로직)·take53/54 freer 실런 word count(카운트만, freer baseline은 resolved 값 없음=draft prose, prose/값 미echo). 신규코드=2c23479(HEAD). manuscript-atelier 커밋0. ccc detangle file-specific add. Anthropic_Invoices zip untracked. take53/54 아직 LEDGER 미보고 — 선제 리뷰(band 폭<persona spread 확증). **caveat: per-condition N=1**(FGP convergence vs band-pressure 분리 불가, FGP-underpowered와 동일 한계) — 단 "band폭<persona spread→clip 강제" 구조 결론과 Bold@56<floor reject는 draw 무관하게 성립. 다음: band 권고 반영/per-persona 검토 / numeric-slot false-pos 수정 / operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
