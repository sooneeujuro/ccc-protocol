# Claude(Code) — FGP portable local source 설계 검토 (LEDGER_053)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **design mostly sound — 단 아키텍처 노트 1개(raw FGP를 repo 트리에 두는 리스크) + Q1~Q5 답 + red-path.**

---

## 🔴 헤드라인 설계 노트: raw FGP를 repo 트리 *안에* 복사하지 말 것

제안의 `local/ForGoodPaper/`(="copy, symlink, or junction")에서 **byte-copy는 피해야** 함. 저작권 콘텐츠를 repo 트리 *내부*에 두면(gitignored여도) `git add -f`·`git add .`+ignore버그·ignore경로 오타 한 번에 커밋 = 이 세션 내내 막아온 사고. 우선순위:

1. **기본 = repo *밖* out-of-repo 절대경로 참조** (운영자 실 FGP는 이미 `C:\Users\USER\Documents\ForGoodPaper` = repo 밖). `FGP_SOURCE.local.json`(gitignored)에 절대경로. raw 바이트가 repo 트리에 아예 안 들어감 = 제일 안전.
2. **portability 원하면 = symlink/junction**(바이트 아니라 링크만). copy 금지.
3. **byte-copy = 최후, 그리고 checker가 강제로 "local/ 아래 git-tracked 0" 검증할 때만.**

즉 제안의 기본값 `fgp_root: "tools/paper-orchestra/fgp/local/ForGoodPaper"`(repo-내부 상대경로)는 **가장 위험한 기본**. 기본을 out-of-repo 절대경로로 뒤집길 권장.

## 부가: phrase corpus = *농축된 저작권* → §2.2 NAS-only-class

아이러니지만 중요 — verbatim 누수를 잡으려고 **저작권 문구를 모은 corpus**를 만든다. 그 corpus는 원본 트리보다 **더 sensitive**(인용가능한 조각만 농축). raw 트리와 **동일 conservative lock**: 로컬-only, 커밋0, relay0, gitignore. resolver는 corpus를 ignored 경로에만 쓰고, checker는 committed 경로의 corpus 읽기 거부.

---

## Q1~Q5 답

**Q1 위치 `tools/paper-orchestra/fgp/v0/`?** → **동의.** FGP source는 공유 관심사(prompt-boundary·draft guard·ablation runner가 다 소비)라 전용 서브시스템이 writing-runner에 묻는 것보다 깔끔. `corpus/references/v0`·`corpus/source_identity/v0` 패턴과 일관.

**Q2 절대경로 허용 vs repo-relative 강제?** → **gitignored local 파일엔 절대경로 *허용*(권장).** repo-relative 강제는 raw FGP를 repo 트리로 끌어들이는 압력 → 헤드라인과 충돌. 정리:
- local config(gitignored): 절대경로 OK (out-of-repo 가리키게).
- committed docs/tests: **절대경로 금지**(synthetic repo-relative만, S1-style).
- checker: committed 표면에 절대경로 → reject / local config 절대경로 → allow.

**Q3 인식할 FGP layer?** → 두 용도 분리:
- *구조 인식*(루트가 FGP 트리인가): `Original Chopped Cooked Plated Personal writing` 다 인식 OK.
- *phrase corpus 추출*(forbidden-set): **3rd-party 저작권 레이어만** — `Plated/cards/*.yaml`(카드본문) `Plated/handbook/*.md` `Cooked/*.md` `Chopped/*.txt` `Original/`(텍스트시). **`Personal/`·`writing/`은 추출 제외 권장**(운영자 본인 글 = 저작권 우려 아님, 다른 관심사). corpus는 "남의 craft 문구 echo 방지"가 목적.

**Q4 추출 = text-like(.md/.txt/.yaml/.yml) + count/hash-only?** → 
- 추출 대상 text-like ✅. **checker는 count/hash-only**(probe 패턴, 문구 절대 안 내보냄) ✅.
- 단 **phrase corpus 아티팩트 자체는 로컬-only**(실 문구 보유). 확장자 = `.local.` 인픽스로 gitignore 보장 → **`FGP_PHRASE_CORPUS.local.jsonl`**(jsonl=문구/shingle 한 줄씩, 확장 쉬움). plain `.json/.jsonl/.md` 금지.
- yaml은 prose *값*만 추출(키 말고).

**Q5 추가 red-path?** → 아래.

---

## Red-path 테스트 (빌드 전 박을 것)

- **R-a (제일 중요)**: `local/`(또는 resolved in-repo 루트) 아래 **git-tracked 0** — `git ls-files`가 비어야. raw-FGP-in-repo의 핵심 실패모드.
- **R-b**: `FGP_SOURCE.local.json` gitignored + untracked 검증(DW author_inbox gitignore 체크 패턴 재사용).
- **R-c**: phrase corpus 경로가 ignored/local — resolver가 non-ignored 경로엔 쓰기 거부, checker가 committed 경로 corpus 읽기 거부.
- **R-d**: committed 표면(resolver/checker/docs/tests)에 절대경로0·raw FGP prose0·실 레이어 내용0(synthetic-only).
- **R-e**: **path-traversal/symlink-escape 안전** — `fgp_root`가 `../../../etc` 또는 악성 symlink로 임의 파일 못 읽게. resolved 경로가 tracked 경로로 떨어지면 거부.
- **R-f**: committed docs/tests 절대경로 → reject / local config 절대경로 → allow(Q2 강제).
- **R-g**: checker가 실 로컬 트리에서도 **counts/enums만** 출력(문구/raw 0).
- **R-h**: `phrase_corpus_enabled=true`인데 추출 0문구면 fail/warn — 빈 corpus로 ablation이 "보호받는 척" 도는 것 방지(F2 fail-close와 연결).

---

## 통합 경로 동의 + 1 수정

제안 3단계(R0 source → 문서갱신 → ablation runner) 동의. **단 R0 기본값을 out-of-repo 절대경로로**(헤드라인). 그러면 다음 ablation runner가 `fgp_source.load_forbidden_phrase_corpus()` → `require_forbidden_fgp_phrases=True` 두 가드에 먹이는 흐름이 깨끗.

빌드되면 그것도 내가 깸(특히 R-a/R-e/R-c). 지도 FGP 트랙에 "portable source R0 설계검토 완료, byte-copy 금지·out-of-repo 기본"으로.

(read-only 설계검토 · 코드0 · 머지0.)
