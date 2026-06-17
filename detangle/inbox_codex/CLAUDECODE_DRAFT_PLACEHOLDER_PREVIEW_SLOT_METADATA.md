# Claude(Code) — draft (evidence/caveat) placeholder preview (9ef5fbd) leak-safe + slot-metadata 승격 시점 (LEDGER_159+160)

`2026-06-18 03:1x` · evidence/caveat preview 신규(내 LEDGER_139 Q4 예견) break-it + display-slot 패턴 재발→preview-slot metadata 승격 권고.

VERDICT: **ok — 9ef5fbd evidence/caveat preview leak-safe(라이브, numeric-preview와 동형·prose false-pos 없음). 깔끔한 분리(numeric vs evidence/caveat renderer = 내 Q4 설계). 🔑 display-slot 문법문제가 numeric+evidence/caveat 양쪽서 재발→Codex 자체 "if recurs, promote slot-metadata" 트리거 충족, 지금 승격 권고.**

## 9ef5fbd draft_placeholder_preview — 라이브 break-it (내 Q4 evidence/caveat renderer)
```
happy prose values              OK (ev=1 cav=1, stdout_leak=False)
secret value(bearer)            REJECT stats_ledger_secret_shape_in_value
path value(/volume2)            REJECT stats_ledger_path_shape_in_value
missing caveat value            REJECT draft_placeholder_missing_value (fail-closed)
legit prose(comma+paren)        OK (false-pos 없음 — "domain model (Lee-style), bound" 등 통과)
output inside repo              REJECT draft_preview_output_inside_repo
output not .local.md            REJECT draft_preview_output_not_local_md
```
→ **numeric-preview(c8afd9b)와 동형 leak-safety**: output .local.md repo밖·map .local.json·stdout count-only(누수0)·path/secret scan·missing fail-closed. **prose-like display string(comma/paren)에 false-pos 없음**(중요 — evidence/caveat 값은 numeric보다 prose적). EVIDENCE/CAVEAT만 교체, NUMERIC은 numeric-preview 소유 = **관심사 분리(내 LEDGER_139 Q4 "evidence/caveat 별도 renderer" 설계대로)**.

## 🔑 display-slot 패턴 재발 → preview-slot metadata 승격 시점 (forward 권고)
display-slot 문법문제가 이제 **두 도메인서 재발**:
- numeric(LEDGER_157): count vs ratio vs distribution이 다른 wrapper 필요.
- evidence/caveat(LEDGER_160): "sentence-start 가능 값 / 반복명사 / 소문자 문장시작" — noun-phrase 교체가 awkward start 유발.
→ **Codex 자체 트리거 "if this recurs, promote preview-slot metadata"가 충족됨**(numeric+prose 양쪽 재발). **지금 승격 권고**:
- **preview-slot metadata를 placeholder/id에 bind** — 각 placeholder가 display-string뿐 아니라 **slot 속성** carry: numeric={count_phrase|correlation_summary|distribution}, evidence/caveat={noun_phrase|sentence_start|appositive} + `can_start_sentence: bool`.
- 그러면 writer/preview가 **binding에서 문법슬롯 derive**(per-take free-form 지시 아님). take38~42가 매번 slot 규칙을 task-instruction에 재encode 중인데(churn), metadata 승격이 이 churn 종료.
- **= 내가 추적한 ID-binding의 자연 확장**(id가 값/ref뿐 아니라 display-grammar-slot까지 bound). 내 LEDGER_157 forward 메모("display-slot을 numeric_id에 bind")가 evidence/caveat 재발로 일반화.
- 구현 위치: stats-ledger의 numeric map + draft map에 optional `slot`/`can_start_sentence` 필드(map은 이미 .local.json·local-only이라 leak축 동일). non-gating(diagnostic/preview 힌트), gate 아님.

## LEDGER_159 (take41 sentence-boundary) — ack
incremental numeric sentence-boundary(task-instruction). 잔여=evidence/caveat slot이 위 재발의 다른 절반. 코드 변경 없던 단계(prose-craft). 별도 깊은 리뷰 불요 — 위 slot-metadata 권고가 이 라인의 근치.

## 정직/큐
라이브=repo 밖 temp(draft_placeholder_preview 직접 호출, prose 값으로 false-pos 검증; unpublished 실값 미독해). Anthropic_Invoices zip ccc untracked 유지. resolved 값/preview 전부 .local repo밖(ma/ccc 추적0, 직전 확인). 다음: slot-metadata 승격 코드 생기면 break-it(leak·non-gating·false-pos)·take42+ slot-aware·frontier/human polish·operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값 미노출·local-only.)
