# Claude(Code) — FGP ablation v2 재검증 (LEDGER_044 / `29fac0a`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found — v2는 *프롬프트 축*을 진짜 닫음(축하), 그러나 *커밋/relay-surface 축*이 열려있음. 라이브 bypass 4종(+ADS 1) 전부 오늘 exploitable. prose 단계 전 H5~H7 필수.**

검증: "다시 깨보라"(운영자) 지시대로 compact adversarial 워크플로우 4 에이전트가 정확히 `origin/codex/draft-context-workspace@29fac0a` 코드에 **실제 repro 실행**. 4/4 전부 bypass 발견.

---

## 솔직한 자기정정

내 직전 메시지에서 v2를 manual read로 "sound"라고 높은 확신으로 판단했는데 — **그건 *프롬프트 축*만 보고 틀렸다.** instruction==상수 경로는 맞게 닫혔지만 **unpinned 컨테이너로 raw FGP prose가 *커밋 파일*에 박히는 축**을 못 찔렀다. 운영자가 "Claude가 다시 깨보게 하라"고 한 직감이 정확히 이걸 잡았다. 독립 adversarial 에이전트의 값어치.

---

## v2가 진짜 닫은 것 (크레딧 — refuted 벡터로 확인)

내 round-1 H1~H4가 v2에 제대로 구현됨. 다음 공격들 **올바르게 거부** 확인:
- nested `policies.raw_fgp_text_in_writer_prompt='allowed'` → `fgp_route_invalid` ✅
- instruction에 prose → `task_instruction_invalid`(상수 정확일치) ✅
- **원래 걱정한 writing_guidance prose 채널 이중 차단**: scaffold append가 instruction을 상수에서 벗어나게 + `writing_guidance_scaffold` 키 추가 → `task_shape_invalid` ✅
- result(`paragraph_md`/`final_paragraph_md`)에 prose → `fgp_result_drift`(recompute 방어) ✅
- 추가 .md/subdir 파일 → `unexpected_surface_file` / 무확장자 → `surface_extension_invalid` ✅
- unicode/ZWSP → `instruction_invalid` · Windows 케이스충돌 → FS가 같은 inode 덮어써 parse fail ✅

**즉 writer-프롬프트 축은 derivation으로 견고.** 좋은 작업.

---

## 여전히 열린 것 — 커밋/relay-surface 축 (4 라이브 bypass, 전부 valid=yes + 커밋파일에 verbatim FGP prose)

| # | 운반체 | 왜 안 막힘 | repro |
|---|---|---|---|
| B1 | **`source_layer_route_config` 내용** | 체커가 키 존재는 강제(top-level exact key-set)하지만 **내용은 한 번도 검증 안 함** — `validate_source_layer_route_config`를 **아예 호출 안 함**. `validate_writing_task`는 이 필드를 조용히 **drop**. | valid=yes, fgp_route_task.json에 prose |
| B2 | **`fgp_route_config` nested 미지의 키** | `validate_fgp_route_config`가 **어느 레벨에도 closed-key-set 검사 없음** — `policies.*`/`routes[i].*`/새 top-level 키 prose 무시하고 통과 | valid=yes |
| B3 | **manifest extra 키** | `_check_manifest`가 열거된 키만 보고 **no-extra-key 거부 없음**. `operator_notes`/`route_policy.leaked_guidance_text`에 prose → **`FGP_LOCAL_ABLATION.safe.json`("safe" 인증 표면!)에 박힘** | valid=yes (CLI exit 0) |
| B4 | **`run_id` prose** | non-empty string만 체크, charset/length cap 없음 → task_id/draft_id/session_id에 verbatim 흐름 | valid=yes |
| B5(2차) | **NTFS ADS** (`baseline_task.json:fgp_guidance`) | `rglob`이 ADS 스트림 미열거 | valid=yes (`dir /r`로 보임; git/cp는 strip하나 native copy/robocopy는 보존) |

**통합 근본원인 (한 줄)**: 체커가 **스칼라/constraints는 *값*으로 핀**(`constraints==_EXPECTED_CONSTRAINTS`, `instruction==상수`)하지만 **route-config 블롭·manifest 컨테이너는 *키 존재*만 요구하고 값/nested 내용을 안 핀다.** + `validate_*` 들이 미지의 키를 **거부 안 하고 조용히 무시**. → **"이름으로 요구하지만 값으로 핀 안 한 키는 전부 prose 밀반입 채널."**

**심각도 (정직)**: 오늘 = **커밋/relay-surface copyright leak**(invariant "must never land in a committed/relayed surface" 절반 위반 — 체커가 raw FGP prose 든 커밋 JSON에 valid=yes 도장). writer-프롬프트 절반은 오늘 안 깨짐(synthetic_run이 이 필드 무시). **단 다음 prose-ablation 단계가 이 unpinned 필드를 프롬프트 컨텍스트로 읽는 순간 직접 프롬프트 인젝션으로 격상.**

---

## 하드닝 (prose 단계 전 must-fix)

- **H5 (primary): unpinned 컨테이너를 *값*으로 핀** (constraints== 방식 미러):
  - 체커: `fgp_route_config`를 `fgp_route_config_to_payload`로, `source_layer_route_config`를 `source_layer_route_config_to_payload`로 **재직렬화해서 on-disk == canonical** 요구. (지금 `validate_source_layer_route_config` 자체를 호출 안 함 — 추가.)
  - manifest: 미지 키 거부(exact-key-set, `route_policy`/`task_summary`/`safety_attestation` 재귀) **또는** manifest 전체를 재도출해 == 요구.
  - `run_id`: `^[A-Za-z0-9._-]{1,64}$` 강제.
- **H6: validator들이 미지 키를 *거부*하게** (defense-in-depth + task JSON 소비하는 모든 미래 runner 보호): `validate_writing_task` top-level 미지키 거부; `validate_fgp_route_config`/`validate_source_layer_route_config` nested closed-key-set(후자는 지금 `.get()`로 무시).
- **H7: `json.loads(object_pairs_hook=...)`로 중복 키 거부** — 중복 instruction 키는 오늘은 안전(stdlib last-wins, 체커·writer 동일 파서)이나 first-wins 파서 쓰는 미래 writer에서 divergence. 선제 차단.
- **H8 (낮음/플랫폼): NTFS ADS** — expected 파일마다 $DATA 스트림 정확히 1개 assert, 또는 "인증 표면은 stream-stripping transport(git/cp)로만 relay" 문서화. transport-conditional이라 우선순위 낮음.

**원칙(round-1에서 이어짐)**: denylist(path/secret regex)는 prose를 구조적으로 못 본다 → **커밋 표면은 allowlist**: 모든 값이 체커-재계산가능/enum/count, free-text 채널은 거부. round-1은 이 원칙을 *instruction 축*에 적용했고, 이번엔 *컨테이너/표면 축*에 마저 적용해야 함.

---

## 다음 순서

Codex H5~H7 빌드 → 내가 round-3 재검증(같은 5 운반체 + B1~B4 RED 테스트 통과 확인) → 그 다음 외부-writer ablation. **지금 prose ablation 금지** (커밋표면 leak 열린 채 진행 금지).

(read-only 리뷰 · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 워크플로우 산출물=로컬 `.scratch/`(gitignore). 비용: 4 에이전트·~474k 토큰, 이전 41개 대비 경량.)
