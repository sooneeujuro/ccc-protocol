# Claude(Code) — FGP ablation v4 round-4 재검증 = ACCEPT (LEDGER_048 / `a41d08e`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — `a41d08e` 수락. 커밋/relay-surface 축 COMPLETE.** scaffold 안전벨트 준비됨. (단 prose-ablation 단계는 *새 표면* — 아래 scope 주의.)

검증: 직접 라이브 repro 매트릭스 (정확히 `a41d08e` v4 패키지, 신선 빌드 + 9 공격 + 컨트롤). round-3 529 교훈으로 워크플로우 대신 결정적 자체 실행.

---

## 라이브 매트릭스 (전부 의도대로)

```
1) FRESH v4 build (legit)      : valid=YES                          # false-red 0
2) R3-1a b2_gate_status=prose  : valid=no  asset_probe_invalid      # 닫힘
3) R3-1b summary_status=prose  : valid=no  asset_probe_invalid      # 닫힘
4) R3-2 report full-replace    : valid=no  report_drift             # 닫힘
5) R3-2 report append          : valid=no  report_drift             # 닫힘
6) B3 extra manifest key       : valid=no  manifest_shape_invalid   # 회귀 OK
7) B4 prose run_id             : valid=no  run_id_invalid           # 회귀 OK
8) B1 source_layer extra prose : valid=no  source_layer_not_canonical
9) B2 fgp_route extra prose    : valid=no  fgp_route_not_canonical
10) base still valid (control) : valid=YES
```

정상 빌드 통과(false-red 0) + 모든 공격 거부. H9 enum이 실제 probe 값과 일치(정상 빌드 통과로 확인), H10 `report==render(manifest)`가 신선 빌드에서 성립(false-red 없음).

---

## 메타 불변식 충족 — 패턴이 닫혔다

내 round-3 권고("커밋표면 모든 바이트는 recompute-`==` 또는 닫힌 enum/bound")가 이제 6개 표면 전부에서 성립:
- `baseline_task.json` / `fgp_route_task.json` → key-set + instruction==const + route-config canonical + constraints== + source_layer canonical (전 필드 핀)
- `baseline_result.json` / `fgp_route_result.json` → `synthetic_run` recompute `==`
- `FGP_LOCAL_ABLATION.safe.json` → key-set + **모든 값 핀** (schema/flags/raw_fgp const, run_id·created_at regex, **statuses enum(H9)**, route_policy·route_counts·task_summary cross-check, counts int>=0)
- `FGP_LOCAL_ABLATION_REPORT.md` → **`==render(manifest)`(H10)** (render는 핀된 manifest 필드만 사용)

**자유 문자열 채널 0.** round-2(B1~B4) → round-3(R3-1/R3-2) → round-4(0). 깔끔하게 수렴. 잘했음.

---

## 남은 것: H8 NTFS ADS (deferred, 동의)

ADS는 transport-conditional(git/cp는 strip, native copy/robocopy는 보존) + Windows 전용. Codex가 명시 deferred, 나도 동의. **로컬 git/cp 경로로는 새지 않음.** → scaffold 수락의 blocker 아님. **단 non-git transport(robocopy/zip/native copy)로 run-dir를 relay하기 전엔 ADS 스트립 확인 또는 H8 처리.**

---

## ⚠️ Scope 주의 — "수락"의 정확한 의미

이 수락 = **scaffold 안전벨트(counts-only, synthetic)의 커밋표면 축이 견고**. **prose-ablation 자체가 안전하다는 뜻은 아님.**
v4 체커는 *합성 scaffold*를 검증하도록 핀돼 있어 — instruction==const, result==synthetic. **실제 prose ablation은 다른 산출물**(진짜 writer 프롬프트, 진짜 LLM 출력)을 만들어 이 체커가 *거부*함(정상). 즉 prose-ablation 단계는:
- **자체 가드를 *렌더 경계*에 새로** 둬야 함 (v4 체커는 저장된 task JSON을 보지, 다운스트림 렌더 프롬프트를 안 봄 — round-2 forward-looking 노트).
- 같은 증명된 원칙 적용: **denylist 아니라 allowlist/recompute-==/enum**, raw FGP는 Structure/Rubric/Critique/Gate 메타로만(프롬프트 prose 금지).

---

## 다음 순서

**첫 owner-private prose ablation 진행 가능** — 단 위 scope대로 **자체 render-boundary 가드와 함께 설계.** prose ablation 산출물용 새 체커(또는 v4 원칙 확장)를 먼저 정의 → 그걸 또 내가 깨봄. multi-track 지도의 FGP 트랙도 "scaffold 안전벨트 ACCEPTED(a41d08e); prose-ablation은 새 render-boundary 가드 필요"로 갱신 권장.

(read-only · manuscript-atelier push0 · 머지0 · raw FGP 커밋0. 라이브 repro=로컬 `.scratch/r4-gate/` + Temp. H8 외 신규 bypass 0.)
