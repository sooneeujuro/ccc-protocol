# Claude(Code) — v2 held-out smoke-test run 시작 직후 crash (PowerShell 버그)

`2026-06-18 20:3x` · `quartet_v2_heldout_take87_n10_20260618T111819Z` 채점하려 폴 → **run이 launch 직후 죽음**. 채점 불가(response 0). 게이트=우회/가짜채점 금지, 사유기록+flag.

VERDICT: **blocked — v2 held-out run이 모델 호출 0회로 crash. runner의 PowerShell logging 라인 quoting 버그. 수정+재launch 필요. (profile v2 코드/내 채점기 문제 아님.)**

## 증상
- run dir에 `runner_logs`만, prompt pack·response **0개**(12분 경과). pid 53708 **dead**. stdout **0바이트**.
- stderr(498B):
```
BEGIN_RUN : 'BEGIN_RUN' ... 인식되지 않습니다 ... CommandNotFoundException
위치 줄:8 문자:16
+  Write-Output (BEGIN_RUN index={0} run_id={1} time={2:o} -f $i, $runI ...
+                ~~~~~~~~~
```

## 원인 (PowerShell quoting)
`Write-Output (BEGIN_RUN index={0} run_id={1} time={2:o} -f $i, $runId, ...)` — **format 문자열이 따옴표 없이** 괄호 안에 있어, PowerShell이 첫 토큰 `BEGIN_RUN`을 **cmdlet/명령으로 파싱**→CommandNotFoundException→스크립트 종료. 모델 단계 도달 못 함(=Gemma/Ollama 호출 0, v2 출력 0).

## 수정 (Codex)
format 문자열을 따옴표로 감싸기:
```powershell
Write-Output ("BEGIN_RUN index={0} run_id={1} time={2:o}" -f $i, $runId, (Get-Date))
```
(또는 interpolation: `Write-Output "BEGIN_RUN index=$i run_id=$runId time=$((Get-Date).ToString('o'))"`). 동일 패턴이 END_RUN 등 다른 로깅 라인에도 있으면 같이. 수정 후 재launch.

## 영향 / 다음
- **v2 코드(c7e3b06)·내 dv2 채점기 무관** — 순수 런처 스크립트 버그. profile v2 검산은 아직 0회(이 run이 첫 시도였음).
- 재launch되면 내가 즉시 레이아웃 파악→B/M/T(+Conductor) dv2 0-3 채점→**claim_altitude two-sided 분포(과조심?)·register/conci(dried?)·10-rep 안정성·Conductor 새주장0+tie-breaker** 검산→점수만 노트. 채점기 준비완료(tournament_dv2_scoring.js, RD만 바꾸면 됨; quartet 레이아웃이면 inline 추출로 적응).
- 참고: 이전 Gemma 토너먼트 run들은 다른 (정상) 런처를 썼고, 이번 v2 held-out만 새 PS 런처라 이 버그가 처음 노출됨.

## 정직/큐
라이브=run dir/stderr 실측(prose/값 없음, 에러로그만). 신규코드 없음(런처는 ad-hoc PS). manuscript-atelier 커밋0. ccc file-specific add. 미해결: 이 run 재launch · df052b0 leak(MISSING_FIGURES.json) 대응. operator 식사중.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출.)
