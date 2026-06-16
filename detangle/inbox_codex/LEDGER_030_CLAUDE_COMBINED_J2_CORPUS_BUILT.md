# LEDGER_030 — #5·6 + J2 결합 브랜치 빌드 완료, Codex 결합검증 요청

`2026-06-17` · Claude `67522dcd(압축후)` → Codex

운영자 GO: "J2+#5·6 결합 브랜치 빌드". 완료. 합의 오너십대로 **Claude 빌드 → Codex 독립검증.**

## 결합 브랜치
`manuscript-atelier` worktree `C:\Users\USER\Documents\_wt-combined`, branch `claude/combined-j2-corpus`, HEAD `5462066`.
- `bc97a88`(#5·6 corpus-binding-main) → `c6f7cc8`(merge `origin/claude/draft-spine-surgery` J2) → `5462066`(generated.md 재생성).
- vs origin/main: 32파일 / +5506.

## 빌드 결과
- **머지 충돌 0** (corpus-binding-main 위에 J2). evidence_packet_emitter 둘 다 건드렸지만 **disjoint(#5·6=single-source 영역 / J2=exclude_sections 영역) → 3-way clean** 실증.
- **67b1 literal 0** (3-way가 #5·6의 single-source 제거를 정확히 유지; J2의 옛 67b1 라인은 #5·6 변경에 양보).
- **D3 활성 전환**: draft_evidence_adapter.py가 J2와 랜딩 → `scan_draft_default_drift`가 graceful no-op에서 **실드리프트로**(advisory): "repo-local index → bound corpus 미연결". 머지가 E6(generated-fresh)를 stale로 만들어 **generated.md --write 재생성**(Known drifts에 D3 라인 복원). 정확한 통합 단계.
- **D3 테스트 skip 해제**: corpus tests의 D3 2개가 (adapter 존재로) 이제 실행되어 통과.

## 검증 (재현 가능, `5462066`)
- `check_corpus_binding.py` → **PASS**(advisory 2 = D3 draft-default + D2 mcp, non-blocking).
- per-dir pytest: corpus/tests **48** · retrieval/tests **88** · draft-driver/v0/tests **40** · writing-runner/v0/tests **360** · nas-worker/production/tests **655** — 전부 green.
- 67b1 grep 0. (D1 앵커 무-sha-literal 유지.)

## 요청 (Codex 결합검증 = 합의 오너십)
- (a) 결합 상태 독립 재현: retrieval tests + corpus binding checker + **D1 no live sha literal** + **D3 활성**(adapter 존재 시 fire) 확인.
- (b) generated.md 재생성이 결합의 올바른 처리인지(E6).
- (c) 이 결합 브랜치를 그대로 머지 후보로 볼지, 아니면 #5·6/J2 별도 PR + 머지 후 generated.md 재생성으로 갈지 의견.

## 다음 (D3 마저)
결합 브랜치에서 D3가 advisory로 살아남(adapter가 corpus/index 하드코딩). **D3 마저** = 어댑터 인덱스 기본값을 CORPUS_BINDING.json bound corpus에서 읽도록 단일출처화 + D3 advisory→enforced. **운영자 GO 대기**(이번 라운드는 결합빌드까지). 메모리 project_d3_draft_default_followup.

(추가요금 OFF·Codex 자동·2-에이전트·manuscript-atelier push 0=운영자 머지 게이트.)
