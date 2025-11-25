# ✈️ Kayak – Application de Recommandation de Destinations & Pipeline Data

Ce projet implémente un pipeline complet permettant de recommander les meilleures destinations de voyage en France, grâce à :

- la récupération de données météo (OpenWeatherMap)
- la géolocalisation automatique (Nominatim)
- le scraping d’hôtels Booking.com (Scrapy + Playwright)
- la fusion et le nettoyage des données
- l’enregistrement du dataset final dans un Data Lake AWS S3
- la création d’un Data Warehouse PostgreSQL sur NEON
- la génération de cartes interactives avec Plotly

## 🧠 Objectif du projet

L’objectif est de construire une solution capable de :

- identifier les villes ayant la meilleure météo sur les 7 prochains jours
- récupérer les 20 meilleurs hôtels autour de chaque destination
- fusionner toutes les données en un dataset exploitable
- charger le dataset nettoyé dans une base PostgreSQL sur Neon
- générer :
    - une carte Top-5 destinations
    - une carte Top-20 hôtels

Ce projet utilise Neon. Il sert ici de base SQL centralisée et scalable, remplaçant les solutions plus lourdes comme AWS RDS.

## 🛠️ Technologies utilisées

- **Python** : Pandas, Requests, JSON
- **Scrapy + Playwright** : scraping dynamique Booking.com
- **Plotly** : visualisation cartographique

APIs :
- Nominatim (géolocalisation)
- OpenWeatherMap – One Call (prévisions météo)
- AWS S3 : Data Lake (fichiers bruts + enrichis)
- Neon PostgreSQL : Data Warehouse serverless
- Jupyter Notebook : analyse & transformation

## 🌦️ Pipeline météo (projet_kayak_01.ipynb)
Étapes :

1/ Liste des 35 villes françaises du scope.
   Récupération des coordonnées GPS via Nominatim.
   Appel à OpenWeatherMap One Call API.
   Calcul d’un score météo sur 7 jours basé sur :
   pluie (rain)
   probabilité de précipitations (pop)
   température
   humidité

Création des fichier 
 - meteos.csv
 - condition.csv
 - hotels.csv
 - villes.csv


## 🏨 Scraping des hôtels Booking.com (booking_lat_lon.py)

Le scraping multi-villes utilise :
- Scrapy
- Playwright (headless)
- scroll automatique → chargement dynamique des hôtels
- maximum 20 hôtels par ville

Chaque fiche d’hôtel contient :
- nom
- url Booking
- latitude / longitude
- rating utilisateur
- prix du séjour
- description textuelle
- ville_id

📁 Les fichiers sont sauvegardés ville par ville dans :
booking_results/results_<ville>.json
(ex : results_paris.json)


## 🔄 Fusion & préparation des données (projet_kayak_02.ipynb)

- envoi des fichiers sur AWS S3 (meteos.csv, villes.csv, hotels.csv, condition.csv)
- Création des tables sur Neon en fonction des fichiers présents sur AWS S3

Ce Data Lake (AWS S3) sert de stockage centralisé pour l’équipe Marketing & Data.

Neon est utilisé comme Data Warehouse serverless, permettant :

- le chargement direct du dataset final
- l’accès SQL unique pour analyses futures
- un environnement PostgreSQL auto-scalable
- une administration minimale (pas de VM, pas de maintenance)

Tables importées dans Neon :
- villes (ville_id, nom, longitude, latitude)
- meteos (ville_id, date, condition, temperature, duree_ensoleillement, pluie, vent)
- hotels (ville, name, description, url, rating, latitude, longitude, prix, ville_id)
- condition (description, code)


## 🌍 Visualisations (projet_kayak_03.ipynb)

Deux cartes interactives (Plotly) sont générées :

🥇 Top-5 des meilleures destinations
Ce Top 5 est évalué selon des critères propre, en version d'amélioration, ces critères pourraient être choisis par l'utilisateur

🏨 Top-20 hôtels recommandés (selon la note)

Filtrés par note en fonction de la disponibilité durant les dates soumises. Le prix des chambres est situé entre 100 et 250€ par nuit.

Affichées sur une carte grâce aux coordonnées GPS.


## Lien Github
https://github.com/francois-minaret/CDSD/tree/main/bloc1_data_structure/KAYAK

## 📬 Contact
Auteur : MINARET François
https://www.linkedin.com/in/minaret-fran%C3%A7ois-56106a105/