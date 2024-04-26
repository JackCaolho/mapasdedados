import pandas as pd
import os

# Caminho relativo para o arquivo CSV
caminho_arquivo = os.path.join('bases-dados', 'densidade-internet-cidades-brasil.csv')
caminho_arquivo2 = os.path.join('bases-dados', 'dicionario_cidades_lat_lon.xlsx')

# Lê o arquivo CSV com separador de vírgula
df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin1')
df2 = pd.read_excel(caminho_arquivo2)

print(df.columns)
print(df2.columns)

# Juntar os dataframes com base no 'id_municipio'
novo_df = pd.merge(df, df2[['id_municipio', 'Latitude', 'Longitude', 'Cidade']], on='id_municipio')

# Exibir a quantidade de linhas do novo dataframe
quantidade_linhas = len(novo_df)
print("Quantidade de linhas:", quantidade_linhas)

# Salvar o novo dataframe em um arquivo CSV
caminho_salvar = os.path.join('resultado-mapas', 'novo_df.csv')
novo_df.to_csv(caminho_salvar, index=False)

print("Dataframe salvo em:", caminho_salvar)
