# HANDOFF — 새 DRIVER 세션 (figure per-paper fill + 잔여작업)

> 🔴🔴 **CRITICAL CORRECTION (a745303e, 2026-06-16 10:30, 소진적 read-only recon 후).**
> **1순위(pilot 기반 per-paper 추출)는 실행하지 마라 — 데이터로 반증됨. 실행 시 corpus 오염.**
> 증거:
> 1. `datalab\pilot`의 bare `<hash>_img.jpg`는 **고유 식별자 아님**. 예: `55d2bfe1...img.jpg` 하나를 **854개 .md**가 참조하는데 alt-text는 전부 다른 figure(amphibole 분배계수 vs Nyiragongo 감람석…). flat이라 물리 파일 1개 → 853편 그림은 이미 붕괴/소실. pilot per-paper 소유권으로 **복원 불가**.
> 2. missing 604 중 **567(94%)**이 다수 논문 공유 hash(일부 596·838편). 유일소유 12, 그중 제목일치 2뿐.
> 3. **진짜 per-pid 소스 0/50**: 후보 전부 대조함 — quarantine `fig_refill_out_20260613\{out,out_raw}`(913·983 pid폴더), renewal `nuc/kim/cha_out`(216), 타 번들. missing 50 pid는 **어디에도 없음.**
> 4. 핸드오프가 추정한 `batch_staging_20260512`·`allegre_convert_staged`는 **존재하지 않음**. `_revalidate_reextract`=json만.
> **결론: 잔여 604그림/51편은 이 회사PC의 어떤 소스로도 안전 복구 불가.** 필요한 건 (a) 실제 datalab 머신의 per-paper 변환출력(여기 없음) 또는 (b) 원본 PDF 재변환(4편은 PDF조차 없음 = 영구공백). pilot에서 강제로 뽑지 말 것.
> → figure 트랙은 **source-level BLOCKED**. 새 driver는 figure 대신 아래 다른 잔여작업(PR화·B 대기·정규화기 PR)에 집중하고, figure는 운영자가 datalab 머신 원본을 마운트/제공할 때까지 보류. 상세 보고: `inbox_codex/021`.

너는 **driver**. 잔여작업을 끝까지 진행한다. baseline = ccc-protocol `detangle/inbox_codex/018_FIGURE_STATUS_CONFIRMED.md` 이후 상태. 오리지널 세션(manuscript-atelier)은 로컬상태만 확인하고 **같은 작업 중복실행 안 함**.

## 🔴 즉시 1순위 — 그림 per-paper(폴더별) 안전 추출. **백그라운드로 돌리고 나머지 작업 동시 진행.**
**문제(확정)**: `C:\Users\USER\datalab\pilot`은 flat — `<regionhash>_img.jpg`(pid 접두 없음) 3,059개가 한 폴더에. region-hash는 **layout 기반이라 논문 간 충돌**(잔여 604 중 477=79%가 다른 pid와 tail 충돌). 파일명 exact-match fill은 이미 실행됨 → **copied=0**(로그 `G:\corpus_md_export_20260612\FIGURES_FILL_RUN_20260616.log`). 강제 tail-매칭 = 남의 그림 박힘 = **절대 금지**(FIGURES_GAP 명시).

**해법(운영자 반복 지시) = 폴더별/논문별 격리 추출**:
- region-hash 파일명으로 매칭하지 말고, **각 논문 단위로 격리해서** 그 논문이 소유한 이미지만 그 논문 pid에 넣어라.
- datalab\pilot에 per-paper `<paper>.md`(3,339) + `<paper>.metadata.json`(3,339, page_stats) + `_manifest.jsonl`(paper_id↔source_pdf↔status) 있음. 각 paper.md가 자기 이미지(`![](<hash>_img.jpg)`)를 참조 → 그게 소유권.
- ⚠️ flat 디렉토리라 hash 파일명 자체가 충돌하면 물리적으로 1개 파일뿐일 수 있음 → **datalab 원본 변환출력(per-paper 폴더 구조)**을 먼저 확인하라. 후보: `C:\Users\USER\datalab\` 의 `_revalidate_reextract`·`batch_staging_20260512`·`allegre_convert_staged` 등 batch 폴더 안에 **논문별 하위폴더**가 있을 가능성. 거기서 폴더별로 뽑으면 hash 충돌 무관.
- paper → 번들 pid 매핑: manifest paper_id/source_pdf ↔ 번들 sidecar bibliographic/doi (번들 slug = md5(pid)[:12] 규칙도 참고).

**실행**: 신규 스크립트 = corpus-precision-critical → ① dry-run 먼저 보고 ② Codex 리뷰 ③ **샘플 시각검증**(채운 그림이 그 논문 거 맞는지 눈으로) ④ `python scripts\fig_render_audit.py` GATE PASS. additive·idempotent·비파괴. articles/는 NAS 번들(git 아님).
**범위**: 잔여 ~604 이미지 / 51편 (README 기준 163편/2,027). 영구공백 4편(Hart1984·Lenat2009·Seton2012·Sleep1996 = PDF 원본 없음)은 allowlist 유지(정상).
**참고**: 운영자 README = `G:\회사에서_그림채우기_README.md` (단 그 README의 exact-match 방식은 pilot 명명 때문에 0매칭 — per-paper 방식으로 대체).

## 현재 상태 (baseline after 018)
- ✅ **normalizer DONE**: VP-NORM-1 coverage **12.9→75.4%**, precision 99.2%(Codex 13라운드 감사). honest ceiling(싱글톤 꼬리라 90%는 force-match=오염). 상세 = `ccc-protocol/detangle/norm_artifacts/FINAL_SUMMARY.md`.
  - ⚠️ 코드 = `manuscript-atelier/tools/corpus-normalize/normalize_corpus.py`+`dryrun_coverage.py` — **UNCOMMITTED**(working tree + 채널 norm_artifacts 복사만). **PR화 필요.**
  - regression probe 20종 PASS. dry-run 타깃 = `G:\corpus_md_export_20260612\sidecars` (읽기전용).
- ⛔ **figures**: per-paper fill 미실행(위 1순위).
- ⏳ **PR#15/16**: Codex 통과(004/005/golden). 머지 대기. PR#16 id-스킴(SiO2 vs SiO2_wt_pct) 구현맞춤 정렬 필요.
- 🚪 **B(sidecar에 정규화 적용)**: 운영자 "박아" 대기. VP-NORM §5(백업→적용→검증→롤백). regression 20/20 통과상태.
- 🚪 **배포**: B후 (corpus_v20260612, 무파괴·롤백).

## 채널/규약 (불변)
- CCCP: ccc-protocol `coop/detangle-20260615`. Claude→Codex=`detangle/inbox_codex/NNN_*.md`, Codex→Claude=`detangle/inbox_claude/NNN_*.md`. 최신 발행=020. watcher 번호무관(미응답 최신 스캔), 3-quiet-wake ping. push 전 `git pull --rebase`.
- **corpus(논문본문·sidecar·index·wiki·그림) git push 절대 금지**(저작권). 채널엔 vocab/코드/aggregate-통계만.
- **B 게이트**: sidecar write = 운영자 전용. 그 전까지 비파괴·읽기전용.
- 예산 $666 캡. 5분 loop cadence.

## 오리지널 세션이 넘기는 로컬 산출물 (중복실행 말 것)
- manuscript-atelier 미커밋: `tools/corpus-normalize/`(정규화기 전체), `.scratch/`, 수정 `.mcp.json`·`docs/handoffs/CORPUS_POLICY.md`.
- ccc-protocol: clean(전부 커밋, 최신 18e226f).
- 그림 fill 1회 실행됨(copied=0). FIGURES_STILL_MISSING.json·FIGURES_MISSING_PDF_MEMO_20260616.md 존재.
