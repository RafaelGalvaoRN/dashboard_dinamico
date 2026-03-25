#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para diagnosticar problemas com coordenadas de municípios
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

# Verificar duplicatas após normalização
print("=" * 80)
print("DIAGNÓSTICO DE COORDENADAS")
print("=" * 80)

normalized_dict = {}
duplicatas = {}

for original_name, coords in coordenadas_rn.items():
    normalized = normalize_location_name(original_name)
    
    if normalized in normalized_dict:
        # Encontrou duplicata
        if normalized not in duplicatas:
            duplicatas[normalized] = []
        duplicatas[normalized].append({
            'original1': normalized_dict[normalized]['original'],
            'coords1': normalized_dict[normalized]['coords'],
            'original2': original_name,
            'coords2': coords
        })
    else:
        normalized_dict[normalized] = {
            'original': original_name,
            'coords': coords
        }

# Relatar duplicatas
if duplicatas:
    print("\n❌ DUPLICATAS ENCONTRADAS (após normalização):\n")
    for normalized, items in duplicatas.items():
        for item in items:
            print(f"  '{item['original1']}' → {item['coords1']}")
            print(f"  '{item['original2']}' → {item['coords2']}")
            print(f"  Normalizado para: '{normalized}'\n")
else:
    print("\n✅ Nenhuma duplicata encontrada\n")

# Verificar coordenadas muito próximas (mesma localidade)
print("=" * 80)
print("VERIFICANDO COORDENADAS DUPLICADAS OU MUY PRÓXIMAS")
print("=" * 80)

coord_dict = {}
for name, coords in coordenadas_rn.items():
    coord_key = (round(coords['lat'], 2), round(coords['lon'], 2))
    
    if coord_key not in coord_dict:
        coord_dict[coord_key] = []
    coord_dict[coord_key].append(name)

duplicados_coords = {k: v for k, v in coord_dict.items() if len(v) > 1}

if duplicados_coords:
    print("\n⚠️  CIDADES COM COORDENADAS IGUAIS OU MUY PRÓXIMAS:\n")
    for coord, cities in sorted(duplicados_coords.items()):
        print(f"  Coordenadas: {coord}")
        for city in cities:
            print(f"    - {city}")
        print()
else:
    print("\n✅ Nenhuma coordenada duplicada encontrada\n")

# Verificar coordenadas inválidas (fora de RN)
print("=" * 80)
print("VERIFICANDO COORDENADAS INVÁLIDAS")
print("=" * 80)

# RN está aproximadamente entre: lat -4.8 a -6.9, lon -35.0 a -38.6
VALID_LAT_MIN, VALID_LAT_MAX = -7.0, -4.5
VALID_LON_MIN, VALID_LON_MAX = -39.0, -34.5

invalidas = []
for name, coords in coordenadas_rn.items():
    lat, lon = coords['lat'], coords['lon']
    if not (VALID_LAT_MIN <= lat <= VALID_LAT_MAX and VALID_LON_MIN <= lon <= VALID_LON_MAX):
        invalidas.append({
            'name': name,
            'coords': coords
        })

if invalidas:
    print(f"\n⚠️  {len(invalidas)} COORDENADAS POTENCIALMENTE INVÁLIDAS:\n")
    for item in invalidas:
        print(f"  {item['name']}: {item['coords']}")
else:
    print("\n✅ Todas as coordenadas estão dentro dos limites de RN\n")

# Total
print("=" * 80)
print(f"TOTAL DE MUNICÍPIOS: {len(coordenadas_rn)}")
print(f"DUPLICATAS: {len(duplicatas)}")
print(f"COORDENADAS DUPLICADAS: {len(duplicados_coords)}")
print(f"COORDENADAS INVÁLIDAS: {len(invalidas)}")
print("=" * 80)
