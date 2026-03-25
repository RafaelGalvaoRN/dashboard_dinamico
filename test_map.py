"""
Script de teste para debug: Visualizar o mapa choropleth de forma simples
"""

import json
import plotly.graph_objects as go
import pandas as pd

# Carregar geojson
with open('data/rio_grande_norte_real.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

print(f"GeoJSON carregado: {len(geojson_data['features'])} features")

# Pegar primeiro recurso para debug
feat = geojson_data['features'][0]
print(f"Primeira feature: {feat['properties']['name_muni']}")
print(f"Code: {feat['properties']['code_muni']} (type: {type(feat['properties']['code_muni'])})")
print(f"QTD: {feat['properties']['qtd']}")

# Carregar dados
df = pd.read_excel('data/rio_grande_norte.xlsx')
municipios = df.groupby('comarca').agg({'qtd': 'sum'}).reset_index()
print(f"\nMunicípios com dados: {len(municipios)}")
print(municipios.head())

# Criar mapa teste simples
fig = go.Figure(data=go.Choroplethmapbox(
    geojson=geojson_data,
    locations=[int(feat['properties']['code_muni']) for feat in geojson_data['features']],
    z=[feat['properties']['qtd'] for feat in geojson_data['features']],
    featureidkey='properties.code_muni',
    colorscale='RdYlGn',
    marker_line_width=1,
    marker_line_color='#2c3e50',
    hovertemplate='<b>%{customdata}</b><br>QTD: %{z}<extra></extra>',
    customdata=[feat['properties']['name_muni'] for feat in geojson_data['features']],
))

fig.update_layout(
    title='Teste - Mapa RN',
    geo=dict(
        scope='south america',
        center=dict(lat=-5.8, lon=-36.0),
        projection_type='mercator',
        showland=True,
        showocean=True,
    ),
    height=700,
)

fig.write_html('teste_mapa.html')
print("\n✓ Mapa salvo em teste_mapa.html")
print("Abra no navegador para verificar!")
