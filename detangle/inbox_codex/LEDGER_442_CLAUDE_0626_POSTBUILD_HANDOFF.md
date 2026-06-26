# LEDGER_442_CLAUDE_0626_POSTBUILD_HANDOFF

timestamp_kst: 2026-06-26
author: Claude (main session, 1M Opus)
recipient: Codex / operator
relay_safety: counts/status/paths/public_DOIs only; no manuscript prose, no resolved numeric values
purpose: 0626 빌드 후속(DOI 백필 + 논문_260624 대조) 보고 + 남은 실행·검증 전량 Codex 핸드오프
note: 운영자 지시 = 이후 실행/검증은 Codex가 (Claude 주간한도 ~98%). 아래 Claude 결과는 모두 **Codex 독립 cross-check 대상**.

## 1. DOI 백필 완료 (결정론적, 로컬 $0)
- 진단: 0626 sidecar 3996 중 doi 채워진 것 1914(47%)뿐. 본문 DOI 교차 → 빈 2082 중 846은 "본문엔 DOI 있는데 sidecar엔 없음"(Haiku 누락), 1237은 본문에도 DOI 없음(책/한국/구논문, 정상).
- 조치: `detangle/sidecar_test_sonnet/doi_backfill.py` — article 본문 상단(6000자) `doi.org/`·`doi:` 라벨 우선 regex → sidecar.doi 백필. reference DOI 오염 방지.
- 결과: **833편 채움, doi 47% → 68%**(2747/3996). 천장 = 본문무DOI 32%(원래 미보유).
- variables_reported(Gemma 인벤토리, sidecar 주력) = 3996/3996(100%), median 24/편 — 정상.
- 감사 산출물: `SIDECAR_DOI_AUDIT.json`.

## 2. 논문_260624 (D:\Academia\References\논문_260624, 91 PDF) corpus 대조
방법(파일명 fuzzy 금지): ① PDF fitz DOI → sidecar.doi ② 미스 → article 본문 DOI grep ③ 미스 → 제목/저자 토큰. 산출물 `REF260624_CHECK.json` / `_CHECK2.json` / `_FINAL.json`.
- 결과(Claude 3단): **91편 중 corpus有 90 / 진짜누락 1**.
- 진짜누락 1편: `김용하 외 (2021) JSTA, 우주과학자에게 필요한 달의 지형과 지질` (DOI 10.52912/jsta.2021.1.2.217, 한국 천문/달지질 — geochem corpus 범위 경계).
- 13 누락후보 중 12편은 DOI-only artifact(corpus에 다른표기로 존재: An2026/Cannao2020/Denny2024/Giuliani2025/Kim&Choi2025/Koh2007/Lockyer2024/Ray2013/Shin2017/Wenzel2021/Yadav2026/Yi2014).
- ★Codex 검증요청: 위 90/1을 독립 재확인(특히 토큰매칭 J<0.5 였던 Ray2013). References 다른 배치(차혜린 138 / 김민서 65 / 1.Common 683)도 같은 방식 대조할지 판단.

## 3. 재인덱스 — 스크립트 blocker는 닫힘(LEDGER_441), 실행만 남음
- B1/B2 패치 완료(Codex). 0626 실행본 `scripts/build_retrieval_units.py`(variables_reported 우선) + `run_dense.bat`(0618 하드코딩 제거).
- 미실행: retrieval_units(전체) → BM25 → BGE dense(GPU). 전제: G: 여유 6.3GB → 0624를 D:로 아카이브해 ~21.8GB 확보 필요(운영자 go 대기).
- ★전부 로컬(GPU/CPU, Claude 토큰 0) — Codex/로컬 스크립트로 실행.

## 4. 남은 큐 (Codex 실행/조율, 운영자 go 게이트 표시)
| # | 작업 | 주체 | 게이트 |
|---|---|---|---|
| A | 0624 → D: 아카이브 (공간 21.8GB 확보) | 로컬 | **운영자 go (비가역)** |
| B | 재인덱스 retrieval_units→BM25→BGE | 로컬 GPU | A 후 |
| C | `.mcp.json` 0624→0626 repoint | 로컬 | B 후 운영자 go |
| D | 논문_260624 누락 1편 처리 (범위 판단) | Codex 판단 | - |
| E | orphan 13 (8 정본없음 + 5 표기차매핑·`__2`중복 dedup) | Codex | - |
| F | References 타 배치(차혜린/김민서/Common) 대조 여부 | Codex 판단 | - |

## 5. 산출물/경로
- 빌드: G:\corpus_20260626 (CORPUS_VERSION 2026-06-26, doi 68%, variables 100%)
- 스크립트/리포트: detangle/sidecar_test_sonnet/ (build_0626.py, doi_backfill.py, ref260624_check*.py, *_AUDIT/_FINAL.json, BUILD_0626_REPORT.json)
- 롤백 안전망: G:\corpus_20260624(보존), D:\corpus_md_export_20260618(아카이브)
