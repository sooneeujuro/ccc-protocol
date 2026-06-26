# LEDGER_440_CLAUDE_0626_CORPUS_BUILD_HANDOFF

timestamp_kst: 2026-06-26
author: Claude (main session, 1M Opus)
recipient: Codex / operator
relay_safety: counts/status/paths/public_DOIs only; no manuscript prose, no resolved numeric values
purpose: 0626 정본 빌드 완료 보고 + 재인덱스 BLOCKER 2건 검토요청 (정본 확정/flip은 검토 후)

## 1. 무엇을 했나 (0624 → 0626 승격 빌드)
- 0618(구버전 정본) → D:\corpus_md_export_20260618 로 아카이브(이동, G: 공간확보). 보존됨.
- 0624 정본 → G:\corpus_20260626 통복제 (articles 3978 + 그림격리 3977폴더 + index + scripts + pdfs + supplementary; papers/ HTML캐시 제외). 21.789GB, FAILED 0.
- sidecar 통합: sidecars_v22_canonical(4014, Haiku verbatim + Gemma inventory) → G:\corpus_20260626\sidecars\
- helium 19편(HLW noble-gas) 추가: flat article + slug폴더(md+그림 262장) + STEM_TO_SLUG 갱신.
- CORPUS_VERSION.json → 2026-06-26 (sidecar=INTEGRATED, index=STALE 표기).

## 2. 결과 (검증게이트 통과)
| 항목 | 값 |
|---|---|
| articles (flat) | 3997 (0624 3978 + helium 19) |
| 그림격리 폴더 | 3977 hash + 19 helium slug |
| sidecars\ json | 3996 (전부 article 대응 — 고아 0 검증) |
| orphan (격리보존) | 13 |
| JSON 유효성 | 랜덤표본 0 깨짐 |
| sidecar ⊆ article | 0 위반 |

sidecar 구조 = Haiku verbatim(bibliographic/abstract/conclusions/references/figure_summaries/geography/analytical) + Gemma inventory(classification.type / made_new_measurements / **variables_reported**). schema v2.2.

sidecar pid 정렬 통계: exact 3976 / rename-map 16 / jaccard(연도일치 강제) 9 / orphan 13.
- jaccard에 **연도 일치 조건** 적용 → Farmer(2013)→Farmer(2007), Porcelli(2018)→Porcelli&Ballentine(2002) 오매핑 차단(다른 판/연도에 inventory 덮어쓰기 방지).

## 3. orphan 13편 (sidecars/_orphan_no_article/)
- **0624 정본에 본문 없음 8편**(0612엔 존재 — 정본화 때 누락/제외): Cande 2011, Torsvik 2014(plate motion); Gilfillan 2009, Miller 2021(17O), Parai 2021, Proskurowski 2008(Abiogenic); Farmer 2013·Porcelli 2018(책/리뷰 챕터 — 다른 판만 정본에 존재).
- **0624에 동일논문 있으나 표기차로 자동매핑 실패 5편**(본문 검색됨, inventory 메타만 누락 = 무해): Drake&Weill 1975, Jambon 1986(sidecar 오타 "Jamron"), Kim 2025→2024, Marty&Zimm 1999, Plummer 1982(오타 "Busenbero"). 각 정본 article은 원본+`__2` 중복 2건 존재(=dedup 사안과 얽힘).

## 4. ★ 재인덱스 BLOCKER — CODEX 검토요청 (정본 검색 품질 직결)
인덱스는 현재 0624 상속분(BM25+BGE, 3902 커버)이라 STALE. helium 19 + 최신 + sidecar inventory 반영하려면 재빌드 필요. 단 스크립트가 현 스키마와 불일치:

**B1. `scripts/build_retrieval_units.py` `variable_aliases()`가 레거시 키 `variables_measured`를 읽음.**
- 현 sidecar는 v2.2에서 `variables_reported`로 이관(variables_measured 제거).
- 영향: 재인덱스해도 chunk의 `variables` 필드가 전부 빈 채로 색인 → **변수기반 검색에 Gemma inventory 반영 안 됨**(classification/country/scope 메타는 정상).
- 제안 수정(1줄): `variables = sidecar.get("variables_reported") or sidecar.get("variables_measured")`. 항목 구조({id, raw_label,...}) 호환.

**B2. `scripts/run_dense.bat`가 `G:\corpus_md_export_20260618\` 하드코딩.**
- 0618은 D:로 아카이브(해당 경로 없음). build_bge_m3_dense.py 경로도 동일 점검 필요.
- 제안: 0626 경로로(또는 GEOCHEM_DATALAB_MD_DIR/GEOCHEM_SIDECAR_DIR env + 상대경로화).

재인덱스 전제: G: 여유 6.3GB(빠듯) → 0626 검증 OK 시 0624를 D:로 아카이브해 ~21.8GB 확보 권장. GPU 비어있음(util 0%).

## 5. 정본 상태 = 미확정 (flip 보류)
- 0626은 staging 상태. 리더 read_paper_ns.py는 sidecar 비참조(MD+그림 뷰어) — 상대경로 self-contained 확인.
- 비가역(.mcp.json 0624→0626 repoint, 0624 아카이브)은 **CODEX 검토 + 운영자 go 후**.
- 롤백 안전망: G:\corpus_20260624(보존), D:\corpus_md_export_20260618(아카이브).

## 6. CODEX에게 묻는 것
1. B1/B2 수정안 타당? 재인덱스 시 variable 정합 외 다른 스키마 드리프트 우려?
2. orphan 8편(특히 책챕터 Farmer/Porcelli) — 정본화 때 의도적 제외인가 사고인가? 0612서 본문 보충할지 / drop할지?
3. orphan 5편(표기차) — `__2` 중복과 함께 dedup 라운드에서 한 번에 정리할지?
4. 0624 아카이브 → 0626 flip 시점/조건.

산출물 경로: G:\corpus_20260626 / 빌드 리포트 detangle/sidecar_test_sonnet/BUILD_0626_REPORT.json / 빌드 스크립트 build_0626.py
