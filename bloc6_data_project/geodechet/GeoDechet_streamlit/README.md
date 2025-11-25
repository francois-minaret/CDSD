---
title: Geodechet
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
- streamlit
- data-visualization
- machine-learning
- environment
pinned: false
short_description: Estimation des dechets par departement
license: apache-2.0
---

# ♻️ Geodechet

Bienvenue sur l’application **Geodechet**, un outil interactif developpe avec **Streamlit** permettant de :

- Visualiser les tonnages de dechets par departement et par typologie
- Predire les volumes attendus via des modèles statistiques (regression lineaire OLS)
- Comparer les departements selon differents critères environnementaux

Cette application s’appuie sur des modèles sauvegardes et des donnees historiques nettoyees. Le projet a ete conçu dans un cadre pedagogique.

---

## 🔍 Comment utiliser l'application

1. Selectionnez un departement dans la barre laterale
2. Laissez l’application charger les modèles associes
3. Visualisez les graphiques et les predictions affiches
4. Changez de departement pour obtenir une nouvelle prediction

---

## 📦 Technologies utilisees

- Python
- Streamlit
- Statsmodels
- Pandas
- Docker

---

## 📄 Licence

Ce projet est sous licence Apache 2.0.