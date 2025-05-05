import streamlit as st
import pandas as pd
from utils.data_utils import DataProfiler
import time

# Load Material Icons and Manrope font, and add custom table styling
st.markdown("""
    <head>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    </head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&display=swap');
    body { font-family: 'Manrope', sans-serif !important; }
    .styled-table {
        border-collapse: collapse;
        width: 100%;
        background-color: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 16px;
    }
    .styled-table th, .styled-table td {
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid #e2e8f0;
        font-family: 'Manrope', sans-serif;
        font-size: 14px;
    }
    .styled-table th {
        background-color: #f1f5f9;
        color: #1e293b;
        font-weight: 700;
    }
    .styled-table td {
        color: #334155;
    }
    .styled-table tr:last-child td {
        border-bottom: none;
    }
    .styled-table tr:hover {
        background-color: #f8fafc;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.subheader("Compare CSVs")

# Check if user is logged in
if not st.session_state.user:
    st.markdown(f'''
        <div class="error-box">
            <span class="material-icons">error</span> Please log in from the Welcome page
        </div>
    ''', unsafe_allow_html=True)
    st.stop()

# File uploader for CSVs
with st.container():
    st.markdown("")
    st.markdown("")
    st.markdown(f'''
        <h5>
            <span class="material-icons">upload</span> Upload CSV Files
        </h5>
    ''', unsafe_allow_html=True)
    st.markdown("")
    uploaded_files = st.file_uploader("Upload CSV files to compare", type=["csv"], accept_multiple_files=True, key="compare_uploader")

# Process uploaded files only if they haven't been processed before
if uploaded_files:
    for uploaded_file in uploaded_files:
        if uploaded_file.name not in [name for name, _ in st.session_state.df_list]:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    df = pd.read_csv(uploaded_file)
                    profiler = DataProfiler(df)
                    file_path = st.session_state.uploads_dir / f"{st.session_state.user}_{uploaded_file.name}"
                    df.to_csv(file_path, index=False)
                    st.session_state.df_list.append((uploaded_file.name, df))
                    st.session_state.profilers.append((uploaded_file.name, profiler))
                    st.markdown(f'''
                        <div class="success-box">
                            <span class="material-icons">check_circle</span> Loaded {uploaded_file.name}
                        </div>
                    ''', unsafe_allow_html=True)
                    st.toast(f"Loaded {uploaded_file.name}")
                    time.sleep(1)
                except Exception as e:
                    st.markdown(f'''
                        <div class="error-box">
                            <span class="material-icons">error</span> Error processing {uploaded_file.name}: {e}
                        </div>
                    ''', unsafe_allow_html=True)
                    st.toast(f"Failed to load {uploaded_file.name}")
                    time.sleep(1)
st.markdown("")
# Check if there are enough datasets to compare
if len(st.session_state.df_list) < 2:
    st.markdown(f'''
        <div class="warning-box">
            <span class="material-icons">warning</span> Please upload at least two CSVs to compare.
        </div>
    ''', unsafe_allow_html=True)
else:
    # Select two datasets to compare
    with st.container():
        st.markdown(f'''
            <h3>
                <span class="material-icons">compare</span> Select Datasets to Compare
            </h3>
        ''', unsafe_allow_html=True)
        st.markdown("")
        file_options = [name for name, _ in st.session_state.df_list]
        file1 = st.selectbox("Select first dataset", file_options, key="file1")
        file2_options = [name for name in file_options if name != file1]
        st.markdown("")
        if file2_options:
            file2 = st.selectbox("Select second dataset", file2_options, key="file2")
        else:
            file2 = None

        if file1 and file2:
            df1 = next(df for name, df in st.session_state.df_list if name == file1)
            df2 = next(df for name, df in st.session_state.df_list if name == file2)

            # Comparison Metrics
            with st.container():
                st.markdown("")
                st.markdown("")
                st.markdown(f'''
                    <h3>
                        <span class="material-icons">table_chart</span> Comparison Metrics
                    </h3>
                ''', unsafe_allow_html=True)
                st.markdown("")
                metrics_data = pd.DataFrame({
                    "Metric": ["Rows", "Columns", "Missing Values", "Common Columns"],
                    file1: [len(df1), len(df1.columns), df1.isnull().sum().sum(), len(set(df1.columns) & set(df2.columns))],
                    file2: [len(df2), len(df2.columns), df2.isnull().sum().sum(), len(set(df1.columns) & set(df2.columns))]
                })
                st.markdown('<table class="styled-table"><tr><th>Metric</th><th>{}</th><th>{}</th></tr>'.format(file1, file2) +
                            ''.join(f'<tr><td>{row["Metric"]}</td><td>{row[file1]}</td><td>{row[file2]}</td></tr>'
                                    for _, row in metrics_data.iterrows()) +
                            '</table>', unsafe_allow_html=True)
                st.markdown("")

            # Display the datasets
            with st.container():
                st.markdown("")
                st.markdown(f'''
                    <h3>
                        <span class="material-icons">dataset</span> Datasets Preview
                    </h3>
                ''', unsafe_allow_html=True)
                st.markdown("")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**{file1}**")
                    st.dataframe(df1.head(), use_container_width=True)
                with col2:
                    st.markdown(f"**{file2}**")
                    st.dataframe(df2.head(), use_container_width=True)