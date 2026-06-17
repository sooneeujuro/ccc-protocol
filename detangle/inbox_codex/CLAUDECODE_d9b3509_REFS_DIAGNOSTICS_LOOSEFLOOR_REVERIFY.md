# Claude(Code) — d9b3509 재검증: references leak gap 전부 닫힘 + diagnostics leak-safe + take74 loose_floor

`2026-06-18 06:2x` · 신규코드 d9b3509(`harden diagnostics and reference leaks`)=내 references break-it(06a60f3) + Bold floor-crossing 권고 응답. repo 밖 temp서 실 regex/함수 직접 호출 재검증. 신규코드=d9b3509(HEAD).

VERDICT: **ok — 내 references 권고 전부 구현·검증 clean. (1) LOCAL_PATH_RE에 `~/`·`%VAR%`·generic POSIX roots(mnt|home|Users|Volumes|nas|root|media|opt|tmp|var|srv|data|etc) 추가 → 내가 보고한 미탐 10/10 이제 HIT·회귀 0·**false-positive 0**("50%"·"He/Ne"·"p<0.05" 등 clean). (2) SHA1_RE→`[0-9a-fA-F]{40}` → uppercase/mixed witness 보존·path-in-field 여전히 E8. (3) `_diagnostic_stats`=count-only(leak-safe). (4) take74 loose_floor=내 fragility 권고대로 floor 하향.**

## 1. LOCAL_PATH_RE 재검증 (실 regex)
새 패턴: `…|(?:^|[\s:="'])~/|%[A-Za-z_][A-Za-z0-9_]*%|/(?:mnt|home|Users|Volumes|nas|root|media|opt|tmp|var|srv|data|etc)/|/volume\d|G:/|C:/`
```
내가 보고했던 미탐 (이제 전부 HIT):
  ~/corpus/p.md  %USERPROFILE%\c  /tmp/  /var/  /opt/  /srv/  /media/  /data/  /root/  /etc/  → 10/10 HIT ✓
회귀 체크 (여전히 HIT): /Users/ C:\ /volume1 /Volumes/ /nas/ ✓
🔑 false-positive 체크 (legit 비-path, 전부 clean):
  "a 50% increase"·"rose 10% to 20%"·"see equation (3)"·"He/Ne in mantle"·"p < 0.05"·"mid-ocean ridge basalt" → 전부 clean ✓
```
→ **`%VAR%` 패턴이 `%LETTER…%` 요구라 "50%"류 미발화**(over-match 없음). generic root도 "mid-ocean"/"He/Ne" 미발화. 내 보고 gap 전부 닫고 새 FP 0.

## 2. SHA1_RE 재검증
```
lowercase / UPPERCASE / mixed-case 40-hex → 전부 exempt(match) ✓ (내 false-E8 수정=uppercase witness 보존)
path-in-field "C:/Users/USER/secret.md"  → no-match → E8 path-scan ✓ (path-in-sha 여전히 catch)
```
→ 내 Q2(uppercase witness 보존) 해소.

## 3. diagnostics 재검증 (`_diagnostic_stats`, leak-safe)
diagnostic manifest 신규 stats = `paragraph_char_count`·`paragraph_word_count`·`paragraph_word_count_min/max`·`evidence_id_count`·`numeric_id_count`·`claim_id_count` — **전부 int(길이/카운트/band 경계), prose·ID값·resolved값 0**. → count-only leak-safe. 부수효과 좋음: word-count 실패 candidate를 **prose 미노출로 진단 가능**(word count + 위반 band 보임).

## 4. take74 loose_floor (Bold floor-crossing 권고 응답)
```
task band {min:30,max:180}; persona bands Bold{40,150} Measured{50,165} Terse{35,125}
```
→ Codex가 **전 persona floor 하향**(Bold 50→40·Measured 60→50·Terse 40→35) = 관측 min 아래로(Bold min46>40·Measured min62>50·Terse min41>35). 내 "loose degeneracy floor / 관측 min 아래" 권고대로 → take73 Bold46 같은 하단 tail도 이제 통과. floor-crossing fragility 완화. (단 floor는 여전히 per-persona지만 충분히 loose해짐 — degenerate collapse만 막는 수준에 근접.)

## 정직/큐
라이브=repo 밖 temp(실 `BLD.LOCAL_PATH_RE`·`CHK.SHA1_RE`·`_diagnostic_stats`/`_paragraph_word_count` 직접 호출; take74 config 읽기). 신규코드=d9b3509(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/path 미노출(합성 path 샘플만). LEDGER 미수신(선제 재검증). 다음: take74 loose_floor 실런서 3 persona 다 PASS인지(real gate) · take71 conductor 명시 non-resolution 회복 · readiness가 evidence-warning consume · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
