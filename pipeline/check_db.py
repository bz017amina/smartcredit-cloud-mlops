import duckdb

# Connexion au fichier DuckDB généré par dlt
conn = duckdb.connect("smartcredit_pipeline.duckdb")

# 1. Afficher les tables présentes dans la base
print("--- Tables disponibles ---")
tables = conn.execute("SHOW TABLES;").fetchdf()
print(tables)

# 2. Afficher un aperçu des données de crédit chargées
print("\n--- Aperçu des 5 premières lignes ---")
query = "SELECT * FROM raw_credit_data.credit_applications LIMIT 5;"
df_preview = conn.execute(query).fetchdf()
print(df_preview)

conn.close()