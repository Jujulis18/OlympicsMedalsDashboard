import streamlit as st
from interface.filters import show_filters
from interface.kpi_cards import show_kpi_cards
from interface.country_map import show_country_map
from interface.table import show_table, show_age, show_graphs, show_compare

if 'page' not in st.session_state:
    st.session_state.page = 'page1'

def display_dashboard(df):
	if st.session_state.page == 'page1':
		st.set_page_config(layout="wide")
		st.title("Dashboard JO 2024")
		filters = show_filters(df)
		st.markdown("---")
		col1, col2 = st.columns([2,1])
		with col1:
			show_kpi_cards(df, filters)
			show_country_map(df, filters)
			show_age(df, filters)
		with col2:
			show_graphs(df, filters)
			col1, col2, col3 = st.columns([2, 2, 1])
			with col2:
				if st.button('Comparer les pays'):
					st.session_state.page = 'comparePage'
		show_table(df, filters)

	elif st.session_state.page == 'comparePage':
		st.set_page_config(layout="wide")
		if st.button('Back'):
			st.session_state.page = 'page1'
		st.title("Compare les pays")
		filters = show_filters(df)
		show_compare(df, filters)