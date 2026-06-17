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

## 🆕 CIR 시스템 stress-test 트랙 (운영자 2026-06-17 밤샘, 두 방향 COMPLETE)
운영자: CIR 미공개 통계논문(`G:/260518_CIR_Statistics`)을 *재료*로 레포 전체 코드 작동 검증 + 과학리뷰 둘 다. Claude=tester#1 독립리뷰, Codex=빌더+전체루프, 교차/수렴.
- **기능 커버리지**: figure MCP×2✅(He·La/Sm vs 위도, 운영자 인라인표시), corpus binding/discovery/D3 fail-closed/BM25(alignment verified)/evidence-demand/draft-driver 파이프(40 tests)/writing-runner/claim-extractor/backchain/source-support 다 작동. fake-green=0-claim READY·writer evidence 0인용; fake-red=#9(내 CORPUS_SOURCE.local.json smoke파일이 retrieval fail-closed 테스트 깸→정리, 진짜결함=테스트 로컬설정 부재 의존).
- **과학리뷰(C1 dVs)**: double-dipping(경계=He+dVs GMM유도→그 경계로 대비검정) + **자기인용 확정**(dVs=Barruol2019 MBAR tomography 모델 샘플값, 신규측정X→published 모델 재분석으로 프레이밍) + Moran's I≈0.91→e-29 p값 부적합. C3 La/Sm=경계 band(step아님)+dataset 교락. → Codex가 비평 수용, **draft v3 본문/제목 substantive 강등 확인**(cosmetic 아님), evidence-demand에 boundary_derivation_independence 추가→contradictory=1/fail.
- **운영자 추적질문 답**(CLAUDECODE_CIR_TRACKING_001): corpus·논지 추적은 allow-list·audit·리비전 생존 수준 안 깨짐; 약한 seam=cited 판정이 prose `(Surname,Year)` 텍스트매칭→writer `[E1]` alias 쓰면 cited=0(ID기반 sidecar로 픽스).
- **통합 모닝브리프**: CLAUDECODE_CIR_MORNING_BRIEF(운영자 AM). 권고: ①citation ID바인딩 ②0-claim→skeleton_only ③external-support target-source 제외(Kim2024+CIR 공통) ④retrieval 테스트 격리.
- 게이트 준수: raw 미공개데이터/figure 커밋0·머지0·read-only. scratch=`C:\Users\USER\Documents\_claudecode_runs\cir_statistics_paper_draft\`.

## 🆕 FGP 규칙개정 본검토 트랙 (2026-06-17, 압축 후 실행 COMPLETE)
LEDGER_040(Codex FGP 규칙 개정안) 본검토 — canonical 원문(`ORCHESTRA_DECISIONS.md` §1 B2/§2 conservative lock, `asymmetric_fgp_routing.md`, G2 §4/§7) 대조.
- **발행: `inbox_codex/CLAUDECODE_FGP_RULE_REVIEW_001.md` (`25f7f18`). VERDICT=issues_found(대부분 동의+2 하드가드).**
- 동의: 모드 0~5 사다리·B2를 commit/relay/production으로 narrowing OK(로컬 owner-private 읽기는 애초 copyright 리스크 아님).
- **하드가드1**: mode 2/3도 `raw_fgp_text_in_writer_prompt=forbidden`(FGP-as-Prose 금지) 유지 — Codex keep-strict 리스트에서 누락된 핵심 런타임 불변식. commit/relay 축≠prose-leak 축.
- **하드가드2**: production "No partial deployment" 글로벌 fail-closed는 §2.3 non-negotiable lock → Codex rule edit으로 못 풀고 **희준 re-lock 채널**. quarantine 완화는 로컬(2/3)만.
- Codex Q1~Q5 명시답 + 8차원 판정표 + C1~C4 최소 checker(C3 prose-route 어테스테이션이 prose-leak 지키는 단일 와이어). cross-link: Draft Workspace pre-commit 스캔이 FGP-derived close-paraphrase도 잡아야.
- **핑퐁 수렴 COMPLETE**: Codex `LEDGER_041_..._ACK`(`27e48f0`)=ok — 두 하드가드 verbatim 수용, 5→4 status 단순화(`not_connected|probe_only|local_private_used|b2_production`, mode3 drop=더 안전), C1~C4 채택. 내 CLOSE=`inbox_codex/CLAUDECODE_FGP_RULE_REVIEW_002_CLOSE.md`. **트랙 CLOSED.**
- **결론: 로컬 FGP 글쓰기 실험 열림 / FGP-as-Prose(원문 직접 writer먹임) 금지.** 다음 실전=1회 ablation(baseline vs FGP-Structure/Rubric/Critique/Gate, C1~C4 seatbelt).
- 캐리포워드: Draft Workspace pre-commit 스캔이 FGP-derived close-paraphrase도 잡아야(MVP A checker 요구로 이월). parking: production §2.3 quarantine re-lock(운영자, 긴급X).
- ⚠️ `Anthropic_Invoices_2026-06.zip` 무접촉(스테이징 금지).

## 🆕 FGP ablation scaffold 검증 트랙 (2026-06-17, B분업=Codex빌드·Claude검증)
Codex가 C1~C4 안전벨트+ablation scaffold 빌드(`dbd499f` on `codex/draft-context-workspace`, LEDGER_042). 내가 adversarial 워크플로우(41 에이전트·5차원·발견마다 회의론자)로 검증.
- **발행: `inbox_codex/CLAUDECODE_FGP_ABLATION_REVIEW_001.md`. VERDICT=issues_found. 33 confirmed/3 refuted.**
- **헤드라인**: C1~C4 체커=**fake-green**. attestation 전부 producer 하드코딩 `True`(fgp_local_ablation.py:140-149), 체커는 echo만(check:130-146), 유일 내용스캔 `_check_safe_surface`는 path/secret *모양*만(prose 안 봄). 오늘 green=prose채널 빈 채 by-construction. **다음 prose-ablation 단계에서 가드 fire 안 함**(task_builder `anchor_exemplars.paraphrased_text` 채널 이미 존재, 200단어 verbatim).
- 라이브 공격 3개 전부 PASS: ATTACK1(nested policy=allowed, 미러는 forbidden) / ATTACK2(subdir prose, glob top-level only) / ATTACK3(instruction에 prose).
- 잘된 점: probe는 진짜 counts-only enforce, 오늘 누수0(by construction), status 스코핑 정확, **production B2 fail-closed 안 건드림**(하드가드2 보존).
- Codex Q1~Q4 답 + 하드닝 H1~H4(H1=체커가 prose-free 도출/H2=nested정책검증/H3=rglob+allowlist/H4=RED테스트). 원칙: **prose는 denylist 불가→allowlist/template-match.**
- **round-1 결과: Codex H1~H4 하드닝 빌드(`29fac0a` schema v2, LEDGER_044) → 내가 재검증.**

### round-2 재검증 (v2 break-it, COMPLETE)
- 발행: `inbox_codex/CLAUDECODE_FGP_ABLATION_REVIEW_002.md`. VERDICT=issues_found. compact 워크플로우 4 에이전트(~474k 토큰) 전부 라이브 bypass 발견.
- **v2가 닫은 것(축1=writer 프롬프트)**: instruction==상수, result recompute, nested policy='allowed' 거부, writing_guidance 채널 이중차단 — round-1 H1~H4 잘 구현됨 ✅.
- **여전히 열린 것(축2=커밋/relay surface)**: 4 라이브 bypass + ADS. (B1)`source_layer_route_config` 내용 미검증(체커가 validate_source_layer_route_config 호출조차 안 함, validate_writing_task가 조용히 drop) (B2)`fgp_route_config` nested 미지키 무시 (B3)manifest extra키(`.safe.json`에 prose) (B4)`run_id` prose (B5)NTFS ADS. 전부 valid=yes + 커밋파일에 verbatim FGP prose.
- 근본원인: 체커가 스칼라/constraints는 *값*으로 핀하지만 route-config 블롭·manifest 컨테이너는 *키 존재*만 요구. validate_* 들이 미지키 거부 안 하고 무시.
- **내 manual "sound" 판단이 축2에서 틀림 — break-it 워크플로우(운영자 "다시 깨보라" 지시)가 잡음.** 정직한 자기정정 노트에 박음.
- 하드닝 H5(컨테이너 값으로 핀: *_to_payload 재직렬화 ==, manifest exact-key, run_id regex)/H6(validator 미지키 거부)/H7(중복키 거부 object_pairs_hook)/H8(ADS, 낮음).
- round-3: Codex H5~H7 빌드(`ada5828` container 하드닝, LEDGER_046) → 내가 round-3 재검증.

### round-3 재검증 (v3 break-it, COMPLETE)
- 발행: `inbox_codex/CLAUDECODE_FGP_ABLATION_REVIEW_003.md`. VERDICT=issues_found.
- **v3가 B1~B4 닫음 확인** ✅: canonical 재직렬화 비교(source_layer/fgp_route 모두 enum, free-text 0), manifest exact key-set+중첩, run_id/created_at regex, 중복키 object_pairs_hook, result recompute. B3는 내 라이브 repro로 `manifest_shape_invalid` 확인.
- **잔여 2채널(같은 root-cause, 둘 다 라이브 valid=YES+커밋파일에 prose)**: (R3-1) manifest `asset_probe_summary.b2_gate_status`·`summary_status`가 "non-empty string"만 요구, enum 미제약(내 직접 repro 확정) / (R3-2) `FGP_LOCAL_ABLATION_REPORT.md`가 render(manifest)와 `==` 대조 안 됨(워크플로우 에이전트 확정).
- 워크플로우 3에이전트 중 2개 API 529로 사망 → R3-1·regression은 내가 직접 라이브 repro로 완성.
- **메타**: round-2(B1~B4)·round-3(R3-1/R3-2) 같은 패턴 재발 = per-field 값핀 + denylist 표면스캔. fix=패턴 닫기("커밋표면 모든 바이트는 recompute== 또는 enum/bound; 자유문자열=prose채널"). H9(b2/summary enum)·H10(report recompute==). H8 ADS는 deferred(동의).
- round-4: Codex H9~H10 빌드(`a41d08e`, b2/summary enum + report==render, LEDGER_048) → 내가 round-4 재검증.

### round-4 재검증 = ACCEPT (COMPLETE)
- 발행: `inbox_codex/CLAUDECODE_FGP_ABLATION_REVIEW_004_ACCEPT.md`. **VERDICT=ok — `a41d08e` 수락, 커밋/relay-surface 축 COMPLETE.**
- 직접 라이브 매트릭스(자체 실행, 워크플로우 대신): 신선 빌드 valid=YES(false-red 0) + R3-1a/b·R3-2(full/append)·B1·B2·B3·B4 전부 거부 + control valid=YES. 10/10 의도대로.
- **메타 불변식 충족**: 6개 커밋표면 전부 recompute-`==` 또는 enum/value-핀(자유문자열 채널 0). round-2(4 bypass)→round-3(2)→round-4(0) 수렴.
- 남은 것: **H8 NTFS ADS만 deferred**(transport-conditional, git/cp는 strip; 동의, scaffold 수락 blocker 아님; non-git relay 전 처리).
- ⚠️ **scope**: 수락=scaffold(counts-only) 커밋표면 견고. **prose-ablation은 새 표면**(writer 프롬프트 렌더 경계) — 자체 가드 필요(v4 체커는 저장 task JSON만 봄, 렌더 프롬프트 안 봄). 같은 원칙(allowlist/recompute/enum, FGP는 Structure/Rubric/Critique/Gate 메타로만).
- **다음: 첫 owner-private prose ablation 가능 — 단 render-boundary 가드와 함께 설계 → 그 새 가드도 내가 깸.** multi-track 지도 FGP 트랙 "scaffold ACCEPTED(a41d08e)"로 갱신 권장. 게이트 동일.

## 🆕 Draft Workspace 커밋표면 검증 트랙 (2026-06-17, A로 감 → ACCEPT)
운영자가 지도검토 플래그2(DW MVP A의 forbidden-surface 가드 미검증)대로 A 진행. Codex break-it로 5표면 뚫림→패치(`f9e3dba`, LEDGER_049) → 내가 재공격.
- **발행: `inbox_codex/CLAUDECODE_DRAFT_WORKSPACE_SURFACE_REVIEW_001.md`. VERDICT=ok — `f9e3dba` 수락.**
- 라이브 매트릭스: control PASS + A1~A5(5패치) 전부 FAIL + 내 probe 3개(P1 generated.md recompute / P2 title path / P3 long-line paste) 전부 FAIL + control still PASS. false-red 0.
- **FGP 4라운드 메타패턴이 DW엔 없음** — Codex가 교훈 선제 적용(generated .md도 recompute-==, 값-핀, dup-key on check 경로, forbidden 스캔에 long-line(2400) paste 휴리스틱, author_inbox gitignore 검증). 첫 리뷰 통과.
- **정직한 scope 경계**(버그 아님): agent_notes의 "sanitized vs raw close-paraphrase"는 구조적 검증 불가 = **process 가드**(에이전트 sanitize). long-line 휴리스틱이 bulk paste만 부분차단. = 내 round-2 cross-link의 정확한 bound. forward: agent_notes→프롬프트/커밋 promote 시 human 게이트 필요.
- **다음 큐(운영자 제시): Zotero R1 closure(LEDGER_039) 또는 FGP prose render-boundary 설계.** 지도 트랙4 "MVP A 커밋표면 ACCEPTED(f9e3dba)"로 갱신 권장. 게이트 동일.
