"""
Configurações do Dashboard
Arquivo central para customizar comportamentos da aplicação
"""

# Caminho do arquivo Excel
EXCEL_FILE_PATH = 'data/exemplo.xlsx'

# Configurações do servidor
HOST = '0.0.0.0'
PORT = 8050
DEBUG = True

# Configurações do mapa
MAP_CENTER_LAT = -23.5
MAP_CENTER_LON = -47
MAP_COLORSCALE = 'Viridis'  # Opções: 'Blues', 'Reds', 'Greens', 'Viridis', 'Plasma', etc.

# Tamanho dos marcadores (ajustar esses valores para mudar o tamanho visual)
MARKER_SIZE_MIN = 10
MARKER_SIZE_MAX = 40

# Estilos e cores
PRIMARY_COLOR = '#007bff'
SUCCESS_COLOR = '#28a745'
WARNING_COLOR = '#ffc107'
DANGER_COLOR = '#dc3545'
BACKGROUND_COLOR = '#f8f9fa'

# Coordenadas das cidades
COORDENADAS = {
    'São Paulo': {'lat': -23.5505, 'lon': -46.6333},
    'Campinas': {'lat': -22.9068, 'lon': -47.0616},
    'Ribeirão Preto': {'lat': -21.1925, 'lon': -47.8105},
    'Santos': {'lat': -23.9608, 'lon': -46.3334},
    'Sorocaba': {'lat': -23.5006, 'lon': -47.4582},
    'Guarulhos': {'lat': -23.4729, 'lon': -46.4917},
    'Osasco': {'lat': -23.5309, 'lon': -46.7919},
    'Mogi Cruzes': {'lat': -23.5014, 'lon': -46.1858},
    'Salto': {'lat': -23.1947, 'lon': -47.2920},
    'Piracicaba': {'lat': -22.7297, 'lon': -47.6500},
    'Tatuapé': {'lat': -23.5555, 'lon': -46.5500},
    'Zona Leste': {'lat': -23.5700, 'lon': -46.4500},
    'Sumaré': {'lat': -22.8260, 'lon': -47.2610},
    'Araraquara': {'lat': -21.7945, 'lon': -48.1758},
    'Praia Grande': {'lat': -24.0093, 'lon': -46.4028},
    'Itu': {'lat': -23.2653, 'lon': -47.2986},
    'Arujá': {'lat': -23.4319, 'lon': -46.3119},
    'Carapicuíba': {'lat': -23.6503, 'lon': -46.8370},
    'Suzano': {'lat': -23.5381, 'lon': -46.3056},
}
