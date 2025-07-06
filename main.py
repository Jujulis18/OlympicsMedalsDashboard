import streamlit as st
import pandas as pd
import json
from interface.layout import display_dashboard
from pathlib import Path

@st.cache_data

def load_data():
    data_path = Path(__file__).parent / "data" / "df_combined.csv"
    data = pd.read_csv(data_path)
    return data

def main():
    df = load_data()
    display_dashboard(df)

if __name__ == "__main__":
    main()
