import plotly.express as px
import streamlit as st
import pandas as pd

def show_table_and_graphs(df, filters):
    # Appliquer les filtres
    if filters["pays"]:
        df = df[df["country"].isin(filters["pays"])]

    df["last_gold"] = pd.to_datetime(df["last_gold"])
    start_date, end_date = filters["date"]
    df = df[(df["last_gold"] >= pd.to_datetime(start_date)) & (df["last_gold"] <= pd.to_datetime(end_date))]

    # Affichage tableau
    st.subheader("Tableau des Médailles")
    st.dataframe(df)

    # Histogramme total par pays
    st.subheader("Histogramme des Médailles par Pays")
    df_agg = df.groupby("country", as_index=False).agg({"total": "sum"})
    fig_bar = px.bar(df_agg, x="country", y="total", color="country", title="Total de Médailles par Pays")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Graphique temporel (médailles par jour)
    st.subheader("Évolution Temporelle des Médailles")
    df_time = df.groupby("last_gold", as_index=False).agg({"total": "sum"})
    fig_line = px.line(df_time, x="last_gold", y="total", title="Nombre de Médailles au Fil du Temps")
    st.plotly_chart(fig_line, use_container_width=True)
