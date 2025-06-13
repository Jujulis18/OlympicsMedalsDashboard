import streamlit as st
import pandas as pd
import json
from pathlib import Path

def load_medal_data():
    data_path = Path(__file__).resolve().parent.parent / "data" / "medals_sample.json"
    with open(data_path, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def show_kpi_cards(filters):
    df = load_medal_data()

    # Filtrage pays
    if filters["pays"]:
        df = df[df["country"].isin(filters["pays"])]

    # Filtrage sexe (exemple simplifié)
    if filters["sexe"] == "Femme":
        df = df[df["female_athletes"] > 0]  # exemple basique
    elif filters["sexe"] == "Homme":
        # On suppose total_athletes - female_athletes = hommes
        df = df[df["total_athletes"] - df["female_athletes"] > 0]

    # Filtrage médaille (exemple : on ne garde que les lignes où total > 0)
    if "Total" not in filters["medaille"]:
        # Ici on n'a qu'une colonne total, on adapte pour or/argent/bronze si dispo
        df = df[df["total"] > 0]

    # Filtrage année (si on a une colonne date ou année, ici on fait simple)
    # Exemple pas implémenté car nos données sont très basiques

    # Calcul KPIs
    total_medals = df["total"].sum()
    total_countries = df["country"].nunique()
    female_ratio = df["female_athletes"].sum() / df["total_athletes"].sum() * 100 if df["total_athletes"].sum() > 0 else 0
    last_gold_date = df["last_gold"].max() if not df.empty else "N/A"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏅 Total Médailles", total_medals)
    col2.metric("🌍 Pays Participants", total_countries)
    col3.metric("♀ % Femmes", f"{female_ratio:.1f}%")
    col4.metric("⏱ Dernière Médaille d'Or", last_gold_date)
