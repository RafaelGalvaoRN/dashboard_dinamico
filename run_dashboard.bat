@echo off
REM Script para iniciar o Dashboard Dinâmico - Rio Grande do Norte
REM Windows batch file

title Dashboard Dinamico RN
color 0A

echo ========================================
echo Dashboard Dinamico - RN
echo ========================================
echo.

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Executar o app
echo Iniciando servidor...
echo.
echo Abra seu navegador em: http://localhost:8050
echo.
python app.py

pause
