# Claude(Code) — 7051602 게이트 패치 break-it 재검 (adversative negation)

`2026-06-19 00:3x` · Codex 7051602("close adversative negation gate", MA 로컬)로 line 68 lookahead에 `but|yet|and` 추가. 내 포괄 배터리(실제 모듈 import, 합성입력, 누출0)로 재검 = `gate_negation_battery.py`. 점수/카운트만.

VERDICT: **주요 우회(but/yet/and contrast-flip) 4/4 닫힘=순개선. 단 (a) adversative 세트 불완전: however/whereas(아마 although/though/while)는 여전히 통과, (b) 선재 갭: neither...nor 오탐. 둘 다 follow-up 권고지만 v3 재런 blocker 아님(잔여 좁음+의미채점 backstop).**

## A. 배터리 결과 (실코드 7051602)
```
✅ 닫힌 우회 (이전 MISS→이제 REJECT):
  "does not vary but controls the signal"     REJECT
  "is not absent, and drives the pattern"     REJECT
  "does not weaken yet drives the coupling"   REJECT
  "is not small but proves the result"        REJECT
  "does not fail but demonstrates ..."        REJECT
  "is not weak, and reveals the process"      REJECT
✅ genuine negation 회귀 없음 (여전히 pass):
  does not control / do not control / never controls / without driving /
  rather than control / instead of driving / cannot drive /
  "does not control or drive" / "does not control and does not drive"
✅ affirmative/가짜negation 여전히 REJECT: "controls"/"not only controls"/"drives"/"does control"/거리먼 negation
❌ 잔여 우회 (여전히 통과, want=REJECT):
  "does not trigger melting HOWEVER controls the pathways"   pass  <-- however 미포함
  "is not minor, WHEREAS it drives the coupling"            pass  <-- whereas 미포함
❌ 선재 precision 갭 (오탐, want=pass):
  "neither controls nor drives the signal"      REJECT  <-- 'neither' cue 아님
  "neither demonstrates nor proves the coupling" REJECT
```

## B. 정확한 원인 (patched regex line 62-70)
- 추가: `(?:\W+(?!only\b|but\b|yet\b|and\b)[A-Za-z...]){0,3}` — but/yet/and를 중간단어로 못 쓰게 → 그 3개 contrast-flip 닫힘.
- **누락**: lookahead에 however/whereas/although/though/while 없음 → 이들 뒤 affirmative 금지어가 3단어 내면 여전히 "negated" 오인 통과. (위험 방향=overclaim 통과, 단 이 접속사들은 but/and보다 덜 흔함.)
- **선재**: cue alternation(line 64)에 no/not/never/without만, **neither/nor 없음** → "neither X nor Y"(정당 bounding)을 false-reject. precision 손실(위험 방향 아님), 패치 회귀 아님.

## C. 권고 (follow-up, blocker 아님)
- (a) line 68 lookahead 확장: `(?!only\b|but\b|yet\b|and\b|however\b|whereas\b|although\b|though\b|while\b|nonetheless\b|nevertheless\b)`. → however/whereas류 닫힘.
- (b) line 64 cue에 `neither` 추가(또는 `\bneither\b...\bnor\b` 처리) → neither/nor 오탐 해소.
- 근본 한계: regex는 negation scope를 완전히 못 풂(meta-가드와 동일). 위 둘 패치해도 더 꼬인 구문은 남을 수 있음 → 의미채점 backstop 유지. 내 dv2 overclaim/causal 플래그가 잔여를 잡음.
- **v3 재런 진행 OK**: 잔여(however/whereas)는 좁고, 그런 출력 나오면 내 채점이 overclaim으로 잡음. 재런 막을 필요 없음.

## 정직/큐
라이브=패치된 게이트 실모듈 import break-it(합성입력). 주요 우회 닫힘 확인 + 잔여 2종(adversative 불완전·neither/nor) 발견. manuscript-atelier 커밋0. ccc file-specific add. 참고: Abstract v3 재런 002842 in-flight(002740은 prepare서 abort된 dead dir). 미해결: 게이트 follow-up(however/whereas·neither)·v3 재런 채점·df052b0 leak.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
