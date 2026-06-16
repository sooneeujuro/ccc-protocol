# STATUS — Claude (회사PC, 세션 67522dcd / 이전 a745303e)

last update: 2026-06-17 02:05 (**머지 후보 전수검토 + 숙제검사 착수**[운영자 지시]. reconcile #1·#5·6 CLOSED. `LEDGER_027`로 인벤토리+분업: Claude=J2/corpus-reader/verification-policy, Codex=harness-review/runbooks/vp-norm/home-detangle. CCCP tight 복귀)

## 🆕 머지 후보 전수검토 트랙 (운영자 "또 뭐 머지할지 검토 + 코덱스랑 숙제검사", 2026-06-17)
- 인벤토리(origin/main 82a3925, 충돌=merge-tree). 분업·판정표 `LEDGER_027`.
- **숙제검사 완료 양측 → 통합 머지-준비표 `LEDGER_029`**:
  - ✅**MERGE-READY**: **J2**(Claude: 실머지 충돌0+488 tests green, draft_evidence_adapter=D3트리거), harness-design-review·revision-methodology-runbooks(Codex), corpus-verification-policy(Claude).
  - ⚠️**NEEDS-WORK**: corpus-reader(.gitignore P0+.mcp.json→#5·6식 rebase), vp-norm(stale 경로+whitespace), **home-detangle(289파일—이미지/논문본문 0이지만 `a2_convert_german.py`가 datalab_key.txt 비밀키경로 읽음+로컬/NAS경로→큐레이션 필수)**.
  - ❌**DON'T MERGE**: corpus-binding-ledger·ledger-migration-apply-state(reconcile가 대체).
  - **순서**: #1+#5·6 → J2(Claude 결합빌드+Codex검증→D3 마저) → docs READY → NEEDS-WORK 수정 후. **운영자 머지 결정/GO 대기.**
- **🟢 결합 브랜치 빌드 완료(운영자 GO "J2+#5·6 결합빌드", 2026-06-17)**: `claude/combined-j2-corpus` HEAD `5462066`(worktree `_wt-combined`) = corpus-binding-main(bc97a88) + merge J2(c6f7cc8) + generated.md 재생성(5462066). **머지 충돌 0, 67b1=0, evidence_packet_emitter disjoint 3-way clean 실증.** D3 활성 전환(adapter 랜딩→advisory drift), generated.md 재생성으로 E6 PASS, D3 테스트 skip 해제 통과. 검증: checker PASS(advisory 2), corpus 48/retrieval 88/draft-driver 40/writing-runner 360/production 655 all green. → **Codex `LEDGER_030_COMBINED`=ok(독립 재현, 머지후보 인정)**. **Codex 추천: #5·6/J2 따로 말고 결합 브랜치 `5462066`을 통째 머지**(상호작용점 이미 검증; 따로 머지하면 post-merge generated.md 재생성+재검증 필요). D3는 이 후보에선 advisory 유지, 다음 GO에서 enforced. **D3 마저·머지는 운영자 GO 대기**.
- **🟡 Anthropic incident(2026-06-16 17:29 UTC, elevated errors across models)로 분류기 다운→Write/Bash 간헐 차단(~02:2x KST). 03:02 복구 확인.** 운영자 결정: **오늘밤 Codex 검증 carry / Claude 휴식**. 막혔던 `LEDGER_031`(overlay 제안 응답=endorse Phase1) 복구 후 push. 빌드(D3마저/NEEDS-WORK/머지)=Claude 복귀 후. Codex=target repo 검증만(빌드는 Claude 단일). discovery/overlay ledger=차기트랙(머지/D3 후 Phase1, 운영자 GO).

## Heartbeat (docs/HEARTBEATS.md adaptive backoff 채택)
- Cadence: **5m 고정**(운영자 지시 2026-06-16, Codex와 동기). 백오프 사다리 폐기 — Claude=병목이라 in-flight 중 늦추면 Codex 멈춤. 이번 라운드는 운영자 수동 wake(자동 타이머 미설정).
- 방금 의미있는 작업 발생(ledger MVP Claude↔Codex 수렴) → quiet_streak 리셋, active 복귀.
- 정지조건: STOP.md 또는 operator 명시 정지. FINAL_SUMMARY는 정지신호 아님.
- ping 규약: 3-quiet due-ping, peer 무응답 반복 시 operator 에스컬레이트(스팸 금지).

## 🆕 Ledger MVP 트랙 (drift-killer, 운영자 발주 2026-06-16)
- **수렴 완료**: Claude(LEDGER_001/003) ↔ Codex(LEDGER_001_REVIEW/002) → 첫 MVP = **migration/apply-state ledger** 만장일치. 아키텍처 LOCK.
- **운영자 Phase 1 GO 받음 → 빌드 완료** (협업모드=Claude 빌드/Codex 검증). manuscript-atelier branch `claude/ledger-migration-apply-state` commit `8a2c51f` (4 files, additive-only, 로컬·미push).
  - 강제체크 green-as-is + pytest 13 passed + 합성드리프트 red 증명. 권고 10건=Phase2 타깃 프리뷰(러너북 :189 오타 포함).
- **Phase 1 클로즈**: Codex `LEDGER_004`=issues_found(3건)→수정 `6a67152`→`LEDGER_005`=**ok**. 잔여 hardening(canonical-path) `efaaf0a` 반영. 전체 production 정적 suite **648 passed**, green-as-is. 3 commits: 8a2c51f/6a67152/efaaf0a.
- **Phase 2 (de-prose) 완료** (운영자 GO): commit `ff19a37` (17 files). 5 SQL헤더+README+claim_client+러너북§1/§6(:189 오타수정) apply-state prose 제거 → APPLY_STATE.json 단일화; 정적테스트 5개 stale-assert 정정; check A2(no-prose,+README)·A3(runbook-ref) **advisory→ENFORCED**; sha256 갱신. 검증: checker PASS(권고 2=by-design A1만), **650 static tests pass**, de-prose grep 0. → migration-apply-state ledger MVP **완성**(Phase1+2).
- Codex `LEDGER_007`=issues_found(2건: claim_client 게이트 0002b 누락 + 체커 출력 cp949 크래시) → **수정 완료** commit `bdd8332`(companion-aware 게이트 + ASCII/reconfigure 출력 + cp949 테스트). checker PASS, 651 tests, cp949 red-path OK. 재검증 `LEDGER_008` 발행.
- Codex `LEDGER_008_..._REREVIEW`=**ok** → **migration/apply-state ledger MVP (Phase 1+2) CLOSED 양측 합의** (`LEDGER_009` 발행). 최종 branch `claude/ledger-migration-apply-state` commits 8a2c51f/6a67152/efaaf0a/ff19a37/bdd8332 (로컬·미push). checker PASS, 651 tests.
- **운영자 게이트**: (1) MVP main 머지 여부(code-only PR 가능). (2) ②live-surface/③decision는 **북극성 미통과로 보류**(운영자·Claude 합의: 인프라위생, 논문 직결 약함).
- **🆕 MVP④ corpus-version binding ledger 설계 착수**(운영자 발의, 북극성 통과 — 초고 인용 재현성): `CORPUS_BINDING.json`(버전 핀 sha1/편수/날짜, 메타만) + per-machine 소스config + 체커(연결 corpus CORPUS_VERSION.json 대조). **실재 드리프트 발견**: `.mcp.json`이 옛 6/02(4470, dedup전) 가리킴 vs 정본 6/12(6/16재빌드, 3903, sha 55522119). 설계안 `LEDGER_010` → Codex review=issues_found(건설적): static JSON만으론 toothless, repo-local corpus-identity anchor도 잡아야. **검증된 핵심 발견**: `bge_dense_adapter.py:22`·`evidence_packet_emitter.py:96`·`EvidencePacket.spec.md:95`가 worker corpus-거부 게이트를 **옛 sha 67b1...에 하드코딩**(정본 55522119는 코드에 0회) = worker가 정본 corpus 거부할 stale 게이트. 수렴 `LEDGER_012`. **운영자 Phase 1 GO → 빌드 완료**: branch `claude/corpus-binding-ledger` commit `e58e81d`(6 files, 로컬). CORPUS_BINDING.json(binding_id geochem_2026-06-16_55522119, 경로0) + check_corpus_binding.py(강제 E1~E7, 리포트 D1~D3) + generated.md + example + tests(10) + gitignore. 검증: checker PASS, 10 tests, **D1이 67b1 stale anchor 3곳 정확 적발**(known_drifts), --verify-source 로컬 6/12 일치 OK, corpus 본문 미커밋. `LEDGER_013` 발행 → Codex 검증 대기.
- Codex `LEDGER_013`=issues_found(E6 재현성: generated.md가 .mcp.json dirty 의존 / D3 미구현) → **수정 완료** commit `c7a7bcd`: render_generated가 .mcp.json 미참조(커밋코드만→clean 재현), D2 런타임전용 강등, D3(draft_evidence_adapter repo-local index 기본) 구현+테스트. checker PASS, known_drifts 4(D1×3+D3), 47 tests. 재검증 `LEDGER_014` 발행.
- Codex `LEDGER_014` 재검증=**ok** → **corpus-binding Phase 1 CLOSED 양측** (`LEDGER_015`). 최종 commits e58e81d+c7a7bcd(로컬).
- **corpus-binding Phase 2 빌드 완료**(운영자 "다 바꿔" GO): commit `047a653`. 67b1→55522119 3 anchor(bge_dense_adapter/evidence_packet_emitter/EvidencePacket.spec)+README/docstring, D1 advisory→ENFORCED, generated.md D3-only. 검증: live 67b1 0(handoff만), checker PASS, **787 tests**. D3(draft default)=advisory 유지(운영적 후속). `LEDGER_016` 발행 → Codex 검증 대기.
- **single-source 리팩터**(운영자 지적: 하드코딩=에러제조기): commit `89e87a8`→`aff15f5`. `CANONICAL_UNITS_SHA1 = _load_bound_units_sha1()`(binding 런타임 읽기), emitter import, spec/README/docstring 이름 참조만(sha 값 0). Codex `LEDGER_017`=issues_found(D1이 bound값 재하드코딩 못잡음 + 55522119 prose 잔존) → `aff15f5`로 수정: **D1=앵커에 40-hex 리터럴 하나라도 있으면 fail**(재하드코딩 적발), prose 제거. checker PASS, 787 tests. 재검증 `LEDGER_018` 발행.
- Codex `LEDGER_018` 재검증=**ok** → **corpus-binding MVP④ CLOSED 양측**(`LEDGER_019`). single-source 도장. 최종 5 commits(e58e81d→c7a7bcd→047a653→89e87a8→aff15f5, 로컬). **오늘 두 ledger MVP(migration apply-state + corpus-version binding) 전부 닫힘.**
## 🔴 머지 직전 발견 (2026-06-16): MVP1 중복
- **origin/main이 이미 `MIGRATION_STATUS.md`(migration apply-state ledger, 운영자 채택 6/11) 보유** = 내 MVP1 중복. 원인: 작업 브랜치가 origin/main보다 **39커밋 뒤+분기**, 시작 전 미확인(Codex도 isolation 리뷰라 놓침). 39커밋엔 리뷰 후속 fix 다수 + senpAI 전체 + 0004가 이미 landed.
- **영향**: MVP1 머지 ㄴㄴ(중복+충돌). MVP④ corpus-binding은 신규(main 없음)→살림.
- **운영자 지시=두 시스템 장점 통합**: main `MIGRATION_STATUS.md`(정본 유지) + 내 체커 이식(`check_migration_status.py`: coverage/no-prose/companion/runbook-ref enforced) → prose ledger에 기계검증 부착. `LEDGER_020`으로 Codex 공유+제안.
- **운영자 지시=전수검토·합치기**: 이번 세션 작업 ↔ origin/main 전수 비교, 비교해 좋은 거 채용, Claude+Codex 파트 분업. **전체 계획·매트릭스 = `detangle/RECONCILE_AUDIT_20260616.md`**(압축 생존용). 분업: Claude=#1·2·3(migration 클러스터, main 표+내 체커 이식), Codex=#5·6(corpus rebase 검증)+교차. `LEDGER_021` 발행.
- **🟢 Claude 파트 #1 빌드 완료 (압축 후 재개, 2026-06-17, commit `91090c5` 로컬·미push)**: 현재 origin/main 위 isolated worktree(`claude/migration-status-checker`)에서 빌드. main `MIGRATION_STATUS.md`(운영자채택) 정본 유지 + `check_apply_state.py` 체커 이식 → `check_migration_status.py`(강제 M1 coverage/M2 companion/M3 no-prose/M4 refs/M5 cells + A1 advisory) + `test_migration_status_ledger.py`(16). 검증: origin/main에서 enforced PASS+advisory 0, production 정적 suite **671 passed**(+16, 회귀 0), MIGRATION_STATUS.md 미터치. APPLY_STATE.json(중복) 폐기. **#2·#3(de-prose) = main 이미 깔끔 → 합칠 것 없음, M3 체커가 상태 유지.** `LEDGER_022` 발행 → **Codex `LEDGER_022`=issues_found(2 blocking: M1 중복 ledger 행 collapse, M2 parent-without-revoke repro A/B)** → **수정 `d4d012a`**: parse가 row_ids(중복포함) 반환해 M1 중복행 적발, M2를 `security_definer_rpc_ids()` 필수쌍+per-target state 양립(parent applied⇒companion applied)으로 재설계, M3 phrase 추가. 재검증: origin/main enforced PASS+advisory 0, **674 passed**(신규 19테스트). `LEDGER_023` 재검증 요청 → **Codex `LEDGER_023`=ok → reconcile #1 CLOSED 양측**(`LEDGER_024`). 최종 commits `91090c5`+`d4d012a`(branch `claude/migration-status-checker`, 로컬·미push). **운영자 머지 게이트 대기**(additive-only 2파일). 다음 = #5·6 corpus(Codex 빌드 대기) → 머지 → D3.
- **Codex `LEDGER_021_VERDICT`(`ea1a280`) = 분업 동의 + #5·6 corpus issues_found**: (a) origin/main의 `.gitignore`에 P0 landmine 가드 이미 존재 → stale 브랜치 .gitignore patch 충돌(내 브랜치가 P0 가드를 지움 — `git diff`로 독립확인). (b) main에 `draft_evidence_adapter.py` 부재인데 corpus-binding generated/tests가 D3 전제 → 깨짐. **둘 다 동의(LEDGER_022)**: corpus PR = 현재 main `.gitignore` 보존 + `CORPUS_SOURCE.local.json` ignore 2줄만 추가, D1·E*만 올리고 D3는 후속으로 분리. → **Codex가 #5·6를 origin/main 위 새 브랜치로 빌드 → Claude 교차검증 → 운영자 머지 게이트.**
- **🟢 #5·6 corpus 빌드 완료 (2026-06-17, commit `bc97a88`, branch `claude/corpus-binding-main`, origin/main 82a3925 위, 로컬·미push)**: 운영자 결정=Claude 빌드/Codex 검증. worktree `C:\Users\USER\Documents\_wt-corpus-binding`. corpus-binding(CORPUS_BINDING.json 단일출처+check_corpus_binding.py E1~E7/D1+example+generated+tests) + **67b1→single-source**(bge/emitter/spec/README, 하드코딩 sha 0) + .gitignore main P0가드 보존+2줄. **J2 오염 차단**(evidence_packet_emitter는 single-source ±14만, exclude_sections 제외). **D3 deferred**(draft_evidence_adapter main 부재→graceful+skipif+generated D3-free). 검증: checker enforced PASS(advisory 1=D2 mcp), corpus 12 passed+1 skipped, retrieval 78, production 655, 67b1=0, diff --check clean. `LEDGER_025` 발행 → **Codex `LEDGER_025`=ok(no blocking, 독립 재현) → #5·6 CLOSED 양측**(`LEDGER_026`). **전수검토 reconcile 본체 완료** — 남은 것=운영자 머지 게이트(#1 `migration-status-checker` + #5·6 `corpus-binding-main`, 둘 다 로컬·additive·push 0) + D3 마저(J2 후). CCCP 활성교환 종료 → idle heartbeat.
- ⏳ **마지막 follow-up = D3 마저**(운영자 2026-06-17 "다 끝나면 D3 꼭"): corpus-binding D3(`scan_draft_default_drift`)는 구현 완료(`c7a7bcd`, 파일 부재 시 graceful)지만 **마저 할 것** = (1) `draft_evidence_adapter.py`를 CORPUS_BINDING.json bound corpus에서 읽도록 단일출처화 (2) D3 advisory→enforced+generated/테스트 재활성. **트리거**: `draft_evidence_adapter`가 main 랜딩(draft-spine J2 머지). 그전엔 corpus PR에서 deferred. 메모리 `project_d3_draft_default_followup`.
- ⚠️ 복구앵커: RECONCILE_AUDIT_20260616 + 이 파일 + HANDOFF + 메모리. 철칙: 작업 전 origin/main 대조. CCCP 재가동(운영자 추가요금 OFF·Codex 자동), 서브에이전트 fleet 금지(2-에이전트), 5분 폴.
- 하드게이트: live infra/DB/secret/deploy 0, corpus 미터치, manuscript-atelier push 0(로컬 리뷰).

## 🆕 037 dense 트랙 (운영자 인수 지시 → 완료)
- 운영자가 원 dense 세션 확인 후 이 세션에 인수("G만 ㄱㄱ, 레포 사본 플래그만"). Codex 037 verdict 3건 정정 완료(G:\corpus_md_export_20260612, 비-git, 재임베딩 0, 비파괴):
  - manifest+build_bge_m3_dense.py:99 build_mode → full_rebuild_20260616(스크립트는 동적 스탬프). dense_search.py Windows 콘솔 안전화. 정확 smoke(Xu2024 top1 cos 0.826) 기록.
  - 검증: PYTHONIOENCODING 없이 EXITCODE=0 + cos 0.826 재현. G:폴더에 DENSE_METADATA_FIX_20260616.md 타임로그.
  - 레포 사본 manifest(incremental_mellor=옛 mellor 증분)는 무접촉(플래그만, 운영자 ⓐ).
- 발행 `inbox_codex/037B_DENSE_METADATA_FIX_DONE.md` → **Codex `037B_..._VERDICT`=ok**(정확 smoke 독립재현 exit0/cos0.826). → **037 dense 트랙 CLOSED.**

## 현재 트랙 상태
- normalizer: ✅ DONE (75.4%, precision 99.2%). 코드 PR화 미완(manuscript-atelier/tools/corpus-normalize, uncommitted).
- figure refill: ⛔ **source-level BLOCKED** — 잔여 604그림/51편, 이 PC 안전소스 0/50. pilot=충돌붕괴(unsafe). 필요=datalab 머신 per-paper 원본 또는 PDF 재변환. 상세 inbox_codex/021.
- B(sidecar 적용): operator "박아" 대기. PR#15/16 머지 대기.

## 발행 최신: inbox_codex/021 (Codex verdict 대기). 핸드오프: detangle/HANDOFF_NEW_DRIVER_20260616.md (🔴 correction 포함).
