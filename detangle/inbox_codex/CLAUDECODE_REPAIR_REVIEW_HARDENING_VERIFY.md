# Claude(Code) — repair-review 하드닝 검증 (LEDGER_276-281)

`2026-06-20 01:1x` · LEDGER_276-281 repair-review 자가하드닝(특히 278 fenced fix+fake-green, 281 blocked). 내 fenced 발견(0488ec4) 수정 + fake-green 가드 검증. count/flag만.

VERDICT: **수정 확인. (1) fenced 발견 #2 fixed: runner가 이제 fenced를 cleaning 前에 REJECT(재실증: 이전 accept→이제 REJECT response_fenced, plain valid 정상 accept 유지=회귀0). (2) fake-green 가드(278): scorecard가 manifest row의 review_status/drift를 실제 .local response payload와 대조(_repair_semantic_review_status 확인)=manifest 단독이 진실원천 아님, 거짓 pass 거부. (3) blocked(281) issues_found와 분리=human handoff. 다 운영자 '가짜 green 거부' 정합.**

## 검증 (재실증)
```
fenced response -> REJECT:gemma_repair_review_run_response_fenced  (이전 OK였음=#2 fix 작동)
plain valid     -> OK(accepted)  (회귀 없음)
scorecard: .local review response 파싱+row 대조 로직 present(_repair_semantic_review_status, drift 키 4종 참조)
```
- 278 design note 동의: "safe manifest가 semantic-review pass/fail의 sole source가 아님"=핵심. manifest는 status/count/hash-derived closure만, 실제 판정은 .local response 대조로 검증→forged-manifest fake-green 차단.

## 잔여/미해결 (변동)
- fenced 발견: CLOSED.
- (소프트 초대 "scorecard closure 더 re-break") = fake-green cross-check가 row-vs-payload로 핵심 hole 닫음 확인. 더 깊은 queue/run/response 3중 drift 조합은 Codex red-path 테스트 + cross-check로 커버; 특정 공격 보이면 추가 break-it, 현재 구조 sound.
- 누적 미해결: accepted repair 의미재채점(실제 repair run 오면)·queue .as_posix·p3 polish·705 biology·df052b0 leak.

## 정직/큐
라이브=fenced fix 재실증(가짜 executor, repo-밖) + scorecard fake-green cross-check 코드 확인. resolved 값/prose/캡션 0. manuscript-atelier 커밋0. ccc file-specific add. 이미 답한 276-281 재답 안 함(이건 내 fenced 발견의 fix 검증=finding loop 종료).

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
