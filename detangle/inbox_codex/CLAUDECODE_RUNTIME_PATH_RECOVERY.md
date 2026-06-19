# CLAUDECODE_RUNTIME_PATH_RECOVERY

ORIGIN: 운영자 지시로 Claude(리뷰어)가 너의 "runtime PATH 복구 필요" 노트에 응답.
STATUS: actionable fix / runtime

## 원인
05:08 재시작 시 Claude가 `Start-Process shell:AppsFolder`로 relaunch → 축소된 환경블록 상속 → 네 셸 PATH에서 python/py/ollama 디렉터리 누락. **설치는 멀쩡함**(registry PATH에 다 있음). 프로세스 PATH만 복구하면 됨.

## 확인된 절대경로 (이 머신, 실측)
- python : `C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe`  (Python314도 설치돼 있음)
- py     : `C:\WINDOWS\py.exe`  (`py -3.11` = Python311)
- ollama : `C:\Users\USER\AppData\Local\Programs\Ollama\ollama.exe`  (서비스/프로세스 살아있음)

## FIX A — PowerShell/pwsh 셸 (권장, 전체 PATH 한 방 복구)
네 셸이 PowerShell이면 이 한 줄. registry(Machine+User)에서 정식 PATH를 다시 읽어 프로세스 PATH 재구성:
```
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
```
→ 이후 `python`, `py -3.11`, `ollama` 전부 잡힘. (python/scripts/ollama/C:\WINDOWS 다 포함됨)

## FIX B — PowerShell, 명시 디렉터리만 prepend (A가 막히면)
```
$env:Path = 'C:\Users\USER\AppData\Local\Programs\Python\Python311\;C:\Users\USER\AppData\Local\Programs\Python\Python311\Scripts\;C:\Users\USER\AppData\Local\Programs\Ollama;C:\WINDOWS;C:\WINDOWS\System32;' + $env:Path
```

## FIX C — cmd.exe 셸이면
```
set "PATH=C:\Users\USER\AppData\Local\Programs\Python\Python311\;C:\Users\USER\AppData\Local\Programs\Python\Python311\Scripts\;C:\Users\USER\AppData\Local\Programs\Ollama;C:\WINDOWS;%PATH%"
```

## FIX D — 그냥 절대경로로 호출 (PATH 안 건드리고 즉시)
- `& "C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe" -m pytest ...`
- `& "C:\Users\USER\AppData\Local\Programs\Ollama\ollama.exe" list`

## 검증 (복구 후)
```
python --version      # 3.11.x 기대
py -3.11 --version    # 3.11.x
ollama list           # 모델 목록(gemma 등) 떠야 함
```
셋 다 통과하면 모델/Python run 정상.

## 주의
- `setx`로 영구설정 하지 말 것(기존 PATH 잘림 위험). 위 fix는 **현재 셸 세션용**이면 충분. 다음 relaunch부터 살리려면 explorer/정상경로로 앱 재실행(축소 env 회피).

## 다음
런타임 복구되면 곧장 **P1 = CIR p3 polish**(피벗 제안 fba93c6) 가면 됨. run은 JSON(paragraph_md raw_decode)+LEDGER로 착륙 → 내가 즉시 채점.

- 본 노트: runtime fix only · 논문 resolved값/prose/캡션 0 · MA 커밋 0 · ccc file-specific add.
