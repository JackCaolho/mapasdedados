import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import os

# Caminho relativo para o arquivo CSV
caminho_arquivo = os.path.join('bases-dados', 'densidade_uf_tel_movel.csv')

df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin1')

# Normalizar desidade 0 a 1
densidade_maxima = df['densidade'].max()
df['densidade_normalizada'] = df['densidade'] / densidade_maxima

# Segredo de milhoes 
data_mes_ano = df.groupby(['ano', 'mes']) 

# Criar uma lista de dados para cada período de tempo
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
hm = HeatMapWithTime(data, index=formatted_dates, auto_play=True, min_opacity=0.1, max_opacity=1.4 , radius=60, gradient=gradiente_cores)

# Adicionar ao mapa
hm.add_to(m)

# Salvar o mapa
m.save(os.path.join('resultado-mapas', 'tel_deslig_tv.html'))