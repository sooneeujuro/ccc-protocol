# Claude(Code) — 9143656 tournament blind-split 재검: 내 de-blind finding 구조적으로 닫힘 (LEDGER_224)

`2026-06-18 11:0x` · 내 prompt_pack_dir de-blind finding fix(9143656) 재검. repo 밖 wrapper 실행해 3 surface 직접 inspect(model 미호출). 신규코드=9143656(HEAD).

VERDICT: **ok — de-blind 통로 구조적으로 닫힘. BLIND.safe.json에 prompt_pack_dir·prompt_packs.local·abs-path·variant-label 전부 없음(entry=blind_id/persona/hashes/counts만) → 채점자가 blind surface만으론 prompt prose 접근 불가=구조적 blind(규율-의존 아님). EXECUTION.local(blind_scoring_surface=false, dir=runner전용)·REVEAL.local(closed) 분리 확인.**

## 검증 (실 wrapper 실행, 3 surface inspect)
```
BLIND.safe.json:
  'prompt_pack_dir' in blind?      False ✓   (내 finding의 통로 제거)
  'prompt_packs.local' in blind?   False ✓
  abs path / variant label?        없음 ✓
  entry keys: blind_variant_id·persona·prompt_line_count·prompt_pack_manifest_sha256·prompt_sha256·repetition·task_sha256
EXECUTION.local.json: exists, blind_scoring_surface=False, prompt_pack_dir 포함 (runner 전용=blind 아님) ✓
REVEAL.local.json: exists, closed (blind→variant 매핑) ✓
```
→ **내 직전 de-blind finding(blind이 prompt_pack_dir로 prose 가리킴) 정확히 닫힘.** 이제 blind은 "내가 prompt dir 안 봄" 규율이 아니라 **구조**(blind surface에 경로 자체가 없음)로 보장. 채점자가 물리적으로 de-blind 불가.
- prompt_sha256/line_count는 blind에 남으나 **같은 variant의 rep 묶기용**(분포 채점에 필요)이고 axis 식별 불가(sha 불투명) — 통과(feature, 누수 아님).

## 토너먼트 장비 상태 = 수용
normalize(e6ec144) + blind manifest 누수 0 + de-blind 구조 차단(9143656) + execution/reveal 분리 + reps→분포 채점 가능. **장비 검토 완료, 45-call 진행 OK**(operator GO 대기 — Ollama 업데이트 중이라 Codex hold 적절).

## 다음
- operator GO 후 Codex 45-call runner 실행 → 각 response real gate → blind scoring manifest(response-only) emit.
- Claude: blind manifest 받으면 변별(루브릭=CLAUDECODE_NONEWNUM_VERIFY_TOURNAMENT_SPEC), variant→prompt reveal은 채점 완료까지 안 봄. persona별 winner(median−λvar−μ(2−worst), pass≥4/5, best-of 금지)→held-out.

## 정직/큐
라이브=repo 밖 temp(실 `prepare_gemma_prompt_tournament` 실행, 3 surface 직접 inspect, prose/값 미노출). 신규코드=9143656. manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 다음: operator GO·45-call run blind 채점 · 백로그(0a68ea8/9a03e90).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
