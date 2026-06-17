# Claude(Code) — 16921e3 재검: preflight consume가 내 task-build trace finding 닫음

`2026-06-18 07:2x` · 16921e3(`writing: consume draft task preflight`, 내 db6d267 task-build trace finding 응답) repo 밖 실 함수 직접 호출 재검. 신규코드=16921e3(HEAD). take83(full sweep discussion) 진행중.

VERDICT: **ok — 내 trace finding 닫힘. gap#2(action_queue_bridge unguarded) FIXED: bridge `build_revision_task_from_action_queue`가 이제 `writing_task_preflight` param 수용+전달(+cli build-task·build-revision-task 양쪽 wire). 강제 robust 확인: preflight 공급시 not-ready/zero-claim(needs_claim_extraction)/evidence-ungrounded refuse — **ready-status인데 ungrounded인 inconsistent payload까지 refuse**(robustness bonus). gap#1(opt-in)은 Codex가 의도적 design 유지(documented optional input-side gate + downstream backstop).**

## 강제 robust 확인 (실 `_validate_writing_task_preflight` 직접 호출)
```
ready+grounded                                   -> PASS
needs_evidence_grounding (내 fe9cb68 forward 케이스) -> REFUSE(task_builder_preflight_not_ready)
needs_claim_extraction (zero-claim)              -> REFUSE
ready-status BUT evidence=needs_evidence_grounding -> REFUSE  ← inconsistent payload도 catch
```
- 강제 조건(line 892-896): `ready_for_task_builder is not True OR task_builder_status != "ready" OR evidence_status == "needs_evidence_grounding"` → refuse. → **claim-present+evidence-unused(needs_evidence_grounding) 빌드 거부 = 내 fe9cb68 forward를 build 레이어서 완전 폐쇄.** + id-mismatch(line 910) 별도 refuse. + ready-but-ungrounded 조합까지 막아 inconsistent payload 방어(견고).

## gap#2 plumbing FIXED (실 signature)
- `action_queue_task_bridge.build_revision_task_from_action_queue`가 이제 `writing_task_preflight` param 수용(확인: signature에 존재)+`build_writing_task`로 전달. → **직전 unguarded였던 bridge 경로가 이제 preflight 강제 가능.**
- cli `_run_build_task`·`_run_build_revision_task` 둘 다 `--writing-task-preflight` 공급시 전달. → 모든 주 build 경로가 preflight 강제 wire됨.

## gap#1 opt-in — 의도적 design (수용)
- `writing_task_preflight` 여전히 기본 None(opt-in). docstring/README: "input-side gate ... preventing callers from ignoring a not-ready/ungrounded/mismatched preflight" + "Optional ... When supplied". → **Codex 설계: optional input-side gate**. 공급시 strict 강제, 미공급시 skeleton/advisory build(downstream gate backstop).
- 잔여(미공급시 empty-claim build 가능)은 이제 **documented 의도 모드**이고 plumbing이 universal(어느 경로든 공급 가능)이라 **구조적 gap은 닫힘** — 남은 건 "operator/orchestration이 real build엔 preflight 공급" 규율(reasonable for optional gate). 내 권고(a)(필수화)는 안 갔지만 (b)(모든 경로 공급 가능)+문서화로 처리 = acceptable.
- 단 메모: real(non-skeleton) build를 preflight 없이 도는 caller가 있으면 early 보호 미발동 — operator가 build 경로별 preflight 공급 일관성 점검 권장.

## 정직/큐
라이브=repo 밖 read-only+실 함수(`_validate_writing_task_preflight` 4-케이스 직접 호출·bridge signature inspect). end-to-end build는 Bundle 7-필드 fixture 복잡으로 미수행(enforcement 코어+plumbing signature 직접 확인=정직). 신규코드=16921e3(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: take83 full sweep(discussion) + 나머지 섹션 sweep INDEPENDENT BLIND(claim-strength gradient) · operator review. **내 finding 라인(references·SHA1·prefix·scope disclaimer·persona collapse·floor fragility·stress fake-green 2종·forward evidence-grounding·task-build path) 전부 landing+verify 완료.**

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
