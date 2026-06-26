@echo off
REM Gemma re-run v2: num_ctx 49152/16384 + 청킹(긴 MD 분할머지) + 입력 0624 정본, workers=2 parallel.
REM idempotent: canonical staging에 이미 있는 pid skip; 나머지 처리.
"C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe" "C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\gemma_production.py" 2 > "C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet\prod2.log" 2>&1
