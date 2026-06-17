# Claude(Code) — stats manifest exporter + localizer break-it (LEDGER_124/125)

`2026-06-17 22:4x` · 124(d96e628 committed skeleton) + 125(c47cf62 local localizer)

VERDICT: **ok — M3 stats-ownership 아키텍처 sound. committed-symbolic / local-real 분리 견고.**

## 124 stats manifest exporter (committed skeleton) = symbolic-only
- 출력 = schema + tables(table_ref, **file_ref=`_file_ref_for_table_ref`=`"local_file:"+...` symbolic**, format, role enum, **columns={} 빈값**) + analyses(stats_run:* refs). **실경로/numeric value/prose 0**(코드+docstring 확인).
- ref 형식 강제: stats_run:* (regex), column:* (regex). draft_context_check 선결(fail-closed). count-only status.
- Codex 테스트: `test_stats_handoff_exports_analysis_manifest_skeleton` / `..._rejects_missing_kind_specific_column` / `..._cli_writes_count_only_status` / `..._requires_stats_backed_request`.
- **M3**: stats 결과가 *값*이 아니라 *stats_run:* ref*로 투영 = writer가 숫자 날조 불가, stats ledger 경유. ✓

## 125 localizer (local-only) = 실경로 격리
- symbolic local_file:* → 실 local 경로 매핑 + 별도 file_registry 생성, **출력은 .local.json(gitignore)**. docstring "outputs local-only, CLI paths must use .local.json, status count-only never echoes paths".
- .gitignore 추가 확인: `stats-ledger/v0/*.local.json` + `drafts/**/stats*.local.json` → 실경로 든 manifest/registry 미커밋.

## 종합
**corpus-binding 패턴(committed=symbolic/identity, local=real)이 stats에 적용** — committed skeleton은 symbolic refs만(누수0), 실경로/값은 local-only(gitignore). M3 stats-ownership(숫자/경로를 writer가 못 보고/못 날조, ref→local resolution→stats ledger) 구조적으로 sound. code-read(symbolic by construction) + 포괄 테스트로 검증(비례).

## 정직/큐
미처리: LEDGER_127(quartet profile v1=prose 튜닝 집대성) + 128(gemma prompt pack) design-review 다음 라운드. 125 localizer는 실행 repro 대신 code-read+gitignore확인(local-only 격리가 .gitignore+docstring로 명확).

(manuscript-atelier 커밋0 · 라이브=code-read+test.)
