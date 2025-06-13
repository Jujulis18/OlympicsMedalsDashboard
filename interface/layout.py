import streamlit as st
from interface.filters import show_filters
from interface.kpi_cards import show_kpi_cards
from interface.country_map import show_country_map
from interface.table import show_table_and_graphs

def display_dashboard(df):
    st.title("Dashboard JO 2024 - Analyse des Médailles")

    # Affiche les filtres dans la sidebar et récupère la sélection
    filters = show_filters(df)

    # Affiche les KPI filtrés en fonction des choix utilisateur
    show_kpi_cards(filters)

    st.markdown("---")
    tab1, tab2 = st.tabs(["Carte des pays", "Analyse détaillée"])

    with tab1:
        show_country_map(df, filters)

    with tab2:
        show_table_and_graphs(df, filters)

   