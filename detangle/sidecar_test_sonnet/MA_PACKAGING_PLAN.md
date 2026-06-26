# MA 패키징 추출목록 (corpus-build 파이프라인 → manuscript-atelier)
작성: 메인세션, 2026-06-25. 목적: "누구나 자기 PDF로 자기 corpus 빌드"하는 재사용 파이프라인을 MA harness에 모듈화. **시행착오는 운영자 하나로 끝, 교훈 박제.**
⚠️ 실행 전제: (a) 논문 corpus 런 final(오늘 저녁) (b) 운영자 확인. 지금은 **계획만**(아무것도 안 옮김/커밋 안 함).

## 타깃 구조: `manuscript-atelier/tools/corpus-build/`
```
corpus-build/
  config.example.yaml        # corpus_root, paths, model(gemma4:12b), num_ctx/predict, datalab key path
  extract/   convert_pdfs.py            # PDF→MD (datalab, slug 그림격리 내장) — 이미 CLI ✅
  sidecar/   gemma_production.py        # 로컬 Gemma 인벤토리 (num_ctx 49152/16384 fix)
             check_complete.py          # 완료 게이트
             run_loop.(py|sh)           # loop_gemma_v2 일반화(미처리 0까지)
             prompts/ (geochem INSTR, geophys GEO_INSTR)
  book/      segment_dryrun.py          # 책 분절 v1 (heading h1/h2 + table_dense override)
             book_gemma_prompt / norm_vocab / holdout_gold / holdout_verify  (CODEX 산출)
  index/     build_retrieval_units.py / build_bm25_index.py / build_bge_m3_dense.py
  reader/    read_paper_ns.py           # namespace 그림격리 리더
  RUNBOOK.md # 엔드투엔드: PDFs → convert → sidecar(loop+gate) → index → reader
```

## 추출/일반화 목록
| 조각 | 소스 | 일반화 작업 |
|---|---|---|
| convert_pdfs.py | 20260612/scripts | ✅ 이미 argparse. 기본값만 config화 |
| gemma_production.py | sidecar_test_sonnet | 하드코딩 4(SF/ARTS/SIDE/STAGE) → **`--corpus-root`서 파생** + SF=`__file__`. num_ctx fix 기본값 |
| check_complete.py | sidecar_test_sonnet | 동일(같은 corpus-root) |
| loop_gemma_v2.bat | sidecar_test_sonnet | python경로+스크립트경로 param화(또는 .py 래퍼로) |
| segment_dryrun_v1_codex.py | sidecar_test_sonnet | `G:\books_v5_out` → `--books-root` |
| 책 sidecar configs | sidecar_test_sonnet | CODEX 산출(prompt/vocab/holdout/verifier) 번들 |
| build_*.py + read_paper_ns.py | corpus_20260624/scripts | 경로 하드코딩 점검(2위치 중복 dedupe) |

## 박제할 교훈 (defaults + RUNBOOK 경고)
1. **num_ctx 49152 / num_predict 16384** (입력+출력>32768 = 13% 잘림 → 0.27%로). 더 길면 청킹.
2. **그림 per-slug 폴더격리** (md5 pid, dict-unique = 권내/권간 충돌 불가).
3. **완료 게이트 루프**(미처리 0까지) + 실패분 staging 미기록=self-healing.
4. **분리/필터는 extraction_model(출처)로** — 스키마키만 보면 고품질 batch 섞임(Sonnet 52 사고).
5. **ollama 직렬, hard-kill 금지**(degrade→재부팅), think:false.
6. **값 추출 금지**(환각) — 인벤토리/locator만, 값은 use-time.
7. no_md(입력없는 sidecar) 게이트서 제외.

## 다음(실행 시)
런 final + 확인 후: corpus-build/ 골격 생성 → 스크립트 복사+일반화(corpus-root) → config.example + RUNBOOK → MA에 커밋(운영자 게이트). 스크래치(qa_*/test_*/assess_*)는 제외.
