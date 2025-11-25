# 🚕 Projet Uber – Analyse Exploratoire & Modélisation Spatio-Temporelle

Ce projet propose une analyse approfondie des données de trajets Uber à New York.
Il combine exploration des données, visualisations avancées, analyses temporelles, analyses géographiques, ainsi qu’un clustering (KMeans / DBSCAN) pour identifier des zones d’activité.

L’ensemble de l’étude est structuré autour de plusieurs notebooks Jupyter pour permettre une lecture progressive du pipeline d’analyse.

## 🧠 Objectifs du projet

L’objectif du projet Uber est de :

- analyser les tendances temporelles des pickups
- étudier la répartition spatiale des trajets
- identifier les zones chaudes (hotspots) via des méthodes de clustering
- comprendre les variations selon les jours / heures / mois
- proposer une segmentation des zones d’activité Uber

Les notebooks permettent de naviguer chronologiquement du nettoyage des données à la modélisation.

## 📂 Structure du projet
📁 Projet Uber
│
├── 01-Uber_Pickups.ipynb
├── projet_uber_EDA.ipynb
├── projet_uber_jour.ipynb
├── projet_uber_jour_cplt.ipynb
├── projet_uber_jeudi_17.ipynb
└── README.md   ← (ce fichier)

## 📘 Description des notebooks
Les données correpsondent aux mois d'avril à septembre 2014

projet_uber_EDA.ipynb
Analyse exploratoire complète : distributions, cartes, tendances temporelles.

projet_uber_jeudi_17.ipynb
Analyse détaillée de l'heure avec le plus de trajets : le jeudi à 17h.

projet_uber_jour.ipynb
Études par jour de la semaine
- lundi matin
- dimanche matin
- jeudi après-midi

heatmaps temporelles

projet_uber_jour_cplt.ipynb
Version complète de la semaine heure par heure : ajout de graphes, analyses comparatives et approfondies.


## 🛠️ Technologies utilisées

- **Python** : Pandas, Numpy
- **Matplotlib / Seaborn / Plotly Express** : visualisation cartographique
- **Scikit Learn (KMeans, DBSCAN, silhouette score, coude)** : Calcul des clusters
- **Folium / Scatter Mapbox** : Visualisations géographiques interactives


## 🔍 Analyses réalisées
1. Exploration temporelle

variations journalières / hebdomadaires / mensuelles
- détection de pics horaires
- heatmaps temporelles

2. Exploration spatiale
- nuages de points géolocalisés
- cartes Plotly Mapbox
- zones d’activité principales

3. Clustering
KMeans
- recherche du meilleur k via inertie + silhouette
- clustering par heure

DBSCAN
- identification automatique des densités
- calcul des centroïdes

4. Interprétations
- zones les plus actives
- relation entre heure / zone / densité
- analyse des variations entre les jours

## Lien Github
https://github.com/francois-minaret/CDSD/tree/main/bloc3_machine_learning/Uber

## 📬 Contact
Auteur : MINARET François
https://www.linkedin.com/in/minaret-fran%C3%A7ois-56106a105/

