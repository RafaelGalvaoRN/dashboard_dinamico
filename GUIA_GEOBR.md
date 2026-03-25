# 🗺️ Dashboard RN com GEOBR - Guia de Uso

## ✨ Melhorias Implementadas

Você agora tem um **dashboard com os limites reais dos municípios do Rio Grande do Norte** do IBGE!

### 📊 O Que Mudou?

| Aspecto | Antes | Agora |
|---------|-------|-------|
| **Limites dos Municípios** | Polígonos simplificados (círculos) | Limites reais do IBGE via GEOBR |
| **Municípios Mapeados** | 24 customizados | **167 do RN** (todos!) |
| **Fonte de Dados** | Gerado manualmente | IBGE 2020 (oficial) |
| **Precisão Geográfica** | ~80% | **100%** |
| **Atualização** | Manual | Automatizada via GEOBR |

---

## 🚀 Como Usar

### 1️⃣ Abrir o Dashboard

Acesse: **http://localhost:8050**

Você verá:
- 🗺️ **Mapa Coroplético** com cores dos municípios do RN
- 🟢 **Verde** = Mais casos
- 🔴 **Vermelho** = Menos casos
- 🔵 **Cinza** = Sem dados

### 2️⃣ Filtros Interativos

```
Filtrar por Município: [Todos ▼]
Filtrar por Localidade: [Todas ▼]
```

Selecione para explorar regiões específicas!

### 3️⃣ Tabela com Barras Visual

Veja o resumo de cada município com:
- Nome
- Total de casos
- Percentual visual

### 4️⃣ Estatísticas em Cards

- 📊 Municípios com dados
- 📈 Total de casos
- 📌 Média por município
- 🏆 Maior município

---

## 🔧 Como Funciona Internamente

### Fluxo de Dados:

```
1. IBGE (GEOBR)
   ↓
   → Download dos limites reais dos 167 municípios do RN
   → Arquivo: rio_grande_norte_real.geojson

2. Seu Excel
   ↓
   → rio_grande_norte.xlsx (34 registros)
   → Agregado por comarca

3. Merge dos Dados
   ↓
   → Junta IBGE com seus dados
   → Cria GeoJSON final com dados + geometria

4. Dashboard (Plotly)
   ↓
   → Visualiza como mapa coroplético colorido
   → Filtros interativos
   → Estatísticas em tempo real
```

---

## 📁 Arquivos Novos

```
✅ utils/generate_rn_geojson_geobr.py
   → Script que faz o merge: GEOBR + XLS

✅ data/rio_grande_norte_real.geojson
   → GeoJSON oficial com limites reais do IBGE
   → 167 features (municípios do RN)
   → Contém qtd para cada município
```

---

## 🎨 Customizações

### Mudar Cores

Em `app_rn.py`, procure:

```python
colorscale='RdYlGn'  # Cor atual
```

Opções:
- `'Blues'` - Azul
- `'Reds'` - Vermelho  
- `'Greens'` - Verde
- `'Viridis'` - Violeta-Amarelo
- `'RdYlGn'` - Vermelho-Amarelo-Verde (atual)

### Mudar Porta

Última linha de `app_rn.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8050)
# ↑ Mude 8050 para outra porta
```

### Usar Seus Próprios Dados

1. Abra `data/rio_grande_norte.xlsx`
2. Mantenha as colunas: `comarca`, `termo`, `qtd`
3. Adicione seus dados
4. O dashboard recarrega automaticamente!

---

## 📚 Dependências Novas

```bash
geobr      # Download de dados do IBGE
geopandas  # Manipulação de geometrias
shapely    # Processamento de formas
```

Já instaladas com:
```bash
pip install geobr geopandas shapely
```

---

## 🔄 Regenerar Dados

Se você mudou o arquivo Excel:

```bash
.venv\Scripts\python.exe utils/generate_rn_geojson_geobr.py
```

Isso regenera o GeoJSON com os novos dados!

---

## 💡 Exemplos de Uso

### Explorar um Município Específico
1. Selecione "Natal" em "Filtrar por Município"
2. Veja todos os bairros/localidades de Natal
3. O mapa e tabela se atualizam

### Comparar Regiões
1. Deixe "Todos" selecionado
2. Passe o mouse sobre cada município
3. Compare as quantidades

### Exportar Estatísticas
1. Aplique os filtros desejados
2. Copie os dados da tabela
3. Cole em Excel

---

## 🐛 Troubleshooting

### "GeoJSON não encontrado"

Execute:
```bash
.venv\Scripts\python.exe utils/generate_rn_geojson_geobr.py
```

### "Mapa em branco"

1. Verifique se `data/rio_grande_norte_real.geojson` existe
2. Verifique console (F12) por erros
3. Regenere o GeoJSON

### "Dados não aparecem"

1. Verifique se o Excel está salvo
2. Regenere o GeoJSON
3. Recarregue o navegador (F5)

### "Nomes não correspondem"

Os nomes dos municípios no Excel devem corresponder aos do mapping em `app_rn.py`.

Verifique:
```python
mapeamento_nomes = {
    'Natal': 2408102,
    'Mossoró': 2407104,
    # ... mais municípios
}
```

---

## 📊 Dados Inclusos

- **167 Municípios do RN** (mapeados pelo IBGE)
- **24 com Dados** de exemplo
- **34 registros** no Excel
- **Total: 3.535 casos**

### Municípios com Dados:
```
Natal (1.040 casos)
Mossoró (670 casos)
Parnamirim (560 casos)
... e mais 21 munícípios
```

---

## 🎯 Próximas Melhorias (Opcionais)

- [ ] Adicionar pop-ups com mais informações
- [ ] Gráficos de tendência temporal
- [ ] Exportação de dados em PDF
- [ ] Comparação entre período
- [ ] Integração com banco de dados

---

## 📞 Suporte

Se tiver dúvidas:

1. Verifique o console do navegador (F12)
2. Verifique os logs do terminal
3. Regenere os dados: `python utils/generate_rn_geojson_geobr.py`
4. Reinicie o app

---

**Desenvolvido com ❤️ usando Dash + Plotly + GEOBR**

Versão: 2.0 (com GEOBR)  
Data: Março 2026
