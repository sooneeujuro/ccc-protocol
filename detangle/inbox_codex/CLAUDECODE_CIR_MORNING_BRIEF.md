# Claude(Code) CIR 모닝 브리프 — 두 방향 통합 (운영자 AM용)

`2026-06-17` · Claude tester#1. sanitized. Codex(INIT_009~013)와 교차/수렴. raw 미공개데이터 커밋0.

## TL;DR
**레포가 실제 미공개 자료로 기능적으로 작동한다. 그리고 중요한 건 — 시스템이 가짜 submission-green을 정확히 거부한다(evidence-demand sufficiency=fail).** 두 방향(기능 전수테스트 + 과학 리뷰) 다 커버. 치명 break 없음, 정밀한 seam/gap 몇 개.

## 운영자 질문 직답
- **초고 뽑혔나?** Codex가 v0~v3 + 전체 writing-loop(페르소나3→컨덕터→리뷰→리비전→패치)까지 산출. 레포 파이프(draft-driver prepare/ingest/assemble, writing-runner) 실행됨. → **YES, 돈다.**
- **corpus·논지 추적 안 깨지나?** **거의 안 깨짐**: evidence ID allow-list 강제, audit sidecar 리비전 후 생존, claim이 reader gate BLOCKED. **약한 seam 1개**: 최종 cited 판정이 prose의 `(Surname,Year)` 텍스트매칭이라 writer가 `[E1]` alias 쓰면 cited=0(candidate-only로). → ID기반 sidecar로 굳히면 됨.
- **figure MCP?** ✅ 작동 (He vs 위도, La/Sm vs 위도 2장 — 운영자에 인라인 표시).
- **논지 약해서 안 도나?** 아니. 파이프는 돌고, 시스템이 "약함"을 정확히 red로 잡음(아래).

## 방향 B — 기능 커버리지
✅ 작동: corpus binding checker · discovery checker · D3 fail-closed(REAL RED) · BM25 retrieval(alignment verified) · evidence-demand · draft-driver 파이프 · writing-runner · claim-extractor · backchain · source-support · figure MCP · review-runner.
⚠️ fake-green: (1) md-reader가 0-claim bundle을 READY (→ skeleton_only 상태 필요) (2) writer가 evidence ID 0개 인용해도 reader READY 가능.
🔧 #9 해소: retrieval fail-closed 테스트 fail = 내 smoke파일(CORPUS_SOURCE.local.json) 환경오염(fake-red), 정리함. 진짜결함=테스트가 로컬설정 부재 의존→정상셋업 머신서 fail(픽스=경로 monkeypatch).
🟢 good-red: claim 붙으면 reader BLOCKED(uncited), evidence-demand/backchain fail, source-support는 metadata-only를 human-review 유지.

## 방향 A — 과학 리뷰 (CIR draft, Codex가 내 비평 수용해 강등)
- **C1 dVs N/S 대비** = (a) 경계가 He+dVs GMM 클러스터링서 유도→그 경계로 대비검정 = **double-dipping** (b) **dVs=Barruol2019 MBAR tomography 모델 샘플값(신규측정X)** → **자기인용 trap** → "published 모델 재분석"으로 프레이밍 필수. (c) Moran's I≈0.91 → e-29 p값 앵커 부적합.
- **C3 La/Sm** = 경계부 band peak(깔끔한 step 아님) + dataset(Kim2017/Furi2011)×위도 교락.
- **He** = -18 부근 저값이나 산포커 n작아 취약.
- → evidence-demand가 covered=0/contradictory=1/fail 반환 = **정확**. Codex가 `boundary_derivation_independence` 역할 추가.

## Kim2024와 같은 class
CIR 자기인용(dVs=Barruol 모델) = Kim2024 self-source trap의 재현. **공통 픽스**: external-support 역할에서 target/source 논문 제외(Codex Kim2024 #2와 동일).

## co-op 노트
Codex=광범위 빌드/실행(20+경로, 전체 루프). Claude=독립 교차검증 + double-dipping/provenance/추적-메커니즘 규명. Codex가 내 비평 수용해 draft 강등. **둘 다 같은 fake-green 결론 수렴.**

## 권고 (우선순위)
1. citation 바인딩 ID기반(텍스트매칭 제거) + `[E1]` 정규화.
2. 0-claim → skeleton_only 비-final 상태.
3. external-support 역할 target-source 제외(Kim2024+CIR 공통).
4. retrieval fail-closed 테스트 경로 격리.
5. CIR은 submission 전 dVs provenance·boundary 독립성 해결 필요 — 현 시스템은 그걸 올바르게 막는 중.
