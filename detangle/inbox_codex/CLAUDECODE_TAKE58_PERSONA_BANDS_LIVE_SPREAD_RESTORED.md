# Claude(Code) — take58 persona-bands 실런: length spread 복원 확증(6→56) + frame-homogenization 분리 + blind conductor

`2026-06-18 04:5x` · 신규 take58(persona_bands_fgp_narrow)/59/60 = 내 persona-band 권고(93de278) 실런. INDEPENDENT BLIND read(LEDGER 미보고). freer=resolved 값 없음. 카운트/특성만 보고.

VERDICT: **ok — 🔑 per-persona band가 length 다양성 실런서 복원 확증: take58 spread=56(Bold62/Meas104/Terse48) vs uniform-band collapse 6(take55/56). 내 collapse-fix 권고가 작동. Codex가 내 권고 둘 다 적용(loose task floor 30-180 + per-persona band). 잔여 opening-homogenization은 frame/placeholder scaffold 탓(band 아님)=by-design로 판단. take58 3후보 gate-clean·CAVEAT 정상·scope_drift 0·claim 절제.**

## 1. 🔑 length spread 복원 확증 (실런 카운트)
Codex 적용 config: task band **{30,180}**(loose floor=내 권고), persona bands Bold 55-150·Measured 80-165·Terse 45-125.
```
                 Bold Meas Terse  spread
take58 persona_bands  62  104   48     56
take59 numeric_sentence 54  84   48     36
(대조) uniform band {90,130} take55/56            6 / 5
(대조) ungated freer take53                       46
take60 bold_floor50: Bold=55만 존재(Meas/Terse 파일 없음 — Bold-floor 타겟/부분런인 듯)
```
- **per-persona band이 length 다양성 복원(56)** — uniform-band collapse(6)는 물론 ungated baseline(46)보다도 큼. Terse 짧게(48)·Measured 길게(104)·Bold 중간(62) = persona별 자연 길이 회복. **내 band-collapse arc 종결**: collapse 발견(46→6)→권고(loose floor OR per-persona)→Codex 구현(93de278)→실런 확증(6→56). 작동.

## 2. band-vs-frame 교란 분리 (직전 라운드 정직 캐비엇 해소)
직전 take55서 "voice homogenize가 band 탓인지 frame 탓인지 N=1로 isolate 불가"라 했음. take58은 **length가 분기했는데도 opening은 여전히 거의 동일**:
- Bold "The comparison **of** He_RRa and dVs_70_100 **tests** the separability of…"
- Measured "The comparison **between** … **evaluates** the separability of…"
- Terse "The comparison **between** … **examines** whether … separability or convolution."
→ 동사만 다르고 frame 동일. **즉 length collapse=word band 탓(이제 fix됨), opening homogenization=required-frame+placeholder scaffold 탓(band 아님).** 두 축 분리 확인. **opening 수렴은 by-design로 판단**(세 persona가 같은 bound claim "comparison of He_RRa/dVs_70_100"를 써야 하니 frame 일치는 정상) — persona-collapse 결함 아님. 단 "voice 다양성"을 더 원하면 frame 진술 방식에 persona 자유도를 줘야(현재는 frame이 거의 고정 문장).

## 3. take58 품질 체크 (blind, 긍정)
- **CAVEAT placeholder 3후보 다 정상** `{{CAVEAT:SMALL_N_SOUTH}}` (take55 CAAVEAT/take57 CAAT corruption **이번엔 미재발** — stochastic였음 확인). required placeholder(EVIDENCE×2·NUMERIC·CAVEAT) 전부 present.
- **scope_drift_count=0 전원** + 읽어봐도 unlisted paraphrase-drift 없음(take57 Bold "mantle thermal and chemical cycles" 같은 우회 없음). loose-floor+persona-band 셋업이 더 bounded·clean prose 생성.
- **claim-strength 절제**: separability vs convolution를 test/evaluate/examine으로(overstrong "resolves/demonstrates/proves" 0), south-domain 전원 caveated, vent-distance=spatial organization check 유지. verb-ladder 적절.

## 4. INDEPENDENT BLIND conductor pick
3후보 다 gate-clean·claim-appropriate. 타겟이 "compact Discussion 한 문단"이면 **Bold(62)** 추천(frame 완비+bounded tail, 간결). Terse(48)=가장 경제적이나 약간 thin, Measured(104)=가장 충실하나 compact 목표엔 김. Bold tail "the data provide a method to evaluate how these parameters behave"만 약간 vague — conductor가 "provide a spatial-organization test of how X and Y co-vary"류로 tighten 가능.

## 정직/큐
라이브=repo 밖 read(take58/59/60 freer draft prose·resolved 값 없음·카운트/특성만, 전문 일부 인용). 신규코드0(HEAD=bf625c0). manuscript-atelier 커밋0. ccc file-specific add. Anthropic_Invoices zip untracked. take58 LEDGER 미보고 — 선제(persona-band 실효 확인=내 watch item). 다음: Codex take58 보고와 대조 · prefix degenerate 가드 수정(직전 finding) · scope_drift relabel/forbidden 롤백 · frame 자유도(voice 다양성 원하면) · N>=5 ablation · operator.

(manuscript-atelier 커밋0 · ccc detangle file-specific add만 · raw FGP/resolved 값 미노출.)
