#!/usr/bin/env python
"""
Script para testar o dashboard Dash local
"""

import os
import sys

# Adicionar o diretório do projeto ao PATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Implementar o teste antes de lançar
print("=" * 60)
print("TESTE DO DASHBOARD DINÂMICO RN")
print("=" * 60)

import pandas as pd
from utils.dynamic_filters import get_categorical_columns, get_numeric_columns

# Carregar dados
excel_file = 'data/dados_servicos_rn.xlsx'
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
    print(f"\n✓ Arquivo carregado: {excel_file}")
    print(f"  Shape: {df.shape}")
    print(f"  Colunas: {', '.join(df.columns)}")
    
    cat_cols = get_categorical_columns(df)
    num_cols = get_numeric_columns(df)
    
    print(f"\n✓ Colunas Categóricas: {cat_cols}")
    print(f"✓ Colunas Numéricas: {num_cols}")
    
    # Testar filtro dinâmico
    print(f"\n✓ Testando filtros dinâmicos...")
    from utils.dynamic_filters import apply_dynamic_filters
    
    filters = {}
    if 'tipo_servico' in cat_cols:
        filters['tipo_servico'] = 'Proteção Integrada'
    
    filtered = apply_dynamic_filters(df, filters)
    print(f"  - Registros após filtro: {len(filtered)}/{len(df)}")
    
    print("\n✓ Tudo funcionando! Iniciando servidor...")
else:
    print(f"✗ Arquivo não encontrado: {excel_file}")
    sys.exit(1)

# Iniciar app
if __name__ == '__main__':
    from app import app
    
    print("\n" + "=" * 60)
    print("Dashboard disponível em: http://localhost:8050")
    print("Pressione Ctrl+C para parar")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
