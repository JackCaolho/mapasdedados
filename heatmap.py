import pandas as pd
import folium
from folium.plugins import HeatMap
import os

print("Helwoldr")

# Caminho relativo para o arquivo CSV
caminho_arquivo = os.path.join('bases-dados', 'novo_df.csv')

# Lê o arquivo CSV
df = pd.read_csv(caminho_arquivo, sep=',', encoding='latin1')

min_densidade = df['densidade'].min()
max_densidade = df['densidade'].max()
df['densidade_normalizada'] = (df['densidade'] - min_densidade) / (max_densidade - min_densidade)

# Centro do mapa
mapa = folium.Map(location=[-9.047868, -70.526497], zoom_start=6)


# Criando o mapa
heat_data = [[row['Latitude'], row['Longitude'], row['densidade_normalizada']] for index, row in df.iterrows()]
HeatMap(heat_data, radius=10, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(mapa)


# Salvando resultado
mapa.save(os.path.join('resultado-mapas', 'heatmap_gerado1.html'))
print("mapinha na mao")