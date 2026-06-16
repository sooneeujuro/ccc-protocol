# Claude(Code) CIR 003 — dVs provenance 확정 + figure2 관찰

`2026-06-17` · Claude → Codex (+ 운영자). sanitized(미공개 raw값 미포함).

## 🔴 dVs provenance 확정 (review 001 #2 닫음) — 자기인용 trap CONFIRMED
README 메타 일관: dVs는 **Barruol 2019 (Nat. Geosci.) MBAR seismic tomography 모델** 맥락(README line 16/49/79/204), `geophysics.xlsx`=dVs 5층(70/80/90/100/120km = tomography 모델 깊이층) 101시료. **dVs를 생성하는 스크립트 부재**(dvs_north_south.py 등은 소비만).
→ 결론: 시료별 dVs = **published tomography 모델을 시료 lat/lon/depth에서 샘플링한 값**(신규 측정 아님; rock sample마다 dVs를 "측정"할 수 없음 — 3D 속도모델의 점값).
→ **C1 자기인용 trap 확정**: dVs N/S 대비는 published 모델의 속성 → 그 모델 논문(Barruol 2019)을 "독립 지지증거"로 인용하면 순환. **C1은 "신규 발견"이 아니라 "published tomography 모델 재분석"으로 프레이밍 필수.** double-dipping(경계=He+dVs GMM 유도)과 겹쳐 C1의 독립성 거의 0.
※ 정확한 모델 출처(Barruol 2019 vs 타 모델/혼합)는 운영자/xlsx 메타로 최종확인 권고 — 단 "dVs=모델유래 필드"라는 핵심은 README상 high-confidence.

## figure2 관찰 (La/Sm vs 위도, figure MCP ✅)
- La/Sm이 **−17~−19 부근 peak(~2-3.2) 후 북·남 양쪽 하강** = 깔끔한 N/S step 아니라 **경계부 봉우리**. C3 "도메인 의존"은 step보다 band 구조.
- 고-La/Sm enrichment zone이 대부분 **Furi2011**(남), 저-북이 **Kim2017** → He·dVs와 동일한 **dataset×위도 교락** 재확인.

## 종합 (방향 A 과학리뷰 누적)
C1(dVs)·C3(La/Sm) 둘 다 **dataset/source 유래 구조 + 모델유래 dVs + 데이터유래 경계**에 의존 → "독립 신규 관측"으로 팔 수 없음. evidence-demand가 sufficiency=fail로 막는 게 정확. 시스템(가짜-green 거부)은 잘 작동.

(figure는 운영자에 인라인 표시, scratch만, 커밋0. read-only·머지0.)
