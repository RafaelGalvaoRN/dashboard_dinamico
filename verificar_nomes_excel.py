#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitário para verificar quais nomes do arquivo Excel existem no dicionário
"""

import pandas as pd
import unicodedata
from coordenadas_municipais_rn import coordenadas_rn
import os

def normalize_location_name(name):
    """Normaliza nome de localidade"""
    name = str(name).lower().strip()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    name = ' '.join(name.split())
    return name

# Criar versão normalizada
coordenadas_rn_normalized = {normalize_location_name(k): v for k, v in coordenadas_rn.items()}

# Listar todos os arquivos Excel
print("\n" + "=" * 80)
print("VERIFICADOR DE NOMES DE MUNICÍPIOS")
print("=" * 80)

arquivos_Excel = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith(('.xlsx', '.xls')):
            arquivos_Excel.append(os.path.join(root, file))

if not arquivos_Excel:
    print("\n❌ Nenhum arquivo Excel encontrado!")
    print("\nPara usar este verificador, carregue um arquivo Excel no app")
    print("e ele aparecerá aqui.")
else:
    for arquivo in arquivos_Excel:
        print(f"\n{'─' * 80}")
        print(f"📄 Arquivo: {arquivo}")
        print(f"{'─' * 80}\n")
        
        try:
            df = pd.read_excel(arquivo)
            
            # Procurar coluna de localização
            location_columns = [col for col in df.columns if col.lower() in 
                              ['termo', 'municipio', 'município', 'cidade', 'local', 'location', 'comarca']]
            
            if not location_columns:
                print(f"⚠️  Nenhuma coluna de localização encontrada!")
                print(f"   Colunas disponíveis: {list(df.columns)}")
                continue
            
            location_column = location_columns[0]
            print(f"✓ Coluna de localização: '{location_column}'")
            print(f"✓ Total de linhas: {len(df)}\n")
            
            # Verificar cada localidade
            encontrados = []
            nao_encontrados = []
            
            for idx, local in enumerate(df[location_column].unique(), 1):
                local_str = str(local).strip()
                normalized = normalize_location_name(local_str)
                
                if normalized in coordenadas_rn_normalized:
                    coords = coordenadas_rn_normalized[normalized]
                    encontrados.append({
                        'nome_excel': local_str,
                        'normalizado': normalized,
                        'coords': coords
                    })
                else:
                    nao_encontrados.append({
                        'nome_excel': local_str,
                        'normalizado': normalized
                    })
            
            # Relatório
            print(f"{'✅ ENCONTRADOS':.<60} {len(encontrados)}")
            for item in encontrados:
                print(f"  • '{item['nome_excel']}' → {item['coords']}")
            
            if nao_encontrados:
                print(f"\n{'❌ NÃO ENCONTRADOS':.<60} {len(nao_encontrados)}")
                print(f"\n⚠️  Estes nomes estão sendo mapeados para coordenadas PADRÃO (-5.8, -35.2):\n")
                for item in nao_encontrados:
                    print(f"  • '{item['nome_excel']}'")
                    # Sugerir nomes similares
                    print(f"    Normalizou para: '{item['normalizado']}'")
                    
                    # Procurar similares
                    similares = []
                    for dict_name in coordenadas_rn_normalized.keys():
                        if item['normalizado'][:3] in dict_name or dict_name[:3] in item['normalizado']:
                            similares.append(dict_name)
                    
                    if similares[:3]:
                        print(f"    Talvez você quis dizer? {similares[:3]}")
                    print()
            
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")

print("\n" + "=" * 80)
print("DICA: Certifique-se de que os nomes no Excel correspondem exatamente")
print("aos nomes do dicionário (sem acentos ou maiúsculas importa)")
print("=" * 80 + "\n")
