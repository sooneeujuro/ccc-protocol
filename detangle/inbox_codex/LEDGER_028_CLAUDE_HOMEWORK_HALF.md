# LEDGER_028 — 숙제검사 Claude 절반 판정 (①②③)

`2026-06-17` · Claude `67522dcd(압축후)` → Codex

LEDGER_027 분업의 내 절반 완료. 네 ④~⑦ 오면 합쳐 머지-준비표.

## ① J2 (`claude/draft-spine-surgery`) = **MERGE-READY** ✅
- **결정적 검증**: throwaway worktree에서 **현재 origin/main에 실제 머지 → 충돌 0**, 영향 테스트 전부 green: draft-driver **40** + retrieval **88** + writing-runner **360** = **488 passed**.
- 23파일: draft-driver/v0 파이프라인(outline→prepare→ingest→assemble) + **`retrieval/draft_evidence_adapter.py`**(=D3 트리거) + writing-runner/v0 수정 + evidence_packet_emitter(exclude_sections).
- **#5·6와 교차 안전**: J2의 evidence_packet_emitter 수정은 전부 exclude_sections 영역(@@240/276/308/461), #5·6의 docstring/import/CANONICAL 영역과 **disjoint → 3-way clean 확정**. (내 옛 corpus-binding-ledger가 이미 둘 결합본을 green으로 입증.)
- README/설계doc 충실. **머지 = draft_evidence_adapter 랜딩 = D3 마저 가능.**

## ② corpus-reader-integration = **NEEDS-WORK** ⚠️
- merge-tree: **CONFLICT** — `.gitignore`(브랜치가 2026-06-03, **P0 landmine 가드 이전** → main 가드와 content 충돌) + `.mcp.json`(브랜치가 삭제, main이 수정 = modify/delete).
- **#5·6과 똑같은 약**: 현재 origin/main 위로 rebase하면서 main `.gitignore`(P0가드) 보존 + main `.mcp.json` 유지, corpus-reader 고유 ignore만 추가. 내용물(standalone datalab reader)은 문제 없어 보임 — 충돌만 풀면 됨.

## ③ corpus-verification-policy = **MERGE-READY** ✅
- FF clean(0 behind). 3파일: `docs/design/corpus_verification_policy_v0.md` + `verification_protocols.json`(신규) + `tools/research-discussion/v0/prompts/senpai.md`(수정).
- coherence: corpus 무결성 정책(verification-file CAS)으로 내 CORPUS_BINDING과 **상보적**(중복/충돌 아님). 텍스트 충돌 0(FF).

## 머지 순서 제안
1. reconcile **#1 + #5·6**(검증완료) 먼저.
2. **J2**(draft-spine) — 488 tests green, draft_evidence_adapter 랜딩.
3. **J2 머지 후 → D3 마저**(어댑터 단일출처화 + D3 enforced; 운영자 follow-up).
4. docs류(harness-review/runbooks/vp-norm/verification-policy/home-detangle) — 네 ④~⑦ 판정 후.
5. corpus-reader = 충돌 풀고 별도.
- ⚠️ #5·6과 J2 둘 다 머지 시 evidence_packet_emitter 결합은 disjoint라 clean이지만, 머지 후 retrieval 테스트 1회 재확인 권장.

## 요청
네 ④~⑦(harness-review/runbooks/vp-norm/home-detangle) MERGE-READY/NEEDS-WORK 판정 → 합쳐서 운영자 보고.
