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
st.title("Analyse des retards")

st.markdown(f"Il existe {df.shape[0]} lignes dans l'étude des retards.", unsafe_allow_html=True)

n_unique_voitures = df['car_id'].nunique()
st.markdown(f"Nombre de véhicules uniques : {n_unique_voitures}", unsafe_allow_html=True)

n_unique_loc = df['rental_id'].nunique()
st.markdown(f"Nombre de personnes uniques utilisant le service : {n_unique_loc}<br>", unsafe_allow_html=True)
st.dataframe(df.head(5))

checkin_counts = df["checkin_type"].value_counts(normalize=True) * 100
st.write("<br><h4>Répartition par type de location</h4>", unsafe_allow_html=True)
fig2 = px.pie(df, names="checkin_type")
st.plotly_chart(fig2, use_container_width=True, key="fig{i}")

for checkin_type, pct in checkin_counts.items():
    st.markdown(f"- {checkin_type} : {pct:.1f}% des locations")
i+=1


st.write("<br><h4>Distribution des retours par type de location</h4>", unsafe_allow_html=True)
fig = px.histogram(
    df,
    x="delay_at_checkout_in_minutes",
    color="checkin_type",
    opacity=0.5,
    labels={"delay_at_checkout_in_minutes": "Retour (minutes)"},
    range_x=[-360, 360],
    width=600, height=600,
)
fig.update_layout(barmode="overlay")
fig.update_yaxes(title="Nombre de locations")

st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Distribution des retours par type de check-in sur la tranche -3/+3h par tranche de 10mn</h4>", unsafe_allow_html=True)
fig = px.histogram(
    df,
    x="delay_at_checkout_in_minutes",
    color="checkin_type",
    opacity=0.5,
    labels={"delay_at_checkout_in_minutes": "Retour (minutes)"},
    range_x=[-180, 180],
    width=600, height=600

)
fig.update_traces(xbins=dict(start=-180, end=180, size=10))
fig.update_yaxes(title="Nombre de locations")
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Proportion des retards par tranche</h4>", unsafe_allow_html=True)
df_retard = df[df['delay_at_checkout_in_minutes'] >= 0].copy()

bins = list(range(0, 601, 20)) + [float('inf')]
labels = [f"{i}–{i+20} min" for i in range(0, 600, 20)] + [">600 min"]

df_retard['tranche_retard'] = pd.cut(
    df_retard['delay_at_checkout_in_minutes'],
    bins=bins,
    labels=labels,
    right=False
)

distribution = (
    df_retard
    .groupby(['checkin_type', 'tranche_retard'])
    .size()
    .reset_index(name='count')
)

distribution['Pourcentage'] = (
    distribution
    .groupby('checkin_type')['count']
    .transform(lambda x: 100 * x / x.sum())
    .round(1)
)

fig = px.bar(
    distribution,
    x='tranche_retard',
    y='Pourcentage',
    color='checkin_type',
    barmode='stack',
    text='Pourcentage',
    labels={
        'tranche_retard': 'Tranche de retard (minutes)',
        'checkin_type': 'Type de check-in'
    },
    color_discrete_sequence=px.colors.qualitative.Safe,
    width=600, height=600
)

fig.update_traces(textposition='inside')
fig.update_layout(
    width=600,
    height=500,
    yaxis_title="Pourcentage (%)",
    xaxis_title="Tranche de retard (minutes)",
    legend_title="Type de check-in",
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    xaxis_tickangle=-45
)
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

st.write("<br><h4>Moyenne / Médiane</h4>", unsafe_allow_html=True)
df_retard2 = df_retard[df_retard['delay_at_checkout_in_minutes'] <= 720].copy()

fig = go.Figure()
colors = {'mobile': 'blue', 'connect': 'red'}

for checkin in df_retard2['checkin_type'].unique():
    subset = df_retard2[df_retard2['checkin_type'] == checkin]
    moyenne = subset['delay_at_checkout_in_minutes'].mean()
    medianne = subset['delay_at_checkout_in_minutes'].median()

    fig.add_trace(go.Histogram(
        x=subset['delay_at_checkout_in_minutes'],
        name=f"Réservation de type - {checkin}",
        nbinsx=30,
        opacity=0.6,
        marker_color=colors.get(checkin, 'gray')
    ))

    fig.add_trace(go.Scatter(
        x=[moyenne, moyenne],
        y=[0, df_retard2['delay_at_checkout_in_minutes'].count()/3], 
        mode="lines",
        line=dict(color=colors.get(checkin, 'gray'), width=2, dash="solid"),
        name=f"{checkin} - Moyenne ({moyenne:.0f} min)"
    ))

    fig.add_trace(go.Scatter(
        x=[medianne, medianne],
        y=[0, df_retard2['delay_at_checkout_in_minutes'].count()/3],
        mode="lines",
        line=dict(color=colors.get(checkin, 'gray'), width=2, dash="dash"),
        name=f"{checkin} - Médiane ({medianne:.0f} min)"
    ))

fig.update_layout(
    title="Distribution des retards réels (0 à 10h) par type de check-in",
    xaxis_title="Retard en minutes",
    yaxis_title="Nombre de locations",
    barmode='overlay',
    width=600,
    height=500,
    legend_title="Légende",
    bargap=0.05
)

st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1
st.write(f"Le nombre d'annulation de location est de {(df['state']=='canceled').sum()}.", unsafe_allow_html=True)

st.write("<br><h4>Délai avec la réservation précédente</h4>", unsafe_allow_html=True)
fig = go.Figure()
colors = {'mobile': 'blue', 'connect': 'red'}

for checkin in df['checkin_type'].unique():
    subset = df[df['checkin_type'] == checkin]
    moyenne = subset['time_delta_with_previous_rental_in_minutes'].mean()
    medianne = subset['time_delta_with_previous_rental_in_minutes'].median()

    fig.add_trace(go.Histogram(
        x=subset['time_delta_with_previous_rental_in_minutes'],
        name=f"Réservation de type - {checkin}",
        nbinsx=30,
        opacity=0.6,
        marker_color=colors.get(checkin, 'gray')
    ))

    fig.add_trace(go.Scatter(
        x=[moyenne, moyenne],
        y=[0, df['time_delta_with_previous_rental_in_minutes'].count()/3], 
        mode="lines",
        line=dict(color=colors.get(checkin, 'gray'), width=2, dash="solid"),
        name=f"{checkin} - Moyenne ({moyenne:.0f} min)"
    ))

    fig.add_trace(go.Scatter(
        x=[medianne, medianne],
        y=[0, df['time_delta_with_previous_rental_in_minutes'].count()/3],
        mode="lines",
        line=dict(color=colors.get(checkin, 'gray'), width=2, dash="dash"),
        name=f"{checkin} - Médiane ({medianne:.0f} min)"
    ))

fig.update_layout(
    xaxis_title="Délai en minutes",
    yaxis_title="Nombre de locations",
    barmode='overlay',
    width=600,
    height=500,
    legend_title="Légende",
    bargap=0.05
)

st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1

df_precedent = df[['rental_id', 'delay_at_checkout_in_minutes']].rename(
    columns={'rental_id': 'previous_ended_rental_id',
             'delay_at_checkout_in_minutes': 'retard_precedent'}
)
df_all = df.merge(df_precedent, on='previous_ended_rental_id', how='left')

df_all['is_canceled'] = (df_all['state'] == 'canceled').astype(int)
st.write(f"{df_all[(df_all['is_canceled']==1)&(df_all['retard_precedent']>df_all['time_delta_with_previous_rental_in_minutes'])].shape[0]} retards peuvent la résultante de la suppression de la réservation suivante")

st.write("<br><h4>Taux et nombre d'annulations selon le retard du précédent client (par type de check-in)</h4>", unsafe_allow_html=True)
df_precedent = df[['rental_id', 'delay_at_checkout_in_minutes']].rename(
    columns={'rental_id': 'previous_ended_rental_id',
             'delay_at_checkout_in_minutes': 'retard_precedent'}
)
df_all = df.merge(df_precedent, on='previous_ended_rental_id', how='left')

df_all['is_canceled'] = (df_all['state'] == 'canceled').astype(int)


bins = np.arange(0, 601, 30)
labels = [f"{i}-{i+30} min" for i in bins[:-1]]

df_all['tranche_retard_precedent'] = pd.cut(
    df_all['retard_precedent'],
    bins=bins,
    labels=labels,
    include_lowest=True,
    ordered=True
)

cancel_stats = (
    df_all.groupby(['checkin_type', 'tranche_retard_precedent'])
    .agg(
        Taux_annulation=('is_canceled', 'mean'),
        Nb_annulations=('is_canceled', 'sum')
    )
    .reset_index()
)

fig = go.Figure()
colors = {'mobile': 'royalblue', 'connect': 'orangered'}

for checkin in cancel_stats['checkin_type'].unique():
    subset = cancel_stats[cancel_stats['checkin_type'] == checkin]

    fig.add_trace(go.Scatter(
        x=subset['tranche_retard_precedent'].astype(str),
        y=subset['Taux_annulation'] * 100,
        mode='lines+markers',
        name=f"{checkin} - Taux d'annulation",
        line=dict(color=colors[checkin], width=3)
    ))

    fig.add_trace(go.Scatter(
        x=subset['tranche_retard_precedent'].astype(str),
        y=subset['Nb_annulations'],
        mode='lines+markers',
        name=f"{checkin} - Nb d'annulations",
        line=dict(color=colors[checkin], width=2, dash='dot'),
        yaxis='y2'
    ))

fig.update_layout(
    xaxis=dict(
        title="Retard du précédent client (tranches de 30 min)",
        categoryorder='array',
        categoryarray=labels,
        tickangle=-45
    ),
    yaxis=dict(
        title="Taux d'annulation (%)",
        tickformat=".0f"
    ),
    yaxis2=dict(
        title="Nombre d'annulations",
        overlaying='y',
        side='right'
    ),
    width=600,
    height=500,
    legend_title="Indicateurs",
)
st.plotly_chart(fig, use_container_width=True, key=f"fig{i}")
i+=1
