# Utiliser une image officielle Python légère
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires (si besoin)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances s'il existe, ou installer directement
# (Tu peux lister tes dépendances ou copier requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code du projet, y compris l'API (app.py) et le modèle (xgb_model.pkl)
COPY . .

# Exposer le port sur lequel tourne FastAPI
EXPOSE 8000

# Commande pour lancer l'API avec Uvicorn au démarrage du conteneur
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]