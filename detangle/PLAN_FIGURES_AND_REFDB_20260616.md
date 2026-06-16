# 계획서 — 그림 채우기 + allowlist 정리 + PDF/supp 통합 (2026-06-16 13:49)

작성: Claude(회사PC, a745303e). **검토용 초안. 운영자 GO + Codex verdict 전엔 실행 안 함.**
비파괴 원칙: 원본 PDF/corpus는 COPY·BACKUP만, 되돌리기 가능.

## 실측 (read-only)
- PDF 분포: G:\RefDB 1,180 · D:\Academia 985(RefDB와 다수 중복) · Desktop\recent_added_pdfs_20260601 20 · Desktop\FinalList 15(+supp8) · Desktop\10mantledynamics 15(+supp2) · Desktop\새 폴더(2) 2. supplementary ~65개 흩어짐.
- 그림 공백: 실제 604개/51편 (allowlist 파일엔 2,028개 = 1,424개는 이미 채워진 stale).
- 그림 PDF: 51편 중 51편 PDF 확보(RefDB/LostnFound). Busigny 2005 포함.

---

## 워크스트림 1 — allowlist 정리 (저위험·비파괴·즉시 가능)
**목적**: allowlist가 실제 공백(604)을 2,028로 2.4배 뻥튀기 → 진실하게 재생성.
- 단계: ① 현 `FIGURES_MISSING_ALLOWLIST.txt` → `.bak_20260616_pre_prune` 백업 ② `fig_render_audit.py`의 실제 missing(=articles에 없는 ref)만으로 재작성 ③ GATE 재실행 PASS 확인.
- 영향: 번들 txt 1개 갱신 + 백업. 그림/본문 무변경. **되돌리기=백업 복원.**
- 주의: 워크스트림 3로 그림 채우면 또 줄어듦 → **3 끝나고 최종 1회 더 재생성** 권장. (지금 1차, 추출 후 2차.)

## 워크스트림 2 — PDF/supplementary 통합 (중위험·COPY라 비파괴)
**목적**: corpus와 쌍으로 들고다닐 단일 레퍼런스 라이브러리. 원본 보존(복사).
- 신규: `G:\corpus_refs_v20260616\` (제안명) — `papers/` + `supplementary/` + `MANIFEST.csv`.
- 소스: 위 6개 폴더 전부.
- 절차: ① 전수 스캔 ② **content-hash(md5) dedup**(같은 내용 1부만) ③ **clean 네이밍**(`Author_Year_TitleShort.pdf`, corpus 논문명 규칙에 맞춤) ④ COPY ⑤ MANIFEST.csv(원경로→새이름→매칭 corpus pid/논문, sha256). supplementary는 논문별로 `supplementary/<paper>/`.
- 영향: **원본 0 변경**(전부 복사). G: 용량 추가(~수 GB). **되돌리기=새 폴더 삭제.**
- 검토 포인트(Codex): dedup 기준(내용해시 vs 제목), 네이밍 규칙, corpus 매칭 방법(sidecar doi/제목), 용량.

## 워크스트림 3 — 그림 재추출 (고위험/비용·게이트 필수)
**목적**: 51편 PDF에서 그림 추출해 corpus 빈칸 채움. **flat pilot 절대 안 씀(충돌).**
**방식 = B(추출+remap) 확정 (운영자 선택).**

### 🔒 논문당 폴더 = 물리 격리 (운영자 지시, 채택)
원래 사고원인 = flat 공용 폴더에서 해시충돌로 섞임. → **추출 전 과정을 논문별 폴더로 격리하면 섞일 수 없음.**
- **추출 워크스페이스**: `G:\fig_rebuild_v20260616\<pid>\` — 논문 1개 PDF는 **자기 폴더에만** 추출. 공용/flat 디렉토리 0. fig01.jpg, fig02.jpg… (폴더 격리라 단순 순번이어도 충돌 불가).
- **번들 배치 2안 (Codex 검토 항목)**:
  - **(i) flat + pid 접두 (스크립트 무변경, 기본 추천)**: 최종은 `articles/<pid>__figNN.jpg`. pid 접두가 이미 고유보장 → 섞임 불가. 기존 read_paper.py/fig_render_audit.py 그대로 동작(둘 다 basename 기준).
  - **(ii) 번들에도 논문별 하위폴더 (완전 물리격리, 스크립트 소폭 수정)**: `articles/<pid>/figNN.jpg` + 본문 ref도 `<pid>/figNN.jpg`. 단 read_paper.py·fig_render_audit.py가 현재 basename만 보므로 **상대경로 지원하게 2줄 수정** 필요(Codex 리뷰 + 백업).
- 추출은 (i)·(ii) 둘 다 논문별 폴더에서 진행 → **물리 격리는 어느 쪽이든 보장.** 차이는 "번들 최종 형태가 flat이냐 폴더냐"뿐.
- 권장: 추출=논문별 폴더(격리) → 검증 → 배치는 **(i) pid 접두 flat**(audited 스크립트 무변경, 가장 저위험). 형이 "번들도 폴더로" 원하면 (ii)로 가고 스크립트 수정분 Codex 검토.

- ⚠️ 미지수: corpus 이미지 이름 `<pid>__<hash>`를 만든 변환기가 이 PC에 결정적 스크립트로 없음(=LLM 'Sonnet 재추출' 추정). → **해시 재현 보장 안 됨.** B는 새 이름 쓰니 무관(본문 ref 교체).
- **Phase 0 (조사, 무비용)**: 원 추출 메커니즘 확정. 해시가 (a)이미지 바이트 md5면 재렌더로 재현 가능 → 이름 그대로; (b)불가면 → 아래 remap 방식.
- **추출 방식 2안 (Codex와 택1)**:
  - **A. 이름 재현**: 원 파이프라인 재현해 `<pid>__<hash>` 그대로 생성 → articles에 복사. 본문 무변경. (재현 가능할 때만.)
  - **B. 추출+remap(권장 안전책)**: PDF에서 그림 결정적 추출(PyMuPDF 등) → 새 이름 → **그 논문 md의 `![Figure N]` 참조를 순서대로 새 이름으로 교체**. 본문 md 이미지줄만 수정(백업). 충돌·해시문제 회피. 리스크=추출순서↔캡션순서 매칭(시각검증으로 확인).
- **Phase 1 (시범 1편, 저비용)**: 그림 많은 1편(예: Seton 2012, 28장)으로 A or B 실행 → **그림 inline 렌더해서 운영자 눈으로 검증** → Codex 리뷰.
- **Phase 2 (배치)**: OK면 나머지 50편 → `fig_render_audit.py` GATE PASS + 샘플 시각검증.
- 비용: 변환/모델(특히 B의 추출은 로컬 가능, A는 파이프라인 의존). Phase별 운영자 GO.
- 영구공백 후보: Busigny 2005(PDF 확보됨, 추출 시도), 그 외 PDF 정상.

---

## 권장 순서
1. **WS1 1차**(allowlist 진실화, 즉시·저위험) — 선택.
2. **WS2**(PDF 통합, 복사라 안전) — WS3의 깨끗한 소스도 됨.
3. **WS3 Phase 0→1**(추출방식 확정 + 1편 시범 + 시각검증) — 여기서 멈추고 운영자 확인.
4. OK면 **WS3 Phase 2** 배치 → **WS1 2차**(최종 allowlist 재생성).

## 게이트
- 각 비용/비가역 단계 = 운영자 GO. corpus/그림 git push 금지(로컬·NAS만). B(sidecar) 게이트 무관(별개).
- Codex 검토 항목: WS2 dedup·네이밍·매칭 / WS3 추출 A vs B·1편 검증기준·본문 md 수정 허용 여부.

---

## ✅ CODEX 검토 반영 (FINAL, B-prime) — 022 verdict + 023 per-paper
Codex verdict=issues_found(건설적). 방향 승인, 가드 추가. 아래로 확정.

### WS3 = B-prime (단순 순서매칭 금지)
논문별 staging 폴더(`G:\fig_rebuild_v20260616\<pid>\`)에 추출 → **live articles/ 직접수정 금지(staged diff 먼저)** → 검증 후 promote.
- **순서만 믿지 말 것.** PDF엔 로고·graphical abstract·표이미지·수식·컬러바·multi-panel 분할·supp그림 섞임. → 3중 검증:
  1. **figure 개수** (그 논문 missing ref 수 vs 추출 후보 수),
  2. **page/caption 텍스트** (PDF의 'Fig./Figure' 캡션 ↔ 본문 alt/caption 대조),
  3. **contact sheet 시각검증** (옛 캡션/ref 옆에 후보 이미지 나란히, 사람 확인).
- 셋이 어긋나면 그 논문은 **manual/blocked**로 표시(강제매칭 금지).
- 본문 md 이미지줄 교체 허용조건: 운영자 GO + 백업/롤백 + staged diff 우선 + 모든 변경줄↔소스PDF/추출이미지 manifest + render GATE PASS + 사람 시각샘플.

### 2-파일럿
- Phase 1a: 작은 논문(2~5장)로 메커니즘 싸게 검증.
- Phase 1b: Seton 2012(28장)로 순서/중복/시각QA 스트레스.
- 각 파일럿 산출물: 추출 manifest · staged md diff · contact sheet · render audit · 최종 채움/잔여 카운트. → **운영자 시각 sign-off 후 50편 배치.**

### WS2 가드 (Codex)
- dedup 키 = **SHA-256**(md5는 보조). 중복 provenance 보존(같은 PDF 여러 출처면 전부 기록).
- 충돌방지 목적지명: `papers/<paper_key>__<sha256_12>__Author_Year_TitleShort.pdf` 또는 `papers/<paper_key>/source.pdf`.
- corpus 매칭 신뢰도 tier: high(DOI exact+연도/제목) / medium(정규화제목+1저자+연도) / low·manual(파일명·약fuzzy).
- supp는 DOI/제목/출처 근거로 논문 연결, 불확실하면 `supplementary/_unmatched/` + manifest행.
- 폴더명 `corpus_refs_v20260616` Codex OK.

### WS1 가드
- 실제 missing = **`md 이미지 refs − articles 존재파일`로 독립 산출**(allowlist 자기참조 금지). report 먼저, 가능하면 fill 후 prune. 최종 allowlist=진짜 잔여만.

### 실행 순서 (Codex)
1. WS2(복사·통합) → 2. WS1(report/보수 prune) → 3. WS3 Phase0(A 재현성 테스트) → 4. B-prime 소파일럿+Seton → 5. 운영자 시각리뷰+Codex 파일럿 검토 → 6. 50편 배치 → 7. 최종 allowlist 재생성+GATE.

**상태: 계획 FINAL. 운영자 GO 대기. (Codex: "가드 반영+운영자 승인 시 진행 이의 없음".)**
