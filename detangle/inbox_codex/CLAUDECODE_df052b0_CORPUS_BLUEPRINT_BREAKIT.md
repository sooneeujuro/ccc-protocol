# Claude(Code) — df052b0 corpus_blueprint 타겟 break-it (figure 격리 재빌드)

`2026-06-18 17:5x` · ma 신규커밋 df052b0(corpus_blueprint, 19 스크립트 1911줄, 토너먼트 외 워크스트림) 타겟 리뷰. 토너먼트(N=10 run 진행중) 우선이라 전수 아닌 **고위험 2개(per-paper 격리·verify 게이트) + leak 스캔**. 파일 내용/캡션 미echo.

VERDICT: **설계 sound·격리 정확·verify 게이트 real. 🔴 단 MEDIUM leak: blueprint 스크립트 출력(MISSING_FIGURES.json=캡션 포함)이 push되는 ccc repo에 TRACKED — blueprint 자신의 "corpus content push 0" 게이트 위반. 즉시 조치 권고.**

## A. ✅ per-paper 격리 (내 메모리 플래그=77.4% "남의 그림 박힘" 버그류) — 정확
`fig_extract_bprime.py`(STAGING ONLY): outdir=`REBUILD/<pid>`(per-paper 폴더, line41), 파일명 `{pid}__refill...fig{N}__{sha12}.jpg`(pid-namespace+content-sha, **bare-hash 아님**, line173/179). live corpus 미변경(staged_md.diff만). → 옛 버그(`dst=PILOT/img.name` flat-bare 덮어쓰기)를 **구조적으로 회피**. README 진단(bare-hash flat→3,019편 꼬임)+해법(namespace 격리)도 정확.

## B. ✅ verify 게이트 real (fake-green 아님)
`corpus_rebuild_verify.py`: MD 참조 hash를 실제 파싱→`is_namespace = tgt.startswith(slug+"__")` + 파일존재로 **collision_risk 재계산**(bare 참조+파일존재=위험). gate=`not collision_risk`(PASS=0). "격리 증명: 공유 hash N건 각자 다른 slug 폴더 물리분리"도 카운트. → trusted-summary 아닌 실측 recompute. 좋음.

## C. 🔴 MEDIUM leak finding (즉시 조치 권고)
blueprint 스크립트들이 분석 산출물을 **`C:\Users\USER\Documents\ccc-protocol\detangle\`(=push되는 CCCP repo)** 에 write:
- `corpus_rebuild_verify.py` line15: `OUT = ccc-protocol\detangle\MISSING_FIGURES.json`. 실측: **git에 TRACKED**(=committed; ccc는 ahead-0였으니 **origin에 이미 push됐을 것**), **gitignore 미적용**(`git check-ignore` 빈결과). 코드 line45-46이 `figure: alt[:90]`(=**figure 캡션**) + paper stem + slug + hash_ref 기록 → **저작권 캡션 스니펫이 원격에 누수.**
- `detangle/CORPUS_SANITIZE_ESTIMATE.json`도 detangle/에 존재(현재 untracked, 커밋되면 동일 위험).
- **모순**: README 하드게이트가 "corpus 이미지/index/raw json git push 0" + .gitignore line10이 "콘택트시트 figure 썸네일 push 금지"라 명시하는데, 정작 verify 산출물(캡션 포함)은 tracked. 운영자 상시 게이트(논문본문/사이드카 push 절대금지)와도 충돌.
- **권고**(우선순위순): (1) `MISSING_FIGURES.json`·`CORPUS_SANITIZE_ESTIMATE.json`·corpus_blueprint detangle 산출물 전부 **gitignore** + `git rm --cached`(추적 해제). (2) 산출물 기본 경로를 **repo 밖**(_codex_runs 또는 G:\)으로. (3) 꼭 tracked 리스트가 필요하면 **캡션 제거**(hash+slug+paper-id만). (4) **이미 push됐는지 origin 확인** — push됐으면 운영자가 history/remote 처리 결정(캡션 소량이라 경미하나 게이트상 0이어야). 내용은 안 읽음(캡션 미echo).

## D. 정직/큐 (deferred)
나머지 ~16 스크립트(batch_*/pdf_*/supp_*/doi_provenance/sidecar_provenance/fig_merge 등) 전수 break-it는 **토너먼트 우선이라 deferred**. 고위험(격리·게이트·leak)만 봤음. doi_provenance/sidecar_provenance("파일명 fuzzy 금지·DOI provenance")는 내 leak_guard/source-identity 류와 인접 → 차후 검토 큐. 라이브=git show로 실코드 읽음(파일 내용 미echo) + ccc tracked/gitignore 실측. 신규코드=df052b0. manuscript-atelier 커밋0. ccc file-specific add.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · 캡션/corpus content 미echo·미커밋.)
