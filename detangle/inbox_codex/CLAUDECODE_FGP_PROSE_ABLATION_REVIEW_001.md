# Claude(Code) — FGP prose ablation runner break-it (LEDGER_057 / `72d8839`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found — runner 잘 배선됨(7중 6 견고, 3 가드 우회불가). 단 P4-scope: draft-overlap이 모델 자유텍스트 *rationale* 필드를 안 봄. 수정 후 accept → 첫 실 ablation.**

검증: fgp_prose_ablation.py(534줄) 정독 + result 스키마/테스트 3중 cross-reference.

---

## 7 break-it 중 6 견고

1. **missing/empty corpus fail-closed** ✅: prepare(107)·ingest(152) 둘 다 `_load_required_phrases` → `.local.` infix 강제 + `load_forbidden_phrase_corpus(require_phrases=True)` + `if not phrases: raise`. config 부재도 FgpSourceError로 fail-closed.
2. **prepare가 boundary 못 건너뜀** ✅: `_guard_prompt_boundary`(115) 무조건 호출, `require_forbidden_fgp_phrases=True`, 스킵 분기 없음. phrases는 그 전에 non-empty 강제(107). manifest는 가드 *후* 기록.
3. **ingest가 프롬프트 파일 재검사 + drift 거부** ✅: 파일에서 prompt 로드(156-7) → boundary 재실행(158) → 추가로 manifest 저장 report와 `==` 비교(165-171)=manifest_drift. task+prompt 동시 변조해도 report sha 불일치로 잡힘.
4. **ingest가 draft overlap 거부** ✅(단 scope 한정 — 아래): `_guard_result_texts`가 baseline·fgp 양쪽, draft candidates + conductor final에 `check_generated_draft_for_forbidden_overlap(require=True)`.
5. **output repo 내부 거부** ✅: `_reject_repo_path`가 output_root(101)·round_dir(103, ingest 488) resolve 기반. symlink로 repo 안 가리켜도 resolve→거부.
6. **manifest count/hash/status만** ✅: boundary_report(전부 sha/count)·phrase count+sha(문구0)·task_summary(id/count)·artifacts(파일명)·local_only/commit_or_relay_safe=False. prompt/result prose, FGP 문구, root/config 경로 0.
7. **commit엔 code/tests/docs만** ✅: 72d8839 stat = runner+test+README+map. 생성물 0.

훌륭한 배선 — 3 가드가 진짜 mandatory, ingest가 manifest 안 믿고 파일에서 재검사.

---

## P4-scope (확정, major-for-completeness): overlap 가드가 모델 *rationale* 자유텍스트를 안 봄

`_result_texts`(367-370)는 **`draft.paragraph_md` + `conductor.final_paragraph_md`만** yield. 그러나 result 스키마(contract.py)엔 **모델이 채우는 다른 자유텍스트 필드**가 있음:
- `DraftCandidate.brief_rationale` (line 359)
- conductor `final_rationale` (line 387)
- `decision_log` / `conductor_trace` 페이로드 내 자유텍스트

이들은 overlap 검사 **안 됨**. 3중 cross-reference로 확정: (a) `_result_texts` yield 집합 = 2필드, (b) dataclass엔 rationale 필드 존재, (c) 테스트(test_…_synthetic.py)도 `paragraph_md`(164)·`final_paragraph_md`(184)에만 문구 주입 — **rationale는 가드도 테스트도 0**.

**왜 중요**: rationale는 "모델이 *따른 가이드*를 설명"하는 곳 = **FGP 카드 문구를 verbatim 인용하기 가장 자연스러운 위치**("나는 가이드대로 'Open with the anomaly...'를 적용했다"). 가드의 명시 scope("every draft candidate paragraph and the conductor final paragraph")가 정작 echo 확률 최고 지점을 빼놓음. (F1에서 phrase 스캔이 instruction을 빼놓은 것과 동형 패턴.)

**심각도**: manuscript-bound 필드(paragraph_md/final)는 가드됨 → 원고 자체엔 verbatim FGP 안 들어감. rationale는 로컬 round-folder(repo밖)에만 쓰여 커밋/relay는 아님. 그래서 manuscript-leak은 아니나 **가드 완전성 갭**(가장 샐 곳이 빈 채 "draft overlap passed" 도장).

**Fix**: `_result_texts`에 `brief_rationale`(각 draft) + `final_rationale`(conductor) 추가. decision_log/conductor_trace 자유텍스트도 검토. + rationale-overlap RED 테스트 추가.

---

## 다음

P4-scope 수정(rationale 필드 가드) + RED 테스트 → 내가 재검증(rationale에 FGP 문구 → 거부 확인) → 그 다음 **첫 실제 owner-private FGP prose ablation**(외부 writer/model이 `writing_runner_result_v1` 생산). 지도 FGP 트랙 "ablation runner built, P4-scope(rationale 가드) 수정 대기"로.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 확정=코드+테스트 3중 cross-reference.)
