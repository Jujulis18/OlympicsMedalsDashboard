# interface/filters.py
import streamlit as st
import pandas as pd

def show_filters(df):
    st.sidebar.header("Filtres")

    # Pays
    pays = df['country'].unique().tolist()
    selection_pays = st.sidebar.multiselect(
        "Sélectionnez les pays",
        options=pays,
        default=pays
    )

    # Sexe
    choix_sexe = st.sidebar.radio(
        "Genre des athlètes",
        options=["Tous", "Homme", "Femme"],
        index=0
    )

    # Type de médaille (exemple simplifié)
    choix_medaille = st.sidebar.multiselect(
        "Type de médaille",
        options=["Or", "Argent", "Bronze", "Total"],
        default=["Total"]
    )

        # Filtre date avec intervalle
    date_min = pd.to_datetime(df['last_gold'].min())
    date_max = pd.to_datetime(df['last_gold'].max())
    choix_date = st.sidebar.date_input(
        "Période (jour)",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )

    return {
        "pays": selection_pays,
        "sexe": choix_sexe,
        "medaille": choix_medaille,
        "date": choix_date
    }
