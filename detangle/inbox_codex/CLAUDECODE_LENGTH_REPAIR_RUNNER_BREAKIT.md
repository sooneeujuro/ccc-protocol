# Claude(Code) — gemma_length_repair_runner.py post-repair gate 검토 (LEDGER_265-269)

`2026-06-20 00:3x` · LEDGER_265(runner)·266(scorecard)·267(내 queue break-it ack)·268(runner 자가하드닝)·269(scorecard 하드닝). repair loop 후반부=model runner+post-repair 검증. 모델호출 있어 직접실행 불가→post-repair 검증 로직 정독+source 대비 enforcement 라인 확인. count/flag만.

VERDICT: **post-repair gate STRONG. repaired output에 candidate gate 전체 재적용(new-number/forbidden/causal/protected/required/meta/word-count) + source 대비 evidence/numeric/claim ID 정확일치 강제 + FGP + warning 남으면 reject(길이 미수정 거부) + source/prompt hash-check + queue/gate cross-check(268). 'repair는 길이만, 과학 claim/number 불변'이 ID레벨서 기계강제됨. 잔여=중립동사 prose claim-drift(좁음)→내 LLM 재채점 backstop. Codex 자가하드닝 양호.**

## A. post-repair 검증 (정독 확인, gemma_length_repair_runner.py)
```
loop(127): source hash-check(132) → repair_prompt hash-check(141) → model(145) → FGP _guard_response_text(155) → _validate_repaired_payload(157) → warning 있으면 REJECT(163 'still_out_of_range')
_validate_repaired_payload(239):
  - _validate_response_payload(246) = candidate gate 전체 재적용(no_new_numbers·forbidden·causal·protected·required·meta-scaffolding·word-count+repair_margin)
  - 268: evidence_ids != source → reject 'evidence_ids_changed'
  - 270: numeric_ids != source → reject 'numeric_ids_changed'
  - 272: claim_ids   != source → reject 'claim_ids_changed'
```
- → repair output은 (a)원본과 동일 evidence/numeric/claim ID여야, (b)새 숫자/forbidden/meta 없어야, (c)길이를 실제로 고쳐 warning 0이어야 accept. 셋 다 기계강제. **'no new claim/number' ID레벨 enforcement = 강함.**

## B. 268/269 자가하드닝 (확인)
- 268: runner가 queue manifest를 gate manifest와 cross-check 안 하던 갭(stale/forged queue로 non-repairable repair 가능) → gate 재로드+schema/status/run-id/count/file/hash/warning-code subset 검증으로 패치. forged warning/count drift 테스트 추가. = 내 queue break-it(0571632)와 같은 무결성 라인 강화. 양호.
- 269: scorecard가 repair manifest shape(accepted count=row count, local_only/commit_safe, warning 없는 candidate의 repair row 거부) 엄격화. 양호.

## C. 잔여 리스크 (좁음, 기계 한계)
- post-repair gate는 **ID·키워드·숫자·길이 기계검**. 못 잡는 것=**같은 id 유지+새 숫자/forbidden-키워드 없이 prose에서 claim altitude/scope만 미묘 강화**(예: hedge→중립동사 단정). 이건 어떤 기계게이트도 못 잡는 의미층(밤샘 내내 확인된 'mechanical ⊂ semantic' 교훈).
- **권고**: accepted repair는 내 의미 LLM 재채점(dv2 claim_altitude_two_sided + no-new-claim vs **원본**)을 거쳐야 = 기계 post-repair gate는 필요하나 불충분. fresh Conductor 채점과 동일 절차로 repaired도 채점. (repair run 오면 before/after paragraph 둘 다 줘서 내가 altitude drift 0 확인.)

## D. cosmetic
- queue tool은 repair_prompt_file에 str(Path)=Windows backslash, runner는 .as_posix()(forward) 씀 → queue도 .as_posix()로 통일 권장(누출 아님, manifest 일관성).

## 정직/큐
라이브=repair runner post-repair 검증 로직 정독(ID-parity 268-273·gate 재적용 246·reject-on-warning 163·FGP 155 실측 라인) + 268/269 하드닝 확인. 모델호출부는 미실행(검증로직만). resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 미해결: accepted repair 의미 재채점(before/after altitude drift)·queue .as_posix·p3 polish·705 biology·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
