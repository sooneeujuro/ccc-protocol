# HANDOFF — figure Datalab 재추출 진행중 (2026-06-16 ~16:3x)

새 세션용. 이전 세션(a745303e)이 Bash 호출 형식 반복오류로 교체. 상태 그대로 이어가면 됨.

## 한 줄
51편 그림 빠진 논문 → Datalab로 재추출 중. 40편은 기존 marker 출력으로 해시매칭(582/604), **10편(미매칭)은 convert_pdfs.py(accurate+use_llm)로 방금 재변환 완료($1.46)**. 남은 건 시각검증 + 머지(corpus 실제 쓰기, 운영자 OK 후).

## 지금까지 (전부 staging, live corpus 0 수정)
- 그림 빠진 51편(604 placeholder) 확정. placeholder = `<slug>__<hash>_img.jpg`, slug=md5(pid)[:12].
- **40편**: `G:\datalab_runs_v20260616\derived\<pid>\images\` 에 `<hash>_img.jpg`. placeholder의 `<slug>` 접두만 붙이면 매칭(582/604 해시일치 확인). 채우기 = `<hash>` → `<slug>__<hash>`로 articles에 복사.
- **10편(미매칭)**: `G:\fig_refix_out\<slug>\` 에 새 MD + `<slug>__<hash>_img.jpg`. convert_pdfs.py(mode=accurate, use_llm=on)로 변환. 10/10 done, 188 img, $1.46.
  - pid: 7ca89945(Xu2024) 3e7dab39(Yi2021) d54aa1e7(Halldorsson2016) ff724e5a(Sakuyama2014) 005dbe86(Sawai2025) 7f31390a(Sorbadere2012) 4a33304a(Goldtz2024) f2936ef7(Cawood2005) 029f6413(Tian2016) 49aa4245(Forster2019)

## ⚠️ 발견: ResearchGate cruft
일부 PDF가 ResearchGate 다운로드라 1페이지에 **저자 프로필 사진·아바타·아이콘**이 박혀있고 Datalab이 그것도 그림으로 추출(MD가 참조함). Sakuyama 예: 26 img 중 67x60 등 초소형 4개 = 아이콘. → **머지 전 필터 필요**: 초소형(<100px) + 페이지1 RG헤더 이미지 드롭 + 그 MD ref도 제거. (또는 운영자가 negligible로 판단하면 그대로.)

## 다음 단계 (순서)
1. **10편 시각검증**: 각 `fig_refix_out\<slug>\` 이미지 contact sheet 렌더 → 운영자에 표시. RG cruft 필터 여부 결정.
2. **머지 (운영자 OK 후 = live 쓰기)**:
   - 10편: convert_pdfs 출력이 정답(MD+이미지 한 쌍). corpus `articles\<원래md파일>` 내용을 새 MD로 교체 + `<slug>__<hash>_img.jpg` 이미지를 articles에 복사. **MD와 이미지 둘 다 같이** (한쪽만 하면 또 빈칸).
   - 40편: `derived\<pid>\images\<hash>` → `articles\<slug>__<hash>` 복사(MD는 기존 유지, placeholder가 이미 맞음).
   - 단 convert_pdfs slug == 기존 corpus pid 확인됨(폴더명이 corpus pid와 일치) → 이미지 접두 그대로 맞음.
3. **재색인**: `build_retrieval_units --all` + `build_bm25_index --build` (10편 MD 교체했으므로).
4. **검증**: `fig_render_audit.py` GATE PASS + allowlist 604→실제잔여 재생성(백업).

## 도구/경로
- convert_pdfs.py: `C:\Users\USER\corpus_md_export_20260612\scripts\convert_pdfs.py` (`--in <pdf폴더> --out <out> --key C:\Users\USER\datalab_key.txt`, mode=accurate/use_llm 기본).
- 키: `C:\Users\USER\datalab_key.txt`.
- 10편 PDF: `G:\fig_refix_in\`. 51편 jobs+PDF매칭: `G:\datalab_runs_v20260616\jobs.csv`.
- cost-safe 하네스(참고): `detangle\scripts\datalab_harness.py` (raw 존재시 재호출 안 함).

## 하드게이트 (불변)
- corpus(논문본문·sidecar·index·그림·raw json) **git push 절대 금지**. 채널엔 aggregate/코드만.
- 유료 Datalab 재호출 = raw 있으면 금지(이중결제). promote/머지 = 운영자 OK 후.
- 비파괴. geochemistry-analyzer 무관(corpus 쪽).

## 협업
- CCCP: branch `coop/detangle-20260615`. Codex 검증중(inbox_codex/inbox_claude NNN). 최신 발행 032대.
- 메모리: toolcall-format(호출형식!), address-preference("너"), figure-refill-source-blocked.
