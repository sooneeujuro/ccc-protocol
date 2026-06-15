HOME: 실행 결과 — VERDICT=issues_found. 상세 `reports/HOME_PUSH_ATTEMPT_FINDINGS.md`.

✅ P0 LANDMINE 가드 = ma `main` 머지 완료(PR #13 → 82a3925, .gitignore-only). main 보호됨 → Codex 축A gitignore와 ma 부분 정합(중복 적용 불필요, pre-commit hook은 별개로 유효).

🛑 senpai-design(7↔12)·geochem A4/A5(2↔6) **둘 다 diverged+중복** — main/origin이 A6/B8/A5/A4-인접 작업 이미 보유. force/diverged-push 안 함. 유실방지 코드번들 백업 → `F:\corpus_build_history\detangle_home_backups_20260615\`.

⚠️ Codex 확인 요청 2건:
1. audit 방법 결함 — `--not --remotes=origin`이 분기(공유브랜치 origin tip 전진)를 못 잡아 "push 안전"으로 오판. `audit_home_clone.ps1`에 `--left-right` ahead/behind + FF판정 추가 권고. DECISION_TABLE A·B 표 정정 필요.
2. geochem A4/A5 = origin의 77ccb450(escape)/c37fc34b(no-zero-fill)와 같은 파일 3개 겹침. 내 correlation-NaN→null 케이스 + verify 스크립트가 origin 대비 살릴 delta인지 impl-diff 리뷰 부탁(iron rule상 geochem 최소터치라 Codex 적합). 일단 번들 백업됨.

노트북 SSD=F: (문서 `G:\corpus_*`는 회사기준; 노트북 G:는 별개 사진 드라이브).
