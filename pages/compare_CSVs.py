import streamlit as st
import pandas as pd
from utils.data_utils import DataProfiler
import time

# ✅ Fix material icons with <link>
st.markdown("""
    <head>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&display=swap');
    body { font-family: 'Manrope', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

st.title("CSV Comparison")
if not st.session_state.user:
    st.error("Please log in from the Home page")
    st.stop()

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            try:
                df = pd.read_csv(uploaded_file)
                profiler = DataProfiler(df)
                file_path = st.session_state.uploads_dir / f"{st.session_state.user}_{uploaded_file.name}"
                df.to_csv(file_path, index=False)
                st.session_state.df_list.append((uploaded_file.name, df))
                st.session_state.profilers.append((uploaded_file.name, profiler))
                st.success(f"Loaded {uploaded_file.name}")
                st.toast(f"Loaded {uploaded_file.name}")
                time.sleep(1)
            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {e}")
                st.toast(f"Failed to load {uploaded_file.name}")
                time.sleep(1)
    st.rerun()

if len(st.session_state.df_list) < 2:
    st.warning("Upload at least two CSVs to compare")
else:
    selected_files = st.multiselect("Choose 2 datasets to compare", [name for name, _ in st.session_state.df_list])
    if len(selected_files) == 2:
        df1 = next(df for name, df in st.session_state.df_list if name == selected_files[0])
        df2 = next(df for name, df in st.session_state.df_list if name == selected_files[1])
        st.subheader(f"Comparing {selected_files[0]} and {selected_files[1]}")
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df1.head())
        with col2:
            st.dataframe(df2.head())
        st.write(f"Shape: {df1.shape} vs {df2.shape}")
        st.write(f"Common columns: {set(df1.columns).intersection(set(df2.columns))}")
    else:
        st.info("Select exactly two CSVs to compare")
