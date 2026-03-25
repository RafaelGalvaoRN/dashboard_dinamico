import pandas as pd
from pathlib import Path


def load_excel(file_path: str) -> pd.DataFrame:
    """
    Carrega um arquivo Excel e retorna um DataFrame.
    
    Args:
        file_path: Caminho para o arquivo Excel
        
    Returns:
        DataFrame com os dados do Excel
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {file_path} não encontrado")
    except Exception as e:
        raise Exception(f"Erro ao carregar arquivo: {str(e)}")


def get_unique_values(df: pd.DataFrame, column: str) -> list:
    """
    Retorna valores únicos de uma coluna, removendo NaN e valores nulos.
    
    Args:
        df: DataFrame
        column: Nome da coluna
        
    Returns:
        Lista de valores únicos ordenados
    """
    import numpy as np
    
    # Obter valores únicos
    unique_values = df[column].unique()
    
    # Filtrar valores NaN/None
    filtered_values = [v for v in unique_values if pd.notna(v) and str(v).strip() != '']
    
    # Converter para string para garantir que tudo é comparável
    filtered_values = [str(v).strip() for v in filtered_values]
    
    # Ordenar
    try:
        return sorted(set(filtered_values))  # set() remove duplicatas de string
    except TypeError:
        # Se ainda houver problema, retornar sem ordenação
        return list(set(filtered_values))


def filter_data(df: pd.DataFrame, comarca: str = None, termo: str = None) -> pd.DataFrame:
    """
    Filtra os dados por comarca e/ou termo.
    
    Args:
        df: DataFrame
        comarca: Nome da comarca (opcional)
        termo: Nome do termo (opcional)
        
    Returns:
        DataFrame filtrado
    """
    filtered_df = df.copy()
    
    if comarca:
        filtered_df = filtered_df[filtered_df['comarca'] == comarca]
    
    if termo:
        filtered_df = filtered_df[filtered_df['termo'] == termo]
    
    return filtered_df


def filter_not_nan(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Retorna um DataFrame contendo apenas as linhas em que a coluna especificada não é NaN.
    
    Args:
        df: DataFrame de entrada
        column: Nome da coluna a ser verificada
        
    Returns:
        DataFrame filtrado
    """
    if column not in df.columns:
        raise ValueError(f"Coluna '{column}' não existe no DataFrame")
    
    return df[df[column].notna()]