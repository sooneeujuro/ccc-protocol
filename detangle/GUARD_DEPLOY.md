# 축 A — 전 repo corpus 가드 배포 (gitignore + pre-commit hook)

목적: 어떤 코드 repo의 git에도 저작권 코퍼스/대용량 산출물이 *새로* 안 들어가게. (이미 들어간 것 = 별도 history rewrite.) 전부 비파괴(ignore는 디스크 안 지움) — 단 repo 커밋이라 **운영자 GO 게이트**. Codex 검증 후 적용.

## 1. pre-commit hook (`scripts/precommit_corpus_guard.sh`)
- 코퍼스/대용량/백업 잔여물이 staged되면 commit 거부. 의도적이면 `ALLOW_CORPUS_COMMIT=1`.
- 설치(clone마다 — hook은 git 따라 안 감):
  ```sh
  cp detangle/scripts/precommit_corpus_guard.sh <repo>/.git/hooks/pre-commit
  chmod +x <repo>/.git/hooks/pre-commit
  ```
  (또는 공유: `git config core.hooksPath <shared-hooks-dir>`.)

## 2. repo별 `.gitignore` 추가 (커밋 = GO 게이트)
### manuscript-atelier
```gitignore
# 저작권 figure/MD 파생 (P0 LANDMINE) + 인덱스 백업/리포트 잔여물
docs/handoffs/**/out/
docs/handoffs/**/out_raw/
docs/handoffs/**/*.jpg
docs/handoffs/**/*.jpeg
docs/handoffs/**/*.png
**/index/*.bak.*
**/index/*.report.json
```
> index 본체(bm25/units/npy)는 이미 `.gitignore:23`로 무시됨 — 위는 백업/리포트 잔여물만 추가.

### geochemistry-analyzer
```gitignore
# 코퍼스 콘텐츠 (앱 런타임 미사용) — 단 variable-vocabulary.json은 빌드 의존이라 제외
wiki/papers/
wiki/data/
tools/geochem-stats/corpus/
paper1-CIR-volatiles/
!tools/geochem-stats/index/variable-vocabulary.json
```
> ⚠️ **이미 git에 tracked**라 ignore만으론 history에서 안 빠짐 → 별도 filter-repo(E단계, GO). ignore는 "앞으로 안 늘게".
> ⚠️ **`variable-vocabulary.json`은 빌드 static import** → 절대 빼지 말 것(FUNCTIONALITY_GUARDRAILS #3).

### sooneeujuro-web
- 코퍼스 0 → hook만 보험으로 설치. gitignore 추가 불요.

## 3. Codex 검증 대기
- 가드 regex가 코퍼스(out*·wiki·sidecar·*.npy·*.bak.*)를 **잡는지** + 앱 정상자산(public 이미지 등)을 **오차단 안 하는지** 교차검증 → `inbox_codex/002`.
- 검증 통과 후 운영자 GO 받아 repo별 적용.
