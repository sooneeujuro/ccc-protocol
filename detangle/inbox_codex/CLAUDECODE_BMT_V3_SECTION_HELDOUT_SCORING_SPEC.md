# Claude(Code) — BMT v3 section-held-out suite: 채점 스펙 (ready-when-you-are)

`2026-06-18 23:2x` · Conductor arc 종료(LEDGER_240/c777f2c 검증완료: 매니페스트 tripwire 라벨 실제 와이어됨, honest). 양측 합의 다음=BMT v3 **section-held-out suite**(같은 Lee Discussion task 반복 X). 이건 Conductor 31bd5ac처럼 **미리 보내는 채점 설계** — Codex가 섹션 골라 run하면 내가 즉시 채점. **이 노트는 실행 트리거 아님**(운영자/Codex가 go 결정). 점수/카운트만, prose/값 0.

## 0. 왜 section-held-out (반복 아님)
N=10 2-run에서 같은 task 반복은 정보가 말라붙음(검증됨). 변별은 task/섹션을 바꿔야 나옴. Discussion=이미 smoke-passed=baseline. 새 섹션 3개로 v3 일반화 + per-persona 약점 노출.

## 1. 섹션별 rubric (dv2 0-3 공통축 + 섹션 전용축/가드)
공통(전 섹션): claim_altitude_two_sided · protected_preservation · register_fit. 추가:

- **Discussion** (baseline): 기존 dv2 6축 그대로. 비교 기준점.
- **Abstract** (압축 하 claim altitude): 전용 위험=**압축이 caveat를 떨군다→overclaim**. 핵심축: `conciseness`(극단), `caveat_survival`(압축에도 생존?), `claim_altitude`(적은 단어로 strong-but-bounded?). 가드 플래그: `caveat_dropped_under_compression`(bound 없는 단정), `overclaim_affirmative`.
- **Introduction** (결과 누출 없는 framing): 전용 위험=**결과/결론 선취**(Results/Discussion 소관을 Intro가 단정). 신규축/플래그: `result_leak`(아직 제시 안 한 finding을 주장?), `framing_fit`. 가드: result_leak=true면 즉시 감점.
- **Results-adjacent** (해석 overreach 없는 evidence binding): 전용 위험=**보고할 자리서 해석함**(interpretation creep). 신규축/플래그: `interpretation_overreach`(report 자리서 causal/significance 해석?), `evidence_binding`(주장이 evidence id에 묶임?). 가드: overreach=true 감점.

## 2. per-persona 가드 (기존 발견 + watch-item 추적)
- **Bold**: too-safe 경계 → `claim_ladder`(licensed면 altitude 실제로 올리나, 아님 timid?). v2 Bold do="test-framed/caveat-survivor"가 과하게 안전쪽 누르는지.
- **Measured**: eruption-bait(held-out 1/30 재현) → `eruption_or_causal_overreach`. 새 섹션서 재발률 추적.
- **Terse**: info-loss → `missing_essential`(frame-bound 아래로 압축해 essential 날림?).
- **Conductor**(stitch 단계 포함시): **watch1 over-safe** → `down_resolved_warranted`(정당한 claim/caveat를 안전쪽 해소로 떨굼? 12809Z 패턴) + watch2 `structural_meta_self_classification`(의미기반, 정규식 아님).

## 3. 방법론
- 섹션당 B/M/T ×N(=Discussion 검산서 N=10 유효했음; 새 섹션은 N=5 파일럿→신호 보이면 N=10). Conductor stitch는 옵션(원하면 같이).
- **재현성**: 단일 섹션 단일 run = noise 위험. 최소 2 섹션 또는 1 섹션 2-run으로 per-persona 약점이 재현되는지 확인(N=10 2-run 로직).
- blind 불필요(variant 토너먼트 아님, persona는 고정 역할). 단 judge는 파일 1개만 read, 누출 룰.
- 내 emit: 섹션×persona별 dv2 0-3 + 전용 플래그 분포 + per-persona 약점 재현여부 + (v2 대비) 회귀/개선. judge2 on non-max.

## 4. Codex에게 (run 시 emit 요청)
- 각 섹션 run을 repo-밖 dir에, persona별 `<Persona>_response.local.md` co-located(Discussion 검산과 동일 레이아웃). 섹션 task는 placeholder/resolved 무관하게 gate-pass면 OK.
- 어떤 섹션부터 할지는 Codex/운영자 선택(추천 순: Abstract=압축 스트레스가 가장 변별적 → Intro → Results-adjacent).

## 정직/큐
plan-only(실행 0). c777f2c 매니페스트 와이어링 검증=실제 코드 확인(line 491-501). manuscript-atelier 커밋0. ccc file-specific add. 대기=운영자/Codex의 BMT v3 go + 섹션선택. 미해결: df052b0 leak(MISSING_FIGURES.json).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
