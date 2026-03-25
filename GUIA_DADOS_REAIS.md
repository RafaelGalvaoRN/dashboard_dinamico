# 📊 Guia de Adaptação de Dados Reais

## Como Usar Seus Dados no Dashboard Dinâmico

Este documento explica como converter seus dados reais sobre Proteção a Crianças e Adolescentes no RN para usar no dashboard.

## 1. Identificar Suas Colunas Disponíveis

### Dados Esperados Sobre Serviços de Proteção

Baseado nas suas perguntas, você provavelmente tem dados sobre:

#### Coluna de Localização (OBRIGATÓRIA)
```
município / comarca / localidade
Valores: Natal, Parnamirim, Mossoró, Caicó, etc.
```

#### Coluna de Proteção Integrada
```
proteção_integrada / termo_operacional / protocolo_integrado
Valores: Sim, Não, Implementado, Em Implementação, etc.
```

#### Coluna de Tipos de Acolhimento
```
tipo_acolhimento
Valores: Familiar, Institucional, Abrigo, Casa Lar, etc.
```

#### Coluna de Natureza do Serviço
```
natureza_do_servico
Valores: Público, Privado, Filantrópico, ONG, etc.
```

#### Coluna de Abrangência
```
abrangencia
Valores: Municipal, Regional, Estadual
```

#### Coluna de Comitê de Cuidados
```
tem_comite_cuidados / comite_rede
Valores: Sim, Não, Em Formação, etc.
```

#### Coluna de Protocolos
```
tem_protocolos_fluxos / protocolos_violencia
Valores: Sim, Não, Em Desenvolvimento, etc.
```

#### Colunas Numéricas (para Agregação)
```
quantidade_beneficiarios
numero_atendimentos
numero_instituicoes
capacidade_acolhimento
etc.
```

## 2. Estruturar seus Dados em Excel

### Exemplo de Estrutura Completa

| Comarca | Município | Tipo Serviço | Proteção Integrada | Tipo Acolhimento | Natureza | Abrangência | Comitê | Protocolos | Beneficiários |
|---------|-----------|--------------|-------------------|-----------------|----------|-------------|--------|-----------|---------------|
| Natal | Natal | Acolhimento | Sim | Familiar | Público | Municipal | Sim | Sim | 45 |
| Natal | Natal | Acolhimento | Sim | Institucional | Privado | Regional | Sim | Sim | 30 |
| Parnamirim | Parnamirim | Assistência | Não | - | Público | Municipal | Não | Não | 120 |
| Mossoró | Mossoró | Proteção Integrada | Sim | - | Público | Estadual | Sim | Sim | 80 |

### Passos para Preparar

1. **Abra seu Excel** com dados sobre serviços de proteção
2. **Adicione/Renomeie colunas** para corresponder aos nomes sugeridos:
   - Coluna de localização → renomear para `municipio`
   - Coluna de serviço → renomear para `tipo_servico`
   - Etc.

3. **Limpe os dados**:
   - Remova espaços em branco no início/fim
   - Valores Sim/Não devem ser uniformes (não misture "Sim" com "SIM")
   - Municípios devem estar com nomes corretos

4. **Preench e valores numéricos**:
   - Use 0 ao invés de deixar em branco
   - Garanta que não há texto em colunas numéricas

## 3. Responder às Suas Perguntas Específicas

### Pergunta 1: Em quantas Comarcas a Proteção Integrada já passou?
**Como usar o dashboard:**
1. Filtrar: `tipo_servico` = "Proteção Integrada" OU `proteção_integrada` = "Sim"
2. Contar não municípios mostrados no mapa
3. Agrupar por comarca para saber em quantas comarcas há implementação

**Dados necessários:**
- Coluna: `proteção_integrada` (Sim/Não)
- Coluna: `comarca` (para agrupar)
- Coluna: `municipio` (para localizar no mapa)

### Pergunta 2: Distribuição dos serviços de acolhimento por Comarcas
**Como usar o dashboard:**
1. Filtrar: `tipo_servico` = "Acolhimento"
2. Na seção "Análises Detalhadas", ver tabela: Municipio x Tipo Acolhimento
3. Agrupar por comarca para ter visão por comarca

**Dados necessários:**
- Coluna: `tipo_acolhimento` (Familiar, Institucional, etc.)
- Coluna: `natureza_do_servico` (Público, Privado, etc.)
- Coluna: `municipio` e `comarca`

3. Qual Acolhimentos e de que tipos estão em cada lugar

### Pergunta 3: Quais municípios dispõem de Comitê de Cuidados?
**Como usar o dashboard:**
1. Filtrar: `tem_comite_cuidados` = "Sim"
2. O mapa mostrará exatamente quais municípios têm comitê
3. Dados estatísticos mostrarão quantidade total

**Dados necessários:**
- Coluna: `tem_comite_cuidados` (Sim/Não)
- Coluna: `municipio`

## 4. Formato do Arquivo Final

### Arquivo Excel Ideal
- **Nome**: `dados_servicos_rn.xlsx`
- **Localização**: Pasta `data/`
- **Formato**: .xlsx (Excel 2007+)
- **Linhas**: Uma por registro (instituição, comarca, serviço, etc.)
- **Colunas**: Seguindo nomes sugeridos acima

### Exemplo de Arquivo Pronto
```
dados_servicos_rn.xlsx
├─ municipio (str)
├─ comarca (str)
├─ tipo_servico (str)
├─ tipo_acolhimento (str)
├─ natureza_do_servico (str)
├─ abrangencia (str)
├─ protecao_integrada (sim/não)
├─ tem_comite_cuidados (sim/não)
├─ tem_protocolos_violencia (sim/não)
├─ quantidade_beneficiarios (número)
└─ data_implementacao (data ou texto)
```

## 5. Importar Seus Dados

### Opção A: Copiar seus dados como estão
1. Prepare a estrutura conforme acima
2. Salve como `data/dados_servicos_rn.xlsx`
3. Execute `python run_dashboard_cli.py`
4. O sistema detectará automaticamente suas colunas

### Opção B: Script de Conversão (avançado)
Se seus dados têm estrutura diferente, crie um script Python:

```python
import pandas as pd

# Carregue seus dados
df_original = pd.read_excel('seus_dados_originais.xlsx')

# Renomeie as colunas
df_original = df_original.rename(columns={
    'Seu Nome de Coluna': 'municipio',
    'Outro Nome': 'tipo_servico',
    'Mais Um': 'tipo_acolhimento',
    # etc...
})

# Limpe os dados
df_original = df_original.str.strip()  # remove espaços
df_original = df_original.fillna('Sem Informação')  # preencha vazios

# Salve no formato esperado
df_original.to_excel('data/dados_servicos_rn.xlsx', index=False)
print("✓ Dados convertidos com sucesso!")
```

## 6. Validar os Dados

Execute o script de validação:

```bash
python test_dashboard.py
```

Deve ser produzido:
```
✓ Arquivo carregado: data/dados_servicos_rn.xlsx
  Shape: (XXX, Y)
  Colunas: municipio, tipo_servico, ...

✓ Colunas Categóricas: [lista de colunas]
✓ Colunas Numéricas: [lista de colunas]

✓ Testando filtros dinâmicos...
  - Registros após filtro: X/XXX

✓ Tudo funcionando! Iniciando servidor...
```

## 7. Usar no Dashboard

1. Clique no botão `run_dashboard.bat` ou execute:
   ```bash
   python run_dashboard_cli.py
   ```

2. O dashboard abrirá automaticamente em `http://localhost:8050`

3. Use os filtros que aparecem automaticamente para sua análise

4. Responda suas perguntas usando a visualização interativa!

## 8. Exemplos de Consultas Reais

### Consulta 1: Cobertura de Proteção Integrada
```
Filtro: proteção_integrada = "Sim"
Analise: Quantos municípios/comarcas têm Proteção Integrada?
Resposta: Mostrada no mapa e na estatística
```

### Consulta 2: Tipos de Acolhimento por Região
```
Filtro 1: tipo_servico = "Acolhimento"
Filtro 2: abrangencia = "Regional"
Analise: Tabela cruzada Municipio x Tipo Acolhimento
Resposta: Distribuição de tipos em cada localidade
```

### Consulta 3: Comitês Instituídos
```
Filtro: tem_comite_cuidados = "Sim"
Analise: Mapa de municípios com comitê
Resposta: Visualização de cobertura geográfica
```

### Consulta 4: Análise Combinada
```
Filtro 1: natureza_do_servico = "Público"
Filtro 2: tipo_acolhimento = "Familiar"
Analise: Onde estão os acolhimentos familiares públicos?
Resposta: Mapa e distribuição
```

## 9. Troubleshooting

### Problema: Filtros não aparecem
- **Verificar**: O arquivo tem as colunas esperadas?
- **Solução**: Renomeie as colunas conforme sugerido

### Problema: Mapa vazio
- **Verificar**: A coluna de município tem nomes corretos?
- **Solução**: Use nomes exatos dos municípios do RN

### Problema: Erros ao carregar
- **Verificar**: Arquivo está aberto em outro programa?
- **Solução**: Feche o Excel antes de rodar o dashboard

## 10. Dados de Teste

Se precisar de dados de teste para validar a estrutura, use:
```bash
python create_sample_data.py
```

Isso gerará um arquivo `dados_servicos_rn.xlsx` com dados fictícios mas realistas.

---

**Próximas etapas**: Após preparar os dados, execute o dashboard clicando em `run_dashboard.bat`!
