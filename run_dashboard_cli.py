#!/usr/bin/env python
"""
Script para iniciar o Dashboard Dinâmico - Rio Grande do Norte
Execute: python run_dashboard_cli.py
"""

import os
import sys
import webbrowser
import time

def main():
    print("\n" + "="*70)
    print("🗺️  DASHBOARD DINÂMICO - RIO GRANDE DO NORTE")
    print("="*70)
    print()
    
    # Verificar arquivo de dados
    excel_file = 'data/dados_servicos_rn.xlsx'
    if not os.path.exists(excel_file):
        print("❌ ERRO: Arquivo de dados não encontrado!")
        print(f"   Procurando: {excel_file}")
        print()
        print("Para criar um arquivo de exemplo, execute:")
        print("   python -c \"import utils.dynamic_filters; \\")
        print("   import pandas as pd; ...\"")
        sys.exit(1)
    
    print(f"✓ Arquivo de dados encontrado: {excel_file}")
    
    # Verificar estrutura de dados
    try:
        import pandas as pd
        df = pd.read_excel(excel_file)
        print(f"✓ Dados carregados com sucesso ({len(df)} linhas, {len(df.columns)} colunas)")
        
        from utils.dynamic_filters import get_categorical_columns, get_numeric_columns
        cat_cols = get_categorical_columns(df)
        num_cols = get_numeric_columns(df)
        
        print(f"✓ Colunas categóricas para filtros: {len(cat_cols)}")
        print(f"✓ Métricas numéricas: {num_cols}")
    except Exception as e:
        print(f"❌ Erro ao validar dados: {e}")
        sys.exit(1)
    
    print()
    print("-"*70)
    print("INICIANDO SERVIDOR DASH...")
    print("-"*70)
    print()
    print("📍 Dashboard disponível em: http://localhost:8050")
    print()
    print("   Você será redirecionado automaticamente em alguns segundos...")
    print()
    print("   Pressione Ctrl+C para parar o servidor")
    print()
    print("-"*70)
    print()
    
    # Abrir no navegador após alguns segundos
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:8050')
            print("✓ Navegador aberto")
        except:
            pass
    
    import threading
    thread = threading.Thread(target=open_browser, daemon=True)
    thread.start()
    
    # Executar app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=8050, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n✓ Servidor encerrado")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao executar app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
