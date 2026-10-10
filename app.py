from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import glob

# Initialisation de l'application FastAPI
app = FastAPI(
    title="SmartCredit Cloud API",
    description="API de scoring du risque de crédit pour le PFE MLOps",
    version="1.0"
)

# Fonction pour charger automatiquement le dernier modèle XGBoost sauvegardé par MLflow
def load_latest_model():
    # Recherche du modèle dans le dossier des artefacts MLflow locaux
    model_paths = glob.glob("mlruns/*/artifacts/model/model.pkl")
    if not model_paths:
        # Fallback : si on sauvegarde un modèle directement en .pkl par la suite
        if os.path.exists("xgb_model.pkl"):
            return joblib.load("xgb_model.pkl")
        raise FileNotFoundError("Aucun modèle entraîné ou trouvé dans MLflow !")
    
    # Prend le plus récent
    latest_path = max(model_paths, key=os.path.getmtime)
    print(f"Modèle chargé depuis : {latest_path}")
    return joblib.load(latest_path)

# Chargement du modèle au démarrage de l'API
model = load_latest_model()

# Définition de la structure des données reçues pour une prédiction
class CreditRequest(BaseModel):
    age: float
    income: float
    loan_amount: float
    interest_rate: float
    loan_to_income_ratio: float
    home_ownership_OTHER: int
    home_ownership_OWN: int
    home_ownership_RENT: int
    loan_intent_EDUCATION: int
    loan_intent_HOMEIMPROVEMENT: int
    loan_intent_MEDICAL: int
    loan_intent_PERSONAL: int
    loan_intent_VENTURE: int
    age_category_Senior: int
    age_category_Young: int
    # Ajoute d'autres variables si ton encodage en a généré d'autres, 
    # ou on adaptera selon les colonnes exactes de ton dataset !

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API SmartCredit Cloud ! Le modèle est prêt."}

@app.post("/predict")
def predict_credit(data: CreditRequest):
    # Transformation des données reçues en DataFrame Pandas
    input_df = pd.DataFrame([data.dict()])
    
    # Prédiction avec le modèle XGBoost
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] # Probabilité de défaut (1)
    
    result = "Risque de Défaut (1)" if prediction == 1 else "Solvable / Pas de défaut (0)"
    
    return {
        "prediction_status": int(prediction),
        "result_text": result,
        "default_probability": round(float(probability), 4)
    }