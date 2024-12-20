import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os

# Caminho para o arquivo
caminho_arquivo = os.path.join('bases-dados', 'novo_df_internet.csv')

df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin1')

df = df[(df['Latitude'] <= 6) & (df['Longitude'] >= -74) & (df['Longitude'] <= -20) & (df['densidade'] <= 100)]


# Segredo de milhoes 
data_mes_ano = df.groupby(['ano', 'mes']) 

# Criar uma lista de dados para cada período de tempo
densidade_maxima = 100
df['densidade_normalizada'] = df['densidade'] / densidade_maxima

data = []
for name, group in data_mes_ano:
    data.append(group[['Latitude', 'Longitude', 'densidade_normalizada']].values.tolist())

# Criar um mapa
m = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)

# Gradiente de cores
gradiente_cores = {
    0.1: '#ADD8E6',   # Azul céu
    0.2: '#87CEEB',   # Azul claro
    0.3: '#7B68EE',   # Azul médio
    0.5: '#FFFF00',   # Amarelo
    0.6: '#FFD700',   # Amarelo médio
    0.7: '#FFA500',   # Amarelo laranja
    0.8: '#FF8C00',   # Laranja
    0.9: '#FF6347',   # Vermelho laranja
    1.0: '#FF0000'    # Vermelho
}


# Criar uma lista de strings formatadas para representar cada período de tempo no formato "Ano - Mês"
formatted_dates = ['{} - {}'.format(year, month_name) for year, month_name in data_mes_ano.groups.keys()]

# Criar o HeatMapWithTime
hm = HeatMapWithTime(data, index=formatted_dates, auto_play=True, min_opacity=0.1, max_opacity=1 , radius=10, gradient=gradiente_cores)

# Adicionar ao mapa
hm.add_to(m)

# Salvar o mapa
m.save(os.path.join('resultado-mapas', 'sabado_animado6.html'))