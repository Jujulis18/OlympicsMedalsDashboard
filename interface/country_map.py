import plotly.express as px
import streamlit as st

def show_country_map(df, filters):
    # Filtrer df selon filters (pays, date, etc) comme précédemment
    if filters["pays"]:
        df = df[df["country"].isin(filters["pays"])]
    
    # Agréger le nombre total de médailles par pays
    df_agg = df.groupby("country", as_index=False).agg({"total": "sum"})

    # Carte choroplèthe
    fig = px.choropleth(
        df_agg,
        locations="country",
        locationmode="country names",
        color="total",
        color_continuous_scale="Viridis",
        title="Répartition des médailles par pays",
        labels={"total": "Nombre total de médailles"},
    )

    st.plotly_chart(fig, use_container_width=True)
