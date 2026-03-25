#!/usr/bin/env python
"""Teste rápido do app para verificar se há erros de callback"""

import sys
import subprocess

print("=" * 60)
print("Testando se o app.py inicia sem erros...")
print("=" * 60)

try:
    # Tentar compilar o arquivo
    result = subprocess.run(
        [sys.executable, "-c", "import app; print('[OK] App importado com sucesso')"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Erro ao importar app:")
        print(result.stderr)
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Verificando estrutura de callbacks...")
    print("=" * 60)
    
    # Verificar callbacks
    result = subprocess.run(
        [sys.executable, "-c", """
import app
print(f'[OK] Callbacks registrados: {len(app.app.callback_map)}')
for i, cb in enumerate(app.app.callback_map.items()):
    print(f'  {i+1}. Output(s): {cb[0]}')
"""],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Erro ao verificar callbacks:")
        print(result.stderr)
        sys.exit(1)
    
    print("=" * 60)
    print("[OK] Tudo OK! O app esta pronto para iniciar.")
    print("=" * 60)
    
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)

