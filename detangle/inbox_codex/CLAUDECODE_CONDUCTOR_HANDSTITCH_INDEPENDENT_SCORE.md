# Claude(Code) — Conductor hand-stitch smoke (LEDGER_238) 독립 재검 + verdict

`2026-06-18 22:2x` · LEDGER_238의 Conductor stitch smoke(3 packs, `quartet_v2_heldout_take87_n10_20260618T112008Z`)를 **독립 재채점**. 중요: 이건 Gemma model run이 아니라 **Codex 손-merge**(`Conductor_codex_response.local.json`, 파일에 "It does not call Gemma" 명시). Codex가 자기 merge를 자기 게이트로 "PASS" 매겼기에, 도장 대신 독립 검증함. pack당 judge 2명(j2=adversarial, "불확실하면 new-claim으로 카운트"), repo 밖 local read, count/flag/점수만.

VERDICT REQUESTED 응답: **지침 coherent는 독립확정. 단 (a) 손-merge지 Gemma 아님=장비 검증 0회 유지, (b) Codex 기계게이트가 놓친 구조적 meta 1건(12809Z). 권고=A(runner 빌드→Gemma→내 채점), runner에 "implication 자기분류 금지(term 아니라 move)" 가드 추가.**

## A. 점수 (count/flag만; prose/값 0)
```
pack       no-new-claim(j1/j2)  tie_breaker          protected  meta(j1/j2)  new_num  bait  dv2(merge,javg)
12009Z     0 / 0                higher+caveat(기존)   byte-exact 무 / 무       0       0     3.0 flat
12427Z     0 / 0                bait DROP(j1 safer,   byte-exact 무 / 무       0       0     ~2.9 (claim_alt j1=2)
                                 j2 bounded-affirm)
12809Z     1 / 0  <-split       higher+caveat(기존)   byte-exact T / F  <-     0       0     ~2.9 (reg j1=2)
```
- 집계: protected 6/6 byte-exact(1.37 Ma 포함) · new_number 0/6 · new_overclaim_or_bait 0/6 · tie_breaker_from_existing **6/6 true**(invent 0). dv2 merge 문단 ≈2.9–3.0(약하지 않음).

## B. 핵심 발견
1. **확인**: 2/3 pack(12009Z·12427Z)은 두 판정 모두 new-claim 0. Codex 손-merge가 강한-모델 기준 no-new-claim·protected·bait-drop을 지킴 → **v2 Conductor 지침이 coherent**하다는 LEDGER_238 주장은 독립으로도 성립.
2. **bait pack(12427Z)**: merge가 eruption-recency frame을 **버림**(safety win). 두 judge는 그걸 "safer retreat"(j1, claim_alt=2) vs "bounded-affirmative, caveat 생존"(j2, claim_alt=3)으로 다르게 라벨 — 둘 다 bait 제거엔 동의.
3. **⚠️ Codex 게이트 미탐(12809Z)**: 마무리 문장이 **자기 함의를 분류하는 구조적 meta 무브**("이건 ~류의 implication" self-classify). j1=meta_sentence true(+new_claim 1), adversarial j2=false. Codex 기계게이트("no meta *terms* detected")는 통과시킴 — 금지**단어**가 아니라 **move**라서 term-매칭으로 안 걸림. **확정 fail은 아님(adversarial j2가 클리어)=경계선.**

## C. 왜 이게 중요(병목 논리)
- 손-merge를 한 건 **강한 Codex**. 실전 Conductor는 **약한 Gemma**. self-classification 같은 메타 무브는 약한 모델이 더 잘함 — 강한 Codex조차 1/3에서 경계를 밟았으니, Gemma는 더 위험.
- 따라서 이 smoke가 세우는 건 "지침 coherent"까지고, **"Gemma가 그 지침을 지키나"(=장비)**는 여전히 미검증. 그게 operator가 짚은 진짜 병목.

## D. 권고 (operator 두 선택지)
- **A(추천): 자동 Conductor stitch runner 빌드** → B/M/T JSON ingest → Gemma로 Conductor 프로필 실행 → local-only Conductor_response + safe manifest emit → 같은 게이트 자동. 그 다음 내가 model-run 출력을 채점 → **진짜 sign-off**. runner는 버리는 테스트 아님 = 실전 글쓰기 시스템이 어차피 필요로 하는 production 부품.
  - 빌드 시 가드 1줄: **Conductor 마무리에서 자기 implication을 분류/명명하지 말 것**(구조적 meta; 기존 `meta_sentence` 게이트를 term→move로 확장). 12809Z가 그 필요를 보여줌.
- B(지금 baseline 수락): 가능하나 상태를 **"Conductor=지침 coherent(독립확정)/장비 미검증/meta-self-classify 경계 1건"**으로 정직 라벨할 때만. 손-sim이 지침 리스크는 줄였고, 남은 "Gemma 준수" 리스크는 첫 실전 run이 드러냄.

## 정직/큐
라이브=Codex 손-merge 3개 + 각 B/M/T 소스 독립 재채점(6 agent, repo 밖 local). Codex 자기채점 그대로 안 받고 검증함. resolved 값/prose/캡션 0 노출·0 커밋. manuscript-atelier 커밋0. ccc file-specific add. 미해결: Conductor **model-run** 검증(runner) · df052b0 leak(MISSING_FIGURES.json).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
