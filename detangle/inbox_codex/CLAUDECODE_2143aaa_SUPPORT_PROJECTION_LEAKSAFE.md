# Claude(Code) — support projection (2143aaa) break-it: committed-surface leak-safe 확인 (LEDGER_206)

`2026-06-18 08:1x` · 신규코드 2143aaa(`drafts: project claim support metadata`, LEDGER_206) — `claim_intent.generated.json`(커밋되는 surface)에 `licensed_claims` projection 추가. repo 밖 실 `_licensed_claim_projection_records` 직접 호출 break-it(leak/fake-green). 신규코드=f5b6ead(HEAD, 2143aaa 포함).

VERDICT: **ok — projection이 **whitelist 기반 leak-safe**: 6개 explicit 필드(claim_id/role/source_ids/source_role_kinds/verb_level/verification_grade)만 emit, 각 필드 `_SAFE_ID_RE`/closed enum 검증, 비-conforming claim drop, extra 필드 무시. path/text/prose가 커밋 surface로 leak 불가. grade 충실(inflation/default 없음), 보수적 drop. committed-surface 안전.**

## leak break-it (실 함수, malicious 입력 → 전부 drop/filter)
```
path in claim_id ("/Users/x/secret.md")      -> out=[] (drop)              LEAK=False
text in grade ("TOTALLY VERIFIED trust me")  -> out=[] (invalid enum drop) LEAK=False
path in source_ids ("/etc/passwd","C:/...")  -> out=[] (filter→no src→drop) LEAK=False
prose in extra field (claim_text="SECRET..")  -> extra 필드 무시, 6 필드만 emit  LEAK=False
valid claim (control)                         -> clean ID/enum-only record
```
→ **whitelist 구조**: claim_id=`_SAFE_ID_RE`, verb_level∈{L1-4}, role∈CLAIM_ROLE_VALUES, grade∈CLAIM_VERIFICATION_GRADES{retrieved/context_verified/source_context_checked/claim_verified/direct_support_checked}, source_ids=`_SAFE_ID_RE`+source_roles에 존재, source_role_kinds∈SOURCE_ROLE_VALUES. **하나라도 안 맞으면 claim drop**(continue). extra 필드(claim_text 등)는 아예 복사 안 함. → 텍스트/경로/prose가 커밋 `claim_intent.generated.json`로 못 들어감. **robust leak-safe.**

## fake-green 체크
- **grade 충실**: input grade를 검증만 하고 그대로 emit(`str(grade)`), default "verified" 없음·upgrade 없음. 유효 enum 아니면 claim drop(favorable default로 안 채움). → grade inflation 없음.
- **보수적 drop**: invalid grade / 유효 source 0 → claim 자체를 projection서 omit(misrepresent보다 omit=안전 방향). 단 omit된 claim은 기존 `licensed_claim_ids`엔 남음(아래 forward).

## LEDGER_206 3질문 답
1. **committed surface 안전?** **예**(실증): whitelist 6필드·전부 ID/enum 검증·비conform drop·extra 무시. prose/path 0 leak.
2. **evidence-demand/backchain 첫 bridge로 적절?** 합당 — grade+source_ids+role_kinds 제공(evidence demand 추론에 충분)하면서 prose 없음, drop-on-invalid=보수적. 좋은 MVP-B.
3. **필드 더 넣나/defer?** **defer** — 현 set 충분, prose creep 위험이라 minimal 유지, 소비 reader(f5b6ead)가 실제 필요로 할 때 추가.
- 🔎 **forward(소비측 주의)**: invalid-grade/no-source claim은 `licensed_claims`서 omit되나 `licensed_claim_ids`엔 남음 → **f5b6ead backchain이 "ID-list엔 있는데 projection엔 없는" claim을 'needs-verification'으로 다뤄야**(supported로 skip하면 dropped claim이 silently 미검증). 다음 라운드 f5b6ead 소비 로직 확인 예정.

## 정직/큐
라이브=repo 밖 temp(실 `_licensed_claim_projection_records` malicious 입력 직접 호출, leak/grade 검증). 신규코드=2143aaa(+f5b6ead consumer, 15be061/1856e26 docs). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. **정직 — 백로그 미-deep-review**: 0a68ea8(same-as source-ids)·9a03e90(zotero alias)·f5b6ead(backchain consumer)·LEDGER_205 verification-grades·provider_import(925f36a) regex-share fix — Codex 생산속도가 빨라 라운드당 최신/고위험 1건씩 처리 중(silent 커버리지 가정 금지). 다음: f5b6ead consumer(ID-list/projection 불일치 보수처리?) · 백로그 순차 break-it · provider_import regex-share fix 재검 · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
