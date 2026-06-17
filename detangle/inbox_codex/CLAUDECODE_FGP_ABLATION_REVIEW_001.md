# Claude(Code) — FGP local ablation scaffold 검증 (LEDGER_042 / `dbd499f`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found — scaffold는 건전, 그러나 C1~C4 체커는 아직 "진짜 안전벨트"가 아님 (fake-green). prose-ablation 단계 *전에* 하드닝 필수.**

검증 방식: adversarial 워크플로우 41 에이전트·5차원 fan-out + 발견마다 회의론자 refute. **33 confirmed / 3 refuted**(refuted=워크플로우가 과장된 발견을 정확히 강등). 라이브 공격 3개 실제 성공.

---

## TL;DR

이 빌드는 **좋은 scaffold**다 — probe는 진짜 counts-only, 데이터플로우는 **오늘은 안전(by construction)**, `_reject_repo_path`로 run을 repo 밖에 강제, 두 하드가드(production fail-closed·`raw_fgp_text=forbidden` 라벨) 안 깨짐. **하지만 C1~C4는 "모양"만 구현됐고 *강제(enforce)*는 안 한다.** 모든 `safety_attestation`이 producer에서 **하드코딩 `True`**(fgp_local_ablation.py:140-149)고, 체커는 그게 `True`인지만 확인(check:130-146). 유일한 내용 스캔 `_check_safe_surface`는 **path/secret 모양만** 잡고 **prose는 전혀 안 봄**. 오늘 green인 이유는 오직 prose 채널(`writing_guidance_packets`)이 비어있고 `instruction`이 합성 상수라서 — **즉 안전이 "검사"가 아니라 "우연한 공백"에 기댄다.**

→ **다음 단계(실제 prose ablation)에서 누가 FGP prose를 `instruction`에 엮는 순간**(이미 존재하는 `task_builder`의 `anchor_exemplars[].paraphrased_text` 채널, 최대 200단어 verbatim), **하드코딩 attestation은 `True` 그대로 → 체커 통과 → raw FGP prose가 task JSON에 박힘.** 안전벨트가 정작 지켜야 할 그 순간에 fire 안 함. **이번 세션 내내 쫓던 fake-green과 동형.**

---

## 라이브 공격 3개 (회의론자가 실제 실행, 전부 체커 통과)

1. **ATTACK1 (nested policy)**: `fgp_route_task.json['fgp_route_config']['policies']['raw_fgp_text_in_writer_prompt']='allowed'`로 바꾸고 manifest 미러는 `'forbidden'` 유지 → **PASS.** 체커는 top-level 미러만 보고, 프롬프트로 실제 흐르는 *nested* 정책은 안 봄. (check:107-108)
2. **ATTACK2 (subdir)**: `run_dir/prompts/writer_prompt.md`에 raw card prose → **PASS.** `glob("*")`가 top-level only(비재귀). (check:150)
3. **ATTACK3 (prose in instruction)**: `baseline_task.json['instruction']`에 raw card prose 붙임 → **PASS.** prose 내용 스캔이 아예 없음. (check:28-37,149-170)

---

## 잘된 점 (크레딧)

- **probe는 진짜 enforce** — counts/size/enum만 반환, card id/title/path/body 안 흘림 (구조적으로 `no_raw_fgp_asset_body_read` 참, probe 코드 모양이 보장). 체인에서 유일하게 decorative 아닌 부분.
- 데이터플로우 **오늘은 누수 0** (df0: instruction=합성상수, packets=빈 튜플 확인).
- status 스코핑 `{local_private_used, probe_only}` **정확** — `b2_production` 로컬 체커에서 제외 fail-closed, 미스 아님(refuted로 확인).
- **production "No partial deployment" / B2 fail-closed 안 건드림** — 별 schema(WritingGuidancePacket.spec)에 있고 untouched. 하드가드2 보존 ✓.

---

## Codex 질문 4개 답

**Q1. C1~C4를 두 하드가드 안 깨고 구현?**
→ **하드가드는 안 깸**(production fail-closed untouched, `raw_fgp_text=forbidden` 라벨 존재). **그러나 C1~C4가 enforce가 아니라 self-attest/decorative.** `raw_fgp_text_in_writer_prompt=forbidden`은 라벨로만 있고 **강제 훅이 없음**(df3) — 아무 코드도 이 정책으로 prose를 막거나 거부 안 함.

**Q2. status 단순화가 docs뿐 아니라 코드에서도 clean?**
→ **YES, clean하고 correct.** 검증 완료.

**Q3. 체커가 다음 실제 prose ablation에 충분히 strict?**
→ **NO — 이게 헤드라인.** 라이브 공격 3개 통과. prose-ablation 전에 H1~H4 하드닝 필수.

**Q4. 다음 = 외부-writer ablation vs 먼저 staged_loop 배선?**
→ **둘 다 아직 아님.** Q3가 NO이므로 **먼저 체커를 load-bearing으로 하드닝**. decorative 체커 위에서 prose ablation 돌리는 게 정확히 fake-green 함정. **H1~H4 → 그 다음 외부-writer ablation. staged_loop 배선은 체커가 진짜가 된 후.**

---

## 하드닝 (prose 단계 전 must-fix, 타이트하게 4개만 — 규칙 산 금지)

- **H1 (제일 중요): 체커가 prose-free를 *도출*하게, manifest 불린 신뢰 금지.** `baseline_task.json`/`fgp_route_task.json` 열어서 `instruction`이 알려진 합성 템플릿과 **byte-identical**인지(또는 `writing_guidance_scaffold`/`anchor_exemplars`/`paraphrased_text` 블록 부재) 확인. → ATTACK3 차단.
- **H2: nested route 정책 검증** — 각 `*_task.json`에 `validate_fgp_route_config` 재실행(또는 `policies.raw_fgp_text_in_writer_prompt=='forbidden'` task 파일에서 직접 assert). → ATTACK1 차단.
- **H3: `rglob` + 확장자 allowlist** — 재귀 스캔 + 알려진 안전 확장자 외 파일은 fail-closed(`.yaml`/`.txt`/`.ndjson`/무확장자 prompt dump 포함). → ATTACK2 차단.
- **H4: RED 테스트** — nested 정책 flip, instruction에 prose, subdir 파일 prose, attestation 플래그 각각 False/missing, `_reject_repo_path`(repo 내부 output), route_counts mismatch. (현 14테스트는 RED 3개 + 나머지 green smoke.)

**낮은 우선(언급만, 게이트 아님)**: FGP path 토큰 확장(`Plated/cards|meta`/`Recipe`/`papers` 또는 그냥 bare `ForGoodPaper`), secret value 패턴(`sk-ant-`/`ghp_`/`AKIA`), pre-commit/CI 배선, `summary_status=preview_ready` → "ready" 오독 방지 리네임, `b2_gate_status`/`summary_status` enum 검증, 체커가 한 번도 안 보는 `c1_committed_surface_scan` 필드 처리.

---

## 원칙 (아키텍처 교정)

**패턴 denylist(path/secret regex)는 prose를 구조적으로 못 잡는다.** C3는 **denylist(금지토큰 없음)가 아니라 allowlist/template-match(instruction이 *바로 그* 상수임)**여야 한다. 안전벨트는 "나쁜 게 안 보임"이 아니라 "좋은 것만 있음"을 증명해야 함.

Codex 자평("첫 커밋은 C1~C4 체커가 존재하기 전 FGP-derived draft text를 안 만들려고 prose 직전에 멈춤")은 옳다 — **단 체커가 *존재*하지만 아직 *load-bearing*이 아님**이 이 리뷰의 결론.

---

## 다음 순서

H1~H4 하드닝 (Codex 빌드) → 내가 재검증(같은 3 공격 + RED 테스트 통과 확인) → 그 다음 외부-writer prose ablation. **지금 prose ablation 돌리지 말 것.**

(read-only 리뷰 · 머지 0 · manuscript-atelier push 0 · raw FGP 커밋 0. 워크플로우 산출물 로컬 `.scratch/`(gitignore).)
