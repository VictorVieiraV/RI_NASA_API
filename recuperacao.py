import pandas as pd

# Substitua 'seu_arquivo.csv' pelo caminho completo do seu arquivo
file_path = "C:/Users/PC/Desktop/Dados_near_earth_objects/near_earth_objects_28_11_2023_22_43_54.csv"

# Ler o arquivo CSV para um DataFrame
df = pd.read_csv(file_path)

# Verificar os nomes das colunas
print(df.columns)

# Filtrar os objetos com Velocidade Relativa à Terra maior que 38966
resultados = df[(df['Velocidade Relativa à Terra em Km/h'] > 10000) & (df['Velocidade Relativa à Terra em Km/h'] < 38967)]
# resultados = df[(df['Data de Aproximação Mais Próxima'] > '2023-Jan-28')]

# Exibir os resultados (apenas as primeiras linhas para evitar resultados muito extensos)
print(resultados.head())
