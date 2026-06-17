# Claude(Code) — references path/hash hardening (6f074cc) break-it: 보고된 gap 닫힘 + LOCAL_PATH_RE allowlist 잔여 gap

`2026-06-18 06:0x` · 신규코드 6f074cc(`references: harden path and hash checks`, leak-hardening=내 도메인) repo 밖 temp서 실 `LOCAL_PATH_RE`·`SHA1_RE` 직접 호출 break-it. LEDGER_184 4질문 응답. (de8168e는 docs-only.)

VERDICT: **ok + issues_found(leak gate gap, 비-active) — 보고된 두 nit 닫힘 확인(/home//Users/ HIT, source_md_sha1 path→E8). 단 🔎 LOCAL_PATH_RE는 **curated prefix allowlist라 비망라**: `~/`(tilde-home)·`%USERPROFILE%/%APPDATA%`(Win env)·`/tmp /var /opt /srv /media /data /root /etc` 미탐. + SHA1_RE lowercase-only라 uppercase/mixed 40-hex sha1을 false-E8(git 관례 lowercase라 경미). 운영자 실 storage(drive/NAS/Users/mnt/Volumes)는 다 잡음.**

## 보고된 gap 닫힘 확인 (실 regex)
```
LOCAL_PATH_RE = ([A-Za-z]:\\|[A-Za-z]:/|\\\\|/mnt/|/home/|/Users/|/volume\d|/Volumes/|/nas/|G:/|C:/)
  /Users/operator/corpus/paper.md  -> HIT ✓ (보고된 gap 닫힘)
  /home/user/x.md                  -> HIT ✓ (보고된 gap 닫힘)
SHA1_RE = ^[0-9a-f]{40}$
  source_md_sha1 = "C:/Users/USER/secret.md"  -> SHA1_RE no-match -> E8 path-scan ✓ (path-in-sha 닫힘)
  source_md_sha1 = <valid 40-hex lowercase>   -> exempt ✓ (witness 보존)
```
→ **Q1 답: 예, /home//Users/ 및 sha-field 면제 gap 닫힘.** path-in-sha가 E8로 잡힘 확인.

## 🔎 LOCAL_PATH_RE allowlist 잔여 gap (leak gate=miss는 잠재 누수)
path battery 실행(HIT=잡힘, miss=미탐):
```
HIT : /Users/ /home/ C:\ C:/ /mnt/ /volume1 /Volumes/ G:\ file:///Users/  + 패턴상 /nas/ G:/ C:/
miss: /root/  /media/  /opt/  /tmp/  /var/  /srv/  /data/  /etc/
miss: ~/corpus/p.md         (tilde-home — 흔한 단축표기)
miss: %USERPROFILE%\...      (Win env-var path — 이 Windows box서 현실적)
```
- LOCAL_PATH_RE는 **알려진 prefix allowlist**(운영자 실 storage G:/·NAS·/Users/·C:\·/mnt/·/Volumes/는 다 커버). 단 **망라적 path 탐지기가 아님** → leak gate로선 위 미탐이 잠재 누수.
- 현실성 순: **`~/`(tilde-home)·`%USERPROFILE%/%APPDATA%`(Win env)가 가장 realistic**(corpus 경로를 이 표기로 적을 수). `/tmp//opt//data/` 등은 corpus엔 덜 likely.
- **비-active 평가**: corpus reference는 구조화된 citation(자유 prose 아님)이고 실 누수면(source_md_sha1)은 이제 SHA-gated라, 이 gap이 active 누수는 아님(defense-in-depth 빈틈). + corpus 자체 non-push 규율이 backstop.
- **권고(Q4)**: leak gate면 최소 `~/`(`(?:^|[\s:=\"'])~/`)와 Win env(`%[A-Za-z_]+%`) 추가, 가능하면 generic POSIX-root(`/(?:etc|var|tmp|opt|srv|root|media|data)/`) 추가. 또는 "known-prefix detector(비망라)"로 문서화하고 corpus non-push 규율을 1차 방어로 명시. (UNC `\\`는 패턴에 `\\\\`로 있음 — 커버, 미탐 아님.)

## SHA1_RE case-sensitivity (Q2)
```
lowercase-40 (git 관례)  -> exempt ✓
UPPERCASE-40 / mixed-40  -> no-match -> E8 (false-positive: 유효 sha1인데 path-scan 강제)
39/41 chars, sha256-64   -> E8 (의도상 OK: 40-hex sha1 아님)
```
→ **Q2 답: lowercase witness는 보존되나 uppercase/mixed-case 40-hex sha1은 false-E8.** git SHA는 관례상 lowercase라 경미하나, 대문자 hex도 유효 sha1 표기 → **`^[0-9a-fA-F]{40}$`로 case-insensitive화 권장**(유효 witness 보존). sha256(64-hex)을 향후 쓰면 별도 처리 필요(현 schema는 sha1이라 무관).

## Q3 (Zotero alias local-only/count-only)
이번 diff(6f074cc)는 path/sha hardening만 건드림 — **Zotero alias 검증부는 미변경이라 이번 라운드 별도 재감사 안 함**(정직). alias count-only는 이전 reference 트랙 리뷰서 확인된 바 있고 이 패치가 회귀 안 시킴. 필요시 다음 라운드 별도 확인.

## 정직/큐
라이브=repo 밖 temp(실 `BLD.LOCAL_PATH_RE`·`CHK.SHA1_RE` 직접 호출, path battery+sha edge). UNC `\\`는 패턴에 있어 미탐 아님(테스트 문자열 escaping 모호로 보고 제외). 신규코드=6f074cc(de8168e=docs). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/path 미노출(테스트는 합성 path 샘플). 다음: LOCAL_PATH_RE에 ~//Win-env 추가시 재확인 · SHA1_RE case-insensitive · readiness가 evidence-warning consume(내 직전 forward) · operator review.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
