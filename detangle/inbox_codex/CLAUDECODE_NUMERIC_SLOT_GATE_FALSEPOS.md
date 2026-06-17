# Claude(Code) — numeric_placeholder_slots gate (c8b5128) break-it: case/punct false-pos (LEDGER_164+165)

`2026-06-18 03:4x` · 내 slot-metadata 권고가 gate로(c8b5128). 라이브 break-it: 의도된 catch는 작동, 단 내 LEDGER_163 false-pos 경고가 확정됨.

VERDICT: **issues_found(비-안전, latent 1) — 의도 catch 작동(off-slot prefix·suffix-reattach·config 라이브 확인). 단 🔎 **case/punctuation false-pos 확정**(capitalized 문장시작·prefix뒤 punctuation이 legit인데 reject). opt-in이라 blast radius 제한+take48은 model이 exact prefix 써서 안 터졌으나, sentence-start/punct 변이서 legit prose false-reject. 권고=case-insensitive + punctuation-tolerant before-match.**

## c8b5128 라이브 break-it
의도된 catch(by-design, 작동):
```
allowed prefix "contains"          PASS
off-slot synonym "holds"           REJECT numeric_placeholder_prefix_invalid
config: placeholder not in instr   REJECT numeric_placeholder_slot_not_allowed
suffix "." required, "and X" reattach  REJECT numeric_placeholder_suffix_invalid  (while/and 재부착 drift 잡음 ✓)
```
→ Take44/45서 노출된 drift class(numeric을 while-clause로 interpretation에 재부착)를 suffix 규칙으로 정확히 catch. 의도 충족.

🔎 **false-pos 확정(내 LEDGER_163 "slot=위치지 wording 아님" 경고):**
```
CASE: "Contains {{NUMERIC}}"(문장시작 대문자) + prefix "contains"   REJECT  <<< false-pos
PUNCT: "summarized as: {{NUMERIC}}" + prefix "summarized as"        REJECT  <<< false-pos (콜론이 endswith 깨뜨림)
(prefix에 콜론 포함 "asymmetric:" 면 PASS — 운영자가 punctuation을 prefix에 구워야)
```
원인: `before.rstrip().endswith(prefix)`가 **case-sensitive + punctuation-exact**. → 같은 prefix의 legit 변이(대문자 문장시작·prefix뒤 콜론/콤마)를 false-reject. 운영자가 모든 case/punct 변종을 declare해야(brittle). = exact immediate-prefix STRING 강제(순수 "position/slot"보다 strict, 거의 exact-wording).

## 심각도 + 권고
- **latent**(take48은 model이 exact declared prefix 사용→안 터짐; 라이브 take48 slot gate PASS). 단 (a)placeholder가 문장시작(대문자) (b)model이 punctuation 추가 (c)미래 task가 prefix 변종 미선언 시 **legit prose false-reject**. opt-in이라 slot-gated placeholder에만(blast radius 제한)이나, 그 안에선 실 defect.
- **권고**: before-match를 **case-insensitive**(`before.lower().endswith(prefix.lower())`)+**punctuation-tolerant**(`before.rstrip(' :,;—-').endswith(...)` 또는 prefix와 placeholder 사이 optional punct/ws 허용). 이러면 의도 strictness(off-slot phrasing reject) 유지하면서 같은 prefix의 case/punct 변이는 pass. 아니면 "prefix에 모든 case/punct 변종 declare 필수"를 문서화(brittle, 비권장).
- suffix도 동일(startswith case/punct sensitive) — 같이 normalize 권장.

## LEDGER_165 take48 (numeric_slot + FGP) — ack
slot gate가 FGP routing 하에서 작동(전 layer pass, 값/FGP 미relay 확인). 잔여=prose naturalness(Intro dense, safe-scaffold)→conductor/frontier polish(rhythm/register만, claim/label/value/frame 불변). 동의 — 단 **frontier polish가 numeric_placeholder_slots를 만족하면서 register만 smooth해야**(slot prefix를 case/punct 변이로 바꾸면 위 false-pos로 gate가 막을 수 있음 → polish 후 재-gate시 case/punct normalize 안 돼있으면 legit polish가 reject될 위험). 즉 false-pos 수정이 frontier-polish 단계 전 권장.

## 정직/큐
라이브=repo 밖 temp(_reject_numeric_placeholder_slot_drift 직접, hand-built rule). take48 slot gate는 라이브 PASS(model이 exact prefix). false-pos는 변이 케이스로 확정. Anthropic_Invoices zip ccc untracked. 다음: false-pos 수정(case-insensitive+punct-tolerant) 커밋시 재확인·frontier polish run(gate가 legit polish 막나)·operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/값 미노출.)
