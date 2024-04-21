import pandas as pd

# Carregar o arquivo CSV
dados = pd.read_csv("C:/Users/gusta/OneDrive/Documentos/GitHub/mapasdedados/bases-nao-tratadas/arrecadacao-estado.csv", delimiter=';', encoding='latin1')

# Função para classificar os impostos por categoria
def classificar_categoria(nome_imposto):
    if "IMPORTAÇÃO" in nome_imposto or "EXPORTAÇÃO" in nome_imposto:
        return "Impostos sobre Importação/Exportação"
    elif "IPI" in nome_imposto:
        return "Impostos sobre Produção e Venda"
    elif "IR" in nome_imposto:
        return "Impostos de Renda"
    elif "COFINS" in nome_imposto or "PIS" in nome_imposto or "CSLL" in nome_imposto or "SEG. SOC." in nome_imposto:
        return "Contribuições Sociais"
    else:
        return "Outras Contribuições e Taxas"

# Selecionar apenas as colunas que representam os impostos
colunas_impostos = [coluna for coluna in dados.columns if dados[coluna].dtype == 'int64']

# Aplicar a função para classificar os impostos e criar uma nova coluna 'Categoria de Imposto'
dados['Categoria de Imposto'] = dados[colunas_impostos].apply(lambda col: classificar_categoria(col.name), axis=1)

# Mostrar os dados com a nova coluna
print(dados)
