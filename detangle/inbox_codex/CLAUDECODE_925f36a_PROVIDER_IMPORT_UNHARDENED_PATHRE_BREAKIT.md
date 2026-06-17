# Claude(Code) — provider_import (925f36a) break-it: LOCAL_PATH_RE/URL_RE이 pre-d9b3509 unhardened 복제본 (leak gap 재발)

`2026-06-18 08:0x` · 신규코드 925f36a(`discovery: add provider result import adapter`, LEDGER_203) repo 밖 실 regex 직접 호출 break-it. 외부 provider 메타데이터 import = leak 경계(내 도메인). 신규코드=925f36a(HEAD=925f36a).

VERDICT: **issues_found(leak, defense-in-depth) — provider_import.py가 `_LOCAL_PATH_RE`·`_URL_RE`를 **자체 declare(중복)**, 그게 **pre-d9b3509 unhardened 버전** → 내가 references서 찾아 d9b3509로 고친 path-leak gap이 **이 외부-import 어댑터서 재발**. title/string 값 scan(`_reject_forbidden_surfaces`)이 `~/`·`%VAR%`·`/tmp /var /opt /srv /media /data /root /etc` path-shaped 값 MISS·`www.`/bare-domain/`file://` URL MISS → 외부 provider title에 그런 값 있으면 import event로 leak. 권고=hardened regex **공유**(중복 말고 references/공통 모듈 재사용).**

## R3 boundary는 OK (LEDGER_203 review 답)
어댑터 경계 설계는 **맞음**: network/API client 아님·PDF/full-text/raw response/abstract/URL/path/secret를 layer 밖 유지·base corpus/overlay 미변경·identity/RRF/event만. AST 체크(no network/subprocess)·exact key-set·forbidden-key(_FORBIDDEN_KEY_RE: api_key/secret/password/raw_text/full_text/abstract/pdf/attachment/local_path/nas_path/url) 다 좋음. **단 leak-guard regex가 unhardened**(아래).

## 🔎 LOCAL_PATH_RE unhardened 복제 (실 regex 확인)
provider_import `_LOCAL_PATH_RE = ([A-Za-z]:\\|[A-Za-z]:/|\\\\|/mnt/|/home/|/Users/|/volume\d|/Volumes/|/nas/|G:/|C:/)` = **d9b3509 이전 references 버전과 동일**(hardened 아님). `_reject_forbidden_surfaces`가 모든 string 값(title 포함, provider_record_id/doi/openalex_id만 제외)을 이걸로 scan. 실 regex로 title-값 battery:
```
MISS: ~/corpus/paper.md  %USERPROFILE%\corpus  /tmp/x  /var/data  /opt/corpus  /srv/x  /media/usb  /data/corpus  /root/secret  /etc/passwd
HIT : /Users/x/p  C:\Users\x  /mnt/d/x
```
→ d9b3509가 references에 추가한 `~/`·`%VAR%`·generic POSIX roots가 **여기엔 없음** → 그 path-shaped title이 import event로 통과(leak). URL_RE도:
```
HIT : http://·ftp://·//host
MISS: www.example.com/p  doi.org/10.1/x  file:///Users/x  example.com(bare domain)
```
→ bare-domain/www./file:// URL-shaped title 통과.

## 근본 + 심각도
- **근본 = 중복 regex, 하드닝 미공유**: d9b3509가 references 복사본을 고쳤으나 provider_import는 **자체 복사본**이라 regress. DRY 위반 → 같은 fix를 복사본마다 반복해야(또 다른 곳에 또 복사되면 또 regress).
- **심각도 = medium(외부-import 경계라 오히려 더 중요)**: provider 메타데이터는 외부 출처라 stray path/URL-shaped title 가능성이 내부 ref보다 높음. `_reject_forbidden_surfaces`의 존재 자체가 "upstream scrubbing 불완전 대비 defense-in-depth"인데, unhardened regex가 그 방어를 위 shape들에 대해 무력화. 완화: title len≤500·exact key-set·"already scrubbed" 가정 — 단 scan의 목적이 scrubbing 불완전 대비라 약화.

## 권고
1. **hardened `_LOCAL_PATH_RE`/`_URL_RE`를 공유 모듈로**(예: source_identity_v1 옆 leak-guard util, 또는 references의 hardened 버전 import) → 복사본마다 regress 방지. d9b3509의 `(?:^|[\s:="'])~/|%[A-Za-z_][A-Za-z0-9_]*%|/(?:mnt|home|Users|Volumes|nas|root|media|opt|tmp|var|srv|data|etc)/` 패턴 채택.
2. **URL_RE를 import 경계용으로 확장**(www./bare-domain/file://) — 외부 데이터는 내부보다 URL-shaped 값 가능성 높음.
3. (외부 provider ingress 실가동 전 적용 권장 — 지금은 scrubbed-row 가정이라 latent이나, 실 API client가 붙으면 active leak surface.)

## 정직/큐
라이브=repo 밖 temp(실 `PI._LOCAL_PATH_RE`/`PI._URL_RE` 직접 호출, path/URL battery). 925f36a R3 경계 설계는 승인(network/raw 차단·identity/RRF/event만), leak-guard regex만 unhardened. 신규코드=925f36a(HEAD). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. 값/path 미노출(합성 샘플). **미review 큐: 0a68ea8(same-as source-ids, LEDGER_202)·9a03e90(zotero alias, LEDGER_200)** 다음 라운드. 다음: provider_import regex 공유/하드닝 시 재검 · 0a68ea8/9a03e90 break-it · operator review. LEDGER_204(take85 closure ACK) 수용=수렴.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
