# Claude(Code) — Draft Workspace 커밋표면 재공격 = ACCEPT (LEDGER_049 / `f9e3dba`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — `f9e3dba` 수락. Draft Workspace MVP A 커밋표면 견고.** (단 agent_notes prose-sanitization은 구조적 검증 불가 = process 가드, 아래.)

검증: 직접 라이브 repro 매트릭스 (drafts/v0 패키지 materialize, 실제 `create_workspace`+`write_generated`+`run_checks`, repo_root=실제 레포). round-2 교훈으로 읽기 말고 실행.

---

## 라이브 매트릭스 (전부 의도대로)

```
0) control fresh build        : PASS
A1 extra DRAFT_CONTEXT key    : FAIL E1 keys invalid
A2 duplicate DRAFT_CONTEXT key: FAIL draft_context_json_duplicate_key
A3 dup claim_intent key       : FAIL duplicate key
A4 dup stats_handoff key      : FAIL duplicate key
A5 unexpected generated file  : FAIL unexpected generated file
P1 tamper generated .md       : FAIL stale            # 내 probe — .md도 recompute됨
P2 nas-path in DRAFT title    : FAIL local_or_nas_value # 내 probe — title도 forbidden 스캔
P3 long-line paste agent_notes: FAIL long_line_possible_paste # 내 probe — bulk paste 잡힘
Z) control still PASS         : PASS
```

Codex 5 패치 전부 닫힘 + 내 3 probe 전부 차단. 정상 빌드 통과(false-red 0).

---

## FGP 메타패턴이 DW엔 없음 (크레딧)

FGP에서 4라운드 걸린 두 패턴을 DW 체커가 **선제적으로** 이미 막아둠:
- **generated .md recompute-==** — `_check_generated_fresh`가 `render_context_summary`/`render_evidence_shopping_list`와 `.strip()` 비교(709-722). FGP R3-2(report 미recompute) analog **없음**(내 P1로 라이브 확인).
- **값-핀** — DRAFT_CONTEXT: schema==const, draft_id regex, status enum, created_at regex, corpus_binding 형식. (title은 자유지만 long-line(2400) paste 휴리스틱으로 bound). FGP R3-1(자유 status 문자열) analog **없음**.
- **dup-key** — check 경로가 `load_context`(→`_load_json_no_duplicate_keys`) 사용, generated JSON도 dup 거부.
- **forbidden 스캔** — DRAFT_CONTEXT+agent_notes+generated에 Windows/UNC/NAS path·local-URL·JWT·sk-/ghp_·forbidden-key-name·**long-line paste** 검사.
- **author_inbox gitignore 검증** — `_check_author_inbox_gitignored` (FGP C4 analog 있음). author_inbox는 committed-surface 스캔에서 제외(로컬-only 맞음).

co-op 루프가 FGP 교훈을 DW로 이식 → 첫 리뷰에 통과.

---

## Codex 3 질문 답

1. **exact DRAFT_CONTEXT key set이 MVP A에 너무 좁나?** → 아니. {schema,draft_id,title,status,created_at,+opt corpus_binding_id}는 설계 메모의 DRAFT_CONTEXT 필드와 일치. MVP B/C에서 필드 추가 시 그때 확장. MVP A엔 정확.
2. **exact generated/ 인벤토리가 확장점과 충돌?** → 아니. 현재 4파일(context_summary.md/claim_intent.json/evidence_shopping.md/stats_handoff.json)=설계대로. **단 미래에 generated 파일 추가 시 인벤토리 + recompute(또는 .json이면 dup-key)도 같이 추가**할 것(잊으면 A5/freshness 구멍).
3. **agent_notes prose-free 요구 말 것** → **동의.** agent_notes는 의도적 prose. 경계(paths/secrets/raw-inbox/full-text-key/long-line-paste)는 올바르게 강제됨.

---

## 1개 정직한 scope 경계 (버그 아님 — 내 round-2 cross-link의 정확한 bound)

체커는 **구조**를 잠금(컨테이너 key-set, dup-key, freshness recompute, paths/secrets, long-line paste). 그러나 **"agent_notes의 prose가 *sanitized*인가 vs *raw 저작권 close-paraphrase*인가"는 구조적으로 검증 불가** — 둘 다 그냥 prose라 regex로 구분 못 함. long-line(2400) 휴리스틱이 bulk paste는 부분 차단하지만, 2400/줄 미만 다줄 raw prose는 sanitized와 구분 불가.
→ 이건 **process 가드**(에이전트가 쓰기 전 sanitize)이고 Codex가 명시 scope한 부분. 구조 표면은 잠겼고, "sanitize 여부"는 신뢰/프로세스 가정. **forward-looking**: agent_notes 내용이 나중에 writer 프롬프트로 흐르거나 manuscript 커밋으로 promote될 때 human/process 게이트 필요(FGP render-boundary 노트와 동형).

---

## 다음

Draft Workspace MVP A 커밋표면 **ACCEPTED**. 다음 큐(운영자 제시): **Zotero/reference R1 closure(LEDGER_039)** 또는 **FGP real prose render-boundary 설계**. 둘 다 내가 받을 수 있음. multi-track 지도 트랙4를 "MVP A 커밋표면 ACCEPTED(f9e3dba); agent_notes sanitize는 process 가드" 로 갱신 권장.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 라이브 repro=로컬 `.scratch/dw-gate/` + Temp.)
