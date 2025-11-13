import pandas as pd
import numpy as np
import streamlit as st

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

i=0
df = pd.read_csv("Data/get_around_pricing_project.csv",sep=',')

st.set_page_config(layout="wide")

st.title("Analyse des prix")

df.drop(columns=['Unnamed: 0'],inplace=True)
st.markdown(f"Il existe {df.shape[0]} lignes dans l'étude des prix.", unsafe_allow_html=True)

Gammes = {
    # Généralistes
    'Citroën': 'Généraliste',
    'Renault': 'Généraliste',
    'Peugeot': 'Généraliste',
    'Nissan': 'Généraliste',
    'Volkswagen': 'Généraliste',
    'Toyota': 'Généraliste',
    'Opel': 'Généraliste',
    'Ford': 'Généraliste',
    'KIA Motors': 'Généraliste',
    'Fiat': 'Généraliste',
    'Mazda': 'Généraliste',
    'Honda': 'Généraliste',
    'SEAT': 'Généraliste',
    'Suzuki': 'Généraliste',
    'Mitsubishi':'Généraliste',
    'BMW': 'Premium',
    'Audi': 'Premium',
    'Mercedes': 'Premium',
    # Sportives/Luxe
    'Ferrari': 'Sportive/Luxe',
    'Porsche': 'Sportive/Luxe',
    'Lamborghini': 'Sportive/Luxe',
    'Maserati': 'Sportive/Luxe',
    'Lexus': 'Sportive/Luxe',
    # Niche/Faible volume
    'PGO': 'Niche',
    'Alfa Romeo': 'Niche',
    'Mini': 'Niche',
    'Yamaha': 'Niche',
    'Subaru': 'Niche'  
}

df['catégorie'] = df['model_key'].map(Gammes)
df['type_km']=df['mileage'].apply(lambda x: 'km faible' if x<= 50000 else 'km élevé' if x>120000 else 'km standard' )
couleur = {
    'black': 'Noir',
    'grey': 'Gris',
    'blue': 'Bleu',
    'white': 'Blanc',
    'brown': 'Marron',
    'silver': 'Argent',
    'red': 'Rouge',
    'beige': 'Beige',
    'green': 'Vert',
    'orange': 'Orange'
}
df['couleur'] = df['paint_color'].map(couleur)

essence = {
    'petrol':'essence',
    'electro':'Electrique',
    'hybrid_petrol':'Hybride',
    'diesel':'diesel'
}
df['essence'] = df['fuel'].map(essence)


df.drop(['paint_color'],axis=1,inplace=True)
df.drop(['fuel'],axis=1,inplace=True)
type_fr = {
    'estate': 'Break',
    'sedan': 'Berline',
    'suv': 'SUV',
    'hatchback': 'Compacte',
    'subcompact': 'Sous-compacte',
    'coupe': 'Coupé',
    'convertible': 'Cabriolet',
    'van': 'Van'
}
df['type'] = df['car_type'].map(type_fr)
df.drop(['car_type'],axis=1,inplace=True)

df = df.rename(columns={'model_key': 'modele','mileage':'kilometrage','engine_power':'puissance','has_gps':'GPS',
                        'has_air_conditioning':'Climatisation','automatic_car':'Boite_auto',
                        'has_getaround_connect':'Systeme_GetAround','has_speed_regulator':'Regulateur',
                        'winter_tires':'Pneus_hiver','private_parking_available':'parking',
                        'rental_price_per_day':'Prix_location'})

st.dataframe(df.head(5))

st.write("<ul><li>Modele → Marque du véhicule</li>",unsafe_allow_html=True)
st.write("<li>Kilometrage → Kilométrage du véhicule au départ de la location</li>",unsafe_allow_html=True)
st.write("<li>Puissance → Puissance du moteur</li>",unsafe_allow_html=True)
st.write("<li>Parking → Parking privé disponible</li>",unsafe_allow_html=True)
st.write("<li>GPS → GPS inclus</li>",unsafe_allow_html=True)
st.write("<li>Climatisation → Climatisation incluse</li>",unsafe_allow_html=True)
st.write("<li>Boite_auto → Boîte automatique</li>",unsafe_allow_html=True)
st.write("<li>Systeme_GetAround → Possède le système Getaround Connect</li>",unsafe_allow_html=True)
st.write("<li>Regulateur → Régulateur de vitesse</li>",unsafe_allow_html=True)
st.write("<li>Pneus_hiver → Equipé de pneus neige</li>",unsafe_allow_html=True)
st.write("<li>Categorie → Gamme de véhicule</li>",unsafe_allow_html=True)
st.write("<li>type_km → indication généraliste du kilométrage</li>",unsafe_allow_html=True)
st.write("<li>Couleur → Couleur de la peinture</li>",unsafe_allow_html=True)
st.write("<li>Essence → Carburant</li>",unsafe_allow_html=True)
st.write("<li>Type → Type de voiture</li>",unsafe_allow_html=True)
st.write("<li>Prix_location → Prix de location par jour</li></ul>",unsafe_allow_html=True)

st.write("<br><h4>Diagramme en boite de la puissance</h4>", unsafe_allow_html=True)

for col in ['puissance','kilometrage']:
    fig = px.box(
        df,
        y='puissance',
        points="all",  
    )
    fig.update_layout(
        yaxis_title='Puissance',
        showlegend=True
    )
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Diagramme en boite du kilométrage</h4>", unsafe_allow_html=True)

fig = px.box(
    df,
    y='kilometrage',
    points="all",  
)
fig.update_layout(
    yaxis_title='Kilometrage',
    showlegend=True
)
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

df = df[(df['puissance']> 25) & (df['puissance']<320)]
df = df[(df['kilometrage']> 0) & (df['kilometrage']<400000)]

st.write("<br><h4>Diagramme de Boite des prix de véhicule en fonction des types</h4>", unsafe_allow_html=True)
fig = px.box(df, x="type", y="Prix_location")
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

df = df[
        ((df['type']=='Cabriolet') & (df['Prix_location']<200)) |
        ((df['type']=='Coupé') & (df['Prix_location']<300)) |
        (df['type']=='Break') |
        ((df['type']=='Compacte') & (df['Prix_location']>30)) |
        (df['type']=='Berline') |
        (df['type']=='Sous-compacte') |
        (df['type']=='Van') |
        ((df['type']=='SUV') & (df['Prix_location']<300) & (df['Prix_location']>30)) 
    ]


st.write("<br><h4>Diagramme de Boite des prix selon le type de carburant</h4>", unsafe_allow_html=True)
fig = px.box(df, x="essence", y="Prix_location")
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Diagramme de Boite des prix selon la catégorie</h4>", unsafe_allow_html=True)
fig = px.box(df, x="catégorie", y="Prix_location",
             title="Prix par type de véhicule")
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Répartition des locations</h4>", unsafe_allow_html=True)
st.write("<h5>Par catégorie</h5>", unsafe_allow_html=True)
df_categorie_counts = df['catégorie'].value_counts().reset_index()
df_categorie_counts.columns = ['catégorie', 'Nombre']
fig = px.bar(df_categorie_counts,
             x='catégorie', y='Nombre', text='Nombre',
             title='Location par catégorie')
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<h5>Par Modèle - Les 10 +</h5>", unsafe_allow_html=True)
df_model_counts = df['modele'].value_counts().head(10).reset_index()
df_model_counts.columns = ['Modèle', 'Nombre']
fig = px.bar(df_model_counts,
             x='Modèle', y='Nombre', text='Nombre')
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<h5>Par type de carburant</h5>", unsafe_allow_html=True)
df_fuel_counts = df['essence'].value_counts().head(10).reset_index()
df_fuel_counts.columns = ['Carburant', 'Nombre']
fig = px.bar(df_fuel_counts,
             x='Carburant', y='Nombre', text='Nombre')
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<h5>Par type - Les 10 +</h5>", unsafe_allow_html=True)
df_type_counts = df['type'].value_counts().head(10).reset_index()
df_type_counts.columns = ['type', 'Nombre']
fig = px.bar(df_type_counts,
             x='type', y='Nombre', text='Nombre')
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

Prix_median = df['Prix_location'].median()
Prix_moyen = df['Prix_location'].mean()


st.write("<h4>Répartition des prix de location</h4>", unsafe_allow_html=True)

fig = px.histogram(df,
                   x='Prix_location',
                   title='Prix de location par jour',
                   labels={"Prix_location": "Prix (€)"})

fig.add_vline(x=Prix_median,
              line=dict(color="green"),
              annotation_text="Médiane",
              annotation_position="top")

fig.add_vline(x=Prix_moyen,
              line=dict(color="red"),
              annotation_text="Moyenne")
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1


for categorie in df['catégorie'].unique():
    prix_moyen_cat = df[df['catégorie']==categorie]['Prix_location'].mean()
    df_prix_moyen = (
        df[df['catégorie'] == categorie]
        .groupby('modele', as_index=False)['Prix_location']
        .mean()
        .sort_values('Prix_location', ascending=False)
    )

    fig = px.bar(
        df_prix_moyen,
        x='modele',
        y='Prix_location',
        title=f"Prix moyen par marque - Catégorie {categorie}",
        text_auto=".1f",
        labels={"Prix_location": "Prix moyen (€/jour)", "modele": "Marque"},
        color='Prix_location',
        color_continuous_scale='Viridis'
    )
    fig.add_hline(
        y=prix_moyen_cat,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Moyenne catégorie : {prix_moyen_cat:.1f}€",
        annotation_position="top right"
    )
    
    st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
    i+=1

df_repartition = df[['type','modele','catégorie']].value_counts().reset_index()
df_repartition.columns = ['type','Marque','catégorie', 'Nombre']

categorie_liste = ['Généraliste','Sportive/Luxe','Premium','Niche']

for cat in categorie_liste:
    st.write(f"<h4>Répartition des types de véhicules par catégorie {cat}</h4>", unsafe_allow_html=True)
    fig = px.bar(df_repartition[df_repartition['catégorie']==cat],
                x='Marque',
                y='Nombre',
                color='type',
                text='Nombre')

    fig.update_layout(barmode='stack', xaxis_title='Modèle', yaxis_title='Nombre de véhicules')
    
    st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
    i+=1

df_repartition = df[['type','type_km','catégorie']].value_counts().reset_index()
df_repartition.columns = ['type','type_km','catégorie', 'Nombre']

categorie_liste = ['Généraliste','Sportive/Luxe','Premium','Niche']

for cat in categorie_liste:
    df_cat = df_repartition[df_repartition['catégorie']==cat]
    km_moyen = df[df['catégorie']==cat]['kilometrage'].mean().round(0)
    st.write(f"<h4>Répartition des types de véhicules par kilométrage {cat} : km moyen : {km_moyen}</h4>", unsafe_allow_html=True)
    fig = px.bar(df_cat,
                x='type',
                y='Nombre',
                color='type_km',
                text='Nombre')

    fig.update_layout(barmode='stack', xaxis_title='Modèle', yaxis_title='Nombre de véhicules')
    st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
    i+=1

df_dummies = pd.get_dummies(df['essence'], prefix='Carburant')
df_final = pd.concat([df.drop('essence', axis=1), df_dummies], axis=1)

df_dummies = pd.get_dummies(df['modele'], prefix='Modele')
df_final = pd.concat([df_final.drop('modele', axis=1), df_dummies], axis=1)

df_dummies = pd.get_dummies(df['type'], prefix='type')
df_final = pd.concat([df_final.drop('type', axis=1), df_dummies], axis=1)
df_corr = df_final.copy()
colonne_bool = df_corr.select_dtypes(include="bool").columns
df_corr[colonne_bool] = df_corr[colonne_bool].astype(int)

numeric_df = df_corr.select_dtypes(include=['number'])

corr = numeric_df.corr().round(3)

target = 'Prix_location'
corr_target = corr[target].drop(target).sort_values(key=abs, ascending=False)

top_corr = corr_target.head(10)

df_top_corr = top_corr.reset_index()
df_top_corr.columns = ['Variable', 'Corrélation']

vars_to_keep = [target] + df_top_corr['Variable'].tolist()
corr_sub = corr.loc[vars_to_keep, vars_to_keep]

color_scale = [
    [0.0, 'blue'],    # corr négative forte
    [0.5, 'white'],   # neutre
    [1.0, 'red']      # corr positive forte
]

st.write(f"<h4>Matrice de corrélation - Top 15</h4>", unsafe_allow_html=True)

fig = px.imshow(
    corr_sub,
    text_auto=True,
    color_continuous_scale=color_scale,
    width=800,
    height=700
)
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write(f"<h3>Conclusion</h3>", unsafe_allow_html=True)
st.write("<ul><li>Le parc de véhicule est essentiellement composé de véhicule diesel.</li>", unsafe_allow_html=True)
st.write("<li>Le kilométrage est plutôt élevé ce qui est préjudiciable car c'est le paramètre qui impacte le plus prix de location.</li>", unsafe_allow_html=True)
st.write("<li>Le prix moyen de location et le prix médian sont très proche et autour de 120€/jour. </li>", unsafe_allow_html=True)
st.write("<li>Le diesel est le carburant le plus représenté</li>", unsafe_allow_html=True)
st.write("<li>Les catégories pré-dominantes sont les SUV, Berline et break.</li>", unsafe_allow_html=True)
st.write("<li>Les 5 marques avec le plus de véhicules sont : Citroën/Renault/BMW/Peugeot/Audi</li></ul>", unsafe_allow_html=True)