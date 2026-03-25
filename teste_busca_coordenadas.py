#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a função de busca de coordenadas
"""

import unicodedata
from coordenadas_municipais_rn import coordenadas_rn

def normalize_location_name(name):
    """Normaliza nome de localidade"""
    name = str(name).lower().strip()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    name = ' '.join(name.split())
    return name

# Criar versão normalizada
coordenadas_rn_normalized = {normalize_location_name(k): v for k, v in coordenadas_rn.items()}

# Testar busca
print("=" * 80)
print("TESTE DE BUSCA DE COORDENADAS")
print("=" * 80)

test_names = [
    'Natal',
    'NATAL',
    'natal',
    'São Gonçalo do Amarante',
    'sao goncalo do amarante',
    'SÃO GONÇALO DO AMARANTE',
    'Arês',
    'ares',
    'GOIANINHA',
    'goianinha ',  # com espaço extra
    'Comarca desconhecida',
    'nova cruz',
    'NOVA CRUZ',
]

print("\n")
for test_name in test_names:
    normalized = normalize_location_name(test_name)
    
    if normalized in coordenadas_rn_normalized:
        coords = coordenadas_rn_normalized[normalized]
        print(f"✅ '{test_name}' → '{normalized}' → {coords}")
    else:
        print(f"❌ '{test_name}' → '{normalized}' → NÃO ENCONTRADO (fallback: -5.8, -35.2)")

print("\n" + "=" * 80)
print("PRIMEIROS 20 NOMES NORMALIZADOS NO DICIONÁRIO:")
print("=" * 80)
for i, (normalized, coords) in enumerate(list(coordenadas_rn_normalized.items())[:20]):
    original_name = [k for k, v in coordenadas_rn.items() if normalize_location_name(k) == normalized][0]
    print(f"{i+1:2d}. '{original_name}' → '{normalized}'")
