import dash
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
from utils.data_loader import filter_not_nan, load_excel, get_unique_values, filter_data
from utils.dynamic_filters import get_categorical_columns, get_numeric_columns, apply_dynamic_filters, create_aggregated_data
import os
import unicodedata
from coordenadas_municipais_rn import coordenadas_rn

# Iniciando o app Dash
app = dash.Dash(__name__)

# Definir caminho do arquivo Excel
EXCEL_FILE_PATH = 'data/dados_servicos_rn.xlsx'

# Carregando os dados iniciais
if os.path.exists(EXCEL_FILE_PATH):
    try:
        df = load_excel(EXCEL_FILE_PATH)
        df = filter_not_nan(df, 'municipio')
    except Exception as e:
        print(f"Erro ao carregar {EXCEL_FILE_PATH}: {e}")
        excel_path = 'data/rio_grande_norte.xlsx'
        if os.path.exists(excel_path):
            df = load_excel(excel_path)
            df = filter_not_nan(df, 'municipio')
        else:
            df = pd.DataFrame({
                'municipio': ['Natal', 'Parnamirim'],
                'tipo_servico': ['Proteção Integrada', 'Acolhimento'],
                'quantidade_beneficiarios': [100, 50]
            })
else:
    excel_path = 'data/rio_grande_norte.xlsx'
    if os.path.exists(excel_path):
        df = load_excel(excel_path)
        df = filter_not_nan(df, 'municipio')
        if 'termo' in df.columns:
            df.rename(columns={'termo': 'municipio'}, inplace=True)
    else:
        df = pd.DataFrame({
            'municipio': ['Natal', 'Parnamirim'],
            'tipo_servico': ['Proteção Integrada', 'Acolhimento'],
            'quantidade_beneficiarios': [100, 50]
        })

# Carregando o GeoJSON dos municípios do RN
geojson_path = 'data/rio_grande_norte_real.geojson'
if os.path.exists(geojson_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        municipios_geojson = json.load(f)
else:
    municipios_geojson = None


def normalize_location_name(name):
    name = str(name).lower().strip()
    name = unicodedata.normalize('NFKD', name)
    name = ''.join([c for c in name if not unicodedata.combining(c)])
    name = ' '.join(name.split())
    return name

coordenadas_rn_normalized = {normalize_location_name(k): v for k, v in coordenadas_rn.items()}

def get_coordinates_from_geojson(municipio_name):
    normalized_name = normalize_location_name(municipio_name)
    if normalized_name in coordenadas_rn_normalized:
        return coordenadas_rn_normalized[normalized_name]
    if municipios_geojson is None:
        return None
    for feature in municipios_geojson.get('features', []):
        feature_name = feature['properties'].get('name', '')
        if normalize_location_name(feature_name) == normalized_name:
            geom = feature['geometry']
            if geom['type'] == 'Polygon':
                coords = geom['coordinates'][0]
                lons = [c[0] for c in coords]
                lats = [c[1] for c in coords]
                return {'lat': sum(lats)/len(lats), 'lon': sum(lons)/len(lons)}
    return None

location_columns = [col for col in df.columns if col.lower() in ['termo', 'municipio', 'município', 'cidade', 'local', 'location']]
location_column = location_columns[0] if location_columns else (df.columns[0] if len(df.columns) > 0 else 'municipio')

if location_column in df.columns:
    coords_list = []
    for local in df[location_column]:
        coord = get_coordinates_from_geojson(str(local)) or coordenadas_rn.get(str(local), {'lat': -5.8, 'lon': -35.2})
        coords_list.append(coord)
    df['lat'] = [c['lat'] for c in coords_list]
    df['lon'] = [c['lon'] for c in coords_list]
else:
    df['lat'] = -5.8
    df['lon'] = -35.2

categorical_columns = get_categorical_columns(df)
numeric_columns = get_numeric_columns(df)

print(f"DataFrames Shape: {df.shape}")
print(f"Categorical columns: {categorical_columns}")
print(f"Numeric columns: {numeric_columns}")


def create_dynamic_filters():
    current_categorical_columns = get_categorical_columns(df)
    filters = []
    for col in current_categorical_columns:
        if col.lower() in ['termo', 'município', 'municipio', 'cidade', 'local', 'location']:
            continue
        unique_values = get_unique_values(df, col)
        filter_div = html.Div([
            html.Label(f'Filtrar por {col}:', style={'fontWeight': 'bold', 'marginBottom': '8px', 'display': 'block'}),
            dcc.Dropdown(
                id={'type': 'dynamic-filter', 'index': col},
                options=[{'label': 'Todos', 'value': 'all'}] +
                        [{'label': str(val), 'value': str(val)} for val in unique_values],
                value='all',
                clearable=False,
                multi=False,
                style={'width': '100%'}
            )
        ], style={'width': '23%', 'display': 'inline-block', 'marginRight': '2%', 'marginBottom': '15px', 'verticalAlign': 'top'})
        filters.append(filter_div)
    return filters


def get_map_column_options():
    """Retorna opções de colunas disponíveis para o mapa (exclui lat/lon/localização)"""
    excluded = {'lat', 'lon', location_column.lower(), 'termo', 'municipio', 'município', 'cidade', 'local', 'location'}
    cols = [col for col in df.columns if col.lower() not in excluded and col not in ['lat', 'lon']]
    return [{'label': col, 'value': col} for col in cols]


# Layout do app
app.layout = html.Div([
    dcc.Store(id='filtered-data-store'),
    dcc.Store(id='file-upload-store'),
    dcc.Interval(id='upload-message-clear-interval', interval=5000, n_intervals=0),

    html.Div([
        html.Img(
            src='/assets/logo-mprn.png',
            style={
                'display': 'block',
                'margin': '0 auto 15px auto',
                'height': '200px',
                'width': '200px',
            }
        ),
        html.H1('🗺️ Dashboard Dinâmico- Rio Grande do Norte',
                style={'textAlign': 'center', 'marginBottom': '10px', 'color': '#1a5490'}),
        html.P('Análise dinâmica de dados da infância com filtros automáticos',
               style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#666', 'fontSize': '14px'}),

        # Upload de arquivo
        html.Div([
            html.Div([
                html.H3('📁 Carregar Dados', style={'marginBottom': '15px', 'color': '#1a5490'}),
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Arraste um arquivo Excel aqui ou ',
                        html.A('clique para selecionar')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '2px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px 0',
                        'backgroundColor': '#e3f2fd',
                        'cursor': 'pointer',
                        'color': '#1a5490',
                        'fontWeight': 'bold'
                    },
                    multiple=False,
                    accept='.xlsx,.xls'
                ),
                html.P('(Default: dados_servicos_rn.xlsx se nenhum arquivo for enviado)',
                       style={'fontSize': '12px', 'color': '#666', 'marginTop': '5px'}),
                html.Div(id='upload-message-div', style={'marginTop': '10px'})
            ], style={'padding': '20px', 'backgroundColor': '#f0f7ff', 'borderRadius': '8px', 'marginBottom': '20px'})
        ]),

        # Filtros dinâmicos
        html.Div([
            html.Div([
                html.H3('Filtros', style={'marginBottom': '20px', 'color': '#1a5490'}),
                html.Div(id='filtros-dinamicos-div', children=create_dynamic_filters(),
                         style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '10px'})
            ], style={'padding': '20px', 'backgroundColor': '#f0f7ff', 'borderRadius': '8px', 'marginBottom': '20px'})
        ]),

        # Mapa
        html.Div([
            html.H2('📍 Mapa de Distribuição', style={'marginBottom': '15px', 'color': '#1a5490'}),

            # ── Seletores do mapa ──
            html.Div([
                # Seletor de coluna
                html.Div([
                    html.Label('Coluna para visualizar no mapa:',
                               style={'fontWeight': 'bold', 'marginBottom': '6px', 'display': 'block', 'color': '#1a5490'}),
                    dcc.Dropdown(
                        id='map-column-selector',
                        options=get_map_column_options(),
                        value=(get_map_column_options()[0]['value'] if get_map_column_options() else None),
                        clearable=False,
                        style={'width': '100%'}
                    )
                ], style={'width': '45%', 'display': 'inline-block', 'marginRight': '3%', 'verticalAlign': 'top'}),

                # Seletor de valor (visível apenas para categóricas)
                html.Div([
                    html.Label('Valor a destacar (apenas colunas categóricas):',
                               style={'fontWeight': 'bold', 'marginBottom': '6px', 'display': 'block', 'color': '#1a5490'}),
                    dcc.Dropdown(
                        id='map-value-selector',
                        options=[],
                        value=None,
                        clearable=True,
                        placeholder='Todos os valores (contagem total)',
                        style={'width': '100%'}
                    )
                ], id='map-value-selector-div',
                   style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

                # Indicador do modo ativo
                html.Div(id='map-mode-indicator',
                         style={'marginTop': '12px', 'fontSize': '13px', 'color': '#555', 'fontStyle': 'italic'})

            ], style={
                'marginBottom': '20px',
                'padding': '15px 20px',
                'backgroundColor': '#e3f2fd',
                'borderRadius': '8px',
                'border': '1px solid #90caf9'
            }),

            dcc.Graph(id='mapa-dinâmico', style={'height': '1000px', 'width': '100%'})
        ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#ffffff',
                  'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        # Análise de ocorrências por localização
        html.Div([
            html.H2('📊 Análise de Distribuição por Localização', style={'marginBottom': '20px', 'color': '#1a5490'}),
            dcc.Graph(id='grafico-distribuicao', style={'height': '400px'})
        ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#ffffff',
                  'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        # Análises por coluna categórica
        html.Div([
            html.H2('🔍 Análises Detalhadas', style={'marginBottom': '20px', 'color': '#1a5490'}),
            html.Div(id='analises-detalhadas')
        ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#ffffff',
                  'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                  'maxHeight': '1200px', 'overflowY': 'auto'}),

        # Tabela de dados
        html.Div([
            html.H2('📋 Dados Detalhados', style={'marginBottom': '20px', 'color': '#1a5490'}),
            html.Div(id='dados-detalhados', style={'overflowX': 'auto'})
        ], style={'marginBottom': '30px', 'padding': '20px', 'backgroundColor': '#ffffff',
                  'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

        # Estatísticas
        html.Div([
            html.H2('📈 Resumo Estatístico', style={'marginBottom': '20px', 'color': '#1a5490'}),
            html.Div(id='stats-div')
        ], style={'padding': '20px', 'backgroundColor': '#ffffff',
                  'borderRadius': '8px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'}),

    ], style={
        'maxWidth': '1600px',
        'margin': '0 auto',
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif'
    })
], style={'backgroundColor': '#f5f5f5', 'minHeight': '100vh', 'padding': '20px'})


# ── Callback 1: Processar upload ──
@callback(
    Output('file-upload-store', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def process_upload(contents, filename):
    global df, location_column
    if contents is None:
        raise PreventUpdate()
    try:
        import base64, io
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        excel_file = io.BytesIO(decoded)
        df = pd.read_excel(excel_file)
        print(f"✓ Arquivo '{filename}' carregado: {df.shape[0]} linhas × {df.shape[1]} colunas")

        location_columns_local = [col for col in df.columns if col.lower() in ['termo', 'municipio', 'município', 'cidade', 'local', 'location']]
        location_column = location_columns_local[0] if location_columns_local else (df.columns[0] if len(df.columns) > 0 else 'municipio')
        print(f"  Coluna de localização: {location_column}")

        if location_column in df.columns:
            coords_list = []
            for local in df[location_column]:
                coord = get_coordinates_from_geojson(str(local))
                if coord is None:
                    coord = {'lat': -5.8, 'lon': -35.2}
                coords_list.append(coord)
            df['lat'] = [c['lat'] for c in coords_list]
            df['lon'] = [c['lon'] for c in coords_list]
        else:
            df['lat'] = -5.8
            df['lon'] = -35.2

        return {'status': 'success', 'filename': filename, 'rows': df.shape[0], 'cols': df.shape[1]}
    except Exception as e:
        import traceback; traceback.print_exc()
        return {'status': 'error', 'filename': filename, 'error': str(e)}


# ── Callback 2: Mensagem de upload ──
@callback(
    Output('upload-message-div', 'children'),
    [Input('file-upload-store', 'data'),
     Input('upload-message-clear-interval', 'n_intervals')],
    prevent_initial_call=True
)
def update_and_clear_upload_message(file_data, n_intervals):
    from dash import callback_context
    if not callback_context.triggered:
        raise PreventUpdate()
    trigger_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == 'upload-message-clear-interval':
        return html.Div()
    if trigger_id == 'file-upload-store':
        if file_data is None:
            return html.Div()
        if file_data['status'] == 'success':
            return html.Div(
                f"✓ Arquivo carregado: {file_data['filename']} ({file_data['rows']} linhas × {file_data['cols']} colunas)",
                style={'color': 'green', 'fontWeight': 'bold', 'padding': '10px',
                       'backgroundColor': '#e8f5e9', 'borderRadius': '5px', 'border': '1px solid #81c784'}
            )
        else:
            return html.Div(
                f"❌ Erro ao carregar arquivo: {file_data.get('error', 'Erro desconhecido')}",
                style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px',
                       'backgroundColor': '#ffebee', 'borderRadius': '5px', 'border': '1px solid #e57373'}
            )
    raise PreventUpdate()


# ── Callback 3: Atualizar filtros dinâmicos ──
@callback(
    Output('filtros-dinamicos-div', 'children'),
    Input('file-upload-store', 'data'),
    prevent_initial_call=False
)
def update_dynamic_filters(file_data):
    return create_dynamic_filters()


# ── Callback 4: Atualizar opções do seletor de coluna do mapa ──
@callback(
    [Output('map-column-selector', 'options'),
     Output('map-column-selector', 'value')],
    Input('file-upload-store', 'data'),
    prevent_initial_call=False
)
def update_map_column_options(file_data):
    options = get_map_column_options()
    default = options[0]['value'] if options else None
    return options, default


# ── Callback 5: Atualizar seletor de valor conforme coluna escolhida ──
@callback(
    [Output('map-value-selector', 'options'),
     Output('map-value-selector', 'value'),
     Output('map-value-selector-div', 'style')],
    Input('map-column-selector', 'value'),
    prevent_initial_call=False
)
def update_map_value_options(selected_col):
    base_style_active   = {'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}
    base_style_inactive = {'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top',
                           'opacity': '0.4', 'pointerEvents': 'none'}

    if selected_col is None or selected_col not in df.columns:
        return [], None, base_style_inactive

    current_cat_cols = get_categorical_columns(df)
    if selected_col in current_cat_cols:
        unique_vals = sorted(df[selected_col].dropna().astype(str).unique())
        options = [{'label': v, 'value': v} for v in unique_vals]
        return options, None, base_style_active
    else:
        return [], None, base_style_inactive


# ── Callback 6: Dashboard principal ──
@callback(
    [Output('mapa-dinâmico', 'figure'),
     Output('grafico-distribuicao', 'figure'),
     Output('analises-detalhadas', 'children'),
     Output('dados-detalhados', 'children'),
     Output('stats-div', 'children'),
     Output('filtered-data-store', 'data'),
     Output('map-mode-indicator', 'children')],
    [Input({'type': 'dynamic-filter', 'index': ALL}, 'value'),
     Input('file-upload-store', 'data'),
     Input('map-column-selector', 'value'),
     Input('map-value-selector', 'value')],
    [State({'type': 'dynamic-filter', 'index': ALL}, 'id')],
    prevent_initial_call=False
)
def update_dashboard(filter_values, file_data, map_column, map_value, filter_ids):
    current_categorical_columns = get_categorical_columns(df)
    current_numeric_columns = get_numeric_columns(df)

    # Aplicar filtros globais
    filters = {}
    for fid, value in zip(filter_ids, filter_values):
        if value != 'all':
            filters[fid['index']] = value
    filtered_df = apply_dynamic_filters(df.copy(), filters)

    if location_column not in df.columns:
        empty = go.Figure()
        return empty, empty, html.Div("Nenhuma coluna de localização encontrada"), \
               html.Div("Nenhum dado"), html.Div("Sem dados"), filtered_df.to_json(), ""

    # ===== LÓGICA DO MAPA =====
    map_mode_text = ""

    if map_column and map_column in df.columns:
        is_categorical = map_column in current_categorical_columns

        if is_categorical and map_value:
            # Contar ocorrências do valor selecionado por município
            temp = filtered_df[filtered_df[map_column].astype(str) == map_value]
            municipios_df = temp.groupby(location_column).agg(
                lat=('lat', 'first'),
                lon=('lon', 'first'),
                valor_mapa=(map_column, 'count')
            ).reset_index()
            color_label = f'Qtd "{map_value}"'
            map_mode_text = f'🔵 Modo: contagem de "{map_value}" em "{map_column}" por município'

        elif is_categorical:
            # Contar total de registros não-nulos por município
            municipios_df = filtered_df.groupby(location_column).agg(
                lat=('lat', 'first'),
                lon=('lon', 'first'),
                valor_mapa=(map_column, 'count')
            ).reset_index()
            color_label = f'Total preenchidos ({map_column})'
            map_mode_text = f'🟡 Modo: total de registros com "{map_column}" preenchido por município'

        else:
            # Coluna numérica: somar
            municipios_df = filtered_df.groupby(location_column).agg(
                lat=('lat', 'first'),
                lon=('lon', 'first'),
                valor_mapa=(map_column, 'sum')
            ).reset_index()
            color_label = f'Soma de {map_column}'
            map_mode_text = f'🟢 Modo: soma de "{map_column}" por município'
    else:
        # Fallback: contagem total
        municipios_df = filtered_df.groupby(location_column).agg(
            lat=('lat', 'first'),
            lon=('lon', 'first')
        ).reset_index()
        municipios_df['valor_mapa'] = filtered_df.groupby(location_column).size().values
        color_label = 'Total de Registros'
        map_mode_text = '⚪ Modo: total de registros por município'

    # Normalizar nomes para bater com GeoJSON
    municipios_df[location_column] = municipios_df[location_column].astype(str).str.title()

    # ── Remover municípios com valor 0 (não têm o dado selecionado) ──
    # Isso garante que só os municípios COM o valor apareçam coloridos
    municipios_com_dados = municipios_df[municipios_df['valor_mapa'] > 0].copy()

    # Construir figura do mapa
    fig_mapa = go.Figure()

    # Camada 0: fundo cinza explícito para TODOS os municípios do RN
    # (inclusive os que não têm dados — eles ficam cinza)
    if municipios_geojson:
        todos_municipios = [f['properties']['name_muni'] for f in municipios_geojson['features']]
        fig_mapa.add_trace(go.Choropleth(
            geojson=municipios_geojson,
            locations=todos_municipios,
            z=[0] * len(todos_municipios),
            featureidkey='properties.name_muni',
            colorscale=[[0, 'rgb(220,220,220)'], [1, 'rgb(220,220,220)']],
            showscale=False,
            marker=dict(line=dict(width=0.5, color='white')),
            hoverinfo='skip',
            name='RN (sem dados)'
        ))

    # Camada 1: APENAS municípios que têm o valor > 0 (coloridos)
    if municipios_geojson and len(municipios_com_dados) > 0:
        fig_mapa.add_trace(go.Choropleth(
            geojson=municipios_geojson,
            locations=municipios_com_dados[location_column],
            z=municipios_com_dados['valor_mapa'],
            featureidkey='properties.name_muni',
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title=color_label),
            marker=dict(line=dict(width=1, color='white')),
            hovertemplate=f'<b>%{{location}}</b><br>{color_label}: <b>%{{z}}</b><extra></extra>',
            name='Municípios com dados',
            zmin=municipios_com_dados['valor_mapa'].min(),
            zmax=municipios_com_dados['valor_mapa'].max(),
        ))

    # Camada 2: pontos apenas sobre municípios com dados
    if len(municipios_com_dados) > 0:
        fig_mapa.add_trace(go.Scattergeo(
            lon=municipios_com_dados['lon'],
            lat=municipios_com_dados['lat'],
            mode='markers',
            marker=dict(size=6, color='white', line=dict(width=1, color='black'), opacity=0.6),
            customdata=municipios_com_dados[[location_column, 'valor_mapa']],
            hovertemplate=f'<b>%{{customdata[0]}}</b><br>{color_label}: <b>%{{customdata[1]}}</b><extra></extra>',
            name='Localidades'
        ))

    fig_mapa.update_layout(
        title=f'Mapa: {color_label}',
        geo=dict(
            scope='south america',
            projection_type='mercator',
            center=dict(lat=-5.8, lon=-36.5),
            projection_scale=22,
            showland=True,
            landcolor='rgb(240, 240, 240)',
            showcoastlines=True,
            coastlinecolor='gray',
            resolution=50,
        ),
        height=1200,
        hovermode='closest',
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # ===== GRÁFICO DE DISTRIBUIÇÃO =====
    dist_data = filtered_df.groupby(location_column).size().reset_index(name='count').sort_values('count', ascending=False)
    fig_dist = px.bar(
        dist_data,
        x=location_column,
        y='count',
        title=f'Distribuição de Registros por {location_column}',
        labels={'count': 'Quantidade', location_column: location_column},
        color='count',
        color_continuous_scale='Viridis',
        height=400
    )
    fig_dist.update_layout(xaxis_tickangle=-45, hovermode='x unified')

    # ===== ANÁLISES DETALHADAS =====
    analises_children = []
    for col in current_categorical_columns:
        if col.lower() in ['termo', 'município', 'municipio', 'cidade', 'local', 'location']:
            continue
        analise_data = filtered_df.groupby([location_column, col]).size().reset_index(name='count')
        pivot_data = analise_data.pivot_table(values='count', index=location_column, columns=col, fill_value=0)
        header_cols = [location_column] + list(pivot_data.columns)
        data_rows = []
        for idx, row in pivot_data.iterrows():
            row_cells = [html.Td(str(idx), style={'padding': '10px', 'borderBottom': '1px solid #ddd', 'fontWeight': 'bold', 'backgroundColor': '#f9f9f9'})]
            for val in row:
                row_cells.append(html.Td(str(int(val)), style={'padding': '10px', 'borderBottom': '1px solid #ddd', 'textAlign': 'center'}))
            data_rows.append(html.Tr(row_cells))
        analises_children.append(
            html.Div([
                html.Div([
                    html.Button(
                        f'▼ {col} por {location_column}',
                        id={'type': 'toggle-analise', 'index': col},
                        style={
                            'width': '100%', 'padding': '12px',
                            'backgroundColor': '#1a5490', 'color': 'white',
                            'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer',
                            'fontSize': '14px', 'fontWeight': 'bold', 'textAlign': 'left', 'marginBottom': '10px'
                        }
                    )
                ]),
                html.Div(
                    html.Table(
                        [html.Tr([html.Th(col_name, style={'padding': '10px', 'backgroundColor': '#e3f2fd',
                                                            'textAlign': 'left', 'fontWeight': 'bold',
                                                            'borderBottom': '2px solid #1a5490'})
                                  for col_name in header_cols])] + data_rows,
                        style={'width': '100%', 'borderCollapse': 'collapse', 'marginBottom': '20px', 'border': '1px solid #ddd'}
                    ),
                    id={'type': 'content-analise', 'index': col},
                    style={'display': 'block', 'paddingBottom': '15px'}
                )
            ], style={'marginBottom': '25px', 'padding': '15px', 'backgroundColor': '#fffbf0',
                      'borderRadius': '8px', 'border': '1px solid #ffe0b2'})
        )

    # ===== TABELA DE DADOS =====
    if len(filtered_df) > 0:
        display_df = filtered_df.head(100)
        table_rows = [
            html.Tr([
                html.Th(col, style={'padding': '12px', 'backgroundColor': '#1a5490', 'color': 'white', 'textAlign': 'left'})
                for col in display_df.columns if col not in ['lat', 'lon']
            ])
        ]
        cores_alternadas = ['#f9f9f9', 'white']
        for idx, (_, row) in enumerate(display_df.iterrows()):
            table_rows.append(
                html.Tr([
                    html.Td(str(row[col]),
                            style={'padding': '10px', 'borderBottom': '1px solid #ddd',
                                   'backgroundColor': cores_alternadas[idx % 2], 'fontSize': '12px'})
                    for col in display_df.columns if col not in ['lat', 'lon']
                ])
            )
        tabela = html.Table(table_rows, style={'width': '100%', 'borderCollapse': 'collapse', 'fontSize': '12px'})
    else:
        tabela = html.Div('Nenhum dado encontrado com os filtros aplicados',
                          style={'color': '#666', 'padding': '20px', 'textAlign': 'center'})

    # ===== ESTATÍSTICAS =====
    total_registros = len(filtered_df)
    total_localizacoes = filtered_df[location_column].nunique() if location_column in filtered_df.columns else 0
    stats_html = html.Div([
        html.Div([
            html.Div([
                html.H4('Total de Registros', style={'color': '#1a5490', 'margin': '0 0 10px 0'}),
                html.P(f'{total_registros:,}', style={'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0', 'color': '#1a5490'})
            ], style={'width': '22%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#e3f2fd', 'borderRadius': '8px', 'marginRight': '2%', 'verticalAlign': 'top'}),
            html.Div([
                html.H4('Localidades', style={'color': '#2e7d32', 'margin': '0 0 10px 0'}),
                html.P(f'{total_localizacoes}', style={'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0', 'color': '#2e7d32'})
            ], style={'width': '22%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#e8f5e9', 'borderRadius': '8px', 'marginRight': '2%', 'verticalAlign': 'top'}),
            html.Div([
                html.H4('Filtros Aplicados', style={'color': '#f57c00', 'margin': '0 0 10px 0'}),
                html.P(f'{len(filters)}', style={'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0', 'color': '#f57c00'})
            ], style={'width': '22%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#fff3e0', 'borderRadius': '8px', 'marginRight': '2%', 'verticalAlign': 'top'}),
            html.Div([
                html.H4('Taxa de Preenchimento', style={'color': '#c62828', 'margin': '0 0 10px 0'}),
                html.P(f'{(len(filtered_df)/len(df)*100):.1f}%', style={'fontSize': '32px', 'fontWeight': 'bold', 'margin': '0', 'color': '#c62828'})
            ], style={'width': '22%', 'display': 'inline-block', 'padding': '20px', 'backgroundColor': '#ffebee', 'borderRadius': '8px', 'verticalAlign': 'top'}),
        ])
    ])

    return fig_mapa, fig_dist, analises_children, tabela, stats_html, filtered_df.to_json(), map_mode_text


# ── Callback 7: Toggle de análises detalhadas ──
@callback(
    Output({'type': 'content-analise', 'index': MATCH}, 'style'),
    Input({'type': 'toggle-analise', 'index': MATCH}, 'n_clicks'),
    State({'type': 'content-analise', 'index': MATCH}, 'style'),
    prevent_initial_call=True
)
def toggle_analise(n_clicks, current_style):
    if n_clicks is None or n_clicks == 0:
        return {'display': 'block', 'paddingBottom': '15px'}
    is_hidden = n_clicks % 2 == 0
    return {
        'display': 'none' if is_hidden else 'block',
        'paddingBottom': '15px' if not is_hidden else '0'
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)