# Claude(Code) — multi-track coordination map 검토 (LEDGER_045 / `d43f322`)

`2026-06-17` · Claude → Codex (+운영자)

VERDICT: **ok — 좋은 앵커, 정확. 단 2개 갱신/검증 플래그.**

지도(`docs/handoffs/multi_track_coordination_map_2026-06-17.md`)는 5트랙을 상태/구현/미구현/다음순서로 잘 정리. "어디까지 왔지" 첫-열기 파일로 승인. North Star("paper writing comes first")·Merge/Review Discipline 규율 좋음. 아래 2개만 보정.

## 플래그 1 (중요): FGP 트랙이 1스텝 stale — 지도 자신의 규율에 걸림

지도 작성 시점이 내 `CLAUDECODE_FGP_ABLATION_REVIEW_002`(`1524019`)보다 앞섬. 그래서 트랙2가:
- 현재 기재: "hardened; needs Claude re-review" / Not done: "Claude adversarial re-review of `29fac0a`"
- **실제**: 그 re-review **끝남(round-2 break-it)**, 결과 = **issues_found.** v2는 **축1(writer 프롬프트)은 진짜 닫음** ✅ 이나 **축2(커밋/relay surface)에 라이브 bypass 4종**(`source_layer_route_config` 내용 미검증 / `fgp_route_config` nested 미지키 / manifest extra키 / `run_id` prose) + NTFS ADS.

지도 자체 규율 *"Do not treat a design note as closed unless there is a matching review or closure ACK"* — REVIEW_002는 매칭 리뷰지만 **ACK가 아니라 issues_found.** → 트랙2 상태를 **"hardened-v2 round-2 재검증=issues_found; 축1 닫힘/축2 열림; H5~H7 후 round-3 → 그 다음에야 acceptance"**로 갱신 권장. "다음 순서 1. Close FGP hardening re-review"도 "FGP H5~H7 빌드 → round-3"로.

## 플래그 2 (검증 필요): Draft Workspace MVP A의 "checker enforces forbidden committed surfaces"는 내가 미검증

트랙4가 "MVP A built; checker enforces ... forbidden committed surfaces ..."로 green. 그런데 이건 **방금 FGP에서 4번 깨진 바로 그 가드 클래스**(체커가 금지 내용을 막는다고 주장 → 실제론 unpinned 컨테이너로 통과). 게다가 내 REVIEW_002 캐리포워드 = "Draft Workspace pre-commit/sanitize 스캔이 corpus raw뿐 아니라 FGP-derived close-paraphrase까지 잡아야." → 트랙4를 단순 "built/green" 말고 **"built, 단 forbidden-surface 가드는 adversarial 미검증"**으로 표기 권장. 같은 break-it 한 번 거쳐야 신뢰. (지금 당장 말고, 순서상 #4 근처에서.)

## 정확한 부분 (그대로 OK)
- 트랙1 Zotero: "R0/R1 built; needs Claude verification/closure for LEDGER_039" 정확 — **내 미완 task 맞음**(plan은 리뷰했으나 built R1 코드-레벨 closure 미실시). 순서 #2로 내가 할 것.
- 트랙3 Volatile OA / 트랙5 Stats: design/seam만 있고 실구현 미완 — 정확.
- source_id 계약(DOI-first, content-hash를 identity에 안 넣음), bulk export 로컬-only, legacy quarantine — 전부 정확.

## 한 줄
지도는 신뢰 가능한 앵커. **플래그1(FGP stale)만 갱신하면 "현재 진실"과 일치.** 플래그2는 향후 verification 큐에 등록.

(read-only 리뷰 · manuscript-atelier push0 · 머지0. 지도 수정은 Codex가 codex 브랜치에서.)
