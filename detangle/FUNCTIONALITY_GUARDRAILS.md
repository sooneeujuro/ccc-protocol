# 기능 보존 guardrails — de-tangle 실행 시 반드시 지킬 것

검증: 2026-06-15 멀티에이전트 제품별 런타임 의존성 조사(전체 = `.scratch/functionality_report.md`).

## 결론
**작품 4개 다 작동함.** verdict: sooneeujuro-web=`preserved`(무조건), geochemistry-analyzer·manuscript-atelier·corpus-search=`preserved-if`(아래 guardrail 지키면 100%). **git-tracked 경로를 런타임에 읽는 제품 = 0개** → de-tangle은 git만 건드리고 앱은 디스크/NAS/배포에서 읽으므로 런타임 무관.

de-tangle 액션 A(P0 gitignore)·B(코퍼스 git-out)·D(클론정리)·E(history rewrite) = **순수 git-only, 런타임 무해.** C(GCA freeze)만 1개 실-결합점.

## 반드시 지킬 guardrails (이걸 지키면 기능 100%)
1. **[치명] manuscript-atelier 물리 index 보존** — `tools/paper-orchestra/corpus/index/{bm25_index.pkl, retrieval_units.jsonl, retrieval_papers.json, embeddings_bge_m3.*}` 삭제/이동 금지. 옮기면 env(`GEOCHEM_BM25_INDEX` 등) 설정.
2. **[footgun] `.gitignore` 먼저 조이기** — index 디렉터리 `*.bak.*` + `*.report.json`이 untracked-but-not-ignored → `git add` 전에 ignore 추가(안 그럼 `git add -A`가 수백MB stage). P0 LANDMINE과 같은 부류.
3. **[치명] geochemistry-analyzer `tools/geochem-stats/index/variable-vocabulary.json` live 트리 유지** — 빌드가 static import(`mixing-mode-inference.ts:23`). live 트리에서 git-out/strip 금지. **history-only strip은 OK.**
4. **[치명] GCA Vercel 배포 LIVE 유지** — freeze=commit금지는 OK, **deployment pause/delete 금지**(manuscript-atelier `.mcp.json:7`이 런타임 호출). C를 commit-freeze로만 하면 무해.
5. **[치명] corpus-search G: + .mcp.json 보존** — `G:\corpus_md_export_20260602\{index,articles}` 삭제 금지(self-anchor). `.mcp.json`에 절대 G: args + offline env(`HF_HUB_OFFLINE=1` 등) 유지(빠지면 모델로드 ~17분 행).
6. **[E 전제] 비-git 자산 out-of-band 백업** — `.env.local`·10.3GB index·`datalab/` MD는 git에 없음 → force-push/re-clone **전에** 별도 스냅샷, re-clone 후 동일 경로 복원. (A4/A5 코드는 git에 있으니 push 백업으로 충분.)
7. **[D] 삭제 클론이 진짜 중복인지** — unpushed=0 **그리고** live index·`.env.local` 미보유 트리인지 확인 후 삭제. Vercel-linked 정본 remote 보존.
8. **[E 운영] force-push 전 20+ `claude/*` 브랜치·worktree 조율** — 전원 re-clone 필요.

## 보너스 (de-tangle과 무관, 덤으로 고칠 fragility)
- GCA canonical alias `sooneeujuro.com/api/mcp/mcp`가 현재 404(`.mcp.json _comment`) → 현재 vercel.app 직접 URL로 회피 중. 한 줄 고치면 fragile 해소.
- sooneeujuro-web `vercel.json` `/api/orchestra/*` → manuscript-atelier 프록시는 **현재 미사용(dormant)** → freeze돼도 무관.
