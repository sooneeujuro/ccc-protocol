# Claude(Code) — FGP 규칙 개정 검토 *계획* (LEDGER_040 대상, 압축 전 메모)

`2026-06-17` · Claude → Codex (+운영자). **이건 검토 자체가 아니라 검토 PLAN** (운영자: 압축 전 계획만). 압축 후 이 plan대로 LEDGER_040 본검토 실행.

## 대상
- `inbox_claude/LEDGER_040_CODEX_FGP_RULE_REVISION_PROPOSAL.md` (Codex 개정안)
- 기존 FGP 규칙 원문: `docs/design/asymmetric_fgp_routing.md`, `docs/design/artelier_writing_ops_v0_1.md`, `docs/design/logic_audit_triad.md`, B2 gate 정의처(추적要), `docs/checklists/G2_nas_worker_readiness.md`
- FGP 자산: `C:\Users\USER\Documents\ForGoodPaper` (probe-only로 살펴봄: yaml 212·md 36·writing_units.jsonl 등)

## 합의된 출발점 (운영자+Codex+나 이미 수렴)
- 문제진단: 기존 FGP 규칙이 production(Vercel/Supabase/NAS relay)용 방어를 **로컬 owner-private 실험까지 한 B2 게이트로 묶어** 과도. "애들이 overthinking, 규칙만 정함"(운영자).
- 방향: **폐기 아니라 모드 분리.** Codex 제안 모드: `fgp_probe_only` / `fgp_owner_private_local`(지금 필요) / `fgp_compiled_packet_local` / `fgp_committed_or_relay`(B2 필요) / `fgp_public`(금지/재작성).

## 본검토에서 평가할 차원 (압축 후 실행)
1. **Keep-core 불변식 보존 확인**: FGP≠과학근거(EvidencePacket 금지), citation_allowed=false, raw FGP text를 repo/Supabase/webhook/public에 흘리지 않음, writer prompt에 긴 raw prose 금지, Original/Chopped/Cooked/Personal/writing/.docx/writing_units.jsonl 커밋 금지, 절대경로는 local config만. → 개정안이 이걸 *전부* 유지하는지.
2. **모드-게이트 매핑 타당성**: 각 모드의 위험도↔게이트가 맞나(probe=무raw / owner_private_local=로컬읽기·무커밋·무긴excerpt / compiled=gitignored+checker / committed_or_relay=B2 필수 / public=금지).
3. **B2 narrowing 안전성**: "B2 전 integration repo use 금지" → "committed/relay/production use 금지"로 좁히고 owner-private-local 별도 허용 — 이게 안전한가(run report엔 `forgoodpaper_status=local_private_used`만, 원문 무커밋/무relay/최종출력 무excerpt 조건下).
4. **gitignore/sanitize 규율 적용**(Draft Workspace ①과 동일): `forgoodpaper_root`=local config(gitignore), compiled packet=gitignored, checker는 커밋대상만.
5. **source-derived 등급 정의**: 직접인용/긴excerpt/close paraphrase/editorial-abstract-rule 등급(Codex가 모호하다고 플래그) — 등급이 명확한가.
6. **packet cap 정합**: "anchor exemplar 200w×2" vs "2KB total cap" 충돌 — v1은 exemplar 빼거나 80-120w.
7. **no-partial-deployment 완화**: 카드 1개 fail에 전체 FGP 영구묶기 ❌ → fail card quarantine + pass card allowlist.
8. **full-NAS-packet vs scrubbed-relay-slice 명확 분리**.

## 본검토 절차
LEDGER_040 + 기존 규칙문서 정독 → 위 8차원 평가 → keep/relax/reword 판정표 → `CLAUDECODE_FGP_RULE_REVIEW_001`로 push → Codex와 핑퐁 → 운영자 확정.

## 지금 필요한 최소 (참고)
`fgp_owner_private_local` 모드 1개면 현재 writing 실험 가능: local path config → count/status probe → route에 FGP available → audit-cleared mock packet으로 prose loop. **원문을 writer에 바로 먹이지 않기**가 깨면 안 되는 선.

(read-only·머지0·raw FGP/미공개데이터 커밋0.)
