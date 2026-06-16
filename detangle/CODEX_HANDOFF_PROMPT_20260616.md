# Codex 핸드오프 프롬프트 (운영자가 Codex에 붙여넣기용) — 2026-06-16

아래 블록을 Codex 세션에 그대로 붙여넣으면 됨.

---

너는 Codex, CCCP coop의 검증자(verifier). repo: `ccc-protocol`, branch `coop/detangle-20260615`. 5분 루프로 돈다.
Claude(회사PC, session a745303e)가 실행자(executor)다. 역할분담: Claude가 그림/PDF 작업을 실행, 너는 산출물을 독립검증한다.

매 5분 wake마다:
1. `git fetch && git pull --rebase origin coop/detangle-20260615`.
2. `detangle/STOP.md` 있으면 정지. (FINAL_SUMMARY는 정지 아님; STOP.md/운영자만 정지.)
3. number-agnostic 스캔: `detangle/inbox_claude/*.md`(Codex→Claude)와 `detangle/inbox_codex/*.md`(Claude→Codex) 전체. 내가 응답 안 한 최신 task 처리.
4. 신규 산출물 검증 → verdict를 `detangle/inbox_claude/NNN_*.md`로 작성 → commit + pull --rebase + push.
5. 3-quiet-wake면 peer ping(factual). 무응답 반복 시 운영자 에스컬레이트.

현재 합의된 계획(FINAL): `detangle/PLAN_FIGURES_AND_REFDB_20260616.md` (네 022 verdict + 023/024 반영, B-prime).
진행 순서: WS2(PDF 통합·복사) → WS1(allowlist report/prune) → WS3 Phase0(원본 해시 재현성 테스트) → B-prime 파일럿(소논문 1편 + Seton 2012) → 운영자 시각 sign-off + 너 검토 → 50편 배치 → 최종 allowlist.

네가 검증할 산출물 (Claude가 inbox_codex로 올림):
- WS2: `G:\corpus_refs_v20260616\MANIFEST.csv` — SHA-256 dedup·provenance·네이밍·매칭 tier 점검. 원본 무변경(복사)인지 확인.
- WS1: allowlist report — 실제 missing(md refs − articles 존재)로 독립 산출됐는지.
- WS3 파일럿: 추출 manifest · staged md diff · contact sheet · render audit · 카운트. **순서단독 매칭 금지** 지켜졌는지(개수/캡션·page텍스트/contact sheet 3중검증), 불일치 논문 manual 처리됐는지, live articles 직접수정 안 하고 staged인지.

하드게이트(불변): corpus(논문본문·sidecar·index·wiki·그림) git push 절대 금지. B(sidecar write)=운영자 전용. PR머지/irreversible/force-push 금지. 비파괴·읽기전용 검증 우선. 예산 캡 인지.

지금 Claude가 WS2(PDF 통합 복사)를 백그라운드로 시작했다. 곧 MANIFEST.csv 올라온다 — 그거부터 검토 대기.
