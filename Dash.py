from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import os
from flask import Flask, send_from_directory

# Caminho dos arquivos
caminho_arquivo1 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Total.csv')
caminho_arquivo2 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Autorizadas.csv')
caminho_arquivo2c = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias.csv')
caminho_arquivo3 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias_2021-2022_Colunas.csv')
caminho_arquivo4 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'Acessos_Telefonia_Fixa_Concessionarias_2007_2020_Colunas.csv')
caminho_arquivo5 = os.path.join('bases-nao-tratadas', 'Telefonia fixa', 'CSV_PORTABILIDADE.csv')

# Leitura dos arquivos
df1 = pd.read_csv(caminho_arquivo1, sep=';', encoding='utf-8')
df2 = pd.read_csv(caminho_arquivo2, sep=';', encoding='utf-8').query('UF == "SP"')
df2_con = pd.read_csv(caminho_arquivo2c, sep=';',low_memory=False , encoding='utf-8').query('UF == "SP"')
df3 = pd.read_csv(caminho_arquivo3, sep=';', encoding='utf-8').query('UF == "SP"')
df4 = pd.read_csv(caminho_arquivo4, sep=';', encoding='utf-8').query('UF == "SP"')
df5 = pd.read_csv(caminho_arquivo5, sep=';', encoding='utf-8').query('SG_UF == "SP"')

# Abreviar nome de empresas para 2 palavras
def abreviar(s):
    palavras = s.split()
    return ' '.join(palavras[:2])

df2['Empresa'] = df2['Empresa'].apply(abreviar)
df2_con['Empresa'] = df2_con['Empresa'].apply(abreviar)
df3['Empresa'] = df3['Empresa'].apply(abreviar)
df4['Empresa'] = df4['Empresa'].apply(abreviar)
df5['NO_PRESTADORA_RECEPTORA'] = df5['NO_PRESTADORA_RECEPTORA'].apply(abreviar)
df5['NO_PRESTADORA_DOADORA'] = df5['NO_PRESTADORA_DOADORA'].apply(abreviar)

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

# juntando dps do melted
df_conc = pd.concat([df3_melted, df4_melted], ignore_index=True)

# Somando os acessos antes de juntar o df2
df_agrupado = df2.groupby(['Ano', 'Mês', 'Tipo de Outorga']).agg({'Acessos': 'sum'}).reset_index().rename(columns={'Acessos': 'Total_Acessos'})

# Juntando o df2 com df2_con 
df2 = pd.concat([df2, df2_con], ignore_index=True)

# Preencher as colunas vazias
df2['Tipo de Pessoa'] = df2['Tipo de Pessoa'].fillna('Desconhecido')


# Somando os acessos
df_agrupado2 = df_conc.groupby(['Ano', 'Mês', 'Tipo de Outorga']).agg({'Acessos': 'sum'}).reset_index().rename(columns={'Acessos': 'Total_Acessos'})

df_agrupado3 = df2.groupby(['Ano', 'Mês', 'Empresa','Tipo de Outorga', 'Tipo de Pessoa']).agg({'Acessos': 'sum'}).reset_index().rename(columns={'Acessos': 'Total_Acessos_Empresa'})

# Concatenar os dataframes
df_final = pd.concat([df_agrupado, df_agrupado2], ignore_index=True)

# Função para agrupar empresas menores e agrupar em "OUTROS" por ano
def agrupar_empresas_por_ano(df, top_n=9):
    df_t10 = pd.DataFrame()
    for ano in df['Ano'].unique():
        df_ano = df[df['Ano'] == ano]
        total_por_empresa = df_ano.groupby('Empresa')['Total_Acessos_Empresa'].sum().sort_values(ascending=False)
        top_empresas = total_por_empresa.head(top_n).index
        df_ano.loc[~df_ano['Empresa'].isin(top_empresas), 'Empresa'] = 'OUTROS'
        df_ano = df_ano.groupby(['Ano', 'Mês', 'Empresa', 'Tipo de Pessoa']).agg({'Total_Acessos_Empresa': 'sum'}).reset_index()
        df_t10 = pd.concat([df_t10, df_ano], ignore_index=True)
    return df_t10

# Mesma função mas usado em outro df
def agrupar_portabilidade_por_ano(df_p, top_n=13):
    df_p10 = pd.DataFrame()
    for ano in df_p['Ano'].unique():
        df_ano = df_p[df_p['Ano'] == ano]

        # Agrupar NO_PRESTADORA_RECEPTORA
        total_port_receptora = df_ano.groupby('NO_PRESTADORA_RECEPTORA')['QT_PORTABILIDADE_EFETIVADA'].sum().sort_values(ascending=False)
        top_port_receptora = total_port_receptora.head(top_n).index
        df_ano.loc[~df_ano['NO_PRESTADORA_RECEPTORA'].isin(top_port_receptora), 'NO_PRESTADORA_RECEPTORA'] = 'OUTROS'

        # Agrupar NO_PRESTADORA_DOADORA
        total_port_doadora = df_ano.groupby('NO_PRESTADORA_DOADORA')['QT_PORTABILIDADE_EFETIVADA'].sum().sort_values(ascending=False)
        top_port_doadora = total_port_doadora.head(top_n).index
        df_ano.loc[~df_ano['NO_PRESTADORA_DOADORA'].isin(top_port_doadora), 'NO_PRESTADORA_DOADORA'] = 'OUTROS'

        df_ano = df_ano.groupby(['Ano', 'Mês', 'NO_PRESTADORA_DOADORA', 'NO_PRESTADORA_RECEPTORA']).agg({'QT_PORTABILIDADE_EFETIVADA': 'sum'}).reset_index()
        df_p10 = pd.concat([df_p10, df_ano], ignore_index=True)
    return df_p10

# Mesma função mas sem filtrar por ano
def agrupar_portabilidade_total(df_t, top_n=9):
    df_t = df_t.copy()

    # Agrupar NO_PRESTADORA_RECEPTORA
    total_port_receptora = df_t.groupby('NO_PRESTADORA_RECEPTORA')['QT_PORTABILIDADE_EFETIVADA'].sum().sort_values(ascending=False)
    top_port_receptora = total_port_receptora.head(top_n).index
    df_t.loc[~df_t['NO_PRESTADORA_RECEPTORA'].isin(top_port_receptora), 'NO_PRESTADORA_RECEPTORA'] = 'OUTROS'

    # Agrupar NO_PRESTADORA_DOADORA
    total_port_doadora = df_t.groupby('NO_PRESTADORA_DOADORA')['QT_PORTABILIDADE_EFETIVADA'].sum().sort_values(ascending=False)
    top_port_doadora = total_port_doadora.head(top_n).index
    df_t.loc[~df_t['NO_PRESTADORA_DOADORA'].isin(top_port_doadora), 'NO_PRESTADORA_DOADORA'] = 'OUTROS'

    df_t = df_t.groupby(['Ano', 'Mês', 'NO_PRESTADORA_DOADORA', 'NO_PRESTADORA_RECEPTORA']).agg({'QT_PORTABILIDADE_EFETIVADA': 'sum'}).reset_index()
    
    return df_t

# Utilizando a função
df6 = agrupar_portabilidade_total(df5)

df_agrupado3 = agrupar_empresas_por_ano(df_agrupado3)

df5 = agrupar_portabilidade_por_ano(df5)

# Inicializar o servidor Flask
server = Flask(__name__)

# Caminho dos HeatMap
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
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Obter opções únicas
opcoes = list(df_final['Tipo de Outorga'].unique())
opcoes.append("Geral")

anos = sorted(df_agrupado3['Ano'].unique())
anos.insert(0, "Geral")

tipos_pessoa = list(df_agrupado3['Tipo de Pessoa'].unique())
tipos_pessoa.append("Geral")

# Layout do aplicativo
app.layout = dbc.Container(children=[
    dbc.Row(
        dbc.Col(html.H1("Dados ANATEL"), className="text-center my-4")
    ),
    dbc.Row(
        dbc.Col(html.H2("Estudo de acessos e portabilidade"), className="text-center mb-4")
    ),
    dbc.Row([
        dbc.Col(dcc.Dropdown(options=[{'label': opt, 'value': opt} for opt in opcoes], value='Geral', id='tipo-de-outorga-dropdown'), width=4),
        dbc.Col(dcc.Dropdown(options=[{'label': ano, 'value': ano} for ano in anos], value='Geral', id='ano-dropdown'), width=4),
        dbc.Col(dcc.Dropdown(options=[{'label': tipo, 'value': tipo} for tipo in tipos_pessoa], value='Geral', id='tipo-pessoa-dropdown'), width=4)
    ], className="mb-4"),
    dbc.Row(
        dbc.Col(dcc.Checklist(
            id='empresa-checklist',
            options=[
                {'label': 'Excluir as maiores', 'value': 'exclude'}
            ],
            value=[],
            inline=True
        ), className="text-center mb-4")
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='Acessos_Telefonia_Fixa_Total'), className="mb-4")
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='Acessos_Telefonia_Fixa_SP'), className="mb-4")
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='pie-chart'), className="mb-4")
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='network-graph'), className="mb-4")
    ),
    dbc.Row(
        dbc.Col(dcc.Graph(id='line-chart'), className="mb-4")
    ),
    dbc.Row(
        dbc.Col([
            html.A(
                html.Button('Heatmap tel fixo', id='link-button-1', className="btn btn-primary mr-2"),
                href='/40028922',
                target='_blank'  # Abre em uma nova aba
            ),
            html.A(
                html.Button('Heatmap internet', id='link-button-2', className="btn btn-primary"),
                href='/sabadoanimado',
                target='_blank'  # Abre em uma nova aba
            )
        ], className="text-center mb-4")
    )
])

# Callback para atualizar o gráfico Acessos_Telefonia_Fixa_Total
@app.callback(
    Output('Acessos_Telefonia_Fixa_Total', 'figure'),
    [Input('tipo-de-outorga-dropdown', 'value')]
)
def update_total(value):
    if value == "Geral":
        # Tipo de gráfico
        fig = px.bar(df1, x="Ano", y="Acessos", barmode="group")
    else:
        tabela_filtrada = df1.loc[df1['Tipo de Outorga'] == value, :]
        fig = px.bar(tabela_filtrada, x="Ano", y="Acessos", color="Tipo de Outorga", barmode="group")
    
    
    fig.update_layout(title='Acessos por Ano')
    
    return fig

# Callback para atualizar o gráfico Acessos_Telefonia_Fixa_SP
@app.callback(
    Output('Acessos_Telefonia_Fixa_SP', 'figure'),
    [Input('tipo-de-outorga-dropdown', 'value')]
)
def update_sp(value1):
    if value1 == "Geral":
        #Tipo de gráfico
        fig2 = px.bar(df_final, x="Ano", y="Total_Acessos", barmode="group")
    else:
        tabela_filtrada = df_final.loc[df_final['Tipo de Outorga'] == value1, :]
        fig2 = px.bar(tabela_filtrada, x="Ano", y="Total_Acessos", color="Tipo de Outorga", barmode="group")

    fig2.update_layout(title='Acessos por Ano SP')
    
    return fig2

# Callback para atualizar o gráfico de pizza
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('ano-dropdown', 'value'), Input('tipo-pessoa-dropdown', 'value')]
)
def update_pie_chart(selected_year, selected_tipo_pessoa):
    filtrado_df = df_agrupado3.copy()

    if selected_year != "Geral":
        filtrado_df = filtrado_df[filtrado_df['Ano'] == selected_year]
    
    if selected_tipo_pessoa != "Geral":
        filtrado_df = filtrado_df[filtrado_df['Tipo de Pessoa'] == selected_tipo_pessoa]

    # Tipo de gráfico
    fig3 = px.pie(filtrado_df, names='Empresa', values='Total_Acessos_Empresa', title=f'Distribuição de Acessos por Empresa em {selected_year}')
    
    return fig3

# Callback para atualizar o heatmap de correlação
@app.callback(
    Output('network-graph', 'figure'),
    [Input('ano-dropdown', 'value'), Input('empresa-checklist', 'value')]
)
def update_heatmap(selected_year, empresa_checklist):
    filtrado_df5 = df5.copy()

    if selected_year != "Geral":
        filtrado_df5 = filtrado_df5[filtrado_df5['Ano'] == selected_year]

    if 'exclude' in empresa_checklist:
        filtrado_df5 = filtrado_df5[~filtrado_df5['NO_PRESTADORA_RECEPTORA'].isin(['TELEFONICA BRASIL', 'CLARO', 'OI S.A.', 'TIM S.A.'])]

    # Cria a tabela dinâmica (pivot table) com a soma das portabilidades
    pivot_table = filtrado_df5.pivot_table(values='QT_PORTABILIDADE_EFETIVADA', 
                                           index='NO_PRESTADORA_DOADORA', 
                                           columns='NO_PRESTADORA_RECEPTORA', 
                                           aggfunc='sum', fill_value=0)

    # Cria o heatmap
    fig4 = go.Figure(data=go.Heatmap(z=pivot_table.values,
                                     x=pivot_table.columns,
                                     y=pivot_table.index,
                                     colorscale='Viridis')) 

    # Adiciona interatividade ao gráfico e ajusta o tamanho
    fig4.update_layout(
        title="Quantidade de Portabilidades Efetivadas",
        xaxis=dict(title="Receptora", tickangle=45, tickfont=dict(size=10)),
        yaxis=dict(title="Doadora", tickfont=dict(size=10)),
        plot_bgcolor='white',
        autosize=False,
        width=1200,  # Ajusta a largura 
        height=1000  # Ajusta a altura
    )

    return fig4

# Callback para atualizar o gráfico de linha
@app.callback(
    Output('line-chart', 'figure'),
    [Input('ano-dropdown', 'value')]
)
def update_line_chart(selected_year):
    filtrado_df6 = df6.copy()

    # Calcular o saldo (NO_PRESTADORA_RECEPTORA - NO_PRESTADORA_DOADORA)
    agrupado = filtrado_df6.groupby(['Ano', 'NO_PRESTADORA_RECEPTORA']).agg(
        Total_Receptora=('QT_PORTABILIDADE_EFETIVADA', 'sum')).reset_index()

    agrupado2 = filtrado_df6.groupby(['Ano', 'NO_PRESTADORA_DOADORA']).agg(
        Total_Doadora=('QT_PORTABILIDADE_EFETIVADA', 'sum')).reset_index()

    combinado = pd.merge(agrupado, agrupado2, left_on=['Ano', 'NO_PRESTADORA_RECEPTORA'], right_on=['Ano', 'NO_PRESTADORA_DOADORA'], how='outer')
    combinado = combinado.fillna(0)
    combinado['Saldo'] = combinado['Total_Receptora'] -combinado['Total_Doadora']

    fig5 = px.line(combinado, x='Ano', y='Saldo', color='NO_PRESTADORA_RECEPTORA', title='Saldo de Portabilidades ao Longo dos Anos')
    
    return fig5


if __name__ == '__main__':  
    app.run_server(debug=True)
