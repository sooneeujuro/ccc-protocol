# Sidecar v2.2 + Corpus 20260624 — 마스터 플랜 / 상태 보존 문서

> **목적**: 4000편 코퍼스 작업 중 길 잃지 않기 + 버전 추적. 이 문서가 단일 진실원천(SSOT).
> 최종 갱신: 2026-06-24. 작업 폴더: `C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\`

## 0. 한 줄 목표
Haiku sidecar(전부 measured로 표기 → 46% 비측정인데 측정으로 오기)를 **v2.2(provenance: measured/cited/modeled + made_new_measurements + 분류교정)**로 업그레이드해서, 코퍼스에 **신뢰 가능한 구조 필터 레이어**를 만들고, 모든 자산을 자족형 **corpus_20260624** 한 폴더로 통합.

## 1. 핵심 결정 (날짜순)
- **Batch API $755 폐기** — 운영자 extra-usage/credits 영구 OFF → API 청구 불가. 모든 추출은 **Max 구독 내 Sonnet subagent** 또는 **로컬 Gemma($0)**.
- **v2.2 설계 = 타깃필드 재추출+머지**: Haiku의 양호한 verbatim 필드(abstract_raw, conclusions_raw, references, figure_summaries, page_anchors, geography, labs) **유지**. **재추출**: `classification.type` + `variables_measured`(+provenance+evidence) + `made_new_measurements`. instruments는 **$0 빈도승급+remap**(재추출 X).
- **Sonnet chunk0(400편) 완료 = 답안지**. 검증 86% 교정, QC clean. staging에 보존.
- **로컬 Gemma 4 12B = $0 대안**. 4편 테스트서 핵심판단(provenance/made_new) 우수, 약점(완전성·분류1건·라벨LaTeX) 튜닝 중.
- **corpus_20260624 = MOVE 통합**(G:), **C: 백업 복사**. sidecar는 Gemma 추출 후 포함.

## 2. 현재 상태 (2026-06-24)
- ✅ Sonnet chunk0 400편 → `G:\corpus_md_export_20260612\sidecars_v22_staging\` (답안지)
- ✅ Gemma 설치확인 `gemma4:12b` (Ollama :11434)
- ✅ Gemma 1차 테스트 4편 통과(품질 쓸만)
- ⏳ **진행 중**: Gemma 프롬프트 튜닝 (vs Sonnet 답안지)
- ⬜ Gemma 전수 추출 (~3948편, $0, ~2-3일 로컬)
- ⬜ corpus_20260624 폴더 통합 + C: 백업
- ⬜ index(BM25+BGE) 재구축 (sidecar 포함, 전 3978)
- ⬜ .mcp.json repoint 20260618→20260624 (+타머신)

## 3. 실행 순서 (차근차근)
1. **Gemma 프롬프트 튜닝** — Sonnet chunk0 답안지로 분류/made_new/provenance 일치율 측정 → 프롬프트 보완 반복. (완전성·분류·라벨 갭 닫기)
2. **이 문서 유지** (단계마다 §2 체크박스 갱신)
3. **Gemma 전수 추출** → v2.2 sidecar 전부 (staging 또는 별도 out 폴더). 로컬 $0, 무쿼터, idempotent skip.
4. **corpus_20260624 통합** (index와 독립, 언제든 가능):
   - `G:\corpus_md_export_20260618` → rename `G:\corpus_20260624`
   - `G:\corpus_pdfs_bundle` → MOVE `corpus_20260624\pdfs\`
   - `G:\corpus_supplementary_bundle` → MOVE `corpus_20260624\supplementary\`
   - 완성본 → **C: 백업** `C:\corpus_20260624_backup\`
5. **index 재구축** — BM25 + BGE-M3 dense, 전 3978 + v2.2 sidecar 메타. `index_new\`에 짓고 검증 후 스왑.
6. **.mcp.json repoint** 18→24 (회사PC; 타머신은 각자 경로)

## 4. 자산/경로
| 항목 | 경로 |
|---|---|
| Sonnet 답안지(400) | `G:\corpus_md_export_20260612\sidecars_v22_staging\` |
| 원본 Haiku sidecar(3948) | `C:\Users\USER\corpus_md_export_20260612\sidecars\` (무손상) |
| MD 원문(추출 입력) | `C:\Users\USER\corpus_md_export_20260612\articles\` |
| 현 정본(통합 대상) | `G:\corpus_md_export_20260618\` (3977 폴더+articles+index+scripts) |
| 진짜 extractor(참조) | `...geochem-corpus-v2\...\extract_metadata_batch_v2.py` (Haiku, enum 95/239, 프롬프트 460-554) |
| 스크립트 | 이 폴더: prod_gen_chunk.py / prod_merge_chunk.py / compare_old_vs_new.py / gemma_test.py / gemma_tune.py / hallucination_gate.py / tims_retrieval_test.py |

## 5. 핵심 스키마 사실 (틀리면 안 됨)
- classification enum: **gas / petrology / both / other** (extract_metadata_batch_v2.py:196). 리뷰/이론/컴파일/방법론 = other.
- instrument enum 22종: irms,sims,qms,gc,icp_ms,noble_gas_ms,ic,xrd,epma,laser_ablation,crds,ftir,inaa,sem,software,aas,xrf,icp_aes,icp_oes,ams,raman,other. **TIMS→other (의도된 설계, tims 카테고리 없음)**.
- v2.2 변수: {id, raw_label, unit, phase, **provenance(measured/cited/modeled), evidence**}.
- provenance 규칙: measured=이 논문이 신규 측정 / cited=타출처 인용·컴파일 / modeled=계산·열역학·thermometer·norm·보정. 애매하면 measured 아님.

## 6. 비용/페이싱 사실
- Sonnet subagent: chunk(400)당 ~22.7M tok, Sonnet 주간 ~9%, 5h창의 ~50%(=2청크/5h창). 현금 $0. 전수≈Sonnet주간 90%.
- 로컬 Gemma: ~50초/편 × 3948 ≈ 2-3일 무인. 현금 $0, **쿼터 0**(최선).
- **auto-wake 금지** (쿼터 위생).

## 7. Gemma 튜닝 프로토콜 (자동 루프, $0 로컬)
**루프**: baseline run → 알림 → 실패분석+프롬프트보완 → 재실행 → 반복. 완료알림이 트리거(auto-wake 불요).
**타깃**: provenance 일치 ~85%(100% 금지=Sonnet 오류 모방=과적합) / 비측정서브셋 ≥80% / made_new ≥90% / 완전성 80–120% 밴드 / classification ≥80% / LaTeX라벨 0.
**과적합 방지**: ① dev 12편(실패 들여다봄)+holdout 25편 disjoint(점수만)—프롬프트 변경은 holdout 오를 때만 채택. ② over-agreement 경계(Sonnet도 정답 아님). ③ plateau시 불일치 샘플 본문 수동판정—남은게 진짜 모호함이면 정지.
**정지**: 타깃충족 OR holdout <2pp 2회연속 OR 6회 상한.
**기록**: 매 회차 프롬프트버전+holdout지표를 GEMMA_TUNE_LOG에 누적.

## 8. 피벗 (2026-06-24 저녁) — provenance 분리 + 인벤토리 모드
**결정**: Gemma는 measured/cited/modeled **판단을 못 함**(4회 튜닝+본문판정 확인, ~50% 천장). → **provenance는 use-time 본문읽기로 분리**, sidecar는 **"데이터 인벤토리"(뭐가 있나)** 만 정확히 보유.
- **필드 rename**: `variables_measured` → **`variables_reported`** (측정+인용+모델 포함 = 정직). 영향 코드 ~10개(build_retrieval_units.py:516 variable_aliases 포함) + 3948 sidecar 마이그레이션. 쓰는 사람 없어 cross-track 안전. **production이 새 키로 씀 → 마이그레이션 거의 자동.**
- **Gemma production 스키마** = classification_type + made_new_measurements + variables_reported{raw_label,id,unit,phase}. (instruments/geo는 Haiku 것 유지, instrument category는 $0 remap.)
- **매처 교훈**: 인벤토리 confirm서 recall 67%로 낮게 나왔으나, gemma_peek으로 **matcher 버그(Gemma ASCII 'delta13C' vs Sonnet unicode 'δ¹³C' 미매칭)** 확인 — 실제 Gemma 인벤토리는 **완전+더 granular**. 매처에 δ/Δ/delta→d, 위·아래첨자→ascii 추가(_canon). 출력 GEMMA_INV_OUTPUTS.json 저장(재측정 시 Gemma 재호출 불요).
- **production**: gemma_production.py (idempotent, ThreadPool 동시요청=Ollama 병렬, 머지→staging v2.2). 편당 ~88초 → 4000 직렬 ~4일/병렬2 ~2일. Sonnet 400(provenance有)은 skip(프리미엄 서브셋 유지).
- **sidecar↔index**: 본문 임베딩(BM25/BGE)=MD에서(sidecar 무관). sidecar→retrieval_papers.json 메타+변수별칭+제목청크. ⇒ sidecar 바뀌면 본문검색 영향0, 변수/메타 필터는 reindex 필요.
- **남은 시퀀스**: ①인벤토리 재측정 확인(bngc0t95g) → ②gemma_production 전수 launch → ③`variables_reported` rename(코드10+Sonnet400 마이그레이션) → ④corpus_20260624 통합(MD+pdf+supp, C:백업) → ⑤index 재구축(전3978) → ⑥.mcp.json repoint.

## 9. 생산 가동 상태 (2026-06-24 밤)
- **LAUNCHED**: `gemma_production.py 1` (직렬). WMI Win32_Process.Create로 `prod_run.bat` 띄움 → services 계열, **Claude 닫혀도 생존**(재부팅 시만 prod_run.bat 재실행, idempotent). 로그=prod.log/prod.err, 진행=PROD_PROGRESS.json(25편마다)+staging 파일수.
- **병렬 안 함(결정)**: 16GB에서 parallel-2 = ctx 32768×2 KV OOM → ctx 낮춰야 → 완전성↓ = 정확도 희생. "정확도 최우선"과 충돌이라 **직렬 ctx32768 고수**. setx OLLAMA_NUM_PARALLEL=1(미래 OOM 방지).
- **속도**: 첫 편들(변수 많은 논문) ~172초/편, ollama 100% GPU(오프로드 아님). 평균은 더 낮을 듯, 25편 체크포인트서 ETA 확정. 대략 ~4-7일, $0/쿼터0.
- **VRAM 메모**: corpus_mcp.py 2개 가동(20260618=PID31004, **20260602=stale 중복**) 각 ~10GB RAM+VRAM 일부. ollama가 이미 100%GPU라 죽여도 Gemma 속도엔 영향 적음. stale 20260602는 청소 후보(운영자 판단).
- **지구물리 라우팅 통합 완료(2026-06-24 밤)**: detector(geophys_detect.py, geo>=6&geo>chem)로 **579편 식별**(GEOPHYS_SUBSET.json). 전용 프롬프트(geophys_test.py 검증: Vp/Vs·velocity model·Moho/LAB·Mw·coseismic uplift 정확 추출 — geochem 프롬프트의 암석명 추출과 천양지차). **gemma_production.py에 라우팅**: pid∈GEOPHYS→GEO_INSTR, else INSTR. variables_reported에 kind필드(seismic_velocity/depth/source/geodetic…), 메타 prompt=geophys/geochem 기록. = 한 run에서 논문유형별 올바른 추출.

## 10. ⚠️ 재부팅 후 재개 (2026-06-25 새벽)
**사고**: parallel-2 실험 중 ollama 반복 hard-kill → GPU/CUDA degraded(짧은 프롬프트도 빈응답, CLI 재시작 무효) → **운영자 재부팅 예정.** corpus_20260624(22GB)+C:백업+staging(413편)+모든 스크립트 디스크 안전, 손실 0.
**재부팅 후 할 일 (운영자 "재개해" 하면):**
1. ollama 자동시작 확인 + **건강 테스트**(짧은 /api/chat+schema가 JSON 뱉나) — 정상이어야 production 재가동.
2. `OLLAMA_NUM_PARALLEL=1` 확인(parallel 절대 금지=throughput 죽음).
3. WMI로 prod_run.bat(=gemma_production.py 1) 재가동 → staging 413부터 idempotent 재개 → **직렬 ~4일 연속**(운영자 의도='지금부터 직렬 4일').
4. 긴논문 간헐 500 나면 → truncation 말고 **청킹** 붙이기(긴논문 분할추출+머지). 단 재부팅 후 500 사라질 수도(GPU 복구되면).
**별건**: 후배 공유 = corpus_20260624를 7-Zip 2GB볼륨+sha256로 압축(코어 9GB/5파트 추천 or 전체 22GB/11파트), 메일로 전송(클라우드/USB 막힘, 200km). ollama 무관, 언제든 가능.

## 11. 최종 운용 설정 (2026-06-25 새벽, 확정)
- **재부팅이 ollama 살림**(parallel 실험 GPU degrade 회수). gemma4:12b = **thinking 모델** — 작은 num_predict면 빈응답(고장아님). 추출엔 **think:false**(gemma_production.py + gemma_inventory.py에 박음). **검증: think:false가 thinking-on보다 holdout recall 85%>77%·prec 77%>73%, 5-10배 빠름.**
- **parallel-2 + think:false 채택**: 재부팅 clean VRAM에선 안정(GPU99%, VRAM 4GB여유, 풀ctx32768=정확도유지). ~1.4배(12-14초/편, 풀MD 프롬프트가 compute-bound라 2배는 아님). **OLLAMA_NUM_PARALLEL=2(setx됨) + prod_run2.bat(=gemma_production.py 2).**
- **현재 가동**: prod_run2.bat WMI, staging ~448/3948, **ETA ~14h**. 진행=PROD_PROGRESS.json/staging.
- **재부팅 후 재개**: OLLAMA_NUM_PARALLEL=2 확인 → ollama 건강체크(think:false 짧은 추출 JSON) → WMI prod_run2.bat → idempotent 이어감. (env 안 맞아 parallel=1돼도 작동, 그냥 느릴뿐.)
- **재개 명령**: `python gemma_production.py 1`(또는 prod_run.bat). 중단/재부팅 후 그냥 재실행=idempotent 이어감.
