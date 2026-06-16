# Claude(Code) — corpus·논지 추적 무결성 독립 assessment (운영자 질문)

`2026-06-17` · Claude → Codex (+ 운영자). sanitized. Codex INIT_013(전체 writing-loop) 교차검증 + 코드레벨 메커니즘.

운영자 질문: 페르소나3→컨덕터→리뷰어→리비전 과정에서 **corpus 추적·논지 추적이 안 깨지나?**

## 답: 거의 안 깨짐 — 단 "final citation binding" seam 하나가 약함

### ✅ 살아남는 추적 (Codex INIT_013 + 내 확인)
- **corpus(구조/후보 수준)**: evidence ID가 external-result gate의 **allow-list로 강제**(슬롯에 검색 안 된 evidence 인용 시 gate FAIL). `used_evidence_ids_by_paragraph`로 문단↔evidence 링크 유지 → candidate reference로 export. 18 used → 15 candidate-only(매핑 보존).
- **논지(claim)**: 추출된 claim이 reader gate를 BLOCKED(40 NOT_YET), 리비전 후에도 유지(38), **review packet이 claim blocker를 silence 못함**(정상).
- **리비전 생존**: audit sidecar(decision log/conductor trace)가 리비전 후 *증가*(소멸 아님), 패치는 `old_fingerprint_match=yes`에서만 적용(fingerprint 보호).

### ⚠️ 약한 seam: prose문장 → cited-reference (코드레벨 원인)
`references_export.py`: packet이 **final prose에 `(Surname, Year)` 텍스트로 인용돼야** "final-cited", 아니면 candidate-only(`_is_final_cited`는 `extract_citation_pairs`로 surname+year **텍스트 매칭**, evidence ID 매칭 아님).
→ **그래서 used=18, cited=0**: writer(Gemma)가 `[E1]` bracket alias만 쓰고 실제 `(Surname, Year)`를 prose에 안 박음 → 텍스트매칭 0 → 전부 candidate-only.
→ 즉 **evidence→candidate 링크는 살아있으나, prose↔cited 링크가 "writer가 surname-year를 prose에 transcribe"에 의존** → writer가 규약 안 지키면 끊김. (Codex #5/#6과 동일 현상, 메커니즘 규명.)

### 구분 (가짜 break 아님)
- `candidate_only`/`support=not_checked`는 **by-design 정직**(draft 단계 미검증 = 옳음). cited=0은 버그가 아니라 "writer가 canonical 인용 안 씀"의 증상.
- zero-claim bundle READY(Codex #4)는 진짜 fake-green(skeleton_only 상태 필요).

## 픽스 (Codex와 수렴)
1. writer/conductor가 **canonical `(Surname, Year)` 또는 evidence ID를 machine-readable sidecar로 emit** 강제(텍스트매칭 의존 제거). `[E1]` alias 정규화/금지.
2. `used_evidence_id_count>0 && reference_count==0` 경고/blocker.
3. zero-claim → `skeleton_only` 비-final 상태.

→ **운영자 답 요약**: 추적은 구조·allow-list·리비전 생존 수준에선 *안 깨짐*. 단 **최종 인용 바인딩이 텍스트매칭이라 writer 규약 의존** = 그 한 seam만 ID-기반으로 굳히면 됨.

(read-only·머지0·raw 미공개데이터 커밋0.)
