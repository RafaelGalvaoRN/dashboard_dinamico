import pandas as pd

# Dados de exemplo com cidades reais de São Paulo
dados = {
    'comarca': [
        'São Paulo', 'São Paulo', 'São Paulo', 'Campinas', 'Campinas', 
        'Ribeirão Preto', 'Ribeirão Preto', 'Santos', 'Santos', 'Sorocaba',
        'Sorocaba', 'Guarulhos', 'Guarulhos', 'Osasco', 'Osasco',
        'Mogi Cruzes', 'Mogi Cruzes', 'Salto', 'Salto', 'Piracicaba'
    ],
    'termo': [
        'São Paulo', 'Tatuapé', 'Zona Leste', 'Campinas', 'Sumaré',
        'Ribeirão Preto', 'Araraquara', 'Santos', 'Praia Grande', 'Sorocaba',
        'Itu', 'Guarulhos', 'Arujá', 'Osasco', 'Carapicuíba',
        'Mogi Cruzes', 'Suzano', 'Salto', 'Itu', 'Piracicaba'
    ],
    'qtd': [
        450, 320, 280, 350, 290,
        410, 360, 380, 250, 320,
        400, 370, 210, 340, 260,
        300, 280, 175, 195, 390
    ]
}

df = pd.DataFrame(dados)
df.to_excel('data/exemplo.xlsx', index=False)
print(f"Arquivo criado com sucesso!")
print(f"\nDados da planilha:")
print(df)
