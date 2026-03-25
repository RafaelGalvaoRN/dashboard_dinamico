# 🗺️ Sistema de Análise Dinâmica de Dados Geográficos - Rio Grande do Norte

#### Dashboard Interativo com Filtros Automáticos

---

## ✨ O que é Este Sistema?

Um **dashboard web interativo** que permite visualizar e analisar dados geográficos do Rio Grande do Norte com **filtros automaticamente gerados** a partir de suas colunas Excel.

### 🎯 Problema Resolvido

Você tem uma planilha com dados sobre serviços de proteção a crianças no RN e quer:

1. ✅ Visualizar onde cada serviço está implementado (no mapa)
2. ✅ Responder perguntas como:
   - "Em quantas comarcas a Proteção Integrada já passou?"
   - "Qual a distribuição de acolhimentos (familiar/institucional/público/privado)?"
   - "Quais municípios têm comitê de cuidados?"
3. ✅ Fazer análises cruzadas dinâmicas
4. ✅ Tudo sem programação - apenas atualizando Excel!

---

## 🚀 Como Começar

### 1️⃣ Instalação (Primeira Vez)

```bash
# Clone ou abra o projeto
cd c:\Users\User\PycharmProjects\sasha

# Ative o ambiente virtual (já criado)
.venv\Scripts\activate

# Instale as dependências (se necessário)
pip install -r requirements.txt
```

### 2️⃣ Prepare Seus Dados

**Opção A**: Use os dados de exemplo (para teste)
```bash
python create_sample_data_dynamic.py
```

**Opção B**: Use seus dados reais
1. Abra `GUIA_DADOS_REAIS.md`
2. Estruture sua planilha conforme orientações
3. Salve como `data/dados_servicos_rn.xlsx`

### 3️⃣ Execute o Dashboard

```bash
# Windows - Double-click
run_dashboard.bat

# Ou execute via Python
python run_dashboard_cli.py

# Ou execute direto
python app.py
```

**Acesse**: `http://localhost:8050`

---

## 🎨 Recursos Principais

### 📍 Mapa Interativo
- Visualiza municípios do RN
- Tamanho/cor dos marcadores proporcional aos dados
- Zoom e pan interativo
- Hover com informações detalhadas

### 🔍 Filtros Dinâmicos
- **Criados automaticamente** para cada coluna de seu Excel
- Múltiplos filtros simultâneos
- Atualização em tempo real
- Sem limite de colunas!

### 📊 Visualizações
- Gráfico de barras de distribuição
- Tabelas cruzadas (análises detalhadas)
- Tabela de dados completa
- Estatísticas resumidas

### 📈 Análises Automáticas
- Contagem de registros
- Distribuição geográfica  
- Agregação por localidade
- Combinações de filtros

---

## 📋 Exemplos de Uso

### Exemplo 1: Proteção Integrada
**Pergunta**: "Em quantas comarcas está implementada?"

1. Filtro: `tipo_servico` = "Proteção Integrada"
2. Mapa mostra os municípios
3. Verifique "Total de Localidades" nas estatísticas
4. Observe na tabela em "Análises Detalhadas" por comarca

### Exemplo 2: Distribuição de Acolhimentos
**Pergunta**: "Quais os tipos (familiar/institucional) por localidade?"

1. Filtro: `tipo_servico` = "Acolhimento"
2. Veja tabela "Distribuição: tipo_acolhimento por municipio"
3. Combinações de natureza (público/privado) automáticas

### Exemplo 3: Cobertura de Comitês  
**Pergunta**: "Quais municípios têm comitê de cuidados?"

1. Filtro: `comite_cuidados` = "Sim"
2. Mapa mostra exatamente quais
3. Contagem nas estatísticas

---

## 📁 Estrutura do Projeto

```
sasha/
├── app.py                           # ← Aplicativo principal
├── run_dashboard.bat                # ← Execute para abrir
├── run_dashboard_cli.py             # ← Execute via Python
├── create_sample_data_dynamic.py    # Gera dados de teste
├── DASHBOARD_DINAMICO.md            # Documentação completa
├── GUIA_DADOS_REAIS.md              # Como adaptar seus dados
├── README_SISTEMA_DINAMICO.md       # Este arquivo
│
├── utils/
│   ├── dynamic_filters.py           # ← Lógica de filtros dinâmicos
│   ├── data_loader.py               # Carregadores de dados
│   └── __init__.py
│
├── data/
│   ├── dados_servicos_rn.xlsx       # Dados a carregar
│   ├── rio_grande_norte.xlsx        # Backup dados simples
│   ├── rio_grande_norte_real.geojson # Mapa do RN
│   └── municipios.geojson           # Referência
│
└── requirements.txt                 # Dependências Python
```

---

## 🛠️ Como Funciona

### Fluxo de Dados

```
Excel File (dados_servicos_rn.xlsx)
    ↓
[Data Loader] Lê arquivo
    ↓
[Dynamic Filters] Detecta colunas:
    - Categóricas → Cria filtros (dropdowns)
    - Numéricas → Usa para agregação/tamanho
    ↓
[Dashboard] Renderiza:
    - Mapa com marcadores
    - Gráficos de distribuição
    - Tabelas cruzadas
    - Estatísticas
    ↓
User Interface → Interação com filtros → Atualização em tempo real
```

### Detecção Automática de Colunas

```python
# CATEGÓRICAS (Criam filtros):
- Tipo de dado: Text/String
- Exemplo: tipo_servico, tipo_acolhimento, natureza

# NUMÉRICAS (Para agregação):  
- Tipo de dado: Integer/Float
- Exemplo: quantidade_beneficiarios, atendimentos_2024
- Ação: SUM (soma) por localidade
```

---

## 📊 Dados Esperados

### Coluna Obrigatória
```
municipio (ou: termo, cidade, local)
```

### Colunas Recomendadas
```
comarca                  # Agrupamento geográfico
tipo_servico            # Tipo principal de serviço
tipo_acolhimento        # Para acolhimentos
natureza                # Público/Privado/ONG
abrangencia             # Municipal/Regional/Estadual
beneficiarios           # Número (agregação)
data_implementacao      # Quando foi implementado
```

### Exemplo de Estrutura
| municipio | tipo_servico | tipo_acolhimento | natureza | beneficiarios |
|-----------|--------------|-----------------|----------|---|
| Natal | Proteção Integrada | - | Público | 150 |
| Parnamirim | Acolhimento | Familiar | Público | 45 |
| Mossoró | Acolhimento | Institucional | Privado | 80 |

---

## 🎓 Recursos Técnicos

### Tecnologias Usadas
- **Dash** (Plotly) - Framework web Python
- **Pandas** - Manipulação de dados
- **Plotly** - Gráficos e mapas interativos
- **Excel/OpenPyXL** - Leitura de dados

### Requisitos
- Python 3.8+
- Dependências em `requirements.txt`
- Arquivo Excel em `data/dados_servicos_rn.xlsx`

### Performance
- Carrega até 10.000+ registros
- Filtros e atualizações em tempo real
- Responsivo em navegadores modernos

---

## ❓ FAQ

### P: Como adiciono novas colunas?
**R**: Basta adicionar colunas no Excel! O sistema detecta automaticamente.

### P: Posso usar números em filtros?
**R**: Apenas colunas de texto criam filtros. Números são usados para agregar/somar.

### P: Como atualizo os dados?
**R**: 
1. Atualize o arquivo Excel `data/dados_servicos_rn.xlsx`
2. Feche o navegador
3. Reinicie o dashboard
4. Dados carregam automaticamente

### P: Posso exportar os dados?
**R**: Atualmente não, mas você pode copiar da tabela ou manter o Excel atualizado.

### P: O sistema funciona offline?
**R**: Sim! Tudo roda localmente. Apenas abra `run_dashboard.bat` quando precisar.

---

## 📞 Suporte

### Problemas Comuns

**Erro: "Arquivo não encontrado"**
- Verifique se existe `data/dados_servicos_rn.xlsx`
- Execute: `python create_sample_data_dynamic.py`

**Erro: "Porta 8050 já em uso"**
- Feche outro dashboard rodando
- Ou mude porta em `app.py`: `port=8051`

**Filtros não aparecem**
- Verifique as colunas do Excel
- Execute: `python test_dashboard.py`

**Mapa vazio**
- Verifique nomes dos municípios
- Use nomes corretos do RN (Natal, Mossoró, etc.)

---

## 🎯 Próximos Passos

1. ✅ **Prepare seus dados** → Veja `GUIA_DADOS_REAIS.md`
2. ✅ **Teste com exemplo** → Execute `create_sample_data_dynamic.py`
3. ✅ **Abra dashboard** → Clique `run_dashboard.bat`
4. ✅ **Comece a explorar** → Use filtros!

---

## 📝 Changelog

### v1.0 - Versão Inicial
- ✨ Filtros dinâmicos automáticos
- ✨ Mapa interativo do RN
- ✨ Análises cruzadas dinâmicas
- ✨ Tabelas de dados
- ✨ Estatísticas resumidas

### Roadmap
- [ ] Exportar PDF/Excel
- [ ] Filtros numéricos avançados (range)
- [ ] Gráficos de série temporal
- [ ] Salvamento de filtros personalizados
- [ ] Integração banco de dados
- [ ] Dashboard mobile

---

## 📄 Documentação Adicional

| Documento | Descrição |
|-----------|-----------|
| [DASHBOARD_DINAMICO.md](DASHBOARD_DINAMICO.md) | Guia completo do sistema |
| [GUIA_DADOS_REAIS.md](GUIA_DADOS_REAIS.md) | Como adaptar seus dados |
| `GUIA_GEOBR.md` | Usar dados do GeoBR |
| `GUIA_RAPIDO.md` | Início rápido |

---

## 📧 Informações

- **Versão**: 1.0
- **Última Atualização**: 2026-03-22
- **Autor**: Sistema Dinâmico RN
- **Localização Padrão**: Natal, Rio Grande do Norte 🇧🇷

---

**Comece agora!** 🚀

Clique em `run_dashboard.bat` e explore seus dados geograficamente!
