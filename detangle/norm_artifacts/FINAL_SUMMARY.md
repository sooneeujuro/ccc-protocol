# FINAL SUMMARY — VP-NORM-1 정규화기 (Claude ↔ Codex 밤샘 co-op, 2026-06-16)

> **결론: corpus 변수 정규화기 완성. coverage 12.9% → 75.4% (5.8배), precision 99.2%(Codex 감사), 전구간 $0·비파괴.**
> Codex(GPT5.5)와 13라운드 CCCP 협업. B(sidecar 적용)·PR머지·ceiling 수락은 **운영자 인계**.

## 1. coverage 트래젝토리 (cycle별)
```
baseline(normalize.py 단독)  12.9%   ← "있으니 다 될거"의 실체
cycle 1 (oxide/trace/REE/ratio)      47.3%
cycle 2 (gas/cation/anomaly/mineral) 56.1%
cycle 3 (precision 수정 6건)          62.1%
cycle 4 (generic ratio/isotope/gloss/CI) 71.2%
cycle 4.1/4.2 (Codex 008/009 통합)    71.2%
cycle 5 (물리/flux/bare δ/용존산화물/age) 73.3%
cycle 6 (부분압/bracket/이상치/캐럿/junk) 74.8%
+ Nd/Na pre-B fix (013B)              **75.4%**  ← FINAL
```
**평탄화 = honest ceiling.** 마지막 cleanup이 <1%p → 더는 precision-safe하게 못 올림.

## 2. 레이어별 분포 (30,717 매칭)
L1 vocab 15,279 · L1c(구조정리) 4,144 · L0(isotope 재사용) 5,191+201 · gloss 1,883 · genrat 1,248 · isorat 850 · ion 581 · co2 422 · age 338 · ree 209 · ci 142 · flux 96 · ovr 69 · brk 43 · val 13 · dox 7 · pp 1.

## 3. precision 이력 (Codex 독립 120-라벨 감사)
cycle3 94.2% → cycle4 retro 97.5% → cycle4 reaudit 95.8% → **cycle4.1/4.2 98.3%** → **cycle5/6 99.2%**.
협업으로 false-match **15+ 패턴** 공동해소 (Claude self-audit: 구조/명백 / Codex: speciation·조성·context·단위·valence nuance).

## 4. ceiling 근거 (왜 90% 아닌가)
남은 25%(10,019 미매칭 / ~7,800 unique) 분해:
| 카테고리 | 비중 | 판정 |
|---|---|---|
| 의도적 차단(REE pattern·coeff·trace/major elements) | ~5% | **정상**(Codex 정책) |
| blank/junk(' '·"·not measured·n.d.) | ~0.3% | **분모 제외**(합의) |
| phase-모호 δ(bare δD·δ¹³C, 상 미상) | ~2% | **raw가 정답** |
| formula/model(Na8·Fe8) | <0.1% | raw |
| **싱글톤 꼬리(각 1-2회, 특이/OCR/복합)** | **~15%, 5,500 unique** | **비가역** |
→ **정규화가능 분모(total−junk−blocked≈38,600) 기준 79.6%.** 90%=싱글톤 force-match=sidecar 오염 → 운영자+Codex 합의로 금지.

## 5. regression probe set (B 적용 전 회귀 가드 — 현재 20/20 PASS)
`Nd→Nd_conc`·`Na→Na_conc`·`n.d.→junk`·`FeOT/FeO_total→Fe_total_oxide_wt_pct`·`total Fe→Fe_total_conc`·`REE(…,Y)→REE_Y_sum`·`TREE(temp)→None`·`CO2(dissolved/mmol-mol)→CO2_conc`·`F(ppm)/F-→F_conc`·`Fe(III)→Fe3_conc`·`Fe(III)/ΣFe ratio→None`·`3H/3He age→age_3H3He`·`Age grid misfit→None`·`P(CO2)→pCO2`·`Pressure(GPa)→pressure`·`LaN/YbN→La_Yb_N`.

## 6. 산출물
- 정규화기: `manuscript-atelier/tools/corpus-normalize/normalize_corpus.py`(L0재사용+L1 vocab+L2 구조+pre-pass) + `dryrun_coverage.py`. 스냅샷: 이 폴더 `normalize_corpus.py`·`coverage_cycle6.json`·`audit_sample_cycle6.json`.
- 채널 로그: `inbox_codex/006~013` + `inbox_claude/006~013B`(Codex verdict 전부).

## 7. 불변식 준수
- **B 게이트 절대 준수**: sidecar **0건 write**. dry-run은 전부 읽기전용(G:\corpus_md_export_20260612\sidecars).
- **corpus git-push 0**: 채널엔 vocab/코드/aggregate-통계만(논문본문·사이드카·인덱스·그림 미포함).
- **지출 $0**: 전 작업 결정적·로컬. 예산 $666 중 0 사용.

## 8. 🚪 운영자 인계 (결정 필요)
1. **75.4% ceiling 수락?** (원래 90% 목표 대비 — 사유: 싱글톤 꼬리 force-match=오염, precision 우선 합의). 정규화가능 기준 79.6%.
2. **B 적용 go?** — VP-NORM-1 §5(백업→정규화→검증→리포트→롤백)로 sidecar에 id 기록. regression 20/20 통과 상태. 운영자 "박아" 한 마디면 적용 가능.
3. **PR#15(verification policy)·PR#16(normalization spec) 머지?** — Codex 004/005/golden 통과. PR#16은 id-스킴(SiO2 vs SiO2_wt_pct) 구현맞춤 정렬 필요.
4. **정규화기 코드 PR화?** — tools/corpus-normalize/ 를 manuscript-atelier PR로(현재 로컬+채널 보존).
- 별개(환경블록): 그림 830편(datalab머신+NAS), 배포(B후) — 운영자 환경 작업.

— Claude(Opus 4.8) + Codex(GPT5.5), CCCP coop/detangle-20260615. 루프 정상종료.
