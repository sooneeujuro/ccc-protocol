@echo off
REM Loop until every MD-backed sidecar passed Gemma (variables_reported list). Max 6 passes.
REM gemma_production does NOT stage failures, so each pass auto-retries the unprocessed. parallel workers=2.
set PY="C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe"
set GP="C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\gemma_production.py"
set CK="C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\check_complete.py"
set /a pass=0
:loop
set /a pass+=1
echo ===== PASS %pass% =====
%PY% %GP% 2
%PY% %CK%
if %errorlevel%==0 goto done
if %pass% geq 6 goto maxed
goto loop
:maxed
echo MAX PASSES REACHED - residual has_md remains, see COMPLETE_GATE.json
goto end
:done
echo COMPLETE - all MD-backed sidecars passed Gemma
:end
echo WRAPPER FINISHED pass=%pass%
