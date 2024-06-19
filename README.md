<h1>Projeto de Visualização de Dados da ANATEL</h1>
<p>Este projeto é uma aplicação web interativa desenvolvida com Dash e Flask, que visa explorar e visualizar dados de acessos e portabilidade de telefonia fixa fornecidos pela ANATEL.</p>

<h3>Funcionalidades</h3>
<li>Visualização de Acessos Totais: Gráficos de barras mostrando os acessos por ano para diferentes tipos de outorgas.</li>
<li>Visualização de Acessos no Estado de SP: Gráficos de barras específicos para o estado de São Paulo.</li>
<li>Gráfico de Pizza: Distribuição de acessos por empresa em um determinado ano.</li>
<li>Heatmap de Portabilidade: Visualização das quantidades de portabilidades efetivadas entre diferentes empresas.</li>
<li>Gráfico de Linha: Saldo de portabilidades ao longo dos anos para cada empresa.</li>
<li>Links para Heatmaps: Acesso a heatmaps específicos para telefonia fixa e internet.</li>

<h3>Estrutura do Projeto</h3>
<li>app.py: Arquivo principal contendo o código da aplicação.</li>
<li>bases-nao-tratadas: Pasta contendo os arquivos CSV com os dados não tratados.</li>
<li>mapasdedados/resultado-mapas: Pasta contendo os arquivos HTML para visualização dos heatmaps.</li>


<h3>Clone este repositório:</h3>

    bash
    Copiar código
    git clone https://github.com/seu-usuario/seu-repositorio.git
    cd seu-repositorio
    Crie um ambiente virtual e instale as dependências:


    bash
    Copiar código
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    Execute a aplicação:


<h3>Estrutura dos Dados</h3>
<li>Telefonia fixa: Diversos arquivos CSV contendo informações sobre acessos de telefonia fixa, separados por autorizadas, concessionárias, e portabilidade.</li>
<li>Transformações: Os dados são lidos, filtrados e transformados conforme necessário para a visualização interativa.</li>

<h3>Exemplos de Visualizações</h3>
<li>Gráfico de Barras: Acessos de telefonia fixa por ano e tipo de outorga.</li>
<li>Gráfico de Pizza: Distribuição de acessos por empresa.</li>
<li>Heatmap de Portabilidade: Quantidade de portabilidades entre empresas.</li>
<li>Gráfico de Linha: Saldo de portabilidades ao longo dos anos.</li>

<h3>Requisitos</h3>
<li>Python 3.x</li>
<li>Bibliotecas: dash, dash-bootstrap-components, plotly, pandas, flask</li>
