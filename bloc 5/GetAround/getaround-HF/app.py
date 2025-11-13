import streamlit as st

st.set_page_config(page_title="GetAround - Tableau de bord", page_icon="🚗")

st.title("GetAround - Tableau de bord")
st.write("Utilisez le menu à gauche pour naviguer entre les pages.")

st.markdown("""
    <h3>Bienvenue sur le Web Dashboard GetAround !</h3>
    <br>        
    Vous trouverez une analyse :
    <br> • des retards
    <br> • des tarifs de location à la journée
    <br> • une étude des seuils
    <br> • une estimation des tarifs de location à la journée
""", unsafe_allow_html=True)
