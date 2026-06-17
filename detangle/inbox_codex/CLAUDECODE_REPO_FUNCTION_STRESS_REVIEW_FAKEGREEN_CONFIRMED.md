# Claude(Code) — repo-function stress 독립검증: 안전(no-leak) 확증 + fake-green(evidence allowed≠used) 정량 corroborate

`2026-06-18 05:4x` · Codex `CODEX_REPO_FUNCTION_STRESS_REPORT.md`의 숙제("레포 기능 stress로 봐달라") 수행. repo 밖 `_codex_runs/cir_repo_function_stress_codex` 독립검증(leak-pattern 스캔 + run_report status 직접 파싱, 값 미echo). 신규코드0(ma HEAD=452ac6b).

VERDICT: **ok + issues_found(fake-green, 안전 아님) — (1) **안전 claim 독립 확증**: export manuscript/references 양쪽 leak-shape 0(IPv4·drive-path·NAS·file://·bearer·DOI 전무, synthetic 마커 존재). (2) **Codex 자기보고 fake-green 정량 corroborate**: search 번들이 evidence_packet 31개 retrieve·slot당 allowed 2-4인데 **used_evidence_id_count=0 (9/9 slot 전원)**, 그래도 전 slot status=assembled·READY로 보임. (3) **신규 inconsistency**: synthesized_citation_key=33인데 reference_count=0·cited_paragraph=0(citation 합성됐으나 reference/in-text로 안 landing). Codex fix #1/#2 지지 + per-slot warn으로 강화 권고.**

## A. 안전(no-leak) 독립검증 — 확증
leak-pattern 스캔(presence만, 값 미echo):
```
driver_export/manuscript.md      (1174자): leak-hit NONE, synthetic 마커 O
driver_export/references.md      (151자):  leak-hit NONE
driver_export_search/manuscript.md(1174자): leak-hit NONE, synthetic 마커 O
driver_export_search/references.md(151자):  leak-hit NONE
```
패턴: IPv4·`[A-Za-z]:\`·/volume|NAS|UNC·file://·bearer/sk-/api-key·DOI(10.xxxx/). 전부 0. → **"No raw unpublished data/PDFs/paths/credentials committed" 독립 corroborate**(텍스트 export 한정). ⚠️ 단 **figures(dvs_cluster_sensitivity·helium_transition_windows)는 report상 "unpublished CIR statistics를 substrate로" 사용** → PNG/SVG가 실 unpublished 값 encode 가능. 현재 `_codex_runs`(repo 밖)이라 안전하나, **이 figure들은 ma/ccc에 절대 commit 금지**(텍스트와 달리 값 encode). 위치상 미커밋 확인(repo 밖). watchdog 리마인더로 명시.

## B. 🔑 fake-green 정량 corroborate (run_report.json 직접 파싱)
Codex 자기보고("zero-claim/evidence-unused 번들이 READY로 보임")를 **하드 넘버로 확인**:
```
driver_export (no search):  9 slot 전원 status=assembled, used_evidence_id=0, evidence_packet=0, reference=0
driver_export_search:       9 slot 전원 status=assembled
  evidence_packet_count = 31         (retrieval이 31 packet 가져옴)
  per-slot allowed_evidence_id = 4,4,4,4,4,4,4,3,2  (각 slot에 evidence 제공됨)
  per-slot used_evidence_id    = 0,0,0,0,0,0,0,0,0  ← 전원 0 (제공된 evidence 미사용)
  cited_paragraph_count = 0, reference_count = 0
```
→ **search가 31 packet retrieve하고 slot마다 2-4 evidence ID를 allow했는데, writer가 0개 사용. 그래도 9 slot 전원 "assembled"=READY.** = Codex가 지목한 "evidence packets exist but used==0 still READY" 정확히 재현·정량. **per-paragraph gate fake-green보다 상위(pipeline-level) fake-green** — 구조적으론 채워졌으나(assembled) 증거-접지(evidence-grounded)는 0인데 readiness가 구분 못 함.
- **추가**: `synthesized_citation_key_count=33`인데 `reference_count=0`·`cited_paragraph_count=0`. citation 합성이 33키 만들었으나 **reference 목록·in-text cite로 0 landing**. "citation 합성 돌았으나 산출물에 안 나타남" 또 다른 ran-but-produced-nothing 갭(Codex fix #2/#3 영역).

## 권고 (Codex fix order 지지 + 강화)
- **Codex fix #1(zero-claim 번들→needs_claim_extraction/advisory) 강력 지지** — "assembled"는 구조(slot 채움)지 증거-접지 아님. readiness가 둘 conflate하는 게 root.
- **Codex fix #2(evidence packet 있는데 used==0이면 warn) 지지 + per-slot로 강화**: run_report상 **9/9 slot 전원 allowed≥1·used=0** = 코너케이스 아니라 전면. aggregate warn뿐 아니라 slot별 "allowed N, used 0" 경고가 진단에 유용.
- **추가 권고**: `synthesized_citation_key>0`인데 `reference_count==0 && cited_paragraph_count==0`이면 별도 warn(citation 합성됐으나 미landing).
- **naming**: slot status에 "assembled"(구조)와 "evidence_grounded"(used>0) 구분 필드 추가 고려 — reader가 구조-완성을 증거-완성으로 오독 방지.

## 정직/큐
라이브=repo 밖 `_codex_runs/cir_repo_function_stress_codex`(leak-pattern 스캔=presence만·값 미echo, run_report.json status 직접 파싱). figures는 미열람(unpublished 값 substrate 가능성 — 위치상 repo 밖 확인, 미커밋). 신규코드0(HEAD=452ac6b). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 별도: claim_phrase N=7 replicate floor60 견고성=4/4 floor60 replicate Measured(62/65/66/72) 전원 ≥60 PASS(STATUS에 기록, 직전 분포의 incremental 확인). 다음: Codex가 readiness/evidence-used warn 구현하면 재검증 · figure leak 확인 필요시 · scope negation-aware · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값/figure 미노출.)
