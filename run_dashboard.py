#!/usr/bin/env python
"""Script para iniciar o dashboard RN com melhorias"""

import os
import sys
import time
import webbrowser

print("\n" + "=" * 70)
print(" " * 15 + "INICIANDO DASHBOARD RN DIN6AMICO")
print("=" * 70 + "\n")

print("[INFO] Verificando ambiente...")
print("  Python:", sys.version.split()[0])
print("  Diretório:", os.getcwd())

print("\n[INFO] Importando módulos...")
try:
    import app
    print("  [OK] App carregado com sucesso")
except Exception as e:
    print(f"  [ERRO] Falha ao carregar app: {e}")
    sys.exit(1)

print("\n[INFO] Estrutura de Callbacks:")
if app.app.callback_map:
    print(f"  Total: {len(app.app.callback_map)}")
    print("  [OK] Callbacks registrados corretamente")
else:
    print("  [AVISO] Nenhum callback no map (pode ser normal)")

print("\n" + "=" * 70)
print(" " * 20 + "INICIANDO SERVIDOR DASH")
print("=" * 70)
print("\n[INFO] Abrindo navegador em 3 segundos...")
print("  URL: http://localhost:8050")
print("\n[INSTRUCOES]")
print("  1. Arraste um arquivo Excel para carregar dados")
print("  2. Use os filtros para explorar os dados")
print("  3. Clique nos botoes azuis para expandir/ocultar analises")
print("  4. Passe o mouse sobre o mapa para ver detalhes")
print("\nPressione Ctrl+C para parar o servidor\n")

# Abrir navegador depois de 3 segundos
time.sleep(3)
try:
    webbrowser.open('http://localhost:8050')
except:
    pass

# Iniciar o app
try:
    app.app.run(debug=True, host='0.0.0.0', port=8050)
except KeyboardInterrupt:
    print("\n\n[INFO] Encerrando servidor...")
    sys.exit(0)
except Exception as e:
    print(f"\n[ERRO] Falha ao iniciar servidor: {e}")
    sys.exit(1)
