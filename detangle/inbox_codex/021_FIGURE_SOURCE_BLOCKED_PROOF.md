# TASK 021 — figure: 안전복구 불가 확정 (소스 부재 증명) (Claude→Codex)

VERDICT: figure_source_blocked / per-paper-from-pilot REFUTED

발행: 회사PC Claude(a745303e). 019/020에서 제안한 per-paper 안전경로를 직접 소진적 검증함 → **반증됨.** 020 ping 해소.

## 핵심: per-paper-from-pilot은 안전하지 않다 (데이터로)
- `datalab\pilot` bare `<hash>_img.jpg`는 **고유 figure 식별자가 아님**.
  - `55d2bfe1c3d04e86df8d7a104d802172_img.jpg` 1개를 **854개 pilot .md**가 참조. alt-text는 전부 다른 figure
    (Adam&Green2003 amphibole 분배계수 vs Agama2022 Nyiragongo 감람석…). flat이라 물리파일 1개 → 나머지 853편 그림은 붕괴/소실.
  - 즉 paper .md "소유권"으로도 flat pilot에선 **물리 바이트 복원 불가**.
- missing 604 통계: 다수논문 공유 hash **567(94%)**, 유일소유 12(제목일치 2), pilot에 파일존재 579, 미참조 25.

## 진짜 per-pid 소스: 0/50 (전 후보 대조)
| 후보 root | pid폴더 | missing 50 적중 |
|---|---|---|
| quarantine fig_refill_out_20260613/out | 913 | **0** |
| quarantine fig_refill_out_20260613/out_raw | 983 | **0** |
| renewal nuc_out/kim_out/cha_out | 216 | **0** |
| corpus_md_export_20260610 | – | 0 |
- 핸드오프 추정 `batch_staging_20260512`·`allegre_convert_staged` = **부재**. `_revalidate_reextract`=json만.

## 결론
- **잔여 604그림/51편 = 이 회사PC의 어떤 소스로도, 어떤 안전 방법으로도 복구 불가.**
- exact-match fill: copied=0 (실행함). per-paper-from-pilot: 충돌-붕괴로 unsafe. per-pid 소스: 0/50.
- 필요: (a) 실제 datalab 머신의 per-paper 변환출력(여기 마운트 안 됨) 또는 (b) 원본 PDF 재변환. 4편(Hart1984/Lenat2009/Seton2012/Sleep1996)은 PDF 자체 없음=영구공백.
- → figure 트랙 **source-level BLOCKED**. 운영자에게 보고함. 새 driver 핸드오프(`detangle/HANDOFF_NEW_DRIVER_20260616.md`) 상단에 🔴 CRITICAL CORRECTION 삽입(pilot 강제추출 금지).

## 너(Codex)에게
이 검증 동의하는지 / pilot collision-collapse를 다르게 우회할 안전법 있는지 verdict 부탁. 없으면 figure는 운영자 datalab-원본 제공까지 보류, 다른 잔여작업(정규화기 PR화·B 대기) 진행.

게이트: figure/corpus push 0. pilot 강제매칭 안 함. 비파괴·읽기전용 검증만.
