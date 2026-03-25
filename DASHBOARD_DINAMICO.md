# 🗺️ Dashboard Dinâmico - Rio Grande do Norte

## Visão Geral

Sistema de visualização e análise interativa de dados geográficos do Rio Grande do Norte com **filtros dinâmicos gerados automaticamente** a partir das colunas da sua planilha Excel.

## Características Principais

✨ **Filtros Automáticos**: Sistema detecta automaticamente as colunas de sua planilha e cria filtros para utilizá-las

📍 **Mapa Interativo**: Visualização dos dados plotados no mapa do RN com cores e tamanhos proporcionais aos valores

📊 **Gráficos de Distribuição**: Análises automáticas de distribuição de dados por localidade

🔍 **Análises Detalhadas**: Tabelas cruzadas mostrando distribuições entre colunas categóricas

📋 **Tabela de Dados**: Visualização completa dos dados com possibilidade de consulta

## Como Usar

### 1. Preparar os Dados

Crie uma planilha Excel (`.xlsx`) com a seguinte estrutura:

**Coluna obrigatória:**
- `municipio` (ou `termo`, `cidade`) - localização no mapa do RN

**Colunas categóricas** (para filtros):
- `tipo_servico` - Ex: "Proteção Integrada", "Acolhimento", etc.
- `tipo_acolhimento` - Ex: "Familiar", "Institucional"
- `natureza` - Ex: "Público", "Privado"
- `abrangencia` - Ex: "Municipal", "Regional"
- Qualquer outra coluna de texto!

**Colunas numéricas** (para agregação):
- `quantidade_beneficiarios`
- `numero_atendimentos`
- Qualquer coluna numérica que deseje somar

### 2. Executar o Dashboard

```bash
# Ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\activate

# Instalar dependências (se necessário)
pip install -r requirements.txt

# Iniciar o servidor
python app.py
```

O dashboard será aberto em: **http://localhost:8050**

### 3. Usar os Filtros

1. **Filtros Automáticos**: Na seção "Filtros", aparecerão dropdowns para cada coluna categórica
2. **Selecione "Todos"** para ver todos os dados, ou escolha um valor específico
3. O dashboard **atualiza automaticamente** mostrando:
   - Mapa com distribuição geográfica
   - Gráfico de barras da distribuição
   - Análises cruzadas (tabelas)
   - Dados detalhados em tabela
   - Estatísticas resumidas

## Exemplos de Análises

Com esse sistema você pode responder a perguntas como:

### 1. Geografia de um Serviço Específico
**Pergunta**: "Em quantos municípios o serviço de Proteção Integrada já foi implementado?"

**Ação**: 
1. Filtrar `tipo_servico` = "Proteção Integrada"
2. Ver o mapa mostrando os municípios
3. Verificar a estatística de "Localidades"

### 2. Distribuição de Tipos de Acolhimento
**Pergunta**: "Distribuição dos serviços de acolhimento por comarca (tipos: familiar, institucional)"

**Ação**:
1. Filtrar `tipo_servico` = "Acolhimento"
2. Vê a tabela em "Análises Detalhadas" mostrando a cruzada entre `municipio` e `tipo_acolhimento`
3. Identificar onde cada tipo está presente

### 3. Análise de Cobertura
**Pergunta**: "Quais municípios possuem serviços com comitê de cuidados?"

**Ação**:
1. Filtrar `comite_cuidados` = "Sim"
2. O mapa mostra apenas os municípios com comitê
3. Verificar quantos municípios têm cobertura completa

### 4. Combinações de Filtros
**Pergunta**: "Quantas instituições privadas de acolhimento familiar existem?"

**Ação**:
1. Aplicar filtros simultaneamente:
   - `tipo_acolhimento` = "Familiar"
   - `natureza` = "Privado"
2. Ver a distribuição resultante no mapa

## Estrutura de Dados Esperada

```
municipio              | tipo_servico         | tipo_acolhimento | natureza | quantidade_beneficiarios
----------------------|----------------------|------------------|----------|------------------------
Natal                 | Proteção Integrada   | -                | Público  | 150
Parnamirim           | Acolhimento          | Familiar         | Público  | 45
São Gonçalo          | Acolhimento          | Institucional    | Privado  | 80
Ceará-Mirim          | Assistência Social   | -                | Público  | 120
Mossoró              | Proteção Integrada   | -                | Público  | 95
```

## Arquivos do Sistema

```
app.py                          # Aplicativo principal Dash
utils/
  ├── dynamic_filters.py       # Funções de detecção e aplicação de filtros
  ├── data_loader.py           # Carregadores de dados
  └── __init__.py
data/
  ├── dados_servicos_rn.xlsx   # Arquivo de exemplo com dados completos
  ├── rio_grande_norte.xlsx    # Dados básicos do RN
  ├── rio_grande_norte_real.geojson  # Mapa do RN
  └── municipios.geojson       # Municípios (referência)
requirements.txt               # Dependências Python
```

## Dependências

- **dash**: Framework web interativo
- **plotly**: Gráficos e mapas interativos
- **pandas**: Manipulação de dados
- **openpyxl**: Leitura de arquivos Excel

## Dicas

1. **Coluna de Localização**: Certifique-se que o nome seja `municipio`, `termo`, `cidade` ou `local`

2. **Nomes de Municípios**: Use os nomes corretos dos municípios do RN para o mapa funcionar:
   - Natal, Parnamirim, Mossoró, Caicó, Currais Novos, etc.

3. **Valores Numéricos**: Colunas com números serão somadas por localização na agregação

4. **Sem Limite de Colunas**: Adicione quantas colunas categorical quiser - o sistema criará filtros automaticamente!

5. **Atualização em Tempo Real**: Todo mudança de filtro atualiza o dashboard instantaneamente

## Troubleshooting

**Problema**: Os filtros não aparecem
- **Solução**: Verifique se o arquivo Excel está no caminho correto (`data/dados_servicos_rn.xlsx`)

**Problema**: O mapa está vazio
- **Solução**: Verifique se a coluna de localização está nomeada corretamente

**Problema**: Erro ao carregar dados
- **Solução**: Verifique se o arquivo Excel não está aberto em outro programa

## Próximas Melhorias

- [ ] Exportar relatórios em PDF
- [ ] Filtros avançados (range numérico, datas)
- [ ] Gráficos de série temporal
- [ ] Download de dados filtrados em Excel
- [ ] Salvamento de filtros como templates
- [ ] Integração com banco de dados

---

**Desenvolvido com ❤️ para análise de dados geográficos do RN**
