# Claude(Code) — FGP prose ablation runner P4 재검증 = ACCEPT (`1aa494b`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — P4 닫힘. FGP prose ablation runner 완전 수락. FGP 체인 end-to-end 하드닝 완료 → 첫 실제 ablation 진행 가능.**

검증: 1aa494b diff 정독 + 라이브(재귀 walker 로직 + 실제 overlap 함수).

---

## P4 fix = 내 권고보다 강함 (크레딧)

내가 "rationale 2필드 추가"를 권했는데, Codex는 더 넓게 — `_result_texts`가 `writing_runner_result_to_dict(result)` **전체를 재귀로 훑어 모든 string surface**를 검사(`_string_values`). 그래서 `brief_rationale`·`final_rationale`·decision_log/conductor_trace **+ 미래 추가될 자유텍스트 필드까지 자동 커버**. future-proof한 선택.

## 라이브 확정

```
result에서 surface된 strings : [..., 'Open every introduction b...'(brief_rationale), ...]   # 재귀가 rationale 끌어냄
FGP in brief_rationale (gap) : REJECT fgp_draft_forbidden_phrase_overlap                      # 닫힘
clean result                 : OK                                                             # 회귀 0
short fields(schema/Bold/id) : OK                                                             # false-positive 0
```

- **P4 갭 닫힘**: rationale(및 모든 중첩 string)이 이제 overlap 검사됨.
- **회귀 0**: paragraph_md/final도 여전히 surface+검사.
- **false-positive 0**: 멀티워드 phrase는 짧은 id/enum/schema 필드에 매치 불가(exact-substring·8-word-shingle 둘 다 짧은 필드 미달). values만 훑고 keys는 안 봄 — 정확.
- 검증 노트: walker는 committed와 byte-identical 로직 + **실제** `check_generated_draft_for_forbidden_overlap`로 거부 확인. Codex in-suite 테스트(`final_rationale` 주입, line 202, `50 passed`)가 동일 모듈 end-to-end 커버.

---

## 🏁 FGP 체인 end-to-end 하드닝 COMPLETE

| 조각 | 상태 |
|---|---|
| rule revision (모드분리) | ✅ |
| scaffold 커밋표면 | ✅ a41d08e (4R) |
| prompt render-boundary (+F1) | ✅ 031fcd6 |
| source R0 (+R-a fail-closed) | ✅ 5a61d27 |
| **prose ablation runner (+P4)** | ✅ 1aa494b |

3 가드(phrase-corpus required / prompt-boundary / draft-overlap[이제 전체 string]) 전부 우회불가 mandatory. 커밋표면·렌더경계·로컬source·결과스캔 다 잠김. ablation runner의 7 break-it 포인트 전부 충족.

---

## 다음 = 첫 실제 owner-private FGP prose ablation

이제 외부 writer/model이 `writing_runner_result_v1` 생산 → `ingest`가 모든 가드 통과시킴. 실행 시 운영자 환경:
- `FGP_SOURCE.local.json` = out-of-repo FGP root(절대경로) 가리키게(example 복사)
- phrase corpus 추출 → prepare → 외부 모델로 baseline·FGP 프롬프트 각각 draft 생성 → ingest
- 그 첫 실런 결과(가드 통과 여부 + baseline vs FGP prose 품질 비교)도 보고 들고 오면 내가 검토.

semantic close-paraphrase는 여전히 구조 backstop 밖 = **human/process 리뷰 게이트**(verbatim/8단어만 자동). 이건 설계상 한계, 운영자 인지 하에.

지도 FGP 트랙 "전 조각 ACCEPTED, 첫 실 ablation ready(semantic은 human 게이트)"로 갱신 권장.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0.)
