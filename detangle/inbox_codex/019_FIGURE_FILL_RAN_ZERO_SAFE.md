# TASK 019 — Figure fill 실행함, 안전매칭 0 (Claude→Codex)

VERDICT: ran / 0_safe_matches / needs_decision

발행: 회사PC Claude(Opus 4.8). operator가 "있는 파일 먼저 당장 백그라운드로 채워라 + 없는 PDF 메모" 명시 승인 → 실행함.

## 실행 내역
- `python G:\corpus_md_export_20260612\scripts\fig_fill_from_datalab.py` (default roots, no --sync-live) 백그라운드 1회.
- additive·idempotent·exact-full-name match. **copied=0, still_missing=604.**
- 로그: `G:\corpus_md_export_20260612\FIGURES_FILL_RUN_20260616.log`.

## 핵심 발견 (왜 0인가 — 중요)
- 잔여 그림 **604개 / 51편**. 그 중 **579개는 datalab\pilot에 물리적으로 존재**.
- 단 datalab\pilot 명명 = `<regionhash>_img.jpg` (**pid 접두 없음**). 번들 요구 = `<pid>__<regionhash>_img.jpg`.
- region-hash tail은 **논문 간 충돌**. 측정: 미충족 604 중 **477개(79%)**가 이미 채워진 **다른 pid와 tail 충돌**.
  - 예: `7b3180e7140f__935eed7aa61f...`(Brenna, 미충족) ↔ 같은 tail이 `068690320b49`,`111f4f64876e`에 이미 채워짐.
  - → datalab의 단일 `935eed7aa61f..._img.jpg`를 Brenna에 넣으면 **틀린 그림 위험**. fill 스크립트가 명시적으로 금지하는 케이스.
- 결론: **exact-match로는 안전 충족 불가.** precision-safe 원칙상 강제 매칭 금지.

## 안전한 충족 경로 (제안, 미실행)
datalab\pilot에 **per-paper `.md` + `.metadata.json`** 존재. 각 논문 자체 메타가 자기 region-hash를 claim하므로:
- 논문 X의 datalab .md가 참조하는 region-hash 이미지 → `pilot/<hash>_img.jpg`를 `articles/<pidX>__<hash>_img.jpg`로 복사.
- 소유권을 **논문 메타로 확정** → tail-충돌 없이 안전. 단 신규 스크립트 = corpus-precision-critical → operator 승인 + 너(Codex) 리뷰 후 진행 권장. 검증(샘플 시각확인 + render audit GATE) 필수.

## 메모
- `G:\corpus_md_export_20260612\FIGURES_MISSING_PDF_MEMO_20260616.md` — 51편 전체 + 4 classic(Hart1984/Lenat2009/Seton2012/Sleep1996, PDF 자체 없음).

## 게이트
figure/corpus push 0. fill은 NAS 번들 articles/에만(git 아님). 강제 region-hash 매칭 안 함. operator에 동일 보고함.
