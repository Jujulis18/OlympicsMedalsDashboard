import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import List, Dict


class OlympicDatasetSlicer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.subsets = {}

    def prepare_olympic_data(self, birth_col='birth_date', medal_col='medal_date'):
        self.data[birth_col] = pd.to_datetime(self.data[birth_col], errors='coerce')
        self.data[medal_col] = pd.to_datetime(self.data[medal_col])
        self.data['age_at_medal'] = (self.data[medal_col] - self.data[birth_col]).dt.days // 365

    def slice_by_gender_medals(self, subset_name='gender_medals'):
        df = self.data.groupby('gender')['medal_code'].count().reset_index(name='nb_medailles')
        self.subsets[subset_name] = df
        return df

    def slice_youngest_medalists(self, n=10, subset_name='youngest'):
        df = self.data.dropna(subset=['age_at_medal']).sort_values('age_at_medal').head(n)
        self.subsets[subset_name] = df
        return df

    def slice_oldest_medalists(self, n=10, subset_name='oldest'):
        df = self.data.dropna(subset=['age_at_medal']).sort_values('age_at_medal', ascending=False).head(n)
        self.subsets[subset_name] = df
        return df

    def slice_multi_discipline_athletes(self, min_disciplines=2, subset_name='multi_disc'):
        df = (
            self.data.groupby(['code_athlete', 'name', 'country_long'])['discipline']
            .nunique().reset_index(name='nb_disciplines')
            .query(f"nb_disciplines >= {min_disciplines}")
            .sort_values("nb_disciplines", ascending=False)
        )
        self.subsets[subset_name] = df
        return df

    def plot_medals_by_gender(self):
        if 'gender_medals' not in self.subsets:
            self.slice_by_gender_medals()

        df = self.subsets['gender_medals']
        fig = px.bar(
            df, x='gender', y='nb_medailles',
            title='Nombre de médailles par genre',
            color='gender',
            color_discrete_map={'M': 'skyblue', 'F': 'lightcoral'}
        )
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    def plot_age_distribution(self, bins=20):
        st.caption("Distribution des âges")
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=self.data['age_at_medal'].dropna(),
            nbinsx=bins,
            marker_color='skyblue'
        ))
        fig.update_layout(
            xaxis_title="Âge", yaxis_title="Fréquence", showlegend=False, height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_youngest_oldest_comparison(self, n=10):
        if 'youngest' not in self.subsets:
            self.slice_youngest_medalists(n)
        if 'oldest' not in self.subsets:
            self.slice_oldest_medalists(n)

        col1, col2 = st.columns(2)
        for col, title, key in [(col1, "Top jeunes", 'youngest'), (col2, "Top vieux", 'oldest')]:
            with col:
                df = self.subsets[key].copy()
                df['Nom'] = df['name'].apply(lambda x: f"{x[:20]}..." if len(x) > 20 else x)
                df = df.rename(columns={'age_at_medal': 'Âge', 'discipline': 'Discipline', 'country_long': 'Pays'})
                st.caption(f"{title} médaillés")
                st.dataframe(df[['Nom', 'Âge', 'Discipline', 'Pays']].reset_index(drop=True), use_container_width=True)

    def plot_medals_by_country(self, top_n=10):
        df = (
            self.data.groupby(['country_long', 'medal_code'])['medal_code']
            .count().unstack(fill_value=0).reset_index()
        )

        df = df.rename(columns={1: 'Or', 2: 'Argent', 3: 'Bronze', 'country_long': 'Pays'})
        
        for col in ['Or', 'Argent', 'Bronze']:
            if col not in df.columns:
                df[col] = 0

        df['Total'] = df[['Or', 'Argent', 'Bronze']].sum(axis=1)
        df = df.sort_values('Total', ascending=False).head(top_n)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['Or'], y=df['Pays'], name='Or', orientation='h',
            marker_color='gold'
            ))
        fig.add_trace(go.Bar(
            x=df['Argent'], y=df['Pays'], name='Argent', orientation='h',
            marker_color='silver'
        ))
        fig.add_trace(go.Bar(
            x=df['Bronze'], y=df['Pays'], name='Bronze', orientation='h',
            marker_color='saddlebrown'
        ))

        fig.update_layout(
            barmode='stack',
            title=f'Top {top_n} pays par nombre de médailles',
            xaxis_title='Nombre de médailles',
            yaxis={'categoryorder': 'total ascending'},
            height=max(400, top_n * 40)
        )

        st.plotly_chart(fig, use_container_width=True)


    def plot_medals_by_discipline(self, top_n=10):
        df = (
            self.data.groupby('discipline')['medal_code']
            .count().sort_values(ascending=False).head(top_n).reset_index()
        )
        df.columns = ['Discipline', 'Nombre_medailles']
        fig = px.bar(
            df, x='Discipline', y='Nombre_medailles',
            title='Médailles par discipline',
            color_discrete_sequence=['lightgreen']
        )
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        fig.update_layout(showlegend=False, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

    def plot_medals_by_discipline_by_countries(self, top_n=10):
        df = self.data.copy()
        top_disc = df['discipline'].value_counts().head(top_n).index
        df = df[df['discipline'].isin(top_disc)]

        df_count = df.groupby(['discipline', 'country_long'])['medal_code'].count().unstack(fill_value=0).reset_index()
        fig = px.bar(
            df_count, x='discipline', y=df_count.columns[1:], barmode='group',
            title='Médailles par discipline et pays'
        )
        fig.update_layout(xaxis_tickangle=-45, height=max(400, top_n * 40))
        st.plotly_chart(fig, use_container_width=True)

    def display_graphs(self):
        n_countries = st.sidebar.slider("Nombre de pays", 5, 25, 10)
        self.plot_medals_by_country(top_n=n_countries)

        n_disciplines = st.sidebar.slider("Nombre de disciplines", 5, 20, 10)
        self.plot_medals_by_discipline(top_n=n_disciplines)

    def display_age(self):
        col1, col2 = st.columns([1, 2])
        with col1:
            bins = st.sidebar.slider("Bins histogramme", 10, 50, 20)
            self.plot_age_distribution(bins=bins)
        with col2:
            n = st.sidebar.slider("Top âges", 5, 20, 10)
            self.plot_youngest_oldest_comparison(n=n)

    def display_compare(self):
        n = st.sidebar.slider("Top disciplines", 5, 20, 10)
        self.plot_medals_by_discipline_by_countries(top_n=n)

    def get_ranking(self, countries: List[str]):
        counts = self.data['country_long'].value_counts()
        return {country: int(counts.rank(ascending=False).get(country, float('nan'))) for country in countries}
