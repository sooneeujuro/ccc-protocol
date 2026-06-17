# Claude(Code) — gemma candidate gate break-it (`52a2e3d`, +id/causal tighten `c1a968f`)

`2026-06-17 23:1x` · Take2/3/4 도중 신규 enforcement 표면. LEDGER 미수신이나 커밋 reviewable이라 선제 break-it.

VERDICT: **issues_found — 안전/누수 ok(라이브). 단 hard-gate 2개(causal_verb_overreach, placeholder_corruption)가 candidate gate에서 *부분만* 강제 — 이름값 대비 커버리지 갭 2건(비-안전, efficacy). id-fabrication/fenced/unknown-placeholder 강제는 정상.**

## c1a968f — 내 v2 issues_found 2건 독립 클로즈 확인
Codex가 자기 Take2/3 런에서 (내 리뷰 도착 전) 독립적으로:
- output-contract `"Do not **add** … evidence ids"` → `"Do not **invent** … evidence ids"` (신규 "arrays may contain only exact IDs"와 모순 해소) ✓ — 내 should-fix와 수렴(문구만 다름, 효과 동일).
- causal 명령에 `"unless the task explicitly licenses causality"` 조건절 추가 ✓.
- (정정: `causal_verb_overreach` 게이트는 c75b268 아니라 **c1a968f**에서 추가됨 — 내 직전 "코드3 vs 노트2"는 커밋 conflation. 노트는 c75b268 기준 정확했음.)

## 라이브 break-it (real pack→runner[injected]→gate, repo 밖 temp)
```
S0 clean valid                 : PASS                      (정상)
H1 'drive' (denylist)          : REJECT causal_verb_overreach   ✓
H1 'cause'   (미등재)          : PASS  <-- HOLE (false-negative)
H1 'controls'(미등재)          : PASS  <-- HOLE
H1 'induce'  (미등재)          : PASS  <-- HOLE
H2 ${{EVIDENCE:..}}$ / [{{..}}] : PASS  <-- HOLE (placeholder $-wrap 손상 미탐지)
H2 placeholder 1/3만 (drop)    : PASS  <-- HOLE (preservation 미강제, subset만)
C  fabricated id               : REJECT evidence_id_not_allowed ✓
C  unknown placeholder         : REJECT placeholder_not_allowed ✓
C  fenced ```json              : REJECT response_fenced         ✓
```

## HOLE 1 — causal_verb_overreach = 평문 lexical denylist(불완전+무조건)
`_CAUSAL_VERB_RE`(L43) = `drive|drives|driven|dictate|dictates|govern|governs|prove|proves|proved`뿐.
- **불완전(false-negative)**: 가장 기본 인과동사 **cause/control/induce/force**(+ caused/controls/controlled 등)가 **없음** → "domain factors **cause** the coupling", "structure **controls** the signals"가 통과(라이브 확인). Take1이 잡은 "drive"는 막지만 동급 과인과는 샌다. 게이트 이름값(causal overreach)에 못 미침.
- **무조건(false-positive 가능)**: 명령은 "unless causality licensed"인데 게이트는 무조건 거부 → task가 인과 license하면 정당verb도 hard-fail = **게이트와 contract 불일치**. (현 discussion task는 인과 미license라 우연히 일치.)
- 권장: (a) 인과동사 lexicon 확장(cause(s)/caused/causing, control(s)/controlled, induce(s)/induced, force(s)/forced, drove, proven, governed/dictated/...). (b) task가 causality license하면 게이트 skip(또는 무조건임을 문서화하고 license-task엔 미적용). (c) lexical은 휴리스틱 스크린일 뿐 — verb-ladder 진짜 판정은 conductor/agent. "스크린"으로 framing 권장.

## HOLE 2 — placeholder_corruption 미강제
게이트는 `_PLACEHOLDER_RE.findall(paragraph) ⊆ allowed`만 체크(L232). 
- `${{EVIDENCE:CIR_DOMAIN_MODEL}}$`·`[{{NUMERIC:..}}]`는 **내부 {{..}} 토큰이 allowed라 subset 통과** — `$`/bracket **wrap 손상 미탐지**(라이브). **이게 Take1 Bold의 실제 `[${{EVIDENCE:..}}]$` 손상** — 지금은 Bold가 fenced라 우연히 막혔을 뿐, non-fenced wrap이면 통과. profile은 placeholder_corruption을 hard-gate로 선언하나 candidate gate엔 해당 검사 없음(unknown-name + fenced만 잡음).
- subset이라 **placeholder drop도 통과**(Terse evidence-anchor 탈락 미강제) — profile Terse 규칙과 갭.
- 권장: placeholder 정확형 검사 추가 — `{{..}}` 인접에 `$`/`[`/`]`/`\` 있으면 reject(예: `\$\{\{`/`\}\}\$`/`\[\{\{`/`\}\}\]` 패턴), 또는 known placeholder 제거 후 잔여 `{{`/`}}`/$-adjacent fragment 검출. 필요시 required-placeholder presence(또는 "evidence anchor ≥1")도 강제.

## minor (code-read)
- `_reject_ids_in_paragraph`(L253) substring 매치(word-boundary 아님) — id가 흔한 substring이면 false-positive 가능(현 id는 길어 저위험).
- 게이트가 response 파일을 re-hash해 summary에 넣지만 **run_manifest의 response_sha256과 cross-check 안 함** — runner↔gate 사이 변조 미탐지. runner의 prompt-hash 규율과 일관되게 response-hash 대조 추가 고려(defense-in-depth).

## 안전/누수 = ok (라이브)
- task_sha256 hash 검증(변조 task 거부), prompt/run manifest schema-pin, persona-set 정확, response file명 `/`·`\` 거부, `_reject_repo_path`(repo 안 거부), exact response key-set.
- **CANDIDATE_GATE.safe.json 누수0**(Take4 실파일 확인): counts(char/id)·sha256·persona·file명·enum status만, prose/path 0. local_only/commit_or_relay_safe=False.
- Take4 실런: v2 exact-ID 주입 후 3후보 전부 **allowed id로 배열 채움**(2 evidence+1 claim, 날조0) → v2 id-fix 작동 확인.

## 종합
candidate gate는 self-assert 아닌 실검사(id-allowlist/fenced/unknown-ph/key-set 정상) + 누수0. 단 **causal·placeholder-corruption 두 hard-gate가 부분 강제** — 이름은 8게이트지만 그중 2개는 candidate 레이어에서 우회 가능. local 품질게이트라 conductor가 backstop(안전 영향 없음)이나, profile이 hard-gate로 선언한 만큼 enforcement 보강 권장. Take5+ 전 (특히 인과동사 lexicon + placeholder 정확형) 수정 권함.

## 큐
Take2/3 = Codex conductor/report 완비(frontier=take3), Take4 = 게이트 통과·conductor 미생성(Codex 진행중 추정). 다음: take3 독립 conductor(frontier) 별도 노트 + LEDGER_133 대기.

(manuscript-atelier 커밋0 · 라이브=로컬 temp gate_breakit + Take4 실 manifest.)
