# Claude(Code) — N=10 hard-task dv2 채점 + N5↔N10 2-run 재현성 VERDICT (LEDGER_234)

`2026-06-18 20:0x` · 081018Z(N=10·round1·M1~M4·dv2, 90/90 pass) dv2 0-3 채점(2×45 배치, judge1+judge2; 1차 full-90은 Claude API 서버 rate-limit으로 실패→백오프 후 배치 성공) → REVEAL → 064019Z(N5)와 winner 2-run 재현성 비교. 점수/카운트만(resolved 값/prose 0).

VERDICT: **변별 magnitude는 재현됨(하드닝 진짜 작동), 단 per-persona winner는 Terse만 재현. Bold·Measured top은 noise-tied. = "재현 가능한 선택"은 부분적: Terse=T2 확정 / 신뢰 가능한 탈락(M1·B1·T3) / B2≈B3·M2≈M3 동률.**

## A. 채점 신뢰성
N=10 90/90 채점(rate-limit 회복 후 2×45 배치). judge1/2 exact 441/540(82%)·mean|diff|0.18(N5는 87%). 신뢰 가능. (rate-limit은 transient 서버측, 데이터 무손실.)

## B. 🎯 2-run 재현성 (N5 064019Z ↔ N10 081018Z)
**claim+caveat cand (핵심축):**
```
[Bold]     N5: B3(1.96)>B1(1.65)>B2(0.94)   N10: B2(1.58)>B3(1.52)>B1(0.67)   winner B3→B2 ❌·B1 폭락
[Measured] N5: M3(1.92)>M2(1.73)>M1(1.23)   N10: M2(1.81)>M3(1.66)>M1(1.45)   winner M3→M2 ❌(top2 swap)
[Terse]    N5: T2(1.47)>T1(1.13)>T3(1.08)   N10: T2(1.69)>T1(1.21)>T3(1.16)   winner T2→T2 ✅
```
**full-6 rank-order:** Bold [B3,B1,B2]→[B2,B3,B1] **reshuffle** · Measured [M3,M2,M1]→[M3,M2,M1] **SAME** · Terse [T2,T1,T3]→[T2,T1,T3] **SAME**.
**변별 magnitude(normalized stdev /scale):** key N5 0.118 ≈ N10 0.111 · full N5 0.065 ≈ N10 0.053 → **두 run 일관**(easy 0.035~0.094 압도). = 하드닝이 만든 분리 수준은 재현됨.

## C. 재현되는 결론 (신뢰 가능) vs 안 되는 것
- ✅ **Terse = T2_frame_bound 확정**: 양 run·full-6·key 전부 1등, rank T2>T1>T3 동일. **T3_minimal_clause 양 run 최하**(easy R1까지 합치면 3-run 최하=robust 탈락).
- ✅ **신뢰 탈락**: **M1_claim_then_caveat**(Measured 양 run 최하), **B1_licensed_max**(N5 2등→N10 **폭락 0.67·최하**; bait 물림 2+overclaim 1의 주범=licensed-max가 M1 미끼에 high-variance로 과욕→crash. "강한 claim"이 가끔 과장으로 넘어감=operator 우려 실측), **T3**(최하).
- ❌ **동률(N10서도 분리 안 됨)**: **Bold B2≈B3**(winner flip, 둘 다 안전·근소차), **Measured M2≈M3**(key-axis top swap, full-6 rank은 M3>M2지만 근소). N=10로도 이 쌍들은 noise 내.

## D. 함의 (operator 핵심목표 "운빨 아닌 반복가능 지시")
- **하드닝 성공**: easy 라운드는 변별 자체가 노이즈였는데(R1↔R2 전 winner flip), 하드닝+0-3은 **변별 magnitude가 재현**되고 **일부 명확한 신호**(T2 winner·M1/B1/T3 탈락)가 나옴. "좋은 장비"가 부분적으로 선택을 가능케 함.
- **단 "persona별 단일 winner" 목표는 Terse만 달성**. Bold/Measured는 N=10로도 top이 noise-tied → 단일 winner 강제는 또 운빨. 정직한 처방:
  - **Terse → T2_frame_bound** 채택.
  - **Measured → M2 또는 M3**(둘 다 좋음, M1 제외). 취향/유지보수로 택1.
  - **Bold → B2_caveat_survivor 또는 B3_test_framed**(둘 다 안전, 근소), **B1_licensed_max 제외**(bait-prone·high-variance=과장 위험).
- 즉 **선택 = "확정 1(T2) + 신뢰 탈락 3(M1·B1·T3) + 동률쌍 2(B2/B3·M2/M3)"**. easy의 "전부 동등"보다 훨씬 나아간 실질 결과.
- 추가 분리 원하면: B2vs B3 / M2 vs M3만 **held-out 다른 task**로 좁혀 재대결(전체 N 더 키우기보다 효율적). 단 ROI 낮음(둘 다 안전하니 취향 채택이 합리적).

## E. 정직/큐
라이브=N10 90 2-judge 채점(2×45 배치, repo 밖 local read·variant blind) + N5↔N10 재현성 + objective. rate-limit 실패는 STATUS에 사유기록 후 백오프-배치로 복구(우회 아님). resolved 값/prose 0 노출·0 커밋. 채점완료 후 REVEAL. manuscript-atelier 커밋0. ccc file-specific add. 미해결: df052b0 leak(MISSING_FIGURES.json) Codex 대응 대기. 다음: operator가 "T2 확정+탈락+동률쌍 취향채택" 수용할지 / B2vsB3·M2vsM3 held-out 갈지 결정.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · resolved 값/prose/캡션 미노출·미커밋·count/점수만.)
