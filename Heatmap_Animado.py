import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os

# Caminho relativo para o arquivo CSV
caminho_arquivo = os.path.join('bases-dados', 'densidade-internet-cidades-brasil.csv')

df = pd.read_csv(caminho_arquivo, sep=';', encoding='latin1')

# Converter as colunas para os tipos corretos
df['Latitude'] = df['Latitude'].str.replace(',', '.').astype(float)
df['Longitude'] = df['Longitude'].str.replace(',', '.').astype(float)
df['densidade'] = df['densidade'].astype(float)

# Normalizar desidade 0 a 1
densidade_maxima = df['densidade'].max()
df['densidade_normalizada'] = df['densidade'] / densidade_maxima

# Segredo de milhoes 
data_mes_ano = df.groupby(['ano', 'mes']) 

# Apenas para printar
for name, group in data_mes_ano:
    print(name)
    print(group)
    print('-----------------')


# Criar uma lista de dados para cada período de tempo
data = []
for name, group in data_mes_ano:
    data.append(group[['Latitude', 'Longitude', 'densidade_normalizada']].values.tolist())

# Criar um mapa
m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)

# Gradiente de cores
gradiente_cores = {
    0.1: '#87CEEB',   # Azul céu
    0.2: '#6495ED',   # Azul claro
    0.3: '#4169E1',   # Azul médio
    0.5: '#FFFF00',   # Amarelo
    0.6: '#FFD700',   # Amarelo médio
    0.7: '#FFA500',   # Amarelo laranja
    0.8: '#FF8C00',   # Laranja
    0.9: '#FF6347',   # Vermelho laranja
    1.0: '#FF0000'    # Vermelho
}


# Criar o HeatMapWithTime
hm = HeatMapWithTime(data, index=list(data_mes_ano.groups.keys()), auto_play=True, max_opacity=0.8, radius=20, gradient=gradiente_cores)

# Adicionar ao mapa
hm.add_to(m)

# Salvar o mapa
m.save(os.path.join('resultado-mapas', 'sabado_animado4.html'))
