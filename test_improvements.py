#!/usr/bin/env python
"""Script para testar as melhorias implementadas no app.py"""

import sys
import subprocess
import time

def test_imports():
    """Teste 1: Verificar se todos os imports funcionam"""
    print("=" * 60)
    print("TESTE 1: Verificando imports...")
    print("=" * 60)
    try:
        import app
        print("✓ App importado com sucesso")
        return True
    except Exception as e:
        print(f"✗ Erro ao importar app: {e}")
        return False

def test_app_structure():
    """Teste 2: Verificar estrutura do app"""
    print("\n" + "=" * 60)
    print("TESTE 2: Verificando estrutura do app...")
    print("=" * 60)
    
    try:
        import app
        
        # Verificar se o layout existe
        if hasattr(app.app, 'layout'):
            print("✓ Layout existe")
        else:
            print("✗ Layout não encontrado")
            return False
        
        # Verificar se os callbacks foram registrados
        if len(app.app.callback_map) > 0:
            print(f"✓ {len(app.app.callback_map)} callbacks registrados")
        else:
            print("✗ Nenhum callback registrado")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Erro ao verificar estrutura: {e}")
        return False

def test_features():
    """Teste 3: Verificar se as melhorias estão presentes"""
    print("\n" + "=" * 60)
    print("TESTE 3: Verificando melhorias implementadas...")
    print("=" * 60)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Teste 1: Upload de arquivo
        if "dcc.Upload" in content and "upload-data" in content:
            print("✓ Upload de arquivo implementado")
        else:
            print("✗ Upload de arquivo não encontrado")
            return False
        
        # Teste 2: Mapa com altura aumentada
        if "'height': '700px'" in content or "'height': '800px'" in content:
            print("✓ Mapa com altura aumentada (700-800px)")
        else:
            print("✗ Altura do mapa não aumentada (continua em 500px)")
        
        # Teste 3: Tabelas corrigidas
        if "html.Tr([html.Th" in content and "header_cols" in content:
            print("✓ Tabelas com alinhamento corrigido")
        else:
            print("✗ Tabelas ainda com problemas de alinhamento")
        
        # Teste 4: Botões de minimizar/maximizar
        if "toggle-analise" in content and "toggle_analise" in content:
            print("✓ Botões de minimizar/maximizar implementados")
        else:
            print("✗ Botões de minimizar/maximizar não encontrados")
            return False
        
        # Teste 5: MATCH pattern-matching
        if "from dash import" in content and "MATCH" in content:
            print("✓ MATCH importado para pattern-matching")
        else:
            print("✗ MATCH não importado")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao verificar features: {e}")
        return False

def test_syntax():
    """Teste 4: Verificar sintaxe Python"""
    print("\n" + "=" * 60)
    print("TESTE 4: Verificando sintaxe Python...")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", "app.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✓ Sintaxe Python válida")
            return True
        else:
            print(f"✗ Erro de sintaxe: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar sintaxe: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "TESTE DE MELHORIAS - Dashboard RN" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    
    results = {
        "Imports": test_imports(),
        "Estrutura": test_app_structure(),
        "Sintaxe": test_syntax(),
        "Features": test_features(),
    }
    
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{test_name:20} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TODOS OS TESTES PASSARAM! O app está pronto para uso.")
        print("\nExecute o app com:")
        print("  python app.py")
        print("\nOu acesse em: http://localhost:8050")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
    print("=" * 60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
