import streamlit as st
from pathlib import Path
import shutil
import time

# Set page config as the FIRST Streamlit command
st.set_page_config(page_title="Data Profiling & EDA", page_icon="📊", layout="wide")

# Custom CSS for Manrope font, centered layout, enhanced UI, and Material Icons
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    body, div, p, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText, .stDataFrame, .stSelectbox, .stMultiselect, .stRadio, .stNumberInput, .stColorPicker {
        font-family: 'Manrope', sans-serif !important;
    }
    .main { background-color: #f8fafc; padding: 24px; }
    .stContainer {
        max-width: 800px;
        margin: 0 auto;
        padding: 24px;
        margin-bottom: 32px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .sidebar .sidebar-content {
        width: 300px !important;
        background-color: #f1f5f9;
        border-right: 1px solid #e2e8f0;
        padding: 20px;
    }
    .sidebar h2 { font-size: 20px; font-weight: 700; color: #1e293b; margin-bottom: 16px; }
    .stFileUploader {
        border: 2px dashed #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        background-color: #f8fafc;
        transition: border-color 0.2s;
    }
    .stFileUploader:hover { border-color: #10b981; }
    .stFileUploader label button {
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        transition: background-color 0.2s !important;
    }
    .stFileUploader label button:hover {
        background-color: #0d8f6b !important;
    }
    h1 { color: #1e293b; font-weight: 700; font-size: 32px; }
    h2, h3 { color: #334155; font-weight: 500; }
    .stTag {
        background-color: #dbeafe;
        color: #1e40af;
        border-radius: 12px;
        padding: 6px 12px;
        font-size: 14px;
        display: inline-flex;
        align-items: center;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .success-box, .error-box, .warning-box, .info-box {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
        font-size: 14px;
    }
    .success-box { background-color: #ecfdf5; color: #064e3b; border: 1px solid #10b981; }
    .error-box { background-color: #fef2f2; color: #991b1b; border: 1px solid #ef4444; }
    .warning-box { background-color: #fefce8; color: #854d0e; border: 1px solid #eab308; }
    .info-box { background-color: #eff6ff; color: #1e40af; border: 1px solid #3b82f6; }
    .stButton>button {
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background-color: #222;
        color: white;
        border-color: #222;
    }
    .stFormSubmitButton>button {
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: none !important;
        transition: background-color 0.2s !important;
    }
    .stFormSubmitButton>button:hover {
        background-color: #0d8f6b !important;
    }
    .stSelectbox, .stMultiselect, .stRadio, .stNumberInput, .stColorPicker {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 8px;
    }
    .stNavigation > div > div > div > div {
        font-size: 14px !important;
        padding: 8px 12px !important;
        margin-bottom: 4px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .stNavigation > div > div > div > div > span {
        font-size: 14px !important;
    }
    .stNavigation [data-testid="stNavigation"] span:empty::before {
        content: "• ";
        color: #1e293b;
    }
    .material-icons {
        font-family: 'Material Icons';
        font-size: 14px;
        vertical-align: middle;
        margin-right: 4px;
    }
    .sidebar-footer {
        margin-top: 24px;
        text-align: center;
        border-top: 1px solid #e2e8f0;
        padding-top: 16px;
    }
    .material-icons.md-18 { font-size: 18px; }
    .material-icons.md-20 { font-size: 20px; }
    .material-icons.md-24 { font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'uploads_dir' not in st.session_state:
    st.session_state.uploads_dir = Path("data/uploads")
if 'df_list' not in st.session_state:
    st.session_state.df_list = []
if 'profilers' not in st.session_state:
    st.session_state.profilers = []
if 'logout_button_counter' not in st.session_state:
    st.session_state.logout_button_counter = 0

# Ensure uploads directory exists
st.session_state.uploads_dir.mkdir(parents=True, exist_ok=True)

# Define navigation with nested structure
pages = {
    "Your account": [
        st.Page("pages/welcome.py", title="Welcome", icon=":material/home:"),
    ],
    "Resources": [
        st.Page("pages/analyse_data.py", title="Analyze Data", icon=":material/insert_chart:"),
        st.Page("pages/compare_CSVs.py", title="Compare CSVs", icon=":material/compare:"),
    ],
}

# Sidebar
with st.sidebar:
    # Data Profiling & EDA header and image at the top
    st.header("Data Profiling & EDA")
    st.image("https://cdn3d.iconscout.com/3d/premium/thumb/data-mining-3d-icon-download-in-png-blend-fbx-gltf-file-formats--server-digital-analysis-pack-files-folders-icons-9316877.png?f=webp", width=200)
    st.markdown('<div class="sidebar-footer">', unsafe_allow_html=True)
    # User section
    st.subheader("User")
    pg = st.navigation(pages)
    for page in pages["Resources"]:
        page.disabled = not st.session_state.user
    # User info and logout
    if st.session_state.user:
        st.markdown(f"Logged in as: **{st.session_state.user}**")
        if st.button("Logout", key="logout_button"):
            shutil.rmtree(st.session_state.uploads_dir, ignore_errors=True)
            st.session_state.user = None
            st.session_state.df_list = []
            st.session_state.profilers = []
            st.session_state.uploads_dir.mkdir(parents=True, exist_ok=True)
            st.markdown(f'''
                <div class="success-box">
                    <span class="material-icons md-18">check_circle</span> Logged out successfully
                </div>
            ''', unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()
    else:
        st.markdown(f'''
            <div class="info-box">
                <span class="material-icons md-18">info</span> Please log in on the Welcome page
            </div>
        ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Run the navigation
pg.run()