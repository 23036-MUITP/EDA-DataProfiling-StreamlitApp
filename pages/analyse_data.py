import streamlit as st
import pandas as pd
from utils.data_utils import DataProfiler

st.markdown("""
    <head>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&display=swap');
    body { font-family: 'Manrope', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

st.title("Data Analysis")
if not st.session_state.user:
    st.error("Please log in from the Home page")
    st.stop()

if not st.session_state.df_list:
    st.warning("No datasets available. Please upload CSVs in CSV Comparison.")
else:
    selected_file = st.selectbox("Select a dataset", [name for name, _ in st.session_state.df_list])
    selected_df = next(df for name, df in st.session_state.df_list if name == selected_file)
    selected_profiler = next(p for name, p in st.session_state.profilers if name == selected_file)

    st.write(f"Rows: {len(selected_df)} | Columns: {len(selected_df.columns)} | Missing: {selected_df.isnull().sum().sum()}")
    st.dataframe(selected_df.head())

    st.subheader("Summary Statistics")
    stats = selected_profiler.get_summary_stats()
    st.dataframe(stats)
