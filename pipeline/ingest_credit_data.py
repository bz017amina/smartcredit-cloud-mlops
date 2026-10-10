import dlt
import pandas as pd
import os

@dlt.source
def credit_source():
    @dlt.resource(name="credit_applications", write_disposition="replace")
    def get_credit_data():
        # Chemin vers ton fichier CSV téléchargé
        csv_path = os.path.join("data", "credit_risk_dataset.csv")
        
        # Lecture du CSV avec Pandas par blocs ou en une seule fois
        df = pd.read_csv(csv_path)
        
        # Convertir le DataFrame en dictionnaires pour que dlt puisse l'ingérer
        yield df.to_dict(orient="records")
    return get_credit_data()

def run_pipeline():
    # 1. Initialiser le pipeline dlt
    pipeline = dlt.pipeline(
        pipeline_name="smartcredit_pipeline",
        destination="duckdb",
        dataset_name="raw_credit_data"
    )
    
    # 2. Exécuter le chargement des données vers DuckDB
    load_info = pipeline.run(credit_source())
    print("Résultat du chargement dlt :")
    print(load_info)

if __name__ == "__main__":
    run_pipeline()