import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plost
from utils.data_utils import DataProfiler
from streamlit_extras.badges import badge
from streamlit_extras.switch_page_button import switch_page
import os
import shutil
from pathlib import Path

# Set page config as the first Streamlit command
st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for light-themed UI with Manrope font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&display=swap');
    body, div, p, span, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stDataFrame, .stMetric, .stSelectbox, .stMultiselect, .stRadio, .stNumberInput, .stColorPicker {
        font-family: 'Manrope', sans-serif !important;
    }
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #10b981; color: white; border-radius: 8px; padding: 8px 16px; }
    .stFileUploader { border: 2px dashed #e2e8f0; border-radius: 8px; padding: 12px; background-color: #ffffff; }
    .metric-card { background-color: #ffffff; padding: 12px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    h1 { color: #1e293b; font-weight: 700; }
    h2, h3 { color: #334155; }
    .sidebar .sidebar-content { background-color: #f1f5f9; border-right: 1px solid #e2e8f0; }
    .stTag { background-color: #dbeafe; color: #1e40af; border-radius: 12px; padding: 6px 12px; font-size: 14px; }
    .stContainer { padding: 16px; margin-bottom: 16px; border-radius: 8px; background-color: #ffffff; }
    .stTabs [role="tab"] { background-color: #e2e8f0; border-radius: 6px; margin-right: 4px; }
    .stTabs [role="tab"][aria-selected="true"] { background-color: #10b981; color: white; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'df_list' not in st.session_state:
    st.session_state.df_list = []
if 'profilers' not in st.session_state:
    st.session_state.profilers = []
if 'uploads_dir' not in st.session_state:
    st.session_state.uploads_dir = Path("data/uploads")

# Ensure uploads directory exists
st.session_state.uploads_dir.mkdir(parents=True, exist_ok=True)


# Login/Logout
def login():
    with st.form("login_form"):
        username = st.text_input("Username", help="Enter your username")
        submit = st.form_submit_button("Login")
        if submit and username:
            st.session_state.user = username
            st.success(f"Welcome, {username}! 🎉")
            st.rerun()


def logout():
    shutil.rmtree(st.session_state.uploads_dir, ignore_errors=True)
    st.session_state.user = None
    st.session_state.df_list = []
    st.session_state.profilers = []
    st.session_state.uploads_dir.mkdir(parents=True, exist_ok=True)
    st.success("Logged out successfully! 👋")
    st.rerun()


# Sidebar Navigation
with st.sidebar:
    st.header("📋 Data Explorer")
    badge(type="github", name="your-repo/data-explorer", url="https://github.com/your-repo/data-explorer")
    st.image("https://via.placeholder.com/150", caption="Data Explorer")
    with st.container():
        if st.session_state.user:
            st.write(f"Logged in as: **{st.session_state.user}**")
            if st.button("Logout", key="logout"):
                logout()
        else:
            st.write("Please log in to access features.")
            login()

    st.markdown("**Navigation**")
    page = st.radio("Go to", ["Home", "Data Analysis", "CSV Comparison"], label_visibility="collapsed")
    if page == "Data Analysis":
        switch_page("Data Analysis")
    elif page == "CSV Comparison":
        switch_page("CSV Comparison")

# Main Page: Home
if page == "Home" or not st.session_state.user:
    with st.container():
        st.title("🌟 Welcome to Data Explorer")
        st.markdown("""
        Analyze and compare CSV files with an intuitive interface. Features include:
        - 📂 Upload and store CSVs
        - 📈 Interactive data profiling
        - 📊 Advanced visualizations
        - 🔍 Compare multiple datasets
        """)
        st.markdown("**Log in to start exploring your data!**")
        st.markdown("**Tags**")
        st.markdown(
            '<span class="stTag">Data Analysis</span> <span class="stTag">EDA</span> <span class="stTag">Visualization</span>',
            unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("Built with Streamlit | v1.0", unsafe_allow_html=True)

# Data Analysis Page
elif page == "Data Analysis" and st.session_state.user:
    with st.container():
        st.title("📊 Data Analysis")
        st.markdown(f"Welcome, {st.session_state.user}! Upload CSVs to analyze.")

        # File Upload Section
        with st.container():
            st.subheader("📂 Upload CSVs")
            uploaded_files = st.file_uploader(
                "Choose CSV files",
                type=["csv"],
                accept_multiple_files=True,
                help="Upload one or more CSV files."
            )
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
                            st.toast(f"Loaded {uploaded_file.name} successfully! 🎉", icon="✅")
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                            st.toast(f"Failed to load {uploaded_file.name}", icon="❌")

        # Dataset Selection
        if st.session_state.df_list:
            with st.container():
                st.subheader("📋 Uploaded Datasets")
                selected_file = st.selectbox("Select a dataset", [name for name, _ in st.session_state.df_list])

                # Robust dataset selection
                selected_df = None
                selected_profiler = None
                for name, df in st.session_state.df_list:
                    if name == selected_file:
                        selected_df = df
                        break
                for name, profiler in st.session_state.profilers:
                    if name == selected_file:
                        selected_profiler = profiler
                        break

                if selected_df is None or selected_profiler is None:
                    st.error("Selected dataset not found. Please try uploading again.")
                    st.session_state.df_list = [(name, df) for name, df in st.session_state.df_list if
                                                name != selected_file]
                    st.session_state.profilers = [(name, p) for name, p in st.session_state.profilers if
                                                  name != selected_file]
                    st.rerun()
                else:
                    # Quick Metrics
                    with st.container():
                        st.subheader("Quick Stats")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rows", len(selected_df), delta_color="off")
                        with col2:
                            st.metric("Columns", len(selected_df.columns), delta_color="off")
                        with col3:
                            st.metric("Missing Values", selected_df.isnull().sum().sum(), delta_color="inverse")

                    # Data Overview and Statistics
                    with st.container():
                        tab1, tab2, tab3 = st.tabs(["📋 Overview", "📉 Statistics", "📊 Visualizations"])

                        # Tab 1: Overview
                        with tab1:
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                with st.expander("Dataset Info", expanded=True):
                                    st.text(selected_profiler.get_basic_info())
                            with col2:
                                with st.expander("Sample Data", expanded=True):
                                    st.data_editor(
                                        selected_df.head(),
                                        column_config={
                                            col: st.column_config.Column(
                                                disabled=True,
                                                help=f"Column {col}"
                                            ) for col in selected_df.columns
                                        },
                                        use_container_width=True
                                    )
                            with st.expander("Missing Values"):
                                missing_data = selected_profiler.get_missing_values()
                                st.dataframe(missing_data, use_container_width=True)
                                if missing_data['Missing Count'].sum() == 0:
                                    st.info("No missing values! 🎉")
                                else:
                                    st.warning(f"Found {missing_data['Missing Count'].sum()} missing values.")

                        # Tab 2: Statistics
                        with tab2:
                            stats = selected_profiler.get_summary_stats()
                            st.dataframe(stats, use_container_width=True)
                            st.download_button(
                                label="📥 Download Statistics",
                                data=stats.to_csv(index=True),
                                file_name=f"{selected_file}_stats.csv",
                                mime="text/csv"
                            )

                        # Tab 3: Visualizations
                        with tab3:
                            numeric_cols = selected_profiler.get_numeric_columns()
                            if numeric_cols:
                                with st.container():
                                    st.subheader("Visualization Options")
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        selected_cols = st.multiselect("Select columns", numeric_cols,
                                                                       default=[numeric_cols[0]])
                                        plot_type = st.radio("Plot type",
                                                             ["Histogram", "Box Plot", "KDE", "Scatter", "Plost Donut"],
                                                             horizontal=True)
                                    with col2:
                                        if plot_type in ["Histogram", "KDE"]:
                                            bins = st.number_input("Bins", 10, 100, 30, label_visibility="collapsed")
                                        if plot_type == "Scatter":
                                            x_col = st.selectbox("X-axis", numeric_cols, label_visibility="collapsed")
                                            y_col = st.selectbox("Y-axis",
                                                                 [col for col in numeric_cols if col != x_col],
                                                                 label_visibility="collapsed")
                                        color = st.color_picker("Color", "#10b981", label_visibility="collapsed")

                                with st.container():
                                    for col in selected_cols:
                                        st.subheader(f"{plot_type} of {col}")
                                        if plot_type in ["Histogram", "Box Plot", "KDE"]:
                                            fig, ax = plt.subplots(figsize=(8, 5))
                                            if plot_type == "Histogram":
                                                sns.histplot(data=selected_df, x=col, bins=bins, color=color, ax=ax)
                                            elif plot_type == "Box Plot":
                                                sns.boxplot(data=selected_df, y=col, color=color, ax=ax)
                                            else:
                                                sns.kdeplot(data=selected_df, x=col, color=color, ax=ax)
                                            st.pyplot(fig, use_container_width=True)
                                        elif plot_type == "Scatter":
                                            fig = px.scatter(selected_df, x=x_col, y=y_col,
                                                             color_discrete_sequence=[color])
                                            st.plotly_chart(fig, use_container_width=True)
                                        elif plot_type == "Plost Donut":
                                            value_counts = selected_df[col].value_counts().reset_index()
                                            value_counts.columns = ['value', 'count']
                                            plost.donut_chart(
                                                data=value_counts,
                                                theta='count',
                                                color='value',
                                                title=f"Donut Chart of {col}",
                                                use_container_width=True
                                            )
                            else:
                                st.error("No numeric columns available.")

# CSV Comparison Page
elif page == "CSV Comparison" and st.session_state.user:
    with st.container():
        st.title("🔍 CSV Comparison")
        if len(st.session_state.df_list) < 2:
            st.warning("Upload at least two CSVs to compare.")
        else:
            st.subheader("Select CSVs to Compare")
            selected_files = st.multiselect(
                "Choose datasets",
                [name for name, _ in st.session_state.df_list],
                default=[name for name, _ in st.session_state.df_list[:2]]
            )
            if len(selected_files) == 2:
                df1 = None
                df2 = None
                for name, df in st.session_state.df_list:
                    if name == selected_files[0]:
                        df1 = df
                    elif name == selected_files[1]:
                        df2 = df
                if df1 is None or df2 is None:
                    st.error("One or both selected datasets not found.")
                else:
                    with st.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**{selected_files[0]}**")
                            st.dataframe(df1.head(), use_container_width=True)
                        with col2:
                            st.write(f"**{selected_files[1]}**")
                            st.dataframe(df2.head(), use_container_width=True)
                        st.subheader("Shape Comparison")
                        st.write(f"{selected_files[0]}: {df1.shape}")
                        st.write(f"{selected_files[1]}: {df2.shape}")
                        st.subheader("Common Columns")
                        common_cols = set(df1.columns).intersection(set(df2.columns))
                        st.write(common_cols)
            else:
                st.warning("Select exactly two CSVs to compare.")