import folium
from folium.plugins import HeatMapWithTime

dados = [ [[-41.2545649, -72.7829354, 13],
    [-36.5986096, 144.6780052, 38],
    [-34.6396556, -58.7898326, 4],
    [-34.6037181, -58.38153, 5],
    [-33.6895237, -53.454704, 17],
    [-33.583333, -56.833333, 2],
    [-33.5198333, -53.3693967, 19],
    [-33.0458456, -71.6196749, 16],
    [-32.9593609, -60.6617024, 5],
    [-32.5662724, -53.3765705, 24],
    [-32.0260806, -53.3951333, 10],
    [-32.0145182, -52.0406082, 12],
    [-31.8695131, -54.1615593, 20],
    [-31.861921, -52.8219388, 9],
    [-31.8546304, -52.8151659, 7],
    [-31.7699736, -52.3410161, 35],
    [-31.766133, -52.5013148, 16]],
        
        [[-41.2545649, -72.7829354, 13],
    [-36.5986096, 144.6780052, 38],
    [-34.6396556, -58.7898326, 4],
    [-34.6037181, -58.38153, 5],
    [-33.6895237, -53.454704, 18],
    [-33.583333, -56.833333, 1],
    [-33.5198333, -53.3693967, 21],
    [-33.0458456, -71.6196749, 16],
    [-32.9593609, -60.6617024, 5],
    [-32.5662724, -53.3765705, 24],
    [-32.0260806, -53.3951333, 10],
    [-32.0145182, -52.0406082, 16],
    [-31.8695131, -54.1615593, 20],
    [-31.861921, -52.8219388, 9],
    [-31.8546304, -52.8151659, 8],
    [-31.7699736, -52.3410161, 33],
    [-31.766133, -52.5013148, 15]],
         
         [[-41.2545649, -72.7829354, 13],
    [-36.5986096, 144.6780052, 39],
    [-34.6396556, -58.7898326, 4],
    [-34.6037181, -58.38153, 5],
    [-33.6895237, -53.454704, 18],
    [-33.583333, -56.833333, 2],
    [-33.5198333, -53.3693967, 21],
    [-33.0458456, -71.6196749, 16],
    [-32.9593609, -60.6617024, 5],
    [-32.5662724, -53.3765705, 24],
    [-32.0260806, -53.3951333, 10],
    [-32.0145182, -52.0406082, 17],
    [-31.8695131, -54.1615593, 22],
    [-31.861921, -52.8219388, 9],
    [-31.8546304, -52.8151659, 8],
    [-31.7699736, -52.3410161, 35],
    [-31.766133, -52.5013148, 16]],
         
         [[-41.2545649, -72.7829354, 1],
    [-36.5986096, 144.6780052, 1],
    [-34.6396556, -58.7898326, 1],
    [-34.6037181, -58.38153, 1],
    [-33.6895237, -53.454704, 1],
    [-33.583333, -56.833333, 1],
    [-33.5198333, -53.3693967, 1],
    [-33.0458456, -71.6196749, 1],
    [-32.9593609, -60.6617024, 1],
    [-32.5662724, -53.3765705, 1],
    [-32.0260806, -53.3951333, 1],
    [-32.0145182, -52.0406082, 1],
    [-31.8695131, -54.1615593, 1],
    [-31.861921, -52.8219388, 1],
    [-31.8546304, -52.8151659, 1],
    [-31.7699736, -52.3410161, 1],
    [-31.766133, -52.5013148, 1],
    [-41.2545649, -72.7829354, 1],
    [-36.5986096, 144.6780052, 1],
    [-34.6396556, -58.7898326, 9],
    [-34.6037181, -58.38153, 5],
    [-33.6895237, -53.454704, 1],
    [-33.583333, -56.833333, 2]]]
         
        
anos = [1, 2, 3, 4]

mapa = folium.Map([-15.788497, -47.899873], zoom_start = 4, tiles = "cartodbpositron")

HeatMapWithTime(data = dados,
               index = anos,
               radius = 40,
               gradient = {0.1: "blue", 0.25: "green", 0.5: "yellow",
                          0.75: "orange", 1:"red"},
               min_opacity = 0.3,
               max_opacity = 1,
               use_local_extrema = True,
               auto_play = False,
               position = "topright").add_to(mapa)

caminho_do_arquivo = "C:\Projeto Gustavo\mapa.html"
mapa.save(caminho_do_arquivo)