import  pandas as pd
import os

# Caminho relativo para o arquivo CSV
caminho_arquivo = os.path.join('bases-dados', 'densidade-internet-cidades-brasil.csv')

# Lê o arquivo CSV
df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')




