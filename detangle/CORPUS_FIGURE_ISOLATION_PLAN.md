# CORPUS 그림 폴더 격리 계획 (2026-06-18)

bare-hash 충돌로 corpus 그림 77.4%가 꼬임 → **이미지를 논문별 폴더로 격리**해서 충돌 원천 차단. 합의된 설계.

## 문제 (측정 완료, 비용 0 / detangle/scripts/corpus_hash_collision)
- 이미지가 `<hash>_img.jpg` (논문 구분 없는 bare 파일명) → 다른 논문의 다른 그림이 같은 hash로 **서로 덮어씀**.
- 논문 3,903편 분류:
  - **A. 진짜 꼬임(figure 충돌): 3,019편 (77.4%)** ← 재추출 대상
  - B. 로고/표지만 공유(무해): 7편
  - C. 깨끗(그림 있고 충돌 0): 848편 (21.7%)
  - D. 그림 없음: 29편
- 충돌 hash 1,294 (진짜 figure 1,130 + 로고 164). 최악: olivine 그림 1개를 811편이 공유.
- 단독 참조 1,037편 = 샘플 3/3 검증상 정상(이미지=논문 일치) → **재추출 제외 가능.**

## 해결 = 이미지만 폴더 격리 (MD는 flat 유지)
```
articles/
  <paper_id>.md                      ← MD는 flat 그대로 (index/sidecar 무손상)
  <paper_id>/                        ← 이 논문 이미지만 격리
      <hash>_img.jpg …
```
- MD 본문 참조: `![](<paper_id>/<hash>_img.jpg)` (상대경로)
- `paper_id` = MD stem (= sidecar id = retrieval_units text_path/paper_id). 새 ID 안 만듦.
- 다른 논문은 다른 폴더 → 같은 hash여도 충돌 불가.

## 의존성 (조사 완료)
| 대상 | 영향 | 근거 |
|---|---|---|
| retrieval_units / bm25 / bge / 검색 | ✅ 무손상 | 레코드에 이미지 경로 키 없음 (text_path=MD파일명, paper_id만) |
| sidecar (`md_file`) / wiki | ✅ 무손상 | MD 파일명만 참조 |
| **`read_paper.py` (운영 reader)** | 🔧 수정 | 현재 basename flat 가정(`(ARTS/name).exists()`, base_href=articles/) → `<pid>/` 상대경로 resolve로 패치 |
| 빌드도구 (fig_render_audit / convert_pdfs / fig_fill) | 🔧 파이프라인서 갱신 | 운영 아님 |
| ⚠️ NAS 배포 reader (`md_view.py` 언급) | ❓ 미확인 | corpus 밖. 운영 reader면 같은 패치 필요 — **위치 확인 필요** |

## 재추출 (그림 복구 — 재명명만으론 덮어쓴 픽셀 복구 불가)
- 대상: 충돌 영향 3,019 ∩ PDF 보유 ≈ **2,900편**.
- 모드: **accurate / LLM_off** (그림만 필요, 텍스트는 LLM_on 초고 유지가 목표 → 그림만 교체 머지 권장).
- 파이프라인: PDF → `_rebuild_20260618/<paper_id>/` 폴더(provenance) → `articles/<paper_id>/` 배포 + MD `![]()` 갱신.
- 검증된 패턴: 이번 세션 51편을 `slug__hash` namespace로 머지 → 충돌 0 (fig_merge.py).

## 미해결 (재추출 GO 전 확정할 것)
1. **NAS reader(`md_view.py`) 위치/패치** — 운영 reader면 read_paper.py와 같이 폴더-resolve 패치.
2. **LLM_off 단가** — 이전 cost ledger or Datalab 가격표 → 2,900편 비용 못박기 (이전 LLM_on 편당 ~$0.15, off는 더 쌈 추정).
3. **재추출 GO** — 비용 확정 후 운영자 승인.

## 파일럿 결과 (2026-06-18 15:10) ✅ 검증 완료
- 10편 `convert_pdfs.py`(accurate, LLM_on) → `G:\corpus_rebuild_20260618\<slug>\`. **$1.34 (편당 $0.134)** → 전체 2,900편 ≈ **$389**.
- 구조: `<slug>/` 폴더 + `<slug>__<hash>_img.jpg` (이중 prefix). slug 0충돌.
- 그림 검증: `001e3e69` = Jolivet & Tamaki 1992 — figure 12개 alt 정확(Japan Sea tectonics), 실제 렌더(Japan Sea 지도 15/25 m.y.)도 일치.
- **격리 증명**: 충돌 hash `2236272d`가 기존 corpus엔 Sawai biostrat였는데 새 폴더선 Japan Sea 지도 = namespace로 안 겹침.
- **LLM 단가 정정**: convert_pdfs 주석 "use_llm on/off **비용 동일**" → LLM_on 유지(텍스트 품질↑, 비용 같음). off 이점 없음.
- convert_pdfs가 이미 폴더격리+namespace 내장 → 파이프라인 새로 짤 것 없음. `--in <pdf폴더> --out <새corpus> --mode accurate --budget <cents>`.
- 미해결: ① 전체 2,900편 GO ② reader(read_paper/md_view) 패치 ③ 새 slug(md5(pid)[:12]) ↔ 기존 paper_id 매핑(통합/교체용).

## 하드게이트
- live corpus 비파괴. 재추출은 staging(`_rebuild`)에서, articles 배포는 운영자 OK 후.
- corpus 본문/이미지/index git push 0. 이 계획/스크립트만 push.
