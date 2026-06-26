@echo off
cd /d "C:\Users\USER\Documents\ccc-protocol\detangle\sidecar_test_sonnet"
"C:\Users\USER\AppData\Local\Programs\Python\Python311\python.exe" gemma_production.py 1 >> prod.log 2>> prod.err
