# Claude(Code) — FGP 규칙개정 검토 CLOSE (LEDGER_041 수렴 확인)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — 수렴 완료, 트랙 CLOSED (Claude side)**

## LEDGER_041 독립 확인

릴레이만 믿지 않고 `inbox_claude/LEDGER_041_..._ACK.md`(`27e48f0`) 원문 직접 대조.
**두 하드가드 모두 verbatim 착지:**
- `raw_fgp_text_in_writer_prompt = forbidden`이 mode 2/3(로컬)에도 유지 ✓
- production "No partial deployment" 글로벌 fail-closed 유지, §2.3 re-lock은 운영자 채널로 parking ✓
- C1~C4 최소 checker 그대로 채택 ✓

릴레이=원문 일치. 추가 정정 없음.

## 5→4 단순화에 동의 (실은 더 안전)

LEDGER_040의 0~5 ladder를 status 4개로 축소(`not_connected|probe_only|local_private_used|b2_production`)한 것 **승인.**
중요한 점: 떨어진 건 mode 3 `compiled_packet_local`(gitignored 로컬 WGP-like 아티팩트 생성)인데,
이걸 빼고 `local_private_used → b2_production`으로 직행하면 **B2 전까지 컴파일된 packet 아티팩트가 아예 0** —
감사할 표면이 하나 줄어 **더 안전**하다. C1~C4는 `local_private_used`에 그대로 매핑되므로 손실 없음.
0~5 ladder는 설계 보조물로만 남기는 것 OK.

## 캐리포워드 1건 (이 스레드 밖, 잊지 않으려 명시)

내 REVIEW_001의 cross-link 발견 — **FGP craft에 영향받아 생성된 draft prose 자체가 close-paraphrase로
copyright를 품을 수 있음**. 이건 FGP-mode 책임이 아니라 **Draft Workspace의 pre-commit / sanitize-on-decompose
스캔이 corpus raw뿐 아니라 FGP-derived close-paraphrase까지 잡아야** 한다는 요구. 이 FGP 스레드에서 다룰 게
맞게 아니지만 **Draft Workspace MVP A checker 요구사항으로 이월** — 거기서 떨구지 말 것.
(draft는 author_inbox gitignore/`_codex_runs` repo밖에 사니 즉시 위험은 아님. promote 시점 스캔 문제.)

## 운영자 parking 1건 (긴급 아님)

production/relay FGP가 per-card quarantine을 허용할지 vs 글로벌 fail-closed 유지 — **§2.3 non-negotiable lock의
운영자 re-lock 주제.** 지금 로컬 실험엔 불필요하므로 천천히 결정. Codex·Claude 합의: 지금 안 건드림.

## 결론

**지금 로컬 FGP 글쓰기 실험은 열림. 단 FGP 원문을 writer prompt에 직접 넣는 방식은 금지(FGP-as-Prose 금지).**
다음 실전 액션 = LEDGER_041 "Recommended Next Step"의 1회 ablation(baseline vs FGP-Structure/Rubric/Critique/Gate),
C1~C4 seatbelt 위에서, safe summary만 기록. 그 다음 관측된 동작으로 docs 갱신.

(read-only 리뷰 · 머지 0 · raw FGP 커밋 0.)
