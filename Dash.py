from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os
from flask import Flask, send_from_directory

# Caminho do arquivo
caminho_arquivo1 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Total.csv')

df1 = pd.read_csv(caminho_arquivo1, sep=';', encoding='utf-8')

caminho_arquivo2 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Autorizadas.csv')

caminho_arquivo3 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias_2021-2022_Colunas.csv')


# Carregar o DataFrame
df2_sp_agrupado = pd.read_csv(caminho_arquivo2, sep=';', encoding='utf-8') \
                    .query('UF == "SP"') \
                    .groupby(['Ano', 'Mês']) \
                    .agg({'Acessos': 'sum'}) \
                    .reset_index() \
                    .rename(columns={'Acessos': 'Total_Acessos'})

df3 = pd.read_csv(caminho_arquivo3, sep=';', encoding='utf-8')

df3_melted = df3.melt(
    id_vars=['Tipo de Outorga', 'CNPJ', 'Município', 'UF', 'Empresa', 'Porte da Prestadora', 'Tipo de Pessoa','Tipo do Acesso' ,'Tipo de Atendimento', 'Código IBGE Município', 'Grupo Econômico' ],
    var_name='Data',
    value_name='Acessos'
)

# Dividir a coluna 'Data' em 'Ano' e 'Mês'
df3_melted[['Ano', 'Mês']] = df3_melted['Data'].str.split('-', expand=True)

# Remover a coluna 'Data'
df3_melted.drop(columns=['Data'], inplace=True)

print(df3_melted.head(3))


# Inicializar o servidor Flask
server = Flask(__name__)

# Servir o arquivo HTML
@server.route('/40028922')
def serve_html_40028922():
    return send_from_directory(
        directory='C:/Projeto Gustavo/GITHUB/mapasdedados/resultado-mapas',
        path='40028922.html'
    )

@server.route('/sabadoanimado')
def serve_html_sabadoanimado():
    return send_from_directory(
        directory='C:/Projeto Gustavo/GITHUB/mapasdedados/resultado-mapas',
        path='sabado_animado6.html'
    )

# Inicializar o aplicativo Dash
app = Dash(__name__, server=server)

# Criar a figura
fig1 = px.bar(df1, x="Ano", y="Acessos", barmode="group")

fig2 = px.bar(df2_sp_agrupado, x="Ano", y="Total_Acessos", barmode="group" )

# Obter opções únicas
opcoes = list(df1['Tipo de Outorga'].unique())
opcoes.append("Geral")

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dados ANATEL'),
    html.H2(children='Gráfico ao longo do tempo'),

    dcc.Dropdown(options=[{'label': opt, 'value': opt} for opt in opcoes], value='Geral', id='Tipo de Outorga'),

    dcc.Graph(
        id='Acessos_Telefonia_Fixa_Total',
        figure=fig1
    ),

    dcc.Graph(
        id='Acessos_Telefonia_Fixa_Autorizadas',
        figure=fig2
    ),

    html.Br(),

    # Botão que redireciona para outra página
    html.A(
        html.Button('Heatmap tel fixo', id='link-button-1'),
        href='/40028922',
        target='_blank'  # Abre em uma nova aba
    ),

    html.A(
        html.Button('Heatmap internet', id='link-button-2'),
        href='/sabadoanimado',
        target='_blank'  # Abre em uma nova aba
    )
])

# Callback para atualizar o gráfico
@app.callback(
    Output('Acessos_Telefonia_Fixa_Total', 'figure'),
    [Input('Tipo de Outorga', 'value')]
)
def update_output(value):
    if value == "Geral":
        fig = px.bar(df1, x="Ano", y="Acessos", barmode="group")
    else:
        tabela_filtrada = df1.loc[df1['Tipo de Outorga'] == value, :]
        fig = px.bar(tabela_filtrada, x="Ano", y="Acessos", color="Tipo de Outorga", barmode="group")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
