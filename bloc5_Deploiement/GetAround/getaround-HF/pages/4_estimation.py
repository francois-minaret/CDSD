import streamlit as st
import requests
import pandas as pd

st.title("Estimation du prix de location d'un véhicule")
st.markdown("""
Renseignez les caractéristiques du véhicule ci-dessous pour obtenir une <u>estimation du prix de location par jour (€)</u> grâce à notre modèle de machine learning.
""",unsafe_allow_html=True)

API_URL = "https://fminaret-getaround-api.hf.space/predict"

with st.expander("Caractéristiques du véhicule"):
    col1, col2 = st.columns(2)
    with col1:
        modele = st.selectbox("Modèle :", 
            ['AlfaRomeo','Audi','BMW','Citroën','Ferrari','Fiat','Ford','Honda','KIAMotors','Lamborghini','Lexus','Maserati','Mazda','Mercedes','Mitsubishi','Nissan','Opel','Peugeot','PGO','Porsche','Renault','SEAT','Subaru','Suzuki','Toyota','Volkswagen','Yamaha'])
        essence = st.selectbox("Type de carburant :", ['diesel', 'Eletrique', 'essence', 'Hybride'])
        couleur = st.selectbox("Couleur :", ['Argent','Beige','Blanc','Bleu','Gris','Marron','Noir','Orange','Rouge','Vert'])
        type_vehicule = st.selectbox("Type de véhicule :", ['Berline','Break','Cabriolet','Compacte','Coupé','Sous-compacte','SUV','Van'])

    with col2:
        kilometrage = st.number_input("Kilométrage (en km) :", min_value=0, max_value=400000, value=50000, step=5000)
        puissance = st.number_input("Puissance moteur (ch) :", min_value=40, max_value=400, value=110, step=10)

with st.expander("Options du véhicule"):
    col1, col2 = st.columns(2)
    with col1:
        Boite_auto = st.radio("Boîte automatique ?", ["Oui", "Non"], horizontal=True)
        GPS = st.radio("GPS intégré ?", ["Oui", "Non"], horizontal=True)
        Pneus_hiver = st.radio("Pneus hiver ?", ["Oui", "Non"], horizontal=True)
        Systeme_GetAround = st.radio("Système GetAround Connect ?", ["Oui", "Non"], horizontal=True)
    with col2:
        Climatisation = st.radio("Climatisation ?", ["Oui", "Non"], horizontal=True)
        parking = st.radio("Parking privé disponible ?", ["Oui", "Non"], horizontal=True)
        Regulateur = st.radio("Régulateur de vitesse ?", ["Oui", "Non"], horizontal=True)

if st.button("Estimer le prix"):
    input_data = {
        "modele": modele,
        "kilometrage": kilometrage,
        "puissance": puissance,
        "essence": essence,
        "couleur": couleur,
        "type": type_vehicule,
        "parking": parking,
        "GPS": GPS,
        "Climatisation": Climatisation,
        "Boite_auto": Boite_auto,
        "Systeme_GetAround": Systeme_GetAround,
        "Regulateur": Regulateur,
        "Pneus_hiver": Pneus_hiver
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            prediction = response.json()
            st.success(f"💰 Prix estimé : {prediction['Prix à la location €/j prédit ']} € / jour")
        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
    except Exception as e:
        st.error(f"Erreur lors de la requête : {e}")
