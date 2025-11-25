import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

import numpy as np
import shap
from sklearn.linear_model import LinearRegression
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser

# partie initialisation
model_paths = {
    "Deblais et Gravats": "model_paths/model_Deblais_gravats.pkl",
    "Dechets verts": "model_paths/model_Dechets_verts.pkl",
    "Encombrants": "model_paths/model_Encombrants.pkl",
    "Materiaux recyclables": "model_paths/model_Materiaux_recyclables.pkl"
}

col_mapping = {
    "Deblais et Gravats": "Deblais_gravats",
    "Dechets verts": "Dechets_verts",
    "Encombrants": "Encombrants",
    "Materiaux recyclables": "Materiaux_recyclables"
}

default_dept = "Aisne"

valeurs_observees = []
valeurs_predites = []
labels = []

categories = {
    "📊 Population": [
        "pop_globale",
        "tranche_age_0-24", "tranche_age_25-59", "tranche_age_60+",
        "csp1_agriculteurs", "csp2_artisans_commerçant_chef_entreprises",
        "csp3_cadres_professions_intellectuelles", "csp4_professions_intermediaires",
        "csp5_employes", "csp6_ouvriers", "csp7_retraites", "csp8_sans_activite",
        "densite" 
    ],
    "🏭 Activite economique": [
        "nbre_entreprises", "nbre_entreprises_agricole", "nb_salaries_secteur_agricole", 
        "nbre_entreprises_industrie", "nb_salaries_secteur_industrie", 
        "nb_salaries_secteur_service", "nbre_entreprises_service"
    ]
}

# Pour la gestion automatique du run eval uniquement au demarrage et en cas de changement de departement
# sinon necessaire de cliquer sur Lancer l'evaluation
if "previous_dept" not in st.session_state:
    st.session_state["previous_dept"] = None

if "auto_run_done" not in st.session_state:
    st.session_state["auto_run_done"] = False

def run_eval(selected_dept, form_input):
    # Transformation en DataFrame
    input_df = pd.DataFrame([form_input])
    input_df_complete = row_default.to_frame().T.copy()
    for col in input_df.columns:
        if col in input_df_complete.columns:
            input_df_complete.at[input_df_complete.index[0], col] = input_df.at[0, col]

    # Verification des incoherences
    Liste_trage = ["pop_globale", "tranche_age_0-24", "tranche_age_25-59", "tranche_age_60+"]
    Somme = 0
    if all(v in form_input for v in Liste_trage):
        for elt in Liste_trage:
            if elt != "pop_globale":
                Somme += form_input[elt]
        if abs(form_input["pop_globale"] - Somme) > 1:
            st.error(f"❌ Incoherence : Population globale = {form_input['pop_globale']} ne correspond pas à la somme des tranches d'âge : {Somme}")

    Liste_CSP = ["pop_globale","csp1_agriculteurs", "csp2_artisans_commercant_chef_entreprises",
                "csp3_cadres_professions_intellectuelles", "csp4_professions_intermediaires",
                "csp5_employes", "csp6_ouvriers", "csp7_retraites", "csp8_sans_activite"]
    Somme = 0
    if all(v in form_input for v in Liste_CSP):
        for elt in Liste_CSP:
            if elt != "pop_globale":
                Somme += form_input[elt]
        if abs(form_input["pop_globale"] - Somme) >1:
            st.error(f"❌ Incoherence : Population globale = {form_input['pop_globale']} ne correspond pas à la somme des CSP : {Somme}")

    Liste_Entreprise = ["nbre_entreprises", "nbre_entreprises_agricole",
                "nbre_entreprises_industrie", "nbre_entreprises_service"]
    Somme = 0
    if all(v in form_input for v in Liste_Entreprise):
        for elt in Liste_Entreprise:
            if elt != "nbre_entreprises":
                Somme += form_input[elt]
        if abs(form_input["nbre_entreprises"] - Somme) > 1:
            st.error(f"❌ Incoherence : Le nombre d'entreprises = {form_input['nbre_entreprises']} ne correspond pas à la somme des types d'entreprise : {Somme}")


    # on reinitialise pour que ça ne se lance pas automatiquement (lourd)
    evaluation = False
    for typologie, path in model_paths.items():
        try:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    model = pickle.load(f)
            else:
                st.error(f"❌ Modèle manquant : {path}")
            expected_cols = model.model.exog_names
            if "const" in expected_cols and "const" not in input_df_complete.columns:
                input_df_complete["const"] = 1.0

            prediction = max(0, model.predict(input_df_complete[expected_cols]).iloc[0])
            valeurs_predites.append(prediction)
            labels.append(typologie)

            filtered = observed_df[
                (observed_df["Departement"] == selected_dept) & (observed_df["annee"] == 2021)
            ]

            excel_col = col_mapping.get(typologie)
            if not filtered.empty and excel_col in filtered.columns:
                valeurs_observees.append(filtered[excel_col].values[0])
            else:
                valeurs_observees.append(0.0)
        except Exception as e:
            st.error(f"Erreur avec le modèle {typologie}")
            st.exception(e)

# === Chargement des donnees
df = pd.read_csv("Data/df_dummies.csv").drop(columns=["Unnamed: 0"], errors="ignore")
observed_df = pd.read_csv("Data/data_wip.csv")

# === Liste des departements
departements = [col.replace("Departement_", "") for col in df.columns if col.startswith("Departement_")]

# === Mise en page
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: left;'>♻️ Simulateur de production de dechets par departement</h1>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: left;'>📍 Choix du departement</h3>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: left;'>📈 Comparaison entre valeurs observees et predites</h3>", unsafe_allow_html=True)

st.markdown("<div style='text-align:left: 60px;'></div>", unsafe_allow_html=True)

selected_dept = st.selectbox("Selectionner un departement", sorted(departements), index=sorted(departements).index(default_dept))

row_default = df[df[f"Departement_{selected_dept}"] == 1].iloc[0]
default_dict = row_default.to_dict()

st.subheader("⚙️ Paramètres modifiables")
form_input = {}
for category_name, variables in categories.items():
    with st.expander(category_name, expanded=False):
        for i, var in enumerate(variables):
            if var in default_dict:
                if category_name == "📊 Population":
                    default_value = int(round(float(default_dict[var])/100)*100)
                else:
                    default_value = int(round(float(default_dict[var])/10)*10)
                val = st.number_input(
                    f"✏️ {var}",
                    min_value=0,
                    value=default_value,
                    step=1,
                    format="%d",
                    key=f"number_input_{selected_dept}_{var}"
                )
                form_input[var] = val
                st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

if st.session_state["previous_dept"] != selected_dept or not st.session_state["auto_run_done"]:
    st.session_state["previous_dept"] = selected_dept
    st.session_state["auto_run_done"] = True
    run_eval(selected_dept, form_input)


# with chart_col:
st.markdown("<div style='text-align:center: 30px;'></div>", unsafe_allow_html=True)

# btn_col = st.columns([3, 2, 3])[1]
# with btn_col:
evaluation = st.button("🔍 Lancer l'evaluation")

st.markdown("<div style='text-align:center: 40px;'></div>", unsafe_allow_html=True)

if evaluation:
    run_eval(selected_dept, form_input)
    st.session_state["auto_run_done"] = True

if valeurs_observees and valeurs_predites:
    x = np.arange(len(labels))
    width = 0.4
    fig, ax = plt.subplots(figsize=(10, 6))

    bars1 = ax.bar(x - width / 2, valeurs_observees, width, label='Observé (2021)', color='steelblue')
    bar_colors = [(1, 0, 0, 0.6) if pred > obs else (0, 0.6, 0, 0.6)
                    for pred, obs in zip(valeurs_predites, valeurs_observees)]
    bars2 = ax.bar(x + width / 2, valeurs_predites, width, label='Prevision', color=bar_colors)

    for i in range(len(labels)):
        ax.text(x[i] - width / 2, valeurs_observees[i] + max(valeurs_observees) * 0.01, f"{valeurs_observees[i]:,.0f}",
                ha='center', va='bottom', fontsize=9)
        ax.text(x[i] + width / 2, valeurs_predites[i] + max(valeurs_predites) * 0.01, f"{valeurs_predites[i]:,.0f}",
                ha='center', va='bottom', fontsize=9)

    ax.set_ylabel("Tonnes")
    ax.set_title("Comparaison Observe vs Predit")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()
    st.pyplot(fig)

    # === Graphiques SHAP ===
    st.markdown("---")
st.subheader(f"📉 SHAP - Analyse des contributions pour le departement : {selected_dept}")

# Menu deroulant
selected_typologie = st.selectbox("Choisissez une typologie de dechets à analyser avec SHAP :", list(model_paths.keys()))

# SHAP pour la typologie selectionnee
typologie = selected_typologie
path = model_paths[typologie]

st.markdown(f"### 🔍 {typologie}")

try:
    with open(path, "rb") as f:
        model_sm = pickle.load(f)

    used_features = model_sm.model.exog_names
    used_features_no_const = [f for f in used_features if f != "const"]
    X_used = df[used_features_no_const].copy()

    if "const" in used_features:
        X_used["const"] = 1.0

    intercept = model_sm.params['const'] if 'const' in model_sm.params else 0
    coefs = model_sm.params[used_features_no_const].values

    lr = LinearRegression()
    lr.intercept_ = intercept
    lr.coef_ = coefs
    lr.feature_names_in_ = np.array(used_features_no_const)

    X_used_corrected = X_used.reindex(columns=lr.feature_names_in_, fill_value=0)

    explainer = shap.Explainer(lr, X_used_corrected)
    shap_values = explainer(X_used_corrected)

    selected_index = df[df[f"Departement_{selected_dept}"] == 1].index[0]

    # === Première ligne : Waterfall + Beeswarm + Moyenne des contributions
    exclude_vars = [
            "Deblais_gravats", "Dechets_verts", "Encombrants", "Materiaux_recyclables"
        ]
    exclude_vars += [
        name for name in shap_values.feature_names
        if name.startswith(("Departement_", "Region_"))
    ]

    # Creation d’un masque pour filtrer les SHAP plots sans toucher à la prediction
    mask = np.array([name not in exclude_vars for name in shap_values.feature_names])
    filtered_shap = shap.Explanation(
    values=shap_values.values[:, mask],
    base_values=shap_values.base_values,
    data=shap_values.data[:, mask],
    feature_names=[name for name in shap_values.feature_names if name not in exclude_vars]
)

    col1 = st.columns(1)[0]

    with col1:
        st.markdown("<h6 style='text-align: center;'>🩜 Waterfall</h6>", unsafe_allow_html=True)
        fig = plt.figure(figsize=(3, 2))
        shap.plots.waterfall(filtered_shap[selected_index], max_display=10, show=False)
        st.pyplot(fig, bbox_inches='tight', dpi=200, clear_figure=True)

   


  
except Exception as e:
    st.error(f"Erreur dans le SHAP pour {typologie}")
    st.exception(e)

# === 🧠 Explication automatique avec Mistral ===



# 1. Recuperation des moyennes absolues des SHAP values
shap_local = filtered_shap[selected_index]

# 2. Creation d’un resume lisible des coefficients (tries par impact)
sorted_indices = np.argsort(np.abs(shap_local.values))[::-1]
top_n = 10
list_coef = "\n".join([
    f"{shap_local.feature_names[i]}: {shap_local.values[i]:.2f}"
    for i in sorted_indices[:top_n]
])

# 3. Prompt + contexte
prompt_template = f"""
Tu es un expert en data science et en statistique, specialise dans l'interpretation des resultats de modèles explicatifs à l'aide des coefficients de Shapley.

Je vais te fournir les valeurs des coefficients de Shapley pour un modèle lineaire de regression, associes à chaque variable explicative.

Ta mission :
Redige un paragraphe clair et synthetique, de 1500 caractères maximum, interpretant le rôle des variables dans le modèle pour repondre au besoin de notre client qui sont les presidents des conseils departementaux. Tu dois identifier :

- Les variables qui ont le plus d’impact positif ou negatif sur la variable cible.
- Les grandes tendances demographiques ou economiques qui expliquent la production de dechets.
- Une interpretation comprehensible par un public non-expert, mais avec une rigueur statistique.

Voici les coefficients :
{list_coef}

Contexte :
- Objectif : Comprendre comment les caracteristiques demographiques et economiques influencent la production des differents types de dechets en France.
- Variable cible : {typologie}
- Modèle utilisé : OLS de Statsmodel avec coefficients de Shapley.
- Variables explicatives :
  - Secteurs d’activites : Nombre de salaries par secteur : Agricole, Service, Industrie.
  - Profils socioprofessionnels (CSP) :
    csp1_agriculteurs, csp2_artisans_commerçant_chef_entreprises, csp3_cadres_professions_intellectuelles, csp4_professions_intermediaires, csp5_employes, csp6_ouvriers, csp7_retraites, csp8_sans_activite.
  - Tranches d’âge : tranche_age_0-24, tranche_age_25-59, tranche_age_60+.
  - Autres variables :
    Densite de population, Population globale, Typologie d'entreprises
  - tu ne dois pas prendre en compte les {exclude_vars} dans ton analyse  
"""

# 4. Appel à l’API Mistral
# Charge les variables d'environnement à partir du fichier .env
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
#st.write(f"Clé API : `****-****-****-{api_key[-4:]}`")
try:
    with st.spinner("🧠 Generation de l'interpretation avec Mistral..."):
        # model_llm = ChatMistralAI(model="mistral-large-latest", mistral_api_key=api_key)
        model_llm = ChatMistralAI(model="mistral-small-latest", mistral_api_key=api_key)
        parser = StrOutputParser()
        response = model_llm.invoke(prompt_template)
        explanation_text = parser.invoke(response)

    # 5. Affichage dans l’interface Streamlit
    st.markdown("#### 🤖 Interpretation automatique (LLM)")
    st.success(explanation_text)

except Exception as e:
    st.error("Erreur lors de l'appel au LLM Mistral.")
    st.exception(e)
