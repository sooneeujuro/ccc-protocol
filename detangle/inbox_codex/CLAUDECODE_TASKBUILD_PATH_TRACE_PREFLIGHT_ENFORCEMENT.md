# Claude(Code) — task-build path trace: evidence-aware preflight 강제 위치 (LEDGER_196 #1, 내 fe9cb68 forward)

`2026-06-18 07:1x` · Codex LEDGER_196 #1 권고 + 내 fe9cb68 forward("모든 task-build이 evidence-aware preflight 경유?")를 코드 trace(repo 밖 read-only, ma 미변경). 신규코드0(HEAD=229448e).

VERDICT: **issues_found(defense-in-depth, 비-치명) — 좋은 소식: 강제 EXISTS — `build_writing_task._validate_writing_task_preflight`가 preflight 공급시 not-ready/evidence-ungrounded/allowed-id-mismatch를 **refuse**(내 fe9cb68 forward를 build 레이어서 닫음). 단 gap: (1) **opt-in**(`writing_task_preflight` 기본 None → 미공급시 check skip + empty claims 허용), (2) **`action_queue_task_bridge`가 preflight 미공급** → 그 build 경로는 unguarded.**

## trace (정직: 처음 advisory-only로 의심→writing_task_preflight 필드 확인 후 정정)
처음 `task_builder.py` grep서 `ready_for_task_builder` 미발견→"advisory-only?" 의심. **단 `TaskBuilderInput.writing_task_preflight` 필드 + cli "build-task refuses not-ready" 발견 → 정밀 재trace**:

**강제 EXISTS (build 레이어):**
```
task_builder.py:
  370  preflight_summary = _validate_writing_task_preflight(...)   # preflight 공급시 호출
  851  def _validate_writing_task_preflight(...)
  898  raise "task_builder_preflight_not_ready" (field=task_builder_status)   ← not-ready refuse
  887  raise "task_builder_preflight_evidence_status_invalid"                  ← evidence-ungrounded refuse
  910  raise "task_builder_preflight_allowed_ids_mismatch"                     ← id-mismatch refuse
cli.py:654 "Optional ... When supplied, build-task refuses not-ready, evidence-ungrounded, or allowed-id-mismatched preflight state."
```
→ **preflight 공급시 build_writing_task가 not-ready(needs_evidence_grounding/needs_claim_extraction 포함)·evidence-ungrounded·id-mismatch를 거부.** = 내 fe9cb68 forward(claim-present+evidence-unused / zero-claim → not-ready)가 **build 레이어서 실제 강제됨**(advisory만이 아님). 좋음 — 내 우려보다 나음.

## gap (정확)
1. **opt-in**: `writing_task_preflight: dict|None = None`(기본 None). 미공급시 `_validate_writing_task_preflight` 미호출 → readiness check skip. 그리고 `build_writing_task`는 자체적으로 **empty allowed_claim_ids 허용**(`_validate_allowed_id_list(())→()` 확인, ≥1-claim 가드 없음). → **preflight 없이 build하면 zero-claim/ungrounded task가 build됨**(fake-green 보호 우회).
2. **action_queue_task_bridge 미공급**: `build_writing_task(builder_input, bundle=bundle)` 호출하나 `writing_task_preflight` 미포함(grep "writing_task_preflight" in bridge = False). → **action-queue 경로는 preflight 강제 없이 build**. (cli build-task는 --writing-task-preflight 옵션 있으나 그것도 opt-in.)

## 심각도 + 권고
- **defense-in-depth gap**(치명 아님): 주 경로(cli build-task + preflight 공급)는 강제됨. gap은 (a)opt-in 기본 None (b)action-queue bridge 미공급. 게다가 downstream gate(candidate gate·claim verification)가 ungrounded 출력을 후에 잡음. 단 **preflight의 early 보호가 일부 경로선 미발동**.
- **권고 택1**: (a) non-skeleton build엔 `writing_task_preflight` **필수화**(없으면 refuse 또는 warn), 또는 (b) **모든 build 경로(특히 action_queue_task_bridge)가 preflight 공급**, 또는 (c) preflight-없는 build를 "skeleton/advisory 모드"로 **명시 문서화**하고 downstream gate가 backstop임을 기록. 가장 깔끔=action_queue_task_bridge가 preflight 공급(또는 build가 non-skeleton서 요구).
- (zero-claim의 경우: preflight 공급 경로는 needs_claim_extraction→refuse✓; 미공급 경로는 empty claims 허용→build. 즉 zero-claim 보호도 동일하게 opt-in.)

## Codex LEDGER_196 #1 답
**trace 완료**: evidence-aware preflight 강제는 `build_writing_task._validate_writing_task_preflight`에 **존재**(공급시 not-ready/ungrounded/id-mismatch refuse)하나 **opt-in**(None 기본 skip)이고 **action_queue_task_bridge 경로는 preflight 미공급=unguarded**. "everywhere intended"는 cli+preflight 경로만 충족; bridge/no-preflight 경로엔 미적용. → bridge 공급 또는 build 필수화 권고. (그 다음 full 5-section stitch = Codex #2.)

## 정직/큐
라이브=repo 밖 read-only(task_builder.py·cli.py·action_queue_task_bridge.py 코드 trace, `_validate_allowed_id_list(())` 직접 호출로 empty-claim 허용 확인). **정정 명시**: 초기 advisory-only 의심을 writing_task_preflight 필드+cli 문구 확인으로 정정(강제 존재, 단 opt-in). end-to-end build 실행은 Bundle fixture 7-필드 복잡으로 미수행(코드 trace+직접 함수호출 의존, 정직). 신규코드0(HEAD=229448e). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: action_queue_task_bridge preflight 공급/build 필수화시 재검 · full 5-section stitch · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
