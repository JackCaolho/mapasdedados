from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os
from flask import Flask, send_from_directory

# Caminho dos arquivos
caminho_arquivo1 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Total.csv')
caminho_arquivo2 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Autorizadas.csv')
caminho_arquivo3 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias_2021-2022_Colunas.csv')
caminho_arquivo4 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias_2007_2020_Colunas.csv')

# Leitura dos arquivos
df1 = pd.read_csv(caminho_arquivo1, sep=';', encoding='utf-8')
df2 = pd.read_csv(caminho_arquivo2, sep=';', encoding='utf-8').query('UF == "SP"')
df3 = pd.read_csv(caminho_arquivo3, sep=';', encoding='utf-8')
df4 = pd.read_csv(caminho_arquivo4, sep=';', encoding='utf-8')

# Transformações no df3 e df4
df3_melted = df3.melt(
    id_vars=['Tipo de Outorga', 'CNPJ', 'Município', 'UF', 'Empresa', 'Porte da Prestadora', 'Tipo de Pessoa', 'Tipo do Acesso', 'Tipo de Atendimento', 'Código IBGE Município', 'Grupo Econômico'],
    var_name='Data',
    value_name='Acessos'
)
df3_melted[['Ano', 'Mês']] = df3_melted['Data'].str.split('-', expand=True)
df3_melted.drop(columns=['Data'], inplace=True)
df3_melted['Ano'] = df3_melted['Ano'].astype(int)
df3_melted['Mês'] = df3_melted['Mês'].astype(int)

df4_melted = df4.melt(
    id_vars=['Tipo de Outorga', 'CNPJ', 'Município', 'UF', 'Empresa', 'Porte da Prestadora', 'Tipo do Acesso', 'Código IBGE Município', 'Grupo Econômico'],
    var_name='Data',
    value_name='Acessos'
)
df4_melted[['Ano', 'Mês']] = df4_melted['Data'].str.split('-', expand=True)
df4_melted.drop(columns=['Data'], inplace=True)
df4_melted['Ano'] = df4_melted['Ano'].astype(int)
df4_melted['Mês'] = df4_melted['Mês'].astype(int)

df_conc = pd.concat([df3_melted, df4_melted], ignore_index=True)

# Agrupar e somar acessos em df2
df_agrupado = df2.groupby(['Ano', 'Mês', 'Tipo de Outorga']).agg({'Acessos': 'sum'}).reset_index().rename(columns={'Acessos': 'Total_Acessos'})

# Agrupar e somar acessos em df3_melted e df4_melted
df_agrupado2 = df_conc.groupby(['Ano', 'Mês', 'Tipo de Outorga']).agg({'Acessos': 'sum'}).reset_index().rename(columns={'Acessos': 'Total_Acessos'})

# Concatenar os dataframes
df_final = pd.concat([df_agrupado, df_agrupado2], ignore_index=True)

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

# Obter opções únicas
opcoes = list(df_final['Tipo de Outorga'].unique())
opcoes.append("Geral")

anos = sorted(df1['Ano'].unique())

# Layout do aplicativo
app.layout = html.Div(children=[
    html.H1(children='Dados ANATEL'),
    html.H2(children='Gráfico ao longo do tempo'),

    dcc.Dropdown(options=[{'label': opt, 'value': opt} for opt in opcoes], value='Geral', id='Tipo de Outorga'),

    dcc.Dropdown(options=[{'label': ano, 'value': ano} for ano in anos], value=anos[0], id='ano-dropdown'),

    dcc.Graph(id='Acessos_Telefonia_Fixa_Total'),

    dcc.Graph(id='Acessos_Telefonia_Fixa_SP'),

    dcc.Graph(id='pie-chart'),

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

# Callback para atualizar o gráfico Acessos_Telefonia_Fixa_Total
@app.callback(
    Output('Acessos_Telefonia_Fixa_Total', 'figure'),
    [Input('Tipo de Outorga', 'value')]
)
def update_total(value):
    if value == "Geral":
        fig = px.bar(df1, x="Ano", y="Acessos", barmode="group")
    else:
        tabela_filtrada = df1.loc[df1['Tipo de Outorga'] == value, :]
        fig = px.bar(tabela_filtrada, x="Ano", y="Acessos", color="Tipo de Outorga", barmode="group")
    return fig

# Callback para atualizar o gráfico Acessos_Telefonia_Fixa_SP
@app.callback(
    Output('Acessos_Telefonia_Fixa_SP', 'figure'),
    [Input('Tipo de Outorga', 'value')]
)
def update_sp(value1):
    if value1 == "Geral":
        fig2 = px.bar(df_final, x="Ano", y="Total_Acessos", barmode="group")
    else:
        tabela_filtrada = df_final.loc[df_final['Tipo de Outorga'] == value1, :]
        fig2 = px.bar(tabela_filtrada, x="Ano", y="Total_Acessos", color="Tipo de Outorga", barmode="group")
    return fig2

# Callback para atualizar o gráfico de pizza
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('ano-dropdown', 'value')]
)
def update_pie_chart(selected_year):
    # Filtrar o DataFrame pelo ano selecionado
    filtered_df = df2[df2['Ano'] == selected_year]

    # Criar o gráfico de pizza
    fig3 = px.pie(filtered_df, names='Empresa', values='Acessos', title=f'Distribuição de Acessos por Empresa em {selected_year}')
    
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)
