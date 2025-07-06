import plotly.express as px
import streamlit as st
import pandas as pd
from scripts.dataset_slicer import OlympicDatasetSlicer
import numpy as np

def show_table(df, filters):

    # Appliquer les filtres
    if filters["pays"]:
        df = df[df["country_long"].isin(filters["pays"])]

    st.subheader("Tableau des Médailles")
    st.dataframe(df)

def apply_filters(df, filters):
    if filters["pays"]:
        df = df[df["country_long"].isin(filters["pays"])]
    if filters["sexe"]:
        if filters["sexe"]=="Femme":
            df = df[df["gender"]=="Female"]
        if filters["sexe"]=="Homme":
            df = df[df["gender"]=="Male"]
    if filters["medaille"]:
        if "Total" not in filters["medaille"]:
            medaille_mapping = {"Or": 1, "Argent": 2, "Bronze": 3}
            filtered_values = [medaille_mapping[m] for m in filters["medaille"] if m in medaille_mapping]
            if filtered_values:
                df = df[df["medal_code"].isin(filtered_values)]
    return df

def prepare_data(df):
    slicer = OlympicDatasetSlicer(df)
    slicer.prepare_olympic_data()
    slicer.slice_by_gender_medals()
    slicer.slice_youngest_medalists()
    slicer.slice_oldest_medalists()
    slicer.slice_multi_discipline_athletes()
    return slicer

def get_ranking(df, filters):
    df_filtered = apply_filters(df, filters)
    slicer = prepare_data(df_filtered)
    return slicer.get_ranking(filters["pays"])

def show_graphs(df, filters):
    df_filtered = apply_filters(df, filters)
    slicer = prepare_data(df_filtered)
    slicer.display_graphs()

def show_age(df, filters):
    df_filtered = apply_filters(df, filters)
    slicer = prepare_data(df_filtered)
    slicer.display_age()

def show_compare(df, filters):
    df_filtered = apply_filters(df, filters)
    slicer = prepare_data(df_filtered)
    slicer.display_compare()
