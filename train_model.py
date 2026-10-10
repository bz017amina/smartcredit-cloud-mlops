import duckdb
import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Configuration de MLflow (enregistrement local)
mlflow.set_experiment("smartcredit_experiment")

print("1. Connexion à DuckDB et chargement des features (Marts)...")
con = duckdb.connect("smartcredit_pipeline.duckdb")
df = con.execute("SELECT * FROM fct_credit_features").df()
con.close()

print(f" Données chargées avec succès ! Dimensions : {df.shape}")

print("2. Préparation des données...")
df_encoded = pd.get_dummies(df, drop_first=True)
df_encoded = df_encoded.fillna(0)

X = df_encoded.drop(columns=['default_status'])
y = df_encoded['default_status']

# Découpage en Train (80%) et Test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Définition des 3 modèles
models = {
    "Logistic_Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random_Forest": RandomForestClassifier(
        n_estimators=100, 
        max_depth=10,          
        min_samples_split=10,  
        random_state=42
    ),
    "XGBoost": XGBClassifier(
        max_depth=5,
        learning_rate=0.1,
        eval_metric='logloss', 
        random_state=42
    )
}

print("\n3. Entraînement, Évaluation et Suivi MLflow des 3 Modèles :")
print("-" * 60)

for name, model in models.items():
    with mlflow.start_run(run_name=name):
        print(f"\n--- Entraînement de : {name} ---")
        model.fit(X_train, y_train)
        
        # Prédictions et Scores
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)
        
        train_acc = accuracy_score(y_train, train_pred)
        test_acc = accuracy_score(y_test, test_pred)
        
        print(f"-> Accuracy Train : {train_acc:.4f}")
        print(f"-> Accuracy Test  : {test_acc:.4f}")
        
        # Logging MLflow
        mlflow.log_param("model_name", name)
        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)
        
        mlflow.sklearn.log_model(
            model, 
            "model", 
            skops_trusted_types=[
                "sklearn.tree._tree.Tree", 
                "xgboost.core.Booster", 
                "xgboost.sklearn.XGBClassifier"
            ]
        )
        
        # Si c'est XGBoost (le meilleur), on le sauvegarde aussi en .pkl pour l'API
        if name == "XGBoost":
            joblib.dump(model, "xgb_model.pkl")
            print(" -> Modèle XGBoost sauvegardé avec succès dans 'xgb_model.pkl' !")

print("\n Tous les modèles ont été entraînés et tracés dans MLflow avec succès !")