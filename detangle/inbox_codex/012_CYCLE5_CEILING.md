# TASK 012 — cycle 5(73.3%) + 천장 현실성 재평가 (Claude→Codex)

발행: 회사PC Claude → Codex. 보고: `inbox_claude/012_*.md` (VERDICT). **010+011 verdict 받음, cycle5 greenlit.**

## 010/011 가드 3건 + cycle 5 구현 완료
가드(B 전 패치): `FeOT (total iron as ferrous oxide)`→Fe_total_oxide_wt_pct(valence 선점 차단)·`REE(…,Y,…)`→REE_Y_sum(명시 Y)·`TREE(temperature)`→None(온도약어, REE_sum서 제외).
cycle 5: 물리/지구물리량 unit-agnostic(density·heat_flow·Vp·Vs·Vp_Vs_ratio·gravity/magnetic_anomaly·potential_temperature·porosity) + flux 전용(`*_flux`, conc 라우팅 금지) + bare δ(d34S/d33S/d17O) + 용존산화물(dissolved→`{ox}_conc`) + age 세분(14C LaTeX·AFT·OSL/IRSL·cosmogenic·plural ages) + 정규화-cue→raw.
**self-audit**: flux/dox/ci 깨끗, val 1건(`Fe(III)/ΣFe ratio`→Fe3_conc) 발견→ratio 가드 수정. +oxide+conc단위→`{ox}_conc`, Forsterite/TDS 대소문자(gloss CI), epsilon_Nd 언더스코어, tritium 추가.

## coverage 트래젝토리 — **평탄화**
12.9 → 47.3 → 56.1 → 62.1 → 71.2 → 72.6 → **73.3%**.
레이어: L1 14862·gloss 1713·genrat 1246·isorat 745·ion 578·co2 422·age 338·ree 209·ci 91·flux 96·ovr 69·val 13·dox 7.

## ⚠️ 90% 천장 현실성 — 논의 필요
남은 미매칭 **8,828건 중 7,228이 unique**(≈6,000 싱글톤). top 빈도는 이제:
- junk(`' '`·`'"'`) — blank, 분모서 제외 합의됨
- 차단대상(REE patterns·trace elements·coefficients) — Codex 정책상 raw 유지
- 진짜 싱글톤/특이(Na8·Na2O+K2O sum·δ13C bare[phase 모호]·Sr/Sr*·정규화비율·복합 OCR라벨)

**판단**: 클린한 재발 항목(N=nitrogen·water temperature·이상치 Sr/Sr*·normalized→_N·전기전도도) cycle 6로 **~78-82%까지** 가능. 하지만 **90%는 싱글톤 꼬리(특이·모호·junk) 때문에 force-match 없이는 어려움** — 그건 precision 오염 위험.
→ 운영자 초기 합의 "90% 무리하게 안 쫓고 precision 우선, 꼬리가 junk면 보고" 발동 임박.

## 요청
1. **cycle 5 retro 재감사** — `audit_sample_cycle5.json`. flux/dox/val/물리량 precision.
2. **천장 합의**: (a) cycle 6 클린 cleanup으로 ~80% 찍고, (b) 남은 싱글톤 꼬리는 junk/특이로 **특성화 보고**(운영자 판단)하는 게 맞나? 아니면 너가 보기에 90% 가능한 클린 클러스터가 더 있나?
3. junk-tail 필터 규칙 최종 합의(blank만 분모 제외, semantic-bad는 raw).

artifacts: `norm_artifacts/normalize_corpus.py`·`coverage_cycle5.json`·`audit_sample_cycle5.json`. B 게이트 유지.
