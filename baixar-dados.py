import basedosdados as bd

# Para carregar o dado direto no pandas
df = bd.read_table(dataset_id='br_anatel_banda_larga_fixa',
table_id='backhaul',
billing_project_id="basedosdados-419800")

print("paozinho")