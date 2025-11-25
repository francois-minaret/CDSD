# 🚗 GetAround – API de Prédiction & Pipeline MLOps

Ce projet implémente un pipeline complet de Machine Learning autour de la prédiction des prix / durées pour la plateforme GetAround, incluant :

- une API de prédiction déployée avec **FastAPI**
- une interface utilisateur **Streamlit**
- un suivi des modèles avec **MLflow**
- un stockage des artefacts sur **AWS S3**
- un déploiement sur **Hugging Face Spaces**
- un entraînement local orchestré avec Python & scikit-learn / XGBoost

---

## 🧠 Objectif du projet

L’objectif est : 
 - effectuer une analyse des retards
 - effectuer une analyse des prix
 - estimer un prix de location
Le projet inclut toute la chaîne MLOps, du preprocessing à la mise en production via API.

---

## 🛠️ Technologies utilisées

- **Python** : Pandas, Scikit-learn, XGBoost, Plotly
- **FastAPI** : API de prédiction
- **Streamlit** : interface de démonstration
- **Docker** : containerisation complète du projet
- **MLflow** : suivi des expériences, versionning des modèles
- **AWS S3** : stockage des modèles et artefacts
- **Hugging Face Spaces** : déploiement de l’API et de l’UI

---

## Mlflow
Pour lancer : mlflow ui --host 127.0.0.1 --port 5000
Mlflow sera disponible sur l'adesse http://localhost:5000

## streamlit 
Pour lancer : streamlit run streamlit_app.py   
    pour un accès http://localhost:8501/
Sinon possibilité également de trouver sur https://huggingface.co/spaces/fminaret/getaround-HF

## API
Pour lancer : uvicorn app:app --reload --port 8000
    pour un accès http://localhost:8000/docs
sinon possibilité également sur https://fminaret-getaround-api.hf.space/docs

## Lien Github
https://github.com/francois-minaret/CDSD/tree/main/bloc5_Deploiement/GetAround

## 📬 Contact
Auteur : MINARET François
https://www.linkedin.com/in/minaret-fran%C3%A7ois-56106a105/