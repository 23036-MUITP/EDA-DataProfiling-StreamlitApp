import streamlit as st
import pandas as pd
from utils.data_utils import DataProfiler

st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

if 'df' not in st.session_state:
    st.session_state.df = None
if 'profiler' not in st.session_state:
    st.session_state.profiler = None

st.title("Data Profiling & EDA")
with st.container():
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    try:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.profiler = DataProfiler(st.session_state.df)
        st.success(f"Loaded {uploaded_file.name}")
        with st.container():
            st.subheader("Dataset Info")
            st.text(st.session_state.profiler.get_basic_info())
            st.subheader("Summary Statistics")
            st.dataframe(st.session_state.profiler.get_summary_stats())
    except Exception as e:
        st.error(f"Error: {str(e)}")