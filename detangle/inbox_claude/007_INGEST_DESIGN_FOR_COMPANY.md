VERDICT: ok

# 회사PC용 — 새 논문 추가 subagent 추출 설계 (풀 컨텍스트)

운영자가 "논문 추가, subagent 배치로 Sonnet/Opus plan 한도 내 돌리면 이득? Opus는?" 물음. 노트북 Claude가 컨텍스트 통째로 정리 → **`INGEST_NEW_PAPERS_SUBAGENT_DESIGN.md`** (자기완결).

요지:
- 새 논문 *추가* = **subagent 추출 이득**(plan 한도 내 ≈무료·검증 내장·Haiku보다 품질↑). 전수 *재추출*은 API batch가 나음(quota 보호).
- 모델 = **Sonnet 4.6 디폴트, Opus 비권**(measured-vs-cited 동급·완결성은 파이프라인 문제·1.7x). low-confidence 소수만 Opus 에스컬레이션.
- 파이프라인 = PDF→datalab MD→subagent 추출+measured/cited 검증(출생부터 verified, PR#15 적용)→QA→적재(게이트).
- 워크플로 스크립트 스케치 + 재사용 자산 경로(a2_convert_german.py datalab 패턴 / claim-extractor v0 / sidecar v2.1 / 검증 PR#15 / refill_runner) 다 문서에 있음.
- 권고: 5~10편 파일럿 먼저. quota 주의(대량이면 throttle→API batch).

⚠️ 현황 확인: GitHub에 **verification 정책만 푸시됨(PR#15)**, 실행 워크플로/record_verification MCP는 **아직 미구현**. 이 설계가 추출 워크플로의 첫 spec.
