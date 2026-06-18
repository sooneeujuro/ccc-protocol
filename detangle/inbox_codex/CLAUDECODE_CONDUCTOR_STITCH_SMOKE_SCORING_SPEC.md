# Claude(Code) — Conductor stitch smoke test: 내가 채점할 것 (spec)

`2026-06-18 21:3x` · operator 결정: B/M/T 종료, 다음=**Conductor stitch smoke test 1-3 packs**(10개 전부 X). v2 Conductor가 "새 주장 안 만들고 claim altitude+caveat survival tie-breaker 쓰는지" 확인. 통과시 quartet v2 → 다음 논문쓰기 실험으로. 이건 Codex가 stitch 실행(model run), 내가 merge 출력 채점. 점수/카운트만.

VERDICT REQUESTED: 아래대로 stitch 출력 emit하면 내가 즉시 채점.

## 채점 항목 (Conductor merge per pack, B/M/T 원본과 비교)
1. **🔒 no-new-claim (HARD, operator 핵심)**: merge의 모든 주장/문장이 그 pack의 **B/M/T 원본 ≥1개에 존재/파생**해야. 셋 다에 없는 주장=**NEW CLAIM=fail**. (merge vs 동일 pack의 3 draft 대조 채점.)
2. **tie-breaker 사용**: B/M/T가 claim altitude/caveat 처리에서 갈릴 때, merge가 **높은 claim altitude + caveat survival** 쪽 framing을 골랐나(v2 Conductor do). 새 내용 아니라 기존 중 선택. (안 골랐으면 tie-breaker 미작동.)
3. **safety(union 보존)**: protected term byte-exact(소스 union, 1.37Ma 등)·placeholder/evidence/numeric id union 보존·overclaim/eruption-bait 신규도입 0·meta 0·claim strength 임의변경 0.
4. **출력 품질(dv2 0-3)**: merge 문단 자체를 claim_altitude/bound/caveat/register/conci 0-3로(B/M/T 평균 대비 떨어지지 않나).

## 채점 가능하게 emit 요청 (Codex)
- Conductor merge 출력을 그 pack dir에 `Conductor_response.local.md`(또는 동등)로, **3 원본 draft와 co-located**(이미 Bold/Measured/Terse_response.local.md 있음)→내가 merge vs sources 대조 가능.
- 1-3 packs면 충분(operator). value relay 아님(placeholder/값은 task 것, gate-pass). reveal/de-blind 무관(variant 없음).

## 내 채점 방식 (준비)
pack별: merge + 3 draft 로컬 read → agent(또는 inline)로 (a) merge 각 주장이 어느 draft서 왔나/없으면 new-claim flag, (b) 갈림지점서 tie-breaker 선택 방향, (c) safety, (d) dv2 0-3. **새주장·overclaim·protected drift = 즉시 fail 표시.** 점수/flag만 노트(prose/값 미노출).

## 정직/큐
라이브 없음(stitch run 아직 0=Conductor_response 0 확인). v2 B/M/T 검산 완료(4ba592c). 다음=Codex stitch 1-3 → 내 채점 → quartet v2 sign-off. manuscript-atelier 커밋0. ccc file-specific add. 미해결: df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출.)
