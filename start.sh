#!/bin/bash

echo "========================================"
echo "Dashboard de Comarcas e Termos"
echo "========================================"
echo ""
echo "Verificando ambiente Python..."
python3 --version

echo ""
echo "Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "Verificando arquivo de dados..."
if [ ! -f "data/exemplo.xlsx" ]; then
    echo "Criando arquivo de exemplo..."
    python3 create_sample_data.py
else
    echo "Arquivo de dados já existe!"
fi

echo ""
echo "========================================"
echo "Iniciando Dashboard em http://localhost:8050"
echo "(Pressione Ctrl+C para parar)"
echo "========================================"
echo ""

python3 app.py
