import streamlit as st
import pandas as pd
import numpy as np
from utils.data_utils import DataProfiler
import time
import plotly.express as px
import plotly.graph_objects as go

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
st.subheader("Data Analysis")

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
    uploaded_files = st.file_uploader("Upload CSV files for analysis", type=["csv"], accept_multiple_files=True, key="analysis_uploader")

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

# Check if there are datasets available
if not st.session_state.df_list:
    st.markdown("")
    st.markdown("")
    st.markdown(f'''
        <div class="warning-box">
            <span class="material-icons">warning</span> No datasets available. Please upload CSVs above.
        </div>
    ''', unsafe_allow_html=True)
else:
    # Select dataset
    with st.container():
        st.markdown("")
        st.markdown(f'''
            <h3>
                <span class="material-icons">dataset</span> Select Dataset
            </h3>
        ''', unsafe_allow_html=True)
        selected_file = st.selectbox("Select a dataset", [name for name, _ in st.session_state.df_list])
        selected_df = next(df for name, df in st.session_state.df_list if name == selected_file)
        selected_profiler = next(p for name, p in st.session_state.profilers if name == selected_file)

    # Edit Data
    with st.container():
        st.markdown("")
        st.markdown("")
        st.markdown(f'''
            <h3>
                <span class="material-icons">edit</span> Edit Data
            </h3>
        ''', unsafe_allow_html=True)
        edited_df = st.data_editor(
            selected_df,
            use_container_width=True,
            column_config={
                col: st.column_config.Column(
                    help=f"Edit values in {col}",
                    disabled=False
                ) for col in selected_df.columns
            }
        )
        # Update session state with edited data
        for i, (name, df) in enumerate(st.session_state.df_list):
            if name == selected_file:
                st.session_state.df_list[i] = (name, edited_df)
                break
        st.download_button(
            label="Download Edited Data",
            data=edited_df.to_csv(index=False),
            file_name=f"{selected_file}_edited.csv",
            mime="text/csv"
        )

    # Data Overview
    with st.container():
        st.markdown("")
        st.markdown("")
        st.markdown(f'''
            <h3>
                <span class="material-icons">info</span> Data Overview
            </h3>
        ''', unsafe_allow_html=True)

        # Dataset Info
        with st.expander("Dataset Info", expanded=True):
            shape_data = pd.DataFrame({
                "Metric": ["Rows", "Columns", "Missing Values"],
                "Value": [len(edited_df), len(edited_df.columns), edited_df.isnull().sum().sum()]
            })
            st.markdown('<table class="styled-table"><tr><th>Metric</th><th>Value</th></tr>' +
                        ''.join(f'<tr><td>{row["Metric"]}</td><td>{row["Value"]}</td></tr>' for _, row in shape_data.iterrows()) +
                        '</table>', unsafe_allow_html=True)

        # Summary Statistics
        with st.expander("Summary Statistics"):
            st.markdown("")
            stats = selected_profiler.get_summary_stats()
            stats = stats.round(2)
            st.markdown('<table class="styled-table"><tr>' +
                        '<th>Statistic</th>' +
                        ''.join(f'<th>{col}</th>' for col in stats.columns) +
                        '</tr>' +
                        ''.join(f'<tr><td>{index}</td>' + ''.join(f'<td>{stats.loc[index, col]}</td>' for col in stats.columns) + '</tr>'
                                for index in stats.index) +
                        '</table>', unsafe_allow_html=True)

        # Missing Values
        with st.expander("Missing Values"):
            st.markdown("")
            missing_df = selected_profiler.get_missing_values()
            if missing_df.empty:
                st.markdown(f'''
                    <div class="info-box">
                        <span class="material-icons">info</span> No missing values found
                    </div>
                ''', unsafe_allow_html=True)
            else:
                missing_df["Missing Percent"] = missing_df["Missing Percent"].round(2)
                st.markdown('<table class="styled-table"><tr><th>Column</th><th>Missing Count</th><th>Missing Percent (%)</th></tr>' +
                            ''.join(f'<tr><td>{index}</td><td>{row["Missing Count"]}</td><td>{row["Missing Percent"]}</td></tr>'
                                    for index, row in missing_df.iterrows()) +
                            '</table>', unsafe_allow_html=True)

    # Visualizations with All Charts
    with st.container():
        st.markdown("")
        st.markdown("")
        st.markdown(f'''
            <h3>
                <span class="material-icons">bar_chart</span> Visualizations
            </h3>
        ''', unsafe_allow_html=True)

        st.markdown("")
        # Customization options
        st.markdown("#### Chart Customization")
        st.markdown("")
        chart_color = st.color_picker("Choose chart color", value="#10b981")
        st.markdown("")
        chart_width = st.slider("Chart Width (px)", 300, 1200, 800)
        st.markdown("")
        chart_height = st.slider("Chart Height (px)", 200, 800, 400)
        st.markdown("")
        st.markdown("")
        # Chart selection
        st.markdown("#### Select Chart Type")
        st.markdown("")
        chart_type = st.selectbox(
            "Choose a chart type",
            ["Histogram", "Box Plot", "Scatter", "Bar Chart", "Line Chart", "Pie Chart", "Area Chart", "Heatmap", "Donut Chart"]
        )
        # Numeric and categorical columns
        numeric_cols = selected_profiler.get_numeric_columns()

        categorical_cols = selected_profiler.get_categorical_columns()
        st.markdown("")
        # Chart-specific options
        if chart_type in ["Histogram", "Box Plot", "Line Chart", "Area Chart"]:
            selected_cols = st.multiselect("Select columns", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [])
        elif chart_type == "Scatter":
            x_col = st.selectbox("Select X-axis column", edited_df.columns)
            y_cols = st.multiselect("Select Y-axis columns", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [])
        elif chart_type == "Bar Chart":
            selected_cols = st.multiselect("Select columns", numeric_cols, default=[numeric_cols[0]] if numeric_cols else [])
            agg_func = st.selectbox("Aggregation", ["count", "mean", "sum"])
            if agg_func != "count":
                group_col = st.selectbox("Group by", categorical_cols)
        elif chart_type in ["Pie Chart", "Donut Chart"]:
            selected_cols = st.multiselect("Select columns", categorical_cols, default=[categorical_cols[0]] if categorical_cols else [])
        elif chart_type == "Heatmap":
            selected_cols = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:2] if len(numeric_cols) >= 2 else numeric_cols)
        st.markdown("")
        st.markdown("")
        # Plot the selected chart
        if chart_type == "Histogram":
            for col in selected_cols:
                st.markdown(f"**Histogram for {col}**")
                fig = px.histogram(
                    edited_df,
                    x=col,
                    nbins=30,
                    title=f"Distribution of {col}",
                    color_discrete_sequence=[chart_color],
                    template="plotly_white"
                )
                fig.update_layout(
                    xaxis_title=col,
                    yaxis_title="Count",
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)

        elif chart_type == "Box Plot":
            for col in selected_cols:
                st.markdown(f"**Box Plot for {col}**")
                fig = px.box(
                    edited_df,
                    y=col,
                    title=f"Box Plot of {col}",
                    color_discrete_sequence=[chart_color],
                    template="plotly_white"
                )
                fig.update_layout(
                    yaxis_title=col,
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)

        elif chart_type == "Scatter":
            if y_cols:
                st.markdown("**Scatter Plot**")
                fig = px.scatter(
                    edited_df,
                    x=x_col,
                    y=y_cols[0] if y_cols else None,
                    title=f"{x_col} vs {y_cols[0] if y_cols else ''}",
                    color_discrete_sequence=[chart_color],
                    template="plotly_white"
                )
                fig.update_layout(
                    xaxis_title=x_col,
                    yaxis_title=y_cols[0] if y_cols else '',
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)
            else:
                st.markdown(f'''
                    <div class="warning-box">
                        <span class="material-icons">warning</span> Select at least one Y-axis column
                    </div>
                ''', unsafe_allow_html=True)

        elif chart_type == "Bar Chart":
            for col in selected_cols:
                st.markdown(f"**Bar Chart for {col}**")
                if agg_func == "count":
                    value_counts = edited_df[col].value_counts().head(10)
                    fig = px.bar(
                        x=value_counts.values,
                        y=value_counts.index,
                        orientation='h',
                        title=f"Top 10 Values in {col}",
                        color_discrete_sequence=[chart_color],
                        template="plotly_white"
                    )
                else:
                    data = edited_df.groupby(group_col)[col].agg(agg_func).reset_index()
                    fig = px.bar(
                        x=data[col],
                        y=data[group_col],
                        orientation='h',
                        title=f"{agg_func.capitalize()} of {col} by {group_col}",
                        color_discrete_sequence=[chart_color],
                        template="plotly_white"
                    )
                fig.update_layout(
                    xaxis_title="Count" if agg_func == "count" else f"{agg_func.capitalize()} of {col}",
                    yaxis_title=col if agg_func == "count" else group_col,
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)

        elif chart_type == "Line Chart":
            for col in selected_cols:
                st.markdown(f"**Line Chart for {col}**")
                line_data = edited_df[[col]].dropna()
                line_data.index = range(len(line_data))
                st.line_chart(
                    line_data,
                    color=chart_color,
                    width=chart_width,
                    height=chart_height
                )

        elif chart_type == "Pie Chart":
            for col in selected_cols:
                st.markdown(f"**Pie Chart for {col}**")
                value_counts = edited_df[col].value_counts().head(10)
                fig = px.pie(
                    names=value_counts.index,
                    values=value_counts.values,
                    title=f"Proportion of Categories in {col}",
                    color_discrete_sequence=[chart_color] + px.colors.qualitative.Pastel[1:]
                )
                fig.update_layout(
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)

        elif chart_type == "Area Chart":
            for col in selected_cols:
                st.markdown(f"**Area Chart for {col}**")
                area_data = edited_df[[col]].dropna()
                area_data.index = range(len(area_data))
                st.area_chart(
                    area_data,
                    color=chart_color,
                    width=chart_width,
                    height=chart_height
                )

        elif chart_type == "Heatmap":
            if len(selected_cols) >= 2:
                st.markdown("**Correlation Heatmap**")
                corr = edited_df[selected_cols].corr()
                fig = px.imshow(
                    corr,
                    text_auto=True,
                    color_continuous_scale="RdBu_r",
                    zmin=-1,
                    zmax=1,
                    title="Correlation Heatmap"
                )
                fig.update_layout(
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)
            else:
                st.markdown(f'''
                    <div class="warning-box">
                        <span class="material-icons">warning</span> Select at least two columns for heatmap
                    </div>
                ''', unsafe_allow_html=True)

        elif chart_type == "Donut Chart":
            for col in selected_cols:
                st.markdown(f"**Donut Chart for {col}**")
                value_counts = edited_df[col].value_counts().head(10)
                fig = px.pie(
                    names=value_counts.index,
                    values=value_counts.values,
                    title=f"Proportion of Categories in {col}",
                    hole=0.4,
                    color_discrete_sequence=[chart_color] + px.colors.qualitative.Pastel[1:]
                )
                fig.update_layout(
                    title_x=0.5,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Manrope", size=14),
                    width=chart_width,
                    height=chart_height
                )
                st.plotly_chart(fig)