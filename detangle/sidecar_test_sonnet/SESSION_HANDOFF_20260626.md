# 세션 핸드오프 2026-06-26 (압축 직전) — 필독

이번 세션 두 트랙 완료. 압축 후 이 문서 + REEXTRACT_PLAN_HANDOFF.md로 이어감.

## 트랙 A: 메인 corpus 사이드카 재추출 — ✅ 완료
- **문제**(어제): 밤샘 Gemma 런이 옛 0612 입력 + **청킹 없이** 돌아 962/2161편 95000자 컷으로 잘림. 운영자가 잡음(메모리에 truncation 거부 기록 있었는데 위반).
- **수정**: 청킹 구현(`gemma_production.py`의 `extract_chunked`, 긴 MD 분할+머지), 입력→0624 정본, parallel-2, 버그픽스(JSON raw_decode, str-guard). num_ctx 49152/16384.
- **런**: `loop_gemma_v2.bat` 완료 → **canonical staging 3899편** = reuse 1199(안잘린 done) + fresh 2700(청킹) + 116(canonical-only). 진짜실패 0. QC 클린(변수 median 24, 긴논문 median 44, enum 0, 빈변수 0).
- **116 canonical-only**(0624 article인데 Haiku 사이드카 없던 것): Workflow subagent(`wf_haiku116.js`)로 Haiku verbatim → Gemma → canonical staging 합류.
- **49 no_md** = 검증완료 양성(레거시 중복 사이드카 + 책챕터 + 잡파일; 본문 DOI/제목으로 다 covered or reference-only 확인). 진짜 누락 0.
- **26 __N 중복 그룹**(53파일) = 같은논문 near-dup **article 파일** 복사본(0624에 중복 존재, DOI/제목 검증). dedup 제안=`DEDUP_PROPOSAL.json`: 그룹당 most-complete keep / Chen 본문+SI 둘다 / Kim·Elderfield·Epstein 불확실→둘다. **article-level이라 canon(Codex)서 실행.**
- 출력: `C:\Users\USER\corpus_md_export_20260612\sidecars_v22_canonical` (3899)
- 격리(옛 오염분): `...\sidecars_v22_QUARANTINE_oldinput_20260625`

## 트랙 B: helium staging refs → corpus 추가 — ✅ 완료
- _inbox PDF 19편(이미 corpus에 있는 3편 제외: Ballentine *Production*/Solomon1996/Kim Latent; APM-REP 3개+readme 제외). Ballentine *Tracing*은 다른논문이라 포함.
- datalab 추출(`datalab_harness.py --jobs jobs_helium.csv --all`, accurate+LLM) → `G:\datalab_runs_v20260616\derived\<pid>\markdown.md`
- Haiku-API verbatim(`haiku_api_sidecar.py`, claude-haiku-4-5, **콘솔 prepaid**, raw requests로 api.anthropic.com 명시=게이트웨이 우회) → `sidecars_haiku` (19)
- Gemma 인벤토리(`gemma_production.py` + GEMMA_SIDE/ARTS/STAGE env) → `sidecars_final` (19). QC 클린(변수 median 25, 빈 0, enum 0).
- 출력: `G:\corpus_helium_add_20260626\{articles, sidecars_haiku, sidecars_final}`
- 비용 ~$3.7 (datalab $2.7 + Haiku $1 콘솔 prepaid)

## 남은 큐 (운영자가 순서 결정)
1. **정본 승격**: canonical staging 3899 + helium 19 → 0624 정본 사이드카 위치로. **리더(`read_paper_ns.py`)/`.mcp.json` 기대경로 확인 먼저.** 정본 수정이라 운영자 go.
2. **인덱스 BM25+BGE**: 승격분 전부(helium 자연포함). 이전 미인덱스 44편. (VOYAGE_API_KEY env에 있음 — 임베딩용?)
3. __N dedup (canon/Codex, DEDUP_PROPOSAL.json)
4. 52 Sonnet 독립병합 (`corpus_md_export_20260612\sonnet52_independent`)
5. 책 파이프라인 (stitch+sidecar+index, GPU 논문 뒤, BOOK_SIDECAR_PLAN.md, G:\books_v5_out)

## 키/인프라/경로
- **ANTHROPIC_API_KEY**: Windows **User env(registry)**에 있음(len 108), 단 이 세션 프로세스 env엔 없음(setx가 세션 시작 후라). 주입: PowerShell `$env:ANTHROPIC_API_KEY = [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','User')`. **raw requests로 https://api.anthropic.com 명시**(ANTHROPIC_BASE_URL 게이트웨이 우회 → 콘솔 prepaid 차감). model `claude-haiku-4-5`, header x-api-key + anthropic-version:2023-06-01.
- **DATALAB_API_KEY**: 프로세스 env에 있음. `datalab_harness.py`(cost-safe idempotent, raw 있으면 재과금X).
- **ollama**: 꺼져있었음 → `Start-Process "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" serve -WindowStyle Hidden`로 살림(fresh start 됨, 재부팅 불필요). gemma4:12b. **hard-kill 금지**.
- gemma_production.py env override: `GEMMA_SIDE`(base sidecar), `GEMMA_ARTS`(MD), `GEMMA_STAGE`(출력). default=0624정본+0612fb / canonical staging.

## 교훈(반복 함정)
- **cp949 stdout 크래시**(유니코드 print) → Windows python 런에 `PYTHONUTF8=1`.
- **trailing-space pid**(Ballentine "...Crust ") → Windows 폴더명 sanitize → `rstrip(" .")` 매칭.
- **no-reactive-alarm**: 경보숫자(누락/중복) 즉답 금지, 측정법(DOI/본문, 파일명 아님) 먼저 검증. 이 세션 거짓경보 6회.
- **follow-settled-decisions**: 사이드카=Gemma 인벤토리+Haiku verbatim **머지**(순수Gemma 아님). 정해진 설계 재론 금지.
- **accuracy**: 알려진 필수수정(청킹)을 전수런 전에 넣기. ollama start≠hard-kill.
