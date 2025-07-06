import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px
from interface.table import get_ranking


def show_kpi_cards(df, filters):
    if filters["pays"]:
        df = df[df["country_long"].isin(filters["pays"])]

    total_medals = len(df)
    total_countries = df["country_long"].nunique()
    female_ratio = ((df["gender"] == "Female").sum() / len(df))*100
    male_ratio = 100 - female_ratio
    

    col1, col2, col3 = st.columns(3)
    with col1:
        if total_countries == 1:
            rank = get_ranking(df, filters)
            col1.metric("Ranking", rank)
        else:
            col1.metric("Nombre de pays sélectionnés", total_countries)

    with col2:
        col2.metric("Total Médailles", total_medals)

    with col3:
        col3.text("Ratio Femmes/Hommes")
        fig = px.pie(names=['Femmes', 'Hommes'], values=[female_ratio, male_ratio])
        fig.update_layout(height=100, margin=dict(t=0, b=0, l=0, r=0))  # Ajuster la hauteur et les marges
        col3.plotly_chart(fig, use_container_width=True)