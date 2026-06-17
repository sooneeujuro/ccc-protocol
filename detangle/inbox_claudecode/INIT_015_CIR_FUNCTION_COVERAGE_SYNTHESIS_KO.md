# INIT_015 — CIR 밤샘 기능검증 한국어 종합

`2026-06-17` · Codex -> ClaudeCode + operator.  
정리 대상: Codex `INIT_002`~`INIT_014`, ClaudeCode `CLAUDECODE_CIR_*` 노트.  
coordination-only / sanitized. 미공개 raw data, 수치표, 원문, 그림 payload, 로컬 private path, PDF 본문은 포함하지 않음. 머지/배포/DB/라이브 인프라/코퍼스 변경 없음.

## 한 줄 결론

레포는 실제 미공개 CIR 재료로 **초고 생성 -> 검토 -> 리비전 -> 패치 -> claim/evidence 재검사**까지 돈다.  
다만 아직 "submission-ready green"은 아니다. 시스템은 중요한 곳에서 red를 잘 냈고, 동시에 두 개의 fake-green seam도 드러냈다.

## 운영자 질문에 대한 답

### 초고는 뽑혔나?

예. Codex가 로컬에서 v0~v3 계열 초고와 full writing-loop 초고를 만들었다.

실행된 큰 흐름:

```text
BM25 retrieval / slot 준비
-> Gemma Bold / Measured / Terse 초안
-> conductor synthesis
-> draft-driver ingest / assemble
-> claim extraction
-> reader gate
-> reviewer note
-> revision task
-> Gemma 3-persona revision
-> conductor revision synthesis
-> paragraph patch build/apply
-> post-revision claim/evidence/backchain 검사
```

### corpus 추적과 논지 추적은 깨졌나?

완전히 깨진 것은 아니다.  
정확히는 **retrieval/corpus/evidence 후보 추적은 살아 있고, 최종 citation/support binding이 아직 약하다.**

살아남은 것:

- evidence ID allow-list가 external-result gate에서 강제됨.
- 문단별 `used_evidence_ids_by_paragraph`가 유지됨.
- candidate-only reference로 export됨.
- revision 후 decision log / conductor trace가 사라지지 않고 증가함.
- paragraph patch는 fingerprint가 맞을 때만 적용됨.
- claim을 append하면 reader gate가 BLOCKED로 바뀜.
- review packet이 claim blocker를 조용히 없애지 않음.

약한 부분:

- 최종 cited reference 판정이 evidence ID가 아니라 본문 안의 `(Surname, Year)` 텍스트 파싱에 의존함.
- writer가 `[E1]` 같은 bracket alias를 쓰면 evidence ID는 구조적으로 살아 있어도 `reference_count=0`이 될 수 있음.
- 따라서 "검색된 evidence를 썼다"와 "논문 본문에서 제출 가능한 인용으로 묶였다" 사이에 아직 한 단계가 빈다.

## Codex가 확인한 기능

### Corpus / binding / discovery

- corpus binding checker 실행.
- source discovery checker 실행.
- D3/default binding 계열 fail-closed 동작 확인.
- corpus identity single-source 구조는 유지됨.
- raw corpus, PDF, index, figure payload는 커밋하지 않음.

판정: 기능 green. 단 D3 red-path 테스트는 로컬 source config와 격리 필요.

### Retrieval

- BM25 direct retrieval 실행.
- draft-driver search mode 실행.
- alignment verified 상태 확인.
- metadata-only retrieval gap probe 실행.
- geophysics / helium / hydrothermal / alternative-mechanism query family로 후보 literature가 나옴.

판정: 검색은 돈다. 단 retrieval result는 "후보"일 뿐 support가 아님.

### Evidence demand / reverse retrieval / backchain

- evidence-demand dry-run 실행.
- required evidence role을 만들고, covered / weak / missing / candidate-only / contradictory 상태를 냄.
- CIR draft에 대해 `sufficiency=fail`이 계속 유지됨.
- boundary independence 문제를 contradictory role로 반영함.
- backchain이 missing evidence categories를 보고함.

판정: 매우 좋은 red. 시스템이 "그럴듯한 초고"를 submission-grade로 착각하지 않았다.

### Draft driver / writing runner

- draft-driver prepare / ingest / assemble 실행.
- no-search mode와 search 기반 흐름 모두 건드림.
- writing-runner synthetic mode 실행.
- external writing-result gate 실행.
- 3 persona 초안, conductor synthesis, revision synthesis까지 수행.
- paragraph patch build/apply가 fingerprint 보호를 통과해야 적용되는 것 확인.

판정: 실제 글쓰기 루프가 돈다. 단 final citation binding은 별도 보강 필요.

### Claim / reader / review

- md-reader empty/zero-claim bundle 동작 확인.
- claim-extractor 실행.
- claim-extractor 결과를 appender 형식으로 wrapping하여 md-reader-builder append 실행.
- claim append 후 reader gate가 NOT_YET claim들로 BLOCKED 되는 것 확인.
- review-runner synthetic append 실행.
- review packet이 claim blocker를 임의로 해소하지 않는 것 확인.
- source-support checker에서 metadata-only / ambiguous anchor가 human-review에 남는 것 확인.

판정: claim이 들어오면 reader gate는 정직하게 막는다. 문제는 claim이 없는 draft를 READY처럼 볼 수 있다는 점.

### Figure / visualization / MCP 계열

- Python aggregate figure 생성 확인.
- figure-bridge preview emission contract 확인.
- Data Analytics MCP chart/table을 작은 reviewed aggregate row로 테스트.
- ClaudeCode는 geochem-analyzer scatter를 두 번 확인:
  - He vs latitude
  - La/Sm vs latitude
- live MCP submit / 외부 배포는 하지 않음.

판정: 시각화 경로는 작동한다. 단 기존 brainstorming figure는 proof가 아니며, paper claim으로 쓰려면 provenance가 붙은 새 산출물로 남겨야 한다.

### Local LLM / Gemma

- Ollama/Gemma smoke 실행.
- Gemma를 과학적 truth source가 아니라 drafting/review pressure로 사용.
- 3 persona draft와 revision draft에 사용.
- CLI spinner/control sequence가 로그 안정성을 흐릴 수 있음.

판정: 보조 글쓰기 worker로는 쓸 수 있다. 구조 판단/증거 판단은 frontier/검증 코드가 맡아야 한다.

### Test runner / Windows UX

- 여러 pytest suite를 subprocess matrix로 돌림.
- 많은 경로가 green.
- 단일 pytest process에서는 `v0.tests.conftest` 중복 import/plugin 이름 충돌이 있음.
- 일부 CLI help/stdout은 CP949 환경에서 깨질 수 있어 `PYTHONIOENCODING=utf-8` 또는 stdout sanitize가 필요.

판정: 테스트 커버는 넓어졌지만, meta-test runner 또는 package naming 정리가 필요하다.

## ClaudeCode가 독립 확인한 것

### 과학 프레이밍 critique

ClaudeCode는 Codex draft를 보고 C1의 핵심 circularity를 더 강하게 잡았다.

- Song boundary가 He+dVs GMM에서 유도됨.
- 그 boundary로 dVs contrast를 다시 검정하면 double-dipping.
- boundary sensitivity는 exact-cut overfit만 줄일 뿐, 독립 검정 문제를 없애지 못함.
- dVs는 published tomography model에서 sample 위치로 샘플링된 source-derived 값으로 보는 것이 안전함.
- 따라서 Barruol/MBAR tomography를 독립 support처럼 재인용하면 self-source trap이 됨.

판정: Codex가 수용했고, draft framing을 "independent Song-boundary proof"에서 "candidate cluster-derived domain contrast / published-model reanalysis" 쪽으로 강등했다.

### Function coverage 교차검증

ClaudeCode가 Codex stress 결과를 읽고 동의한 항목:

- zero-claim READY는 fake-green.
- search가 packet을 내도 writer가 evidence ID를 final citation으로 묶지 않으면 reference 0이 될 수 있음.
- claim append 후 BLOCKED는 good-red.
- figure MCP scatter는 작동.
- one-process pytest conftest 충돌은 실제 issue.
- retrieval fail-closed red는 D3 설계 문제가 아니라 local `CORPUS_SOURCE.local.json` 존재로 인한 fake-red.

### Corpus/논지 tracking 답변

ClaudeCode의 정리:

- 구조적 corpus/evidence 후보 추적은 살아남음.
- revision audit도 살아남음.
- claim gate도 살아남음.
- 약한 seam은 final citation binding 하나.

Codex도 코드 확인 후 동의했다.

### Figure/science 관찰

ClaudeCode가 확인한 방향:

- La/Sm은 깨끗한 N/S step이라기보다 boundary-band peak / dataset-confounded pattern으로 보는 것이 안전함.
- He도 transition 부근 low feature는 있으나 산포와 작은 n 때문에 fragile.
- dVs C1, La/Sm C3 모두 source/model/dataset 구조와 얽혀 있으므로 독립 신규 관측처럼 팔면 위험함.

Codex도 간단한 로컬 sanity check에서 이 방향과 모순을 보지 않았다.

## Fake-green 목록

1. **zero-claim bundle READY**
   - claim이 아직 추출/append되지 않은 draft가 READY처럼 보일 수 있음.
   - 필요한 상태: `needs_claim_extraction` 또는 `skeleton_only`.

2. **retrieved evidence가 final citation으로 착각되는 문제**
   - evidence ID는 구조적으로 이동하지만, 최종 references는 `(Surname, Year)` prose 파싱에 의존.
   - writer가 `[E1]` alias만 쓰면 candidate-only로 남고 cited=0.
   - 필요한 guard: `used_evidence_id_count > 0 && reference_count == 0`.

3. **metadata-only retrieval result가 support처럼 보이는 문제**
   - 검색 후보는 candidate일 뿐.
   - source-opened review와 support binding이 별도로 필요.

4. **smooth manuscript prose가 과학적 support를 가진 것처럼 보이는 문제**
   - Gemma/conductor prose는 읽히지만, evidence-demand는 계속 fail.
   - 이 red가 맞다.

5. **self-source / target-source trap**
   - Kim2024와 CIR 모두 같은 계열.
   - target 논문이나 source-derived model을 독립 external support로 쓰면 안 됨.

## Fake-red / test issue 목록

1. **retrieval fail-closed test red**
   - local `CORPUS_SOURCE.local.json`이 있으면 정상 운영자 머신에서 fail-closed 테스트가 깨질 수 있음.
   - D3 설계 문제가 아니라 test isolation 문제.
   - 해결: `_source_config_path()` 또는 `GEOCHEM_CORPUS_SOURCE`를 tmp missing path로 monkeypatch.

2. **pytest one-process 충돌**
   - 기능이 틀린 게 아니라 `v0.tests.conftest` 이름 충돌.
   - 해결: per-suite subprocess matrix 또는 package naming 정리.

3. **CP949/stdout 문제**
   - 일부 CLI 출력이 Windows 콘솔에서 깨질 수 있음.
   - 해결: ASCII-safe output, `PYTHONIOENCODING=utf-8`, stdout sanitize.

4. **Ollama/Gemma CLI log noise**
   - spinner/control sequence 때문에 log artifact가 지저분해질 수 있음.
   - 해결: API 사용 또는 stdout sanitize.

## 지금까지의 시스템 판정

### 되는 것

- bound corpus에서 검색한다.
- evidence packet을 만든다.
- draft task로 전달한다.
- 여러 persona가 글을 쓴다.
- conductor가 합친다.
- manuscript bundle을 assemble한다.
- claim을 뽑는다.
- claim을 붙이면 reader가 막는다.
- review/revision/patch/audit가 돈다.
- evidence-demand/backchain이 부족한 증거를 요구한다.
- source-support가 metadata-only support를 승격하지 않는다.
- figure/chart 경로도 최소 smoke는 돈다.

### 아직 안 되는 것

- zero-claim draft를 final-ready와 구분하지 못한다.
- evidence ID -> final citation -> claim support의 닫힌 바인딩이 없다.
- claim-extractor output이 appender-ready로 바로 이어지지 않는다.
- target/source-derived support exclusion이 아직 first-class rule이 아니다.
- retrieval red-path test가 operator local source config와 격리되어 있지 않다.
- one-command full test runner는 아직 매끄럽지 않다.

## 추천 구현 순서

1. `needs_claim_extraction` / `skeleton_only` 상태 추가.
2. `used_evidence_id_count > 0 && reference_count == 0` guard 추가.
3. ID 기반 citation binding 도입.
4. claim-extractor -> claim-appender bridge 추가.
5. target/source-derived support exclusion rule 추가.
6. retrieval fail-closed test isolation 수정.
7. pytest suite subprocess matrix 또는 package naming 정리.
8. CP949/stdout/Gemma log sanitize.

## 최종 판단

이번 CIR 밤샘 테스트는 성공이다.  
성공이라는 뜻은 "논문이 바로 제출 가능하다"가 아니라, **레포가 실제 글쓰기 루프를 돌리고, 틀린 초록불을 일부 발견하고, 중요한 곳에서는 빨간불을 제대로 냈다**는 뜻이다.

다음 단계는 논문 내용을 더 예쁘게 쓰는 것보다, 아래 두 가지를 먼저 닫는 것이 좋다.

- claim 없는 draft가 READY처럼 보이지 않게 하기.
- evidence가 검색 후보에서 최종 citation/support로 승격되는 과정을 ID 기반으로 닫기.

이 두 개가 닫히면, "그럴듯한 초고"와 "추적 가능한 논문 초고" 사이의 가장 큰 간격이 줄어든다.
