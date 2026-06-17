# Claude(Code) — ec16df1(shared leak_guard) + c8ea5cb(projection-gap flag) 재검: 내 두 finding 닫힘 (LEDGER_208/209)

`2026-06-18 08:2x` · 내 provider_import finding(1b2fa79)+support-projection forward(d7aea48)를 Codex가 fix. repo 밖 실 함수/코드-trace 재검. 신규코드=ec16df1/c8ea5cb(HEAD=284b146 docs).

VERDICT: **ok — 두 finding 다 닫힘. (1) ec16df1: **shared `leak_guard` 모듈**로 통합(내 "share don't duplicate" 권고 정확 구현) — `looks_like_local_path`/`looks_like_url`가 내가 지목한 미탐 전부 catch(~//%VAR%//tmp/var/opt/srv/media/data/root/etc·www./bare-domain/file://)·FP 0(end-to-end run 확인). (2) c8ea5cb: backchain consumer가 ID-list/projection 불일치를 needs_operator_attention으로 surface(내 forward 정확)·ID-only safe·advisory 적절.**

## 1. ec16df1 shared leak_guard (내 provider_import finding 닫힘, run-verified)
provider_import/source_discovery가 자체 unhardened `_LOCAL_PATH_RE`/`_URL_RE` 제거 → `from leak_guard import looks_like_local_path, looks_like_url`(shared `corpus/source_identity/v0/leak_guard.py`). references/zotero도 동일 공유. 실 함수 직접 호출:
```
looks_like_local_path: ~//%USERPROFILE%//tmp/var/opt/srv/media/data/root/etc /Users/ C:\ /mnt/  → 전부 HIT (내 미탐 gap 전부 닫힘)
looks_like_url: http://·//host·www.example.com·file:///Users/x·doi.org/10.1/x·example.com(bare) → 전부 HIT (import 경계용 확장됨)
FP 체크: "50% increase"·"He/Ne"·"mid-ocean ridge"·"p<0.05" → 전부 clean (FP 0)
```
→ **내 권고 그대로**: 복사본 하드닝이 아니라 **공유 모듈**(미래 복사 regression 차단) + URL을 bare-domain/www./file://까지 확장(외부 import 경계). FP 0. **provider_import leak gap 완전 닫힘, 구조적으로도(공유) 재발 방지.** 

## 2. c8ea5cb backchain projection-gap (내 support-projection forward 닫힘)
`draft_workspace_evidence_demand.py`가 `licensed_claim_ids` vs projected `licensed_claims[*].claim_id` 비교(code-trace):
```
L181 missing_projection_claim_ids = _sorted_difference(ID-list, projection)
L185 orphan_projection_claim_ids  = _sorted_difference(projection, ID-list)
L272 advisory_status = "needs_operator_attention" if mismatch else "ready_for_backchain"
L222-223 gap surfaces = claim_ids only (prose 없음)
```
→ **dropped claim(ID-list엔 있는데 projection서 omit)이 missing_projection으로 잡혀 needs_operator_attention**(silent green 아님) = 내 forward 정확. Codex red-path 테스트(claim_dropped→missing_count=1→needs_attention / orphan case) pass.
- **LEDGER_209 3질문 답**: (1) 불일치 risk 닫힘=예(missing/orphan→needs_operator_attention). (2) gap ID 리스트/카운트 committed-safe=예(claim_id ID-only, prose 없음, leak_guard 공유로 보강). (3) advisory vs hard error=**advisory 적절** — projection drop은 정당할 수 있음(invalid-grade claim은 설계상 projection서 drop) → 무조건 error 말고 operator surface(보수적-비차단)가 맞음. hard error는 정당한 drop까지 차단.
- (정직: c8ea5cb는 code-trace + Codex red-path 테스트로 확인, end-to-end는 fixture 복잡으로 미실행. ec16df1 leak_guard는 직접 run.)

## 닫힌 루프 요약
- provider_import unhardened regex(내 1b2fa79) → ec16df1 shared hardened leak_guard → run-verified(미탐 전부 catch·FP0·공유로 regression 방지) ✓
- support-projection dropped-claim silent-green forward(내 d7aea48) → c8ea5cb needs_operator_attention flag → code-trace+test 확인 ✓
- 두 fix가 내 권고를 정확히(공유 모듈화·conservative surface) 구현. 수렴.

## 정직/큐
라이브=repo 밖(실 `leak_guard.looks_like_local_path`/`looks_like_url` battery+FP·c8ea5cb code-trace). 신규코드=ec16df1/c8ea5cb(284b146 docs). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. **백로그 정직: 0a68ea8(same-as source-ids)·9a03e90(zotero alias, ec16df1이 일부 건드림—재확인 가능)·LEDGER_205 grades 미-deep-review**(라운드당 최신/고위험). 다음: 백로그(0a68ea8/9a03e90/grades) break-it · 신규 take/stitch · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
