"""
Script para baixar os limites reais dos municípios do Rio Grande do Norte usando GEOBR
e criar um GeoJSON com os dados para o dashboard.
"""

import geobr
import geopandas as gpd
import pandas as pd
import json
from pathlib import Path


def download_rn_municipios_geobr():
    """
    Baixa os limites reais dos municípios do RN usando a API do GEOBR (IBGE)
    """
    print("⏳ Baixando limites dos municípios do RN do IBGE...")
    
    try:
        # Baixar municípios do RN (código 24 é o código IBGE do RN)
        rn = geobr.read_municipality(code_muni="RN", year=2020)
        
        print(f"✓ {len(rn)} municípios do RN baixados com sucesso!")
        print(f"✓ Colunas disponíveis: {list(rn.columns)}")
        
        return rn
        
    except Exception as e:
        print(f"✗ Erro ao baixar: {str(e)}")
        return None


def merge_dados_com_geometria(geom_df, dados_df):
    """
    Merge entre a geometria dos municípios e os dados do Excel
    """
    
    # Criar mapping entre nomes do Excel e códigos IBGE
    # Isso é necessário porque o Excel tem nomes e o IBGE tem códigos
    
    mapeamento_nomes = {
        'Natal': 2408102,
        'Mossoró': 2407104,
        'Parnamirim': 2409159,
        'São Gonçalo do Amarante': 2411308,
        'Ceará-Mirim': 2403007,
        'Caicó': 2402303,
        'Currais Novos': 2404508,
        'Apodi': 2400505,
        'Açu': 2400303,
        'São Rafael': 2410704,
        'Touros': 2413509,
        'Areia Branca': 2401034,
        'Governador Dix-Sept Rosado': 2405202,
        'Iguatu': 2405809,
        'Patu': 2409209,
        'Pau dos Ferros': 2409308,
        'São Miguel': 2410407,
        'Santa Cruz': 2410506,
        'João Câmara': 2406102,
        'Assú': 2401506,
        'Macaíba': 2407003,
        'Extremoz': 2404904,
        'Goianinha': 2405301,
        'Araranguá': 2400808,
    }
    
    # Agregar dados por comarca (município)
    dados_agg = dados_df.groupby('comarca').agg({
        'qtd': 'sum'
    }).reset_index()
    
    # Mapear nomes para códigos
    dados_agg['code_muni'] = dados_agg['comarca'].map(mapeamento_nomes)
    
    print(f"\n✓ Dados agregados: {len(dados_agg)} municípios com dados")
    
    # Merge com geometria
    geom_df['code_muni'] = geom_df['code_muni'].astype(int)
    dados_agg['code_muni'] = dados_agg['code_muni'].astype(int)
    
    merged = geom_df.merge(dados_agg, on='code_muni', how='left')
    
    # Preencher valores faltantes com 0
    merged['qtd'] = merged['qtd'].fillna(0)
    
    print(f"✓ Merge realizado: {len(merged)} linhas")
    
    return merged


def criar_geojson_com_dados(gdf, output_path='data/rio_grande_norte_real.geojson'):
    """
    Converte o GeoDataFrame para GeoJSON com os dados agregados
    """
    
    # Converter para GeoJSON
    geojson_data = json.loads(gdf.to_json())
    
    # Salvar
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ GeoJSON salvo em: {output_path}")
    print(f"✓ Features: {len(geojson_data['features'])}")
    
    return output_path


def main():
    """
    Workflow principal
    """
    print("=" * 60)
    print("🗺️  Gerando GeoJSON dos Municípios do RN com GEOBR")
    print("=" * 60)
    
    # 1. Baixar geometria do IBGE
    rn_geom = download_rn_municipios_geobr()
    if rn_geom is None:
        print("❌ Erro: Não foi possível baixar os dados do GEOBR")
        return False
    
    # 2. Carregar dados do Excel
    print("\n⏳ Carregando dados do Excel...")
    excel_path = 'data/rio_grande_norte.xlsx'
    try:
        df_dados = pd.read_excel(excel_path)
        print(f"✓ Dados carregados: {len(df_dados)} registros")
    except Exception as e:
        print(f"✗ Erro ao carregar Excel: {str(e)}")
        return False
    
    # 3. Merge dos dados com geometria
    print("\n⏳ Mesclando dados com geometria...")
    rn_merged = merge_dados_com_geometria(rn_geom, df_dados)
    
    # 4. Criar GeoJSON
    print("\n⏳ Criando GeoJSON...")
    geojson_path = criar_geojson_com_dados(rn_merged)
    
    # 5. Info final
    print("\n" + "=" * 60)
    print("✅ GeoJSON criado com sucesso!")
    print("=" * 60)
    print(f"\nEstatísticas:")
    print(f"  • Municípios: {len(rn_merged)}")
    print(f"  • Total de casos: {rn_merged['qtd'].sum():,.0f}")
    print(f"  • Máximo: {rn_merged['qtd'].max():,.0f}")
    print(f"  • Mínimo: {rn_merged['qtd'].min():,.0f}")
    print(f"  • Média: {rn_merged['qtd'].mean():,.1f}")
    print(f"\nArquivo: {geojson_path}")
    
    return True


if __name__ == '__main__':
    main()
