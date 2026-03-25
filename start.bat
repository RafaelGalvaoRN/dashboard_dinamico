@echo off
REM Script para iniciar o dashboard

echo ========================================
echo Dashboard de Comarcas e Termos
echo ========================================
echo.
echo Verificando ambiente Python...
python --version

echo.
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Verificando arquivo de dados...
if not exist "data\exemplo.xlsx" (
    echo Criando arquivo de exemplo...
    python create_sample_data.py
) else (
    echo Arquivo de dados ja existe!
)

echo.
echo ========================================
echo Iniciando Dashboard em http://localhost:8050
echo (Pressione Ctrl+C para parar)
echo ========================================
echo.

python app.py

pause
