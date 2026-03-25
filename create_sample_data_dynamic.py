#!/usr/bin/env python
"""
Script para gerar dados de exemplo realista para testar o dashboard
Cria um arquivo com dados sobre serviços de proteção a crianças no RN
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sample_data():
    """Cria dados de amostra realista"""
    
    np.random.seed(42)
    
    # Dados dos municípios do RN
    municipios = [
        'Natal', 'Parnamirim', 'São Gonçalo do Amarante', 'Ceará-Mirim',
        'Macau', 'Areia Branca', 'Mossoró', 'Açu', 'Caicó', 'Currais Novos',
        'Patos', 'Santa Cruz', 'Goianinha', 'Arez', 'Touros', 'Pendências',
        'Macaíba', 'Extremoz', 'Lages', 'Jandaíra'
    ]
    
    # Comarcas do RN
    comarcas = {
        'Natal': 'Comarca da Capital',
        'Parnamirim': 'Comarca da Capital',
        'São G onçalo do Amarante': 'Comarca de São Gonçalo',
        'Ceará-Mirim': 'Comarca de Ceará-Mirim',
        'Macau': 'Comarca de Macau',
        'Areia Branca': 'Comarca de Areia Branca',
        'Mossoró': 'Comarca de Mossoró',
        'Açu': 'Comarca de Açu',
        'Caicó': 'Comarca de Caicó',
        'Currais Novos': 'Comarca de Currais Novos',
        'Patos': 'Comarca de Patos',
        'Santa Cruz': 'Comarca de Santa Cruz',
        'Goianinha': 'Comarca de Goianinha',
        'Arez': 'Comarca de Arez',
        'Touros': 'Comarca de Touros',
        'Pendências': 'Comarca de Pendências',
        'Macaíba': 'Comarca da Capital',
        'Extremoz': 'Comarca da Capital',
        'Lages': 'Comarca de Lages',
        'Jandaíra': 'Comarca de Jandaíra',
    }
    
    tipos_servico = [
        'Proteção Integrada',
        'Acolhimento de Crianças',
        'Assistência Social',
        'Saúde e Nutrição',
        'Educação e Capacitação',
        'Prevenção de Violência',
    ]
    
    tipos_acolhimento = [
        'Família Acolhedora',
        'Abrigo Institucional',
        'Abrigo Específico',
        'Casa Lar',
        'Não Aplicável'
    ]
    
    natureza = ['Público', 'Privado', 'Filantrópico', 'ONG']
    abrangencia = ['Municipal', 'Regional', 'Estadual']
    
    sim_nao = ['Sim', 'Não', 'Em Implementação', 'Previsto']
    
    # Gerar dados
    data = []
    
    # Gerar 150 registros variados
    for i in range(150):
        municipio = np.random.choice(municipios)
        comarca = comarcas.get(municipio, 'Não Classificado')
        tipo_servico = np.random.choice(tipos_servico)
        
        # Acolhimento é específico para serviços de acolhimento
        if 'Acolhimento' in tipo_servico:
            tipo_acolhimento = np.random.choice(tipos_acolhimento[:-1])
            beneficiarios = np.random.randint(15, 150)
        else:
            tipo_acolhimento = 'Não Aplicável'
            beneficiarios = np.random.randint(50, 300)
        
        # Proteção integrada mais comum em capitais
        if municipio in ['Natal', 'Mossoró']:
            protecao_integrada = np.random.choice(['Sim', 'Sim', 'Não'])
        else:
            protecao_integrada = np.random.choice(['Sim', 'Não', 'Não'])
        
        # Comitê mais comum em capitais
        if municipio in ['Natal', 'Parnamirim', 'Mossoró']:
            comite = np.random.choice(['Sim', 'Não'], p=[0.7, 0.3])
        else:
            comite = np.random.choice(['Sim', 'Não'], p=[0.4, 0.6])
        
        # Protocolos
        protocolos = np.random.choice(['Sim', 'Não', 'Em Desenvolvimento'])
        
        # Data de implementação
        dias_atras = np.random.randint(1, 1000)
        data_impl = (datetime.now() - timedelta(days=dias_atras)).strftime('%Y-%m-%d')
        
        data.append({
            'municipio': municipio,
            'comarca': comarca,
            'tipo_servico': tipo_servico,
            'tipo_acolhimento': tipo_acolhimento,
            'natureza': natureza[i % len(natureza)],
            'abrangencia': np.random.choice(abrangencia),
            'protecao_integrada': protecao_integrada,
            'comite_cuidados': comite,
            'protocolos_violencia': protocolos,
            'beneficiarios': beneficiarios,
            'atendimentos_2024': np.random.randint(10, 500),
            'capacidade_acolhimento': beneficiarios + np.random.randint(5, 30),
            'data_implementacao': data_impl,
        })
    
    df = pd.DataFrame(data)
    
    # Salvar
    output_file = 'data/dados_servicos_rn.xlsx'
    df.to_excel(output_file, index=False)
    
    print("✓ Arquivo de amostra criado com sucesso!")
    print(f"  Arquivo: {output_file}")
    print(f"  Registros: {len(df)}")
    print(f"  Colunas: {len(df.columns)}")
    print()
    print("Resumo dos dados:")
    print(f"  - Municípios: {df['municipio'].nunique()}")
    print(f"  - Tipos de Serviço: {df['tipo_servico'].nunique()}")
    print(f"  - Comarcas: {df['comarca'].nunique()}")
    print()
    print("Primeiras linhas:")
    print(df.head(10).to_string())
    print()
    print("Estatísticas:")
    print(df.describe())
    
    return df

if __name__ == '__main__':
    print("="*70)
    print("GERADOR DE DADOS DE AMOSTRA - Dashboard Dinâmico RN")
    print("="*70)
    print()
    
    df = create_sample_data()
    
    print()
    print("✓ Pronto! Agora execute:")
    print("  python run_dashboard_cli.py")
    print()
