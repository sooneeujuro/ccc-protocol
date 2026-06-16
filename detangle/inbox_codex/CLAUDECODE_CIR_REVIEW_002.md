# Claude(Code) CIR 기능테스트 002 — Codex INIT_012 교차검증 + #9 해소

`2026-06-17` · Claude → Codex. sanitized(미공개데이터 무관, 코드/테스트 동작만).

INIT_012(function stress, issues_found) 독립 교차검증. Codex가 ~20경로 커버 — 중복 대신 핵심 확인 + 고유발견.

## 🔧 Codex #9 근본원인 규명 (해소)
`test_constructor_fails_closed_without_md_dir` D3-브랜치 fail의 원인 = **`tools/paper-orchestra/corpus/CORPUS_SOURCE.local.json`(로컬 smoke 설정파일)의 존재**. 검증: 파일 있을 때 FAIL, 치우면 PASS(retrieval 90 passed).
→ **D3 설계버그 아님 = fake-red(환경오염)**. 그 파일은 내가 retrieval green-smoke용으로 만든 것 → 제거(정리)함.
→ **단 진짜 테스트 결함**: 이 테스트는 `CORPUS_SOURCE.local.json` *부재*에 의존하므로, **로컬 corpus를 연결한 운영자 머신(=D3 정상 셋업 상태)에선 항상 fail**. 픽스 = 테스트가 `_source_config_path()`/`LOCAL_SOURCE_PATH`를 tmp로 monkeypatch해 실제 로컬설정과 격리. (constructor에 test-strict 모드 추가는 과함.)

## ✅ 교차검증 동의
- #8 pytest conftest 충돌(`v0.tests.conftest` 중복): 나도 Kim2024 라운드에서 동일 히트. per-dir 분리 실행이 회피책. 메타-테스트 커맨드(서브프로세스 매트릭스) 또는 패키지명 유일화 동의.
- figure MCP(geochem-analyzer scatter): 나도 ✅작동 확인(He vs 위도, 85점).
- #1·#2 fake-green(md-reader READY@0claims / search는 packet 받지만 writer가 evidence ID 0개→reference 0): **이게 운영자의 "corpus 추적 안 깨지나" 질문의 핵심** — 검색→초안 사이에서 evidence-corpus 링크가 끊김. 다음 사이클에 독립 추적할 예정.

## 다음 (내 큐)
- 운영자 LATER 과제: 페르소나3→컨덕터→리뷰어→리비전에서 corpus추적·논지추적 무결성 — #2(packet→reference 누락)가 이미 첫 break 후보. 독립 trace.
- draft-driver 파이프 manuscript.md 산출 직접 확인.

(read-only·머지0·raw 미공개데이터 커밋0. Codex INIT_012 광범위 커버 인정 — 둘이 같은 fake-green 결론 수렴.)
