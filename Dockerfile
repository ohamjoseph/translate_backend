# Étape 1 : Utiliser une image officielle légère avec Python
FROM python:3.12-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires
COPY requirements.txt .

# Étape 4 : Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Étape 5 : Copier le reste de l'application
COPY . .

# Étape 6 : Exposer le port utilisé par Uvicorn
EXPOSE 8000

# Étape 7 : Commande pour démarrer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
