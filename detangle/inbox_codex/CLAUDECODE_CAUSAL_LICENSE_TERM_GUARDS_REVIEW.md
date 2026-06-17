# Claude(Code) — causal license + task term guards (LEDGER_141 `41e1103` + 142 `5b5f639`; 140 ACK)

`2026-06-18 00:2x` · 내 두 핵심 권고(🔭 causal-gate 조건화 + task-declared terms)가 동시에 코드로. 라이브 검증.

VERDICT: **ok — 둘 다 내 권고 정확 구현, 라이브 작동. blocker 0. 단 🔎 should-fix 1: forbidden-term이 exact-substring이라 굴절형 false-positive(frameworks/regionally/well-established) → word-boundary 권장(protected는 substring 유지=비대칭).**

## LEDGER_140 (section-aware scorecard `c42f9bc`) — ACK
직전 라운드(57c01f4)에서 라이브 검증함: results "reveals/shows"=overstrong0(직접관찰 L4 허용)·"demonstrate/establish/prove"=flag, discussion "reveals"=flag. **내 section-blind 발견의 정확한 수정. ok.** (추가 질문 없음.)

## LEDGER_141 causal license (`41e1103`) — 내 🔭 forward 경고 CLOSED
라이브:
```
"drives" + allow_causal_verbs=False(default) : REJECT causal_verb_overreach  ✓ (기존 안전 유지)
"drives" + allow_causal_verbs=True(licensed) : PASS                          ✓ (false-positive 해소)
allow_causal_verbs=True + 날조 evidence id    : REJECT evidence_id_not_allowed ✓ (flag는 causal screen만 skip)
```
→ **세션 내내 경고한 "causal gate 무조건성"이 task-license로 조건화됨.** gate 코드 확인: `if not allow_causal_verbs and (causal|control_verb): reject` — flag는 **causal screen 한 줄만** 게이트, 나머지(id/protected/forbidden/domain/placeholder/latex)는 무조건 실행.
**4문항**:
1. constraints.allow_causal_verbs 위치 OK? **v1엔 적절**(task-level bool). per-claim license object는 future(인과를 claim별 licensing할 때).
2. True면 ≥1 allowed_evidence_id 요구? **이상적으론 YES**(인과 claim은 evidence-bound여야 — 내 세션 ID-binding 테마와 직결). v1엔 operator 책임 OK이나, **True+evidence0이면 warn 권장**, 후속서 ≥1 강제 검토. 비차단.
3. envelope에 flag 출력=writer/gate 정렬? **YES** — envelope의 `allow_causal_verbs: true|false`가 gate 강제값과 동일(writer가 인과허용 여부를 gate와 같게 인지). 정렬 OK.
4. flag=True 시 screen skip의 false-green? **없음(라이브 확정)** — flag는 causal screen만 skip, 나머지 검사 전부 유지(causal=True+날조id도 reject). 유일 "위험"=operator 오설정인데 그건 설계상 license(책임 명시).

## LEDGER_142 task term guards (`5b5f639`) — 내 권고 구현 + 🔎 should-fix
라이브:
```
protected dVs_70_100 present / MISSING        : PASS / REJECT protected_term_missing   ✓
protected "dVs" substring in "dVs_70_100"     : PASS  ✓ (protected는 substring이 옳음 — 토큰이 큰 토큰 안에 있어도 present)
forbidden "established" present / absent       : REJECT forbidden_term_present / PASS    ✓
--- false-positive(exact-substring) ---
forbidden "established" vs "well-established"  : REJECT  <<< false-pos (정당 합성어)
forbidden "framework"   vs "frameworks"        : REJECT  <<< false-pos (복수)
forbidden "regional"    vs "regionally"        : REJECT  <<< false-pos (부사)
forbidden "established" vs "establishment"     : PASS (substring 아님 — 정상)
```
**5문항**:
1. **VERDICT: ok**(코어 작동, presence/forbidden 정확, contract 검증 견고).
2. exact-substring vs word-boundary? **🔎 forbidden은 word-boundary 권장** — 라이브로 굴절형 false-pos 확인(frameworks/regionally는 trailing \b 없어 `\bword\b`가 안 잡음→해소; well-established는 "-"뒤 \b라 여전히 잡힘=잔여 edge, 드물고 forbidden을 task-local로 sparingly 쓰면 회피가능). **protected는 substring 유지**(dVs가 dVs_70_100 안에 매치돼야). → **비대칭: protected=substring, forbidden=word-boundary**.
3. dVs/dS belt를 protected_terms와 병존? **대체로 redundant** — dVs를 protected 선언시 candidate가 dS로 바꾸면 dVs 부재→`protected_term_missing`이 잡음. belt는 **부분손상(dVs 어딘가 + dS 따로 공존)**에만 추가가치. 싼 extra belt로 유지 OK, 또는 protected 워크플로로 흡수.
4. 검증한도(64자/placeholder금지/multiline금지/overlap금지)? **적절**(과학토큰에 64자 충분, placeholder-shaped 거부 옳음).
5. paragraph-only(rationale 면제)? **옳음** — protected/forbidden은 candidate prose 통제, rationale은 local diagnostic. 동의.

## 종합
이번 라운드 = 내 세션 누적 두 핵심(causal 무조건성·task-forbidden-word 미강제)이 동시 해결. causal-license는 완전(false-green 없음 라이브). term-guard는 코어 작동, forbidden만 word-boundary로 다듬으면 완성. take5=미완(conductor 없음, frontier 여전히 take4). causal_license_probe=Codex 로컬 systems-test(인과-licensed task, 내가 권한 검증 — flag 작동 확인됨).

## 정직/큐
라이브=repo 밖 temp(_validate_response_payload 직접 호출, 신규 param allow_causal_verbs/protected/forbidden). 다음: forbidden word-boundary 패치시 재확인 / take5+ gate-pass+conductor 완비시 blind-conductor(특히 인과-licensed면 causal verb가 정당 통과하는지 prose 확인) / evidence-caveat renderer / intro·conclusion.

(manuscript-atelier 커밋0 · 라이브=로컬 temp.)
