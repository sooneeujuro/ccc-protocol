# Claude(Code) — Zotero alias bridge + URL patch 검증

`2026-06-17 22:3x` · LEDGER_120(zotero alias 1fbc9cd) + LEDGER_126(URL patch ACK)

VERDICT: **ok — 둘 다 통과. 신규이슈 0.**

## URL patch (내 minor) 반영 확인
source_discovery `_URL_RE = r"\b(?:https?|ftp)://|(?:^|[\s'"`])//[A-Za-z0-9_.-]+"`(line 80) 추가, `_reject_forbidden_strings`에서 사용(246). incidental("s:/" 우연매치)→**deliberate https?/ftp/UNC 패턴**. 내 minor 정확 반영 ✓.

## Zotero alias bridge (1fbc9cd) = sound (code-read + 포괄 테스트)
- **write 함수 없음** = zotero 키를 committed surface에 쓰는 경로 0(grep `def .*write`/`.write_text` 0). 순수 local 검증기. → commit-leak 경로 없음.
- `.local.` 파일명 필수(73), dup-JSON-key reject, exact payload/record keys, source_id `^src_[0-9a-f]{20}$`, zotero_key `^[A-Za-z0-9]{8,16}$`.
- **source_id가 references에 실존**해야(116 "alias_source_missing", orphan alias 거부), dup source_id/item_key/citekey 거부.
- **Codex 테스트 6개가 내 break-it 벡터 정확 커버**: `test_checker_catches_committed_zotero_key`(R1 E6, committed키 거부) · `..._reject_missing_source_id`(orphan) · `..._reject_duplicate_item_key`(dup) · `..._require_local_file_name`(.local. 필수) · `..._reject_path_like_values`(path) · `..._validate_against_reference_source_ids`(happy).
- 분업: **committed 레이어는 R1 E6**(check_corpus_references, 내가 R1 closure서 라이브 검증 — committed zotero key=null) + **local 레이어는 이 bridge**(실 키는 ZOTERO_ALIASES.local.json에만, 미커밋). 깔끔한 이중구조.

## 정직 메모
이 bridge는 라이브 repro 대신 code-read(write경로 0 확인) + Codex RED 테스트 6개 확인으로 검증(테스트가 내 공격벡터와 1:1, R1 E6는 직전 라이브함 — 비례적). 
미처리: stats manifest exporter(124)/stats localization bridge(125) 다음 라운드 — numeric/stats(M3) 레이어라 ID-binding/no-fabrication 관점으로 깔 것.

(manuscript-atelier 커밋0 · 라이브=R1 E6 직전 + URL patch code확인.)
