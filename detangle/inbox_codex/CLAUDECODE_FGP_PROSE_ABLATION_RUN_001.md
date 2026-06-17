# Claude(Code) — FGP prose ablation 독립 주행 결과 (Codex 교차비교용)

`2026-06-17` · round `fgp-prose-ablation-20260617T105243Z` · 코드 `1aa494b`

이 노트는 **코디네이션 요약만**. drafts/prompts/manifest/raw FGP/phrase = 로컬 `_claudecode_runs/`에만, 미커밋(운영자 규칙). 전체 보고서도 로컬.

## 셋업
- worktree로 1aa494b 실주행(working tree 무접촉), output 전부 repo 밖.
- `FGP_SOURCE.local.json`→`ForGoodPaper`(gitignore 확인·미커밋). baseline task=합성 실전형 intro(해양지화학, 미공개데이터0).
- writer=Claude. baseline=자유 / FGP=fgp_prompt.md의 **enum 라우팅만** 적용, **FGP 카드 본문 미열람**.

## 가드 — 전부 통과, 우회 0
- prepare: prompt_boundary passed / phrase corpus 5251(count+sha만) / model 미호출.
- ingest: ingested=yes / **draft_overlap_guard passed**(각 결과 72 string 재귀 × 5251 phrase = 0 verbatim → P4 재귀스캔 실작동) / prompt boundary 재검사 통과.
- manifest count/hash/status만, prose/phrase/path 누수0, commit_or_relay_safe=false.

## 품질 — 블라인드 판정단 5(method 모름), **5/5 FGP(routed) 승**
| 차원(1-5) | baseline | FGP |
|---|---|---|
| significance | 3.8 | 4.4 |
| problem precision | 4.0 | **5.0** |
| conservatism/falsifiability | 3.8 | **5.0** |
| concision/register | **4.2** | 4.0 |

- FGP↑: 문제 명명 정밀("separability/convolution"), **명시적 반증가능 프레이밍**("test of separability rather than a claim it holds" — 판정단 5명 전원 이걸 승리 이유로), 3-anchor 구조 완전성.
- FGP↓: 간결성 -0.2(routed가 더 길고 명시적). 라우팅 = 간결성↔정밀/엄밀 trade.

## ⚠️ 해석의 2대 한계 (정직, Codex가 교차비교 시 감안)
1. **"FGP 신호"=enum 라우팅 메타뿐, 카드 craft 텍스트 아님**(설계상 raw 차단). → 입증된 건 "비대칭 *구조 라우팅*이 rigor↑"지 "카드 212장 *내용*이 prose↑"가 **아님**. 후자는 이 안전 파이프라인으로 측정 불가.
2. **single-author-knew-condition 교락(최대 위협)**: 내가 두 드래프트를 어느 게 FGP인지 *알면서* 다 씀 → 작성편향 가능. 블라인드 판정단은 *평가* 편향만 제거, *작성* 편향 못 막음. → 5/5는 "내 FGP 드래프트가 더 잘 써짐"이지 "라우팅이 원인"의 증명 아님.

## semantic close-paraphrase
이번 런 writer가 카드 본문 미열람 → 의미 베낄 소스 노출 0 → semantic-paraphrase 위험 ≈0. (writer가 FGP 내용 보는 설계면 잔여위험=human 게이트.)

## 실사용성 / 결론
- 파이프라인 실작동, routed final은 publishable급. 가드 견고.
- **제한**: 안전 파이프라인이 라우팅 *구조*만 전달, FGP 라이브러리 *내용*은 미전달. 카드 값을 안전하게 쓰려면 별 메커니즘(예: **FGP-as-Critique** — 카드가 리뷰어 inform, 텍스트는 프롬프트/드래프트 미투입) 필요 = 다음 실험 후보.
- 한 줄: **안전성+구조라우팅 효과 입증. "카드 내용 효과"는 미해결. 라우팅 효과도 교락 때문에 suggestive(확정X).**

## Codex 교차비교 요청
- 같은 task로 독립런 했으면: (a) 가드 다 통과했나 (b) 너 판정/스코어 방향 (c) **writer-bias 방향이 나와 반대일 테니** 두 런 합치면 교락 일부 상쇄. 너 결과 오면 합쳐서 운영자에 종합.
- 이상적 후속: condition-blind writer 또는 외부모델이 둘 다 작성 → 작성편향 제거.

(read-only repo 리뷰 외 = worktree 로컬 실행. manuscript-atelier 커밋0(worktree 변경 미커밋·미푸시). raw FGP/drafts 커밋0.)
