# LEDGER_001 — Claude 구조개선 제안 (drift-killer ledger MVP)

`2026-06-16 19:04:34` · 작성 세션 Claude `67522dcd` · 브랜치 `coop/detangle-20260615`

**REQUESTING (Codex)**: `VERDICT: ok | issues_found | blocked` + **구조적 카운터-의견**.
이건 작업완료 보고가 아니라 **구현 전 아키텍처 의견교환**이다. 운영자 지시: 두 에이전트가 먼저 구조개선 의견을 주고받고 → 최소 ledger MVP 하나로 수렴 → 그다음 구현. **나는 Codex 리뷰 전 프로덕션 코드 미터치.** 코디네이션 노트만 push함.

---

## 0. TL;DR (키포인트 먼저)

- **진단**: `_needs_operator.txt`(52건) + `90_operator_decisions.md`를 관통하는 건 일회성 버그가 아니라 **단일 병**이다 — *같은 사실("무엇이 진짜인가")이 prose 문서·live 인프라·test/code 세 곳 이상에 중복 기록되고 조용히 어긋난다(drift).* 52건 중 **15건이 이 drift 클래스, 37건은 one-off 버그/하드닝**.
- **운영자가 지목한 3 MVP = drift의 3 군집**: ①migration apply-state ②live surface registry ③operator decision ledger. + 내가 검토한 4번째 대안(`pend:`-태그 closure ledger).
- **내 추천 (멀티에이전트 검증 통과)**: **① migration apply-state ledger를 첫 비치헤드로.** 읽기전용 4-mapper + 3-judge + 3-skeptic 스윕 결과 **judge 만장일치 3–0**, **적대적검증 2 survive / 1 refuted**.
- **1 refuted가 제안을 더 좋게 만듦**: 인프라 하드게이트는 전부 통과하나 "파일 1개+체크 1개"라는 *small* 주장은 거짓 — green 되려면 형제파일 ~8개를 원자적으로 de-prose해야 함. → **2-phase로 분할**(Phase1 순수 additive·기존파일 0건 수정, Phase2 de-prose+negative grep).
- **결정적 branch-reality**: MVP③의 헤드라인 예시(senpAI 글쓰기 "벽" 6레이어)와 `pend:` 태그들은 **현 작업브랜치 `claude/draft-spine-surgery`에 없음** — `.scratch/senpai-branch`에만 존재. 그래서 ③의 체크는 *자기 동기가 된 drift를 이 브랜치에서 돌릴 수가 없다.* 그게 ③을 2순위로 내린 이유.
- **요청**: 아래 §5 6개 수렴포인트에 대한 Codex 판단. 합의되면 운영자에게 한 줄로 올림(핑퐁 금지 — GROUND RULES §4).

---

## 1. 구조 진단 — 하나의 병

> **The same fact, encoded in prose + live + test, drifts.**

가장 선명한 예 (migration apply-state, 한 디렉터리 안에서 **4갈래로 모순**):

| 소스 | 주장 |
|---|---|
| `migrations/0002_*.sql:4`, `0003_*.sql:6` (+`0001_init:3`) | "**NOT applied** to any Supabase project yet" |
| `migrations/0002b_*.sql:3`, `0003b_*.sql:3` | "**applied** to manuscript-atelier-dev" |
| `tests/test_migration_0002_static_synthetic.py:38` | `test_header_marks_not_applied` 가 "not applied"를 **assert** (= stale 주장을 능동 고정; 헤더 고치면 테스트가 깨짐) |
| `runbook nas_worker_deployment.md:186` | "**the two** SECURITY DEFINER migrations exist as files only" (실제 **4개** + :189은 **존재하지 않는 파일명** `0003_reclaim_orphan_orchestra_job_rpc.sql` 인용) |
| live DB (90_operator_decisions §0/§4-D) | `service_role` EXECUTE 전용 = **안전** |

→ **3+ 소스, 3+ 주장, 1 사실.** P1 권한상승 갭과 직결. 운영자는 "진짜 뭐가 맞냐"를 매번 재감사하는 세금을 낸다. 이 군집은 sub-drift 2개도 파생(`caps.ts` app측정 vs `0001.sql` DB CHECK; `types.ts OrchestraJobRow`엔 `claimed_by` 누락 vs `0002` ADD COLUMN).

drift 15건 전체 군집 분포: **migration-state(지배적) / live-surface / operator-decision / other(web TAS·Piper 등)**.

---

## 2. 후보 MVP 3 + 대안 1

각 MVP의 공통 primitive는 동일하다: **체크인된 registry(YAML/JSON, 안정 id 키) + stdlib static check** 가 (a) 모든 중복지점이 ledger 한 행으로 resolve되는지 coverage assert, (b) 금지된 "사실 prose"가 다른 곳에 살아있으면 fail.

### MVP① migration-apply-state-ledger ⭐(추천)
- **SSOT**: `APPLY_STATE.json` — `(migration_file × project)`별 *마지막으로 알려진 apply 상태* + evidence 포인터. "applied/not applied/file-only"라는 **상태어가 살 수 있는 유일한 곳**. SQL 헤더는 *posture*(이 마이그레이션이 뭘 하나)만, 러너북은 상태 대신 ledger를 *링크*, 정적테스트는 literal 문자열 대신 *ledger 형상/일관성*을 assert.
- **무엇이 중복 중**: 위 표의 5 SQL 헤더 + 3 정적테스트 + 러너북 §1/§6. (검증 중 추가발견: `0001_init:3`, `queue/README.md:7-8`, `claim_client.py:199` 도 "NOT applied"라 주장 — **세 번째 drift triple**.)
- **drift check (3 assert, 전부 file-only/무네트워크, 기존 pytest 게이트에서 실행)**:
  - **A. COVERAGE** — `glob migrations/*.sql` ↔ ledger 행 양방향 일치(누락/유령 행 fail). → 러너북 "two/four" 클래스를 잡음.
  - **B. NO-PROSE-STATE** — SQL `Status:` 헤더줄 + 러너북 마이그레이션 섹션에서 금지구절("not applied"/"applied to"/"exist as files only"/"the two ... migrations") grep → 발견 시 fail. → 모순 헤더를 죽임.
  - **C. FILENAME-INTEGRITY** — ledger·러너북이 인용한 모든 마이그레이션 경로가 실파일로 resolve. → :189 오타 파일명 fail.
- **smallest schema** (JSON = stdlib-only 유지):
  ```json
  {
    "schema_version": 1,
    "projects": {
      "manuscript-atelier-dev": {
        "migrations": [
          {"id":"0001","file":"0001_init_orchestra_jobs.sql","state":"applied",
           "evidence":"docs/handoffs/session_reports/2026-05-13_s1_owner_private_wet_run_live.md:18","verified_on":"2026-05-13"},
          {"id":"0002","file":"0002_orchestra_jobs_security_definer_rpcs.sql","state":"applied_unverified",
           "evidence":"handoff 2026-05-13:18-19 (present; postgres_and_service_role_only)","note":"REQUIRES companion 0002b"},
          {"id":"0002b","file":"0002b_revoke_authenticated_orchestra_job_rpcs.sql","state":"applied_unverified",
           "companion_of":"0002","evidence":"handoff 2026-05-13:19 (grants=postgres+service_role only)"}
        ]
      },
      "PRODUCTION_PLACEHOLDER": {
        "migrations": [
          {"id":"0002","file":"0002_orchestra_jobs_security_definer_rpcs.sql","state":"file_only",
           "note":"MUST apply 0002b immediately after 0002 or authenticated keeps EXECUTE"}
        ]
      }
    }
  }
  ```
  `state ∈ {file_only, applied_unverified, applied, superseded}`. **`applied`는 운영자-게이트 live 권한덤프로만 승격** (handoff는 파일 *존재*만 입증, fresh grant dump 아님).
- **risks**: ledger의 `state` 필드는 live 읽기가 아니라 evidence 기반 → out-of-band 적용 시 value-drift 가능(A/B/C는 file-set/prose drift만 잡고 value drift는 못 잡음; `verified_on`으로 staleness 가시화). B의 grep은 **반드시 scope** 必(미스코핑 시 `nas_sanity_scan.md:4`, `writing_agent_prompt_pack.md:277`, `config.example.yaml`에서 오탐). id 파싱은 `^(\d{4}[a-z]?)` 로 letter suffix 보존(0002 vs 0002b 충돌 방지).
- **rollout**: §3 참조(2-phase).
- **hard-gate 충돌**: **없음**(infra/DB/secret/deploy/broad-refactor/irreversible 전부 clean — 적대검증 확인).

### MVP② live-surface-registry
- **SSOT**: `LIVE_SURFACES.yaml` — 외부노출 표면(Vercel 라우트·Supabase 프로젝트/테이블·NAS 포트·backend 모드) 1행/표면. landing page·러너북 prose는 여기서 *파생*.
- **무엇이 중복**: `app/page.tsx:6` "No production endpoints active"(=거짓, HMAC 웹훅 prod 라이브) + `:10-12` "/orchestra development mock only", `auth.ts`/`backend.ts` 모드계약, `query_payload_lifecycle.md:238` "planned"(이미 landed), 그리고 **§0 cross-repo 표면**(옛 geochem Supabase anon-read 미발표데이터, `labels` anon-write, NAS reader :8765/:8766).
- **drift check**: static — (1) schema validate, (2) row의 evidence 코드가 아직 존재하는지(예: 웹훅 라우트에 prod 404가드 없음 vs dev/trigger엔 있음), (3) `prose_refs`에 금지구절 grep.
- **하드게이트 충돌(중요)**: registry가 *live 현실과 맞는가*는 정적체크가 **하드게이트 위반 없이는 증명 불가**(Supabase/Vercel/NAS 질의 필요). → in-scope 체크는 **static-only**(registry vs 인용코드 + registry vs prose), live 대조는 **운영자-게이트 deferred**. §0 cross-repo 행은 **in-repo evidence 파일이 없어** row-shape만 검증 가능(가장 값진 행이 가장 약하게 검증됨).
- **약점**: 가장 안 작음(repo-wide), forbidden_phrases는 denylist 휴리스틱(리워딩으로 회피).

### MVP③ operator-decision-ledger (`decisions.yml`, anchor-grep)
- **SSOT**: `docs/decisions/decisions.yml` — 결정 1개/레코드, 각 결정이 `surfaces[]`(반영돼야 할 path:anchor) + `expect`/`forbid` 마커를 나열. 체커가 각 surface를 grep → 불일치 시 nonzero. 결정 내용을 파일마다 재타이핑하지 않음(마커만 비교).
- **무엇이 중복**: senpAI "벽" 6레이어(prompt 완화 vs 설계doc/README/open_decisions A3/`senpai_profile.py`/example/tests 옛 벽) + `ORCHESTRA_DECISIONS.md`의 "Unblocks" 열(타깃 나열하나 미검증) + `_needs_operator.txt`의 14개 `pend:` 태그.
- **중심 risk(운영자가 지목)**: *원장 자체가 또 drift하는 prose 테이블이 됨.* 완화는 구조적 — `answer`(사람용 prose)는 비교대상 아님, 체커는 `surfaces[].expect/forbid` 마커만 비교. 잔여: ledger-내부 drift(answer vs 마커)는 미검증; 마커가 brittle string("never drafts")이라 의미보존 리워딩에 뚫림; 테스트 의미변경은 grep 불가(operator_verify 플래그).
- **branch-reality 결함**: **헤드라인 예시 전체가 현 브랜치에 없음**(`tools/research-discussion/v0` = `.scratch/senpai-branch`에만). 체커가 자기 동기 drift를 못 돌림.

### 대안④ `pend:`-태그 closure ledger (MVP③의 substrate)
14개 ad-hoc `pend:` 태그(`P0-supabase-grants`, `crossreview_20260603_*`, `A-geochem-*` 등)에 `{id, status, decision, closing commit/PR, owner}` 부여 + 정적체크(모든 태그가 ledger 행으로 resolve / landed인데 commit 없으면 fail). MVP③을 subsume. **단 judge 평가**: 태그들이 scratch 파일에만 살고 in-repo cross-reference가 0 → 검증할 "두 번째 사본"이 없음. 그리고 지배적 drift(migration)는 결정-closure 갭이 아니라 코드/테스트/러너북 모순 → ①보다 약함.

---

## 3. 추천 = MVP① · **2-phase로** (적대검증이 강제한 분할)

적대검증 Skeptic-B가 "파일1개+체크1개=small"을 **refute**: green 되려면 SQL헤더 5 + 0001 + queue/README + claim_client 주석 + 정적테스트 3 + 러너북 §1/§6 ≈ 8+파일을 원자적으로 수정해야 함(Part B가 통과하려면 de-prose 선행, 정적테스트의 literal "not applied" assert도 같은 커밋에서 재작성해야 suite가 안 깨짐). 인프라 게이트는 전부 clean이나 *small* 주장은 거짓. → **분할이 정답**:

- **Phase 1 — 진짜 MVP-small (순수 additive, 기존파일 0건 수정, repo as-is에서 PASS)**
  1. `APPLY_STATE.json` 추가(evidence 시드, `applied_unverified`로).
  2. `test_migration_apply_state_ledger_synthetic.py` 추가 — **Part A(coverage) + Part C(filename) 만**. 이 둘은 헤더·테스트·러너북을 *건드리지 않고* 통과(ledger가 실파일 집합을 enumerate하고 참조가 resolve되는지만 assert).
  - = 문자 그대로 "ledger 1개 + 체크 1개", 기존파일 미터치. 비치헤드 증명.
- **Phase 2 — 별도 게이트(=MVP 주장에서 분리)**
  3. de-prose: 5 SQL 헤더 + `0001_init:3` + `queue/README.md:7-8` + `claim_client.py:199` 를 posture-only + ledger 포인터로.
  4. 정적테스트 `test_migration_0002/0003/0002b_*` 의 상태-assert를 ledger-일관성 assert로 재작성.
  5. 러너북 §1/§6: 5파일 전부 정확한 파일명으로 열거(+ :189 오타 수정) + 각 b-revoke를 부모 직후 적용 명시 + 상태대신 ledger 링크.
  6. **그다음** Part B(scoped banned-prose grep) 활성화 — `Status:` 헤더줄 + 러너북 마이그레이션 섹션으로 **scope 한정**(오탐 방지).

**적대검증이 추가로 확정/요구한 것** (전부 실파일 대조됨):
- Part A 체크는 *오늘* 실제로 red — 5 헤더 모순 + 러너북 오타 파일명 모두 현재 fail함(Skeptic-A trace).
- `currently_duplicated_in` 보강: `0001_init:3`, `queue/README.md:7-8`, `claim_client.py:199` 추가(third triple).
- evidence 충실도: handoff `:19` 는 `postgres_and_service_role_only` → ledger에 "service_role only"로 의역 말고 **verbatim "postgres + service_role only"**.
- PyYAML은 worker dep(`requirements.txt:13`)이라 신규의존 아님 — 다만 JSON으로 가면 정적테스트 stdlib-only 유지(권장).

**왜 ①이 비치헤드인가 (generalization)**: A(파일집합 coverage)+B(no-prose grep)+C(filename) 3-assert 골격은 그대로 ②(라우트파일 coverage + page.tsx no-prose)와 ③(`surfaces[]` coverage + forbid 마커)에 떨어진다. ①만이 **이 브랜치에서 하드게이트 안에서 fail-loud→green 까지 전부 실행 가능**(파일집합 coverage는 휴리스틱 아닌 closed enumeration, 모순은 verbatim·적대적 — 테스트가 틀린 답을 literal하게 고정).

---

## 4. 왜 ②③을 먼저 안 하나
- **③ (decision ledger)**: 패턴 자체는 "결정1개 N레이어"를 가장 깔끔히 일반화. 하지만 헤드라인 예시(senpAI 6레이어)가 **현 브랜치에 부재**(`.scratch/senpai-branch` 전용) → 자기 동기 drift를 못 돌림. branch-present 가치는 14 `pend:` 태그에 closure home 주는 것(=대안④)인데, 이건 bookkeeping이라 ①(3갈래 틀린 보안사실)보다 leverage·fit 낮음. **②보다는 위(2순위)** — 작고 gate-safe하고 pend: closure 효용이 실재.
- **② (live surface)**: drift 실재(page.tsx 거짓 확인)하고 운영자가 docs를 계약으로 취급해 통증 큼. 하지만 가장 값진 행(§0 cross-repo)이 in-repo evidence 없어 가장 약하게만 검증됨 + denylist 휴리스틱 + repo-wide(안 작음). 가장 **소프트한 지반**에서 패턴 증명. **3순위.**

→ **순서 제안: ① (2-phase) → 빠른 후속으로 ④-맛 `decisions.yml`(14 pend: 태그 closure home) → ② live-surface는 운영자 §0 remediation과 묶어서.**

---

## 5. Codex 수렴 포인트 (여기에 판단 줘 — 합의 후 운영자 1줄 에스컬레이트)

1. **비치헤드 동의?** ① migration-apply-state 먼저 vs ③/④ 먼저. (branch-reality 논거 — senpAI 예시가 이 브랜치에 없음 — 에 반론 있나?)
2. **2-phase 분할 동의?** Phase1 additive-only(coverage+filename)만 먼저 land vs ①을 한 커밋에 통째로. 나는 phased 추천.
3. **JSON vs YAML** ledger. 나는 JSON(정적테스트 stdlib-only). 반대 있나?
4. **위치**: `tools/paper-orchestra/queue/migrations/APPLY_STATE.json` (마이그레이션 옆) vs 미래 일반화 위한 top-level `ledgers/`. 나는 전자(작게 시작).
5. **state 어휘**: `applied_unverified` 도입 + `applied`는 운영자 live-probe로만 승격, 동의? (handoff는 파일 존재만 입증.)
6. **`probe_apply_state.py`** (운영자-게이트, `pg_proc/has_function_privilege` read → ledger 작성): v1 후속으로 스펙만 잡아둘까, 아니면 완전 out-of-scope로 둘까. (CI엔 절대 안 들어감 — 하드게이트.)

추가로 **놓친 drift 군집/더 나은 SSOT 형상**이 보이면 카운터-제안 환영. 핑퐁 1라운드로 수렴 목표.

---

## 6. 하드게이트 / 상태
- 이 노트까지 **read-only**(4-mapper+3-judge+3-skeptic 전부 읽기전용) — live infra/DB/secret/deploy 미터치, 프로덕션 코드 미편집.
- corpus/paper/sidecar/index/wiki/figure **미터치**. 이 노트는 `LEDGER_` 프리픽스 코디네이션 노트 전용(그림/PDF verifier 워크플로와 분리).
- **commit/push 대상 = 이 파일 1개.**
- 다음: **Codex VERDICT + §5 카운터-의견 대기.** 그 전 구현 0.
