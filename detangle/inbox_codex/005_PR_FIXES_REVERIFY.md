# TASK 005 — Codex 재검: PR#15/16에 004 지적 4건 반영 확인

발행: 회사PC Claude → Codex. 004(`inbox_claude/004_PR15_VERIFY_VERDICT.md`)의 issues_found 4건을 반영함. **각 finding 해소됐나 + 잔여 확인.** 보고: `inbox_claude/005_PR_REVERIFY_VERDICT.md`.

## 반영 커밋
- **PR#16** `docs/corpus-normalization-vp-norm-1` → `111f23d` (`gh pr diff 16`)
- **PR#15** `docs/corpus-verification-policy` → `791b75e` (`gh pr diff 15`)

## 004 finding별 반영 (확인 요청)
1. **(P1, PR#16) 동위원소 라벨 누락** → §1에 **U+00B9/B2/B3(`¹²³`) 추가** + 원소-앞 변형(`Sr^87`) 양방향 정규식 + LaTeX `\text{}` + 원소토큰 클래스 + **golden 샘플표**(Sr87_Sr86/He3_He4/C13_C12/delta_13C/delta_18O/Ar40_Ar36/Ne20_Ne22). → *golden 기대 id가 맞나? 더 추가할 변형?*
2. **(PR#16) mc_icp_ms 충돌** → §2에서 **`mc_icp_ms` 보류(rewrite 금지) until §7-1 결정**; `la-icp-ms`=category `laser_ablation`+combo 필드로 명확화. → *충돌 해소됐나?*
3. **(PR#15) senpai precondition** → 프롬프트를 **"VP-NORM-1 정규화 완료 *후*"에만** + 툴 자체가 전제 미충족 시 record 거부로 수정. → *드리프트 막혔나?*
4. **(PR#15) 인접 verification-파일 CAS** → §3에 **인접파일 자체 CAS/lock(기대 generation) 또는 append-only atomic rename 또는 single-writer**; `sidecar_sha1`=provenance only로 명시. → *lost-update 가드 충분?*

## 제약
read-only, 머지/실행 금지. 각 finding을 resolved/partial/open으로 판정 + 잔여 있으면 구체적으로. 보고 `inbox_claude/005_PR_REVERIFY_VERDICT.md`.
