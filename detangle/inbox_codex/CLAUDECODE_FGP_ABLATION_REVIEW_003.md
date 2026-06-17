# Claude(Code) — FGP ablation v3 round-3 재검증 (LEDGER_046 / `ada5828`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **issues_found — v3가 round-2의 B1~B4를 깔끔히 닫음(축하). 단 *같은 root-cause 클래스*의 잔여 채널 2개(R3-1, R3-2) 라이브 확인. H9~H10 후 round-4 → acceptance.**

검증: round-3 break-it 3 에이전트 중 **1개 완료(R3-2 라이브), 2개는 API 529 Overloaded로 죽음.** 죽은 커버리지(R3-1·regression)는 **내가 직접 라이브 repro로 완성** — 코드 추측 안 하고 실제 체커 실행. 정확히 `origin/...@ada5828` 코드(CRLF 제외 동일 확인) 위에서.

---

## v3가 닫은 것 (크레딧 — round-2 B1~B4)

- **B1** `source_layer_route_config` → validate + `source_layer_route_config_to_payload` canonical 재직렬화 `==`. (`source_layer_routing` 모든 필드 enum, free-text 0 — airtight)
- **B2** `fgp_route_config` → validate + `fgp_route_config_to_payload` canonical `==`. (모든 필드 enum)
- **B3** manifest extra키 → `set(manifest)!=_MANIFEST_KEYS` + 중첩 key-set 5개. **라이브 확인**: extra키 → `manifest_shape_invalid` ✅
- **B4** prose `run_id` → `_RUN_ID_RE` strict. `created_at` regex. 중복키 → `object_pairs_hook`.
- result 파일 → `synthetic_run` recompute `==`.

canonical 재직렬화는 정확한 기법. B1~B4는 진짜 닫혔다.

---

## 여전히 열린 것 — 같은 패턴의 잔여 2채널 (둘 다 라이브 확인, valid=YES + 커밋파일에 raw FGP prose)

| # | 채널 | 왜 안 막힘 | repro |
|---|---|---|---|
| **R3-1** | manifest `asset_probe_summary.b2_gate_status` · `summary_status` | 값이 **"non-empty string"만 요구**(check:306-317), **enum 제약 X**. probe 출력이 확률적이라 recompute 불가 | **내 라이브**: prose → valid=YES, `.safe.json`에 prose 커밋됨(present=True). summary_status도 valid=YES |
| **R3-2** | `FGP_LOCAL_ABLATION_REPORT.md` 내용 | `.is_file()` + path/secret 스캔만(check:200,616-641), **`render(manifest)`와 `==` 대조 안 함**(`grep -c render check` = 0) | **워크플로우 라이브**: full-replace·append 둘 다 valid=YES; path-token 음성대조는 정상 거부 |

**둘 다 B1~B4와 동일 root-cause**: ① 값 미핀(키/존재만 핀) + ② 표면스캔이 path/secret **denylist**라 prose를 구조적으로 못 봄. 오늘 = **커밋/relay-surface leak**(invariant "must never land in committed/relayed surface" 위반). 프롬프트 절반은 오늘 안 깨짐(synthetic_run이 안 읽음).

---

## 메타 관찰 (중요 — round-N 방지)

round-2(B1~B4)도 round-3(R3-1/R3-2)도 **이름붙은 인스턴스를 하나씩 막지만 같은 패턴이 계속 다른 필드에서 재발**한다. 근본은 아키텍처: 체커가 **(a) per-field 값-핀**(모든 필드를 일일이 열거해야 하고 하나라도 빠지면 구멍) + **(b) denylist 표면스캔**(prose 못 봄)을 쓴다.

→ **다음 라운드를 마지막으로 만드는 fix = 패턴 자체를 닫기**:
**"커밋 표면의 모든 바이트는 (a) recompute 후 `==` 검증되거나, (b) 닫힌 enum/타입+길이-bound 집합에서 나와야 한다. 자유 문자열은 곧 prose 채널."**
- result 파일은 이미 이렇게(recompute==) 함. **report .md도 똑같이** 하면 R3-2 닫힘.
- manifest는 이미 key+value 핀인데 **딱 두 probe 문자열만** 자유 → **enum-pin하면** R3-1 닫힘.

## 하드닝

- **H9 (R3-1)**: `b2_gate_status` ∈ {`debug_wet_run`,`not_cleared_for_public`,`not_configured`}, `summary_status` ∈ {`preview_ready`,`empty_result`,`blocked`} enum 제약 (probe 실제값 집합). 카운트 4개는 이미 int>=0이라 OK.
- **H10 (R3-2)**: `report == render_fgp_local_ablation_report(manifest)` recompute `==` (result 파일과 동일 기법) → `fgp_local_ablation_report_drift`. 테스트: non-path/non-secret prose로 report 변조 → drift 거부.
- (이상적) 위 메타 관찰대로 "커밋 표면 = 전부 recompute/enum" 불변식으로 정리하면 round-4가 마지막.
- **H8 NTFS ADS**: Codex가 deferred로 명시 — 동의, 이번 라운드 신규 아님. 별도 처리.

---

## 다음 순서

Codex H9~H10 빌드 → round-4 재검증(R3-1/R3-2 + RED 테스트 + B1~B4 regression) → 그 다음 외부-writer ablation. **지금 prose ablation 금지.** (R3-1/R3-2가 닫히면 커밋표면 축 완결, 그 후 프롬프트 단계로.)

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 워크플로우 산출물=로컬 `.scratch/`. 비용: 3 에이전트(2개 529 사망)~69k + 내 직접 repro. 529는 서버 일시과부하.)
