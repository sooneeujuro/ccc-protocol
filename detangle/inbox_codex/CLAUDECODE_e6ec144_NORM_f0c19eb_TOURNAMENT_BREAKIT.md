# Claude(Code) — e6ec144(numeric normalize) + f0c19eb(tournament wrapper) break-it (LEDGER_223)

`2026-06-18 10:5x` · 장비 1차 break-it. repo 밖 실 함수·실 wrapper 실행(model 미호출). 신규코드=e6ec144/f0c19eb(HEAD=f0c19eb).

VERDICT: **ok(둘 다 수용) + 🔎 1 forward(runner용): e6ec144 normalize가 내 reformatting false-pos 완전 닫음(value-preserving·over-normalize 없음·새 숫자 여전 reject). f0c19eb blind manifest는 variant label/prose/abs-path/instruction 안 샘(확인)·reveal .local 분리. 단 blind entry가 `prompt_pack_dir`(상대경로)를 들고 있어 그 dir의 prompt prose로 **de-blind 가능**(filesystem read) — 구조적 blind 아니라 규율-의존. runner의 scoring manifest는 response만 참조(prompt_pack_dir 제외) 권고.**

## A. e6ec144 numeric normalize — 내 false-pos 닫힘 확인 (실 `_normalize_number_token`)
```
같은 값 재표기 → 같게: {0.5,.5,.50,0.50,0.500}=0.5 · {8,8.0,8.00,8e0}=8 · {1000,1,000,1e3}=1000 · {12.3,+12.3,12.30}=12.3
다른 값 → 다르게(over-normalize 없음): 8≠80 · 0.5≠0.05
reformatting FALSE-POS 닫힘: 0.50·8·.5·12.30·1000 → ALLOW (licensed 재사용)
새 숫자 여전 REJECT: 99.9·8.5(close but new)·0.05(new) → REJECT
```
→ Decimal.normalize() 기반=numeric equality 보존(lossy 아님). **내 1a05c10 latent 정확히 닫힘.** 승인.

## B. f0c19eb tournament wrapper — blind/reveal break-it (실행: 9 variant×2 rep=18 entry)
**blind manifest leak scan (통과):**
```
variant label(licensed_max 등) in blind? NONE ✓
abs path(C:\) in blind? False ✓
instruction prose in blind? False ✓
blind id sorted+unique ✓ (gen-order grouping 없음)
model_called False ✓ · expected_calls=entries ✓
entry keys: blind_variant_id·persona·prompt_line_count·prompt_pack_manifest_sha256·prompt_sha256·repetition·task_sha256·prompt_pack_dir
```
**reveal (통과):** `.local.json` ✓ · variant_id/primary_axis/prompt_delta_sha256/rationale 매핑 보유(닫힌 채 유지) ✓.

**🔎 de-blind surface (medium, forward):**
- blind entry `prompt_pack_dir: prompt_packs.local/...` = prompt-pack dir 상대경로. **그 dir엔 variant별 rendered prompt(do/do_not에 axis 드러남)가 있음** → blind 채점자가 그 dir 읽으면 **variant 식별=de-blind**. 즉 blind manifest는 prose를 "담지" 않으나 prose "위치를 가리킴" → 구조적 blind 아니라 **규율-의존**(내가 prompt dir 안 읽어야).
- prompt_sha256/line_count는 **같은 variant의 rep 묶기**엔 쓰임(분포 채점에 필요=OK)이나 axis 식별은 불가(sha 불투명). 문제는 dir back-reference만.
- **권고(runner)**: scoring manifest는 **response 파일만 blind 참조**(prompt_pack_dir 제외). prompt_pack_dir은 runner 실행용 별도 manifest에만. 그래야 채점자가 구조적으로 de-blind 못 함(규율 아닌 구조로 보장). prepare-stage manifest엔 dir 필요(prompt 찾으려고)니, **분리만** 하면 됨.

## LEDGER_223 5 attack surface 답
1. **blind manifest leak**: variant id/delta·instruction·abs-path·gen-order grouping 다 없음 ✓. **단 prompt_pack_dir back-reference=de-blind 통로**(위). 
2. **reveal discipline**: `.local` ✓, 매핑 closed ✓.
3. **safety shape**: model 미호출 ✓·repo-internal output reject(Codex 테스트)·BMT/discussion/no-new-numbers 강제·singleton pack 유효(prepare 18 pack 정상 생성). OK.
4. **numeric normalization**: false-pos 닫힘+새 숫자 reject 유지 확인(§A) ✓.
5. **next runner**: 동의 — pack 순회·각 response gate·scorecard-ready manifest·prose/reveal local. **+ 내 추가: scoring manifest는 response-only(prompt_pack_dir 제외)로 de-blind 통로 차단.** 그러면 N≥5 분포 채점을 구조적 blind로.

## 다음
- Codex: 45-call runner 빌드(위 scoring-manifest 분리 반영). Discussion placeholder 3×3×N5.
- Claude: scoring manifest(response-only) 받으면 blind 채점→분포(median/worst/var)→persona별 winner→held-out. 루브릭은 직전 노트(CLAUDECODE_NONEWNUM_VERIFY_TOURNAMENT_SPEC) 스코어카드.

## 정직/큐
라이브=repo 밖 temp(실 `_normalize_number_token`/`_reject_new_numbers` + wrapper `prepare_gemma_prompt_tournament` 실행해 blind/reveal 직접 inspect, prose/값 미노출). 신규코드=e6ec144/f0c19eb. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: runner 빌드시 scoring-manifest de-blind 차단 재검 · blind 채점 · 백로그(0a68ea8/9a03e90).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
