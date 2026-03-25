"""
Módulo para gerar filtros dinâmicos baseado nas colunas de um DataFrame
Detecta automaticamente colunas categóricas e numéricas
"""

import pandas as pd
from typing import List, Dict, Any


def get_categorical_columns(df: pd.DataFrame, threshold: float = 0.9) -> List[str]:
    """
    Identifica colunas categóricas de um DataFrame.
    
    Critérios:
    - Colunas com tipo texto (object, string, str, category)
    - Excetua colunas numéricas (int, float) mesmo que tenham poucos valores únicos
    
    Args:
        df: DataFrame
        threshold: Proporção máxima de valores únicos para considerar categórica
                  (padrão: 0.9 = máx 90% de valores únicos)
    
    Returns:
        Lista de nomes de colunas categóricas
    """
    categorical_cols = []
    
    for col in df.columns:
        # Ignorar colunas de localização (lat/lon)
        if col in ['lat', 'lon']:
            continue
        
        dtype_name = str(df[col].dtype).lower()
        
        # Colunas de texto são sempre categóricas
        if 'object' in dtype_name or 'string' in dtype_name or 'str' in dtype_name or 'category' in dtype_name:
            # Mas não incluir se for a coluna de quantidade/números
            if not any(x in col.lower() for x in ['quantidade', 'total', 'count', 'sum', 'valor', 'price']):
                categorical_cols.append(col)
    
    return categorical_cols


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """
    Identifica colunas numéricas de um DataFrame.
    
    Args:
        df: DataFrame
    
    Returns:
        Lista de nomes de colunas numéricas
    """
    numeric_cols = []
    
    for col in df.columns:
        # Ignorar colunas de localização
        if col in ['lat', 'lon']:
            continue
        
        dtype_name = str(df[col].dtype).lower()
        if 'int' in dtype_name or 'float' in dtype_name:
            numeric_cols.append(col)
    
    return numeric_cols


def apply_dynamic_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Aplica filtros dinâmicos a um DataFrame.
    
    Args:
        df: DataFrame
        filters: Dicionário com {coluna: valor} ou {coluna: [valores]}
    
    Returns:
        DataFrame filtrado
    """
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if column not in filtered_df.columns:
            continue
        
        if isinstance(value, list):
            # Se for uma lista, usar "in"
            filtered_df = filtered_df[filtered_df[column].isin(value)]
        else:
            # Se for um valor único
            if value != 'all':
                filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df


def create_aggregated_data(df: pd.DataFrame, group_cols: List[str], 
                           agg_cols: Dict[str, str] = None) -> pd.DataFrame:
    """
    Cria dados agregados a partir de um DataFrame.
    
    Args:
        df: DataFrame
        group_cols: Colunas para agrupar
        agg_cols: Dicionário com {coluna: função_agregação}
                 Funções: 'sum', 'mean', 'count', 'min', 'max', 'first', 'last'
    
    Returns:
        DataFrame agregado
    """
    if not agg_cols:
        agg_cols = {}
    
    try:
        return df.groupby(group_cols).agg(agg_cols).reset_index()
    except Exception as e:
        print(f"Erro ao agregar dados: {e}")
        return df


def get_unique_values(df: pd.DataFrame, column: str) -> List:
    """
    Retorna valores únicos de uma coluna.
    
    Args:
        df: DataFrame
        column: Nome da coluna
    
    Returns:
        Lista de valores únicos (ordenados)
    """
    if column not in df.columns:
        return []
    
    values = df[column].unique().tolist()
    # Remover NaN
    values = [v for v in values if pd.notna(v)]
    return sorted(values)


def filter_data(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Filtra dados por múltiplas colunas.
    
    Exemplo:
        filter_data(df, comarca='Natal', termo='Natal')
    
    Args:
        df: DataFrame
        **kwargs: Dicionário com filtros {coluna: valor}
    
    Returns:
        DataFrame filtrado
    """
    filtered_df = df.copy()
    
    for column, value in kwargs.items():
        if value is not None and column in filtered_df.columns:
            filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df


def generate_analysis_questions(df: pd.DataFrame, location_col: str) -> Dict[str, str]:
    """
    Gera perguntas analíticas automáticas baseado nas colunas do DataFrame.
    
    Exemplos:
    - "Em quantas [localidades] o [serviço] já existe?"
    - "Qual a distribuição de [tipo] por [localidade]?"
    
    Args:
        df: DataFrame
        location_col: Nome da coluna de localização
    
    Returns:
        Dicionário com perguntas sugeridas
    """
    questions = {}
    categorical_cols = get_categorical_columns(df)
    
    for i, col in enumerate(categorical_cols):
        if col == location_col:
            continue
        
        # Pergunta 1: Contagem por localidade
        questions[f'q{i}_count'] = f"Em quantas {location_col}s o {col} está presente?"
        
        # Pergunta 2: Distribuição
        questions[f'q{i}_dist'] = f"Como está distribuído o {col} por {location_col}?"
    
    return questions
