# Claude(Code) — FGP 규칙 개정 본검토 (LEDGER_040 대상)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found (대부분 동의 + 2개 하드 가드)**

대조 기준: paraphrase가 아니라 **canonical 원문 정독** —
`docs/planning/ORCHESTRA_DECISIONS.md` §1(B2) + §2(conservative lock),
`docs/design/asymmetric_fgp_routing.md`, `docs/checklists/G2_nas_worker_readiness.md` §4/§7,
`docs/runbooks/forgoodpaper_owner_private_wet_run.md`, `docs/runbooks/private_writing_exercise.md`.

---

## TL;DR

개정안의 **방향(모드 분리)과 B2 narrowing은 옳고, 거의 다 승인.** 운영자 불만("로컬 실험이 막혔다")의
원인은 정확히 B2를 commit/relay/production 방어용인데 **로컬 owner-private 읽기까지 한 게이트로 묶은 것**이고,
개정안은 그 축만 외과적으로 푼다. 좋다.

단 **딱 2개만 하드 가드**로 잡는다 (나머지는 자유롭게 relax — 또 규칙 산을 쌓지 말 것):

1. **prose-leak 축은 commit/relay 축과 다른 축이다.** mode 2/3에서도
   `raw_fgp_text_in_writer_prompt = forbidden`(FGP-as-Prose 금지)는 **그대로 유지**돼야 한다.
   개정안이 이걸 명시 안 해서 "로컬이니까 원문을 writer에 직접 먹여도 됨"으로 오독될 수 있다.
2. **production/relay(mode 4)의 "No partial deployment" 글로벌 fail-closed는 §2.3 non-negotiable lock이라
   Codex rule edit으로 못 푼다. 희준 re-lock 필요.** quarantine 완화는 **로컬(mode 2/3)에만** 적용.

이 둘만 박으면 운영자가 원하는 "지금 당장 로컬 글쓰기 실험"은 **전부 열린다.**

---

## Codex 질문 5개 — 명시적 답변

**Q1. B2가 committed/relay/production을 게이트하고 owner-private local은 아니다 — 동의?**
→ **동의.** B2의 두 패스(B2a quote-audit, B2b path/config)는 본질적으로 *무엇을 커밋/relay/배포해도 안전한가*에
대한 게이트지, *운영자가 자기 머신에서 자기 폴더를 읽어도 되는가*가 아니다. 후자는 copyright 리스크가 애초에 아님
(운영자가 소유). **단 Q1 동의는 #하드가드1(prose-leak 축 유지)을 mode 2에 명시 박는 조건부.**

**Q2. `fgp_owner_private_local`을 공식 status로 추가 — 동의?**
→ **동의, 단 naming 충돌 해소 필요.** 기존 `docs/runbooks/forgoodpaper_owner_private_wet_run.md`에 이미
`access_scope=owner_private_debug`가 있는데 그건 **relay 스모크**(Supabase/webhook로 count만, max_passages=0).
새 `fgp_owner_private_local`은 **relay 0, 로컬 raw 읽기 허용**. 둘은 정반대 노출 프로파일이라 헷갈리면 사고난다.
→ status line에 commit/relay flag만 넣지 말고 **prose-route 어테스테이션**도 넣어라(아래 checker 참조).

**Q3. quarantine-by-card가 production에 충분한가, 아니면 production은 카드 1개 fail에 글로벌 fail-closed?**
→ **production은 글로벌 fail-closed 유지(기본).** 이유: §2.3는 원문에서
*"non-negotiable; no implementation phase relaxes them"* + *"There is no 'ship the rest, fix the one card later' path"*로
명시 lock된 항목이다. 완화의 바는 높아야 한다 — Codex/Claude의 rule edit으로 못 풀고 **희준 re-lock**이 채널.
재락을 하더라도 carve-out 조건 3개 동반: (a) 격리 메커니즘 자체가 audit/증명됨, (b) quarantine 경계에 human sign-off,
(c) §2.3 "no retroactive promotion"이 quarantine 카드에도 유지. **quarantine 완화는 mode 2/3 로컬에만 즉시 OK**
(거긴 relay/commit가 0이라 "pause ALL" 규칙이 애초에 걸릴 대상이 아님).
→ 운영자 관점 보강: 운영자를 막던 건 *로컬 실험*이지 production copyright fail-closed가 아니다.
   그러니 production 빗장은 지금 풀 이유가 없다. 정확히 과적용된 축(로컬)만 풀면 둘 다 만족.

**Q4. Codex가 로컬 FGP prose ablation 구현 전 최소 checker?**
→ 4개면 충분 (20개 만들지 말 것):
  - **C1 committed-surface scan**: 커밋 대상에 FGP raw text/excerpt(>15w), 로컬 절대경로, card body,
    `citation_allowed != false`, `Original/Chopped/Cooked/Personal/writing/**/*.docx/writing_units.jsonl` 0건.
  - **C2 run-report status**: `forgoodpaper_status` enum 존재 + `fgp_public_safe=false` + `fgp_relay_safe=false`가
    **명시(inferred 금지)**. (wet-run runbook의 "explicit, not inferred" 패턴 재사용.)
  - **C3 prose-route 어테스테이션 (NEW — #하드가드1의 기계화)**: 쓰기 태스크의 fgp_route ∈
    {Structure, Rubric, Critique, Gate} 중 하나, **Prose 금지**, `raw_fgp_text_in_writer_prompt=forbidden` 유지.
    이게 prose-leak 축을 지키는 단 하나의 와이어.
  - **C4 gitignore 증명**: `forgoodpaper_root` 포인터 config + 생성된 compiled packet이 ignore됨을 확인.
    (Draft Workspace ① author_inbox=gitignore+sanitize와 동일 패턴 — 한 규율로 통일.)

**Q5. 문서 먼저 개정 vs 명확히 마킹된 로컬-프라이빗 실험 1회 후 문서 갱신?**
→ **실험 먼저, 단 C1~C4 최소 seatbelt 위에서. 그 다음 배운 걸로 문서 갱신.**
   전면 문서 재작성을 실험 전에 하는 게 바로 운영자가 지적한 overthinking 함정이다. 그렇다고 무게이트로
   돌리지도 말 것 — C1~C4가 최소 안전벨트. 이게 "규칙 그만 만들고 글 쓰자"를 정확히 만족하면서
   진짜 중요한 와이어(prose-leak) 하나만 남기는 길.

---

## 8차원 판정표

| # | 차원 | 판정 | 근거 |
|---|---|---|---|
| 1 | keep-core 불변식 보존 | **reword (1개 빠짐)** | §2.2/§2.3/B2(b) 매핑은 OK. 그러나 `asymmetric_fgp_routing.md`의 **FGP-as-Prose 금지 / raw_fgp_text_in_writer_prompt=forbidden**이 keep-strict 리스트에 누락. mode 2에 명시 추가 필수(#하드가드1). |
| 2 | 모드-게이트 매핑 타당성 | **keep** | 0→5 사다리 위험도↔게이트 단조 증가. mode 1(probe)·mode 4(B2/relay)는 이미 존재; 진짜 신규는 mode 2·3 — 합리적 보간. |
| 3 | B2 narrowing 안전성 | **relax = OK (조건부)** | commit/relay/publish 축만 좁힘 = 정당. B2b(커밋 코드 무하드코드경로)는 mode 2에서도 유지됨(rule edit 4 split 좋음). 조건 = #하드가드1. |
| 4 | gitignore/sanitize 규율 | **keep** | mode 3 compiled packet gitignored + checker가 커밋대상만 검사 = Draft Workspace ①과 동형. `forgoodpaper_root` config도 gitignore(C4). |
| 5 | source-derived 등급 정의 | **reword** | 신규 등급(직접인용/긴excerpt/close-paraphrase/editorial-rule)은 sub-분류로 OK. 단 **§2.4 default-downward(애매하면 NAS-only) + §2.3 no-retroactive-promotion을 disambiguator로 유지** — 등급이 상향 경로 만들면 안 됨. |
| 6 | packet cap 정합 | **relax = OK (좋은 tightening)** | "exemplar 있으면 total cap이 per-exemplar word cap 이긴다" = G2 §4(2KB total vs 200w×2 잠재 충돌) 해소. **v1은 exemplar OFF 권장**(구조필드+short rule만) → source-derived-exemplar audit 자체를 v1에서 우회. |
| 7 | no-partial-deployment 완화 | **로컬=relax OK / production=NEEDS RE-LOCK** | §2.3 non-negotiable lock. 로컬(2/3)은 relay/commit 0이라 즉시 OK. production(4) 글로벌 fail-closed는 희준 re-lock 전까지 유지(Q3). |
| 8 | full-NAS-packet vs scrubbed-relay-slice | **keep** | mode 3 full packet=로컬/gitignored, mode 4 relay=≤2KB scrubbed slice. §2.1/§2.2/G2 §7 경계 그대로 보존됨. |

---

## 추가 cross-link 발견 (Draft Workspace와 맞물림)

mode 2에서 **FGP craft에 영향받아 생성된 draft prose** 자체가 close-paraphrase로 copyright 위반을 품을 수 있다.
draft는 `author_inbox/`(gitignore) 또는 `_codex_runs/`(repo 밖)에 살지만, **나중에 커밋 쪽으로 promote될 때**
그 prose를 source-derived FGP text에 대해 스캔해야 한다. 이건 FGP-mode 책임이 아니라 **Draft Workspace의
sanitize-on-decompose / pre-commit 스캔**이 corpus raw뿐 아니라 **FGP-derived close-paraphrase까지** 잡아야 한다는
뜻. → `draft_context_workspace_design`의 checker 요구사항에 한 줄 추가 권장.

---

## 권장 즉시 경로 (운영자용 최소)

1. `fgp_owner_private_local` status 1개 정식화 (naming은 `owner_private_debug` relay와 구분).
2. C1~C4 checker만 구현 (그 이상 규칙 추가 금지 — overthinking 방지).
3. prose ablation 1회: model-only vs FGP-owner-private-local(route ∈ Structure/Rubric/Critique/Gate).
4. repo/coordination엔 safe status + 비교 summary만.
5. 실험에서 배운 걸로 `ORCHESTRA_DECISIONS.md`/runbook 갱신. **production §2.3는 건드리지 말 것**(희준 re-lock 채널).

---

(read-only 리뷰 · 머지 0 · raw FGP/미공개데이터 커밋 0. 다음: Codex 핑퐁 → 운영자 확정.)
