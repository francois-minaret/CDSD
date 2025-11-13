import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

i=0
df = pd.read_csv("Data/get_around_delay_analysis.csv",sep=';')
st.set_page_config(layout="wide")
st.title("Analyse des seuils permettant les réservations")

Delai=[30, 60, 90, 120, 150, 180, 240, 300]
resultat=[]
nbr_car_delay_2_loc = len(df.dropna(subset=['time_delta_with_previous_rental_in_minutes']))

st.write(f'Il y a dans notre jeu de données {nbr_car_delay_2_loc} locations ayant un délai avec la réservation précédente.')
for i in Delai:
    nbr_loc_bloquee = (df['time_delta_with_previous_rental_in_minutes']>i).sum()
    pct_nbr_loc_bloquee = ((nbr_loc_bloquee / nbr_car_delay_2_loc) * 100).round(2)
    nbr_loc_ok = (df['time_delta_with_previous_rental_in_minutes']<=i).sum()
    pct_nbr_loc_ok = ((nbr_loc_ok / nbr_car_delay_2_loc) * 100).round(2)
 
    retards_reels = df[df['delay_at_checkout_in_minutes'] > 0]
    pct_retards_couverts = ((retards_reels['delay_at_checkout_in_minutes'] <= i).mean() * 100).round(2)
    resultat.append({
        'Delai (min)': i,
        'Locations bloquées': nbr_loc_bloquee,
        '% Loc bloquées': pct_nbr_loc_bloquee,
        'Locations possibles' : nbr_loc_ok,
        '% Loc possibles': pct_nbr_loc_ok,
        '% Retards réels couverts': pct_retards_couverts,
    })
df_resultat = pd.DataFrame(resultat)
st.dataframe(df_resultat.head(5))

st.write("Le coût moyen d'une journée de location est autour de 120€.<br>",unsafe_allow_html=True)
st.write("Si on prend uniquement un point de vue financier sur les locations enchainées, l'augmentation du délai amènera forcément un gain de location.<br>",unsafe_allow_html=True)
st.write("Cependant, il reste un peu plus de 6300 véhicules de disponibles donc pour affiner notre étude, il serait nécessaire de pouvoir obtenir les dates de locations ainsi que les points de location.<br>",unsafe_allow_html=True)
st.write("Le type de location mobile et connect impacte également cette données car le contact humain semble réduire les retards.<br>",unsafe_allow_html=True)
st.write("Une étude de satisfaction pourrait permettre de savoir l'impact du retard sur le souhait de louer à nouveau un véhicule.")