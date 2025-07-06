import plotly.express as px
import streamlit as st

def show_country_map(df, filters):
    if filters["pays"]:
        df = df[df["country_long"].isin(filters["pays"])]
    
    df_agg = df.groupby("country_long", as_index=False).agg(
        total=('medal_code', 'size'),
        disciplines=('discipline', 'nunique')
    )

    fig = px.choropleth(
        df_agg,
        locations="country_long",
        locationmode="country names",
        color="total",
        color_continuous_scale="Viridis",
        title="Répartition des médailles par pays"
    )

    st.plotly_chart(fig, use_container_width=False)
