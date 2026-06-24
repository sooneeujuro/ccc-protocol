# 새 논문 추가 — subagent 배치 추출 설계 (회사PC 실행용, 풀 컨텍스트 핸드오프)

작성: 노트북(`soone`) Claude → 회사PC Claude. **회사PC엔 이 대화 컨텍스트가 없으므로 이 문서는 자기완결.**
계기: 운영자가 "논문 추가하려는데, subagent 호출로 배치 몇 개 만들어 Sonnet/Opus를 plan 한도 내에서 돌리면 이득 있나? Opus는?" 질문. 아래가 그 답 + 실행안.

---

## 0. TL;DR (결론)
- **새 논문 추가 = subagent 추출이 명백히 이득.** plan(Max 구독) 한도 안이라 소량은 marginal $ ≈ 0, 기존 Haiku 베이스라인보다 품질↑, **추출+measured/cited 검증을 한 번에** 박아 "출생부터 verified" sidecar 생성.
- **모델 = Sonnet 4.6 디폴트. Opus는 비권**(선별 에스컬레이션만): measured-vs-cited 품질은 Sonnet과 동급, 장문완결성은 모델이 아니라 파이프라인 문제, Opus는 ~1.7x quota/시간.
- **전수 4k 재추출이면 반대로 API batch가 나음**(plan 인터랙티브 quota를 안 태움). 새 *추가*는 subagent, 전수 *재추출*은 API batch — 작업 종류로 갈림.

---

## 1. 비용 재구성 (핵심 통찰)
- 2026-06-15에 나온 "$755"는 **batch API(토큰 과금)** 기준이었음. 모델별 전수 견적: **Sonnet 4.6 $755 / Haiku $648 / 의심 503편만 $96**(batch -50% 반영).
- **subagent로 돌리면 Max plan 한도(구독) 안 → marginal $ ≈ 0.** 비용 장벽 소멸. 진짜 제약은 **plan usage cap(5h/주간 한도) + wall-clock + 추출 품질**로 이동.
- **결정 규칙**:
  | 작업 | 권장 경로 | 이유 |
  |---|---|---|
  | 새 논문 *추가* (수십~수백) | **subagent 배치** | plan 한도 내 ≈무료, 검증 내장, 품질↑ |
  | 전수 *재추출* (수천) | **API batch** | plan quota 보호, -50% batch, 대량 스케일 |
  | 의심분만 (503편) | API batch $96 or subagent | 규모 보고 택 |

## 2. 모델 선택 — Sonnet 디폴트, Opus 비권
2026-06-15 모델 비교 결과 그대로:
- 기존 sidecar = **87% Haiku-4.5** 추출. 약점: 인용 vs 측정 구분 / classification / 장문 조기종료.
- **measured-vs-cited: Opus 4.8 ≈ Sonnet 4.6 동급**(Opus가 더 안 나아짐).
- **장문 완결성(refs/figures 빈칸) = 모델이 아니라 파이프라인(출력예산·청킹) 문제** → Opus로도 안 고쳐짐. ★진짜 품질 레버는 모델이 아니라 파이프라인.
- Opus = ~1.7x 토큰/시간 → plan 한도 더 빨리 깎고 느림.
- **→ 디폴트 Sonnet 4.6. Opus는 Sonnet이 confidence=low/불완전 플래그한 소수만 선별 에스컬레이션.** 블랭킷 Opus 손해.

## 3. 파이프라인 (출생부터 verified)
```
새 PDF
  └─(A) datalab 변환 → MD          [기존 스크립트 패턴, 회사PC가 datalab 키로 실행]
       └─(B) subagent: full MD 읽고
             ├ sidecar JSON 추출 (스키마 강제)
             └ measured|cited|modeled 판정(증거 인용구) = PR#15 lazy-verification 출생적용
                  └─(C) 스키마/시각 QA → low-confidence면 Opus 재시도
                       └─(D) 적재 (sidecars + verifications)
```
- 새 논문은 기존 4k Haiku sidecar보다 나은 품질로, **검증층 포함된 채** 들어감.
- (A) datalab과 (B) 추출 분리: (A)는 HTTP/스크립트(키 필요), (B)는 LLM fan-out. subagent가 Bash로 (A)도 할 수 있으나, 대량은 (A) 일괄변환 후 (B) fan-out이 깔끔.

## 4. 워크플로 스크립트 스케치 (회사PC가 거의 그대로 실행)
```js
export const meta = {
  name: 'ingest-new-papers',
  description: 'Extract sidecars for newly-added papers — Sonnet default, Opus escalation, verified-from-birth',
  phases: [{title:'Extract'},{title:'Escalate'},{title:'QA'}],
}
// args = [{paper_id, md_path}]  (datalab 변환 끝난 MD 경로들)
const papers = args
const out = await pipeline(papers,
  // 1) Sonnet 추출 + measured/cited 검증 동시 (스키마 강제)
  (p) => agent(EXTRACT_AND_VERIFY_PROMPT(p), {
           label:`extract:${p.paper_id}`, phase:'Extract',
           schema: SIDECAR_V21_PLUS_VERIFICATIONS, model:'sonnet' }),
  // 2) Sonnet이 low-confidence/불완전 플래그 → 그 논문만 Opus 재추출
  (sc, p) => (sc && (sc._extract_confidence==='low' || sc._incomplete))
        ? agent(EXTRACT_AND_VERIFY_PROMPT(p), {label:`opus:${p.paper_id}`, phase:'Escalate',
                schema: SIDECAR_V21_PLUS_VERIFICATIONS, model:'opus'})
        : sc,
  // 3) 스키마/필수필드 QA (결측 0치환 금지 — null 유지)
  (sc, p) => agent(QA_PROMPT(sc, p), {label:`qa:${p.paper_id}`, phase:'QA', schema: QA_VERDICT})
)
return out.filter(Boolean)
```
- 동시성 자동 cap(~min(16, cores-2)). 스키마 강제라 형식오류 0. 검증 내장.
- 적재(D)는 워크플로 밖에서 운영자/회사PC 확인 후(라이브 sidecar 쓰기 = 게이트).

## 5. 재사용할 기존 자산 (재발명 금지)
- **datalab 변환 패턴**: `manuscript-atelier` repo `docs/handoffs/autonomous_run_20260614/work/a2_convert_german.py` — `requests` + `X-API-Key`(키=`C:\Users\soone\artelier_private\datalab_key.txt`) + `https://www.datalab.to/api/v1/convert`, `output_format=markdown, mode=accurate`, `request_check_url` 폴링. (urllib는 403 — 반드시 `requests`.)
- **PDF 소스**: NAS `\\100.108.229.47\manuscript_atelier\corpus_v20260519\source_pdfs\<slug>.pdf` (slug = md5(paper_id)[:12]). 신규 PDF는 RefDB(`\\100.108.229.47\RefDB`)에서 가져온 것일 수 있음.
- **추출 코드/스키마**: `tools/paper-orchestra/claim-extractor/v0/extractor.py` + `cli.py` + README. sidecar는 **v2.1**(extraction_meta.extraction_model 포함). 기존 추출 프롬프트는 회사PC `coop/scratch`에 있던 것 재사용 가능(단 lazy-verification은 그 의존 끊는 방향 — 새 판정 프롬프트 1급 부수임무로).
- **검증 스키마/정책**: `corpus_verification_policy_v0.md` (ma **PR #15**) — `verifications_v0.1`(variable_id+raw_label_snapshot+confidence+evidence_loc+sidecar_sha1) + measured/cited/modeled 정의 + (A)corpus-provenance 허용 / (B)student-claim 금지 구분.
- **figure refill 패턴**(병렬 러너 참고): `docs/handoffs/fig_refill_20260613/refill_runner.py`.

## 6. quota 주의 (subagent의 진짜 비용)
- subagent는 **네 Max 인터랙티브 quota**를 먹음 → 소량(추가)엔 OK, **대량이면 5h/주간 usage cap에 걸려 throttle**. 그 경우 API batch로 전환(돈은 들지만 plan을 안 막음).
- 즉 "공짜"는 *소량 한정*. 규모 크면 API batch가 실질 우위.

## 7. 권고: 파일럿부터
- **새 논문 5~10편으로 파일럿** subagent 배치 → 품질·속도·quota 소모 체감 → 좋으면 풀가동.
- 파일럿 산출 sidecar는 staging에만(라이브 적재 = 게이트).

## 8. 운영자/회사PC 게이트
- 라이브 sidecar 쓰기·적재 = 게이트(결측 0치환 금지, null 유지).
- 추가할 논문 목록/규모 미정 → 운영자가 PDF/목록 주면 (A)변환부터.
- Jackson 2017 Caroline 등 RefDB 사냥 결과(`reports/PDF_HUNT_REFDB_RESULT_20260616.md`)와 연계 가능(그 36편도 신규 추출 대상이면 같은 파이프라인).

— 노트북 Claude. 질문/수정은 보드로.
