import basedosdados as bd
import pandas as pd

# Carregar os dados
df = bd.read_table(dataset_id='br_anatel_telefonia_movel',
                   table_id='densidade_uf',
                   billing_project_id="projetooscar")  

# Salvar os dados em um arquivo CSV
df.to_csv('densidade_uf.csv', index=False)

print('Arquivo CSV criado com sucesso!')

