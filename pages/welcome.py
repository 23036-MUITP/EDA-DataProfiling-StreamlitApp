import streamlit as st
import time

# Page content for Welcome
with st.container():
    if not st.session_state.user:
        st.markdown(f'''
            <h4>
                <span class="material-icons md-24">login</span> Login
            </h4>
        ''', unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Username", help="Enter your username")
            submit = st.form_submit_button("Login")
            if submit and username:
                st.session_state.user = username
                st.markdown(f'''
                    <div class="success-box">
                        <span class="material-icons md-18">check_circle</span> Welcome, {username}
                    </div>
                ''', unsafe_allow_html=True)
                time.sleep(1)
                st.rerun()
    else:
        st.subheader(f"Welcome, **{st.session_state.user}**!")
        st.markdown("")
        st.markdown("")
        st.markdown("**Features Include:**")
        st.markdown("")
        st.markdown("""
            <p><span class="material-icons md-20">upload</span> Upload and store CSVs</p>
            <p><span class="material-icons md-20">insights</span> Interactive data profiling</p>
            <p><span class="material-icons md-20">bar_chart</span> Advanced visualizations</p>
            <p><span class="material-icons md-20">compare</span> Compare multiple datasets</p>
        """, unsafe_allow_html=True)
        st.markdown("")
        st.markdown("")
        st.markdown("")
        st.markdown("**Tags:**")
        st.markdown("")
        st.markdown(f'''
            <span class="stTag">
                <span class="material-icons md-18">tag</span> Data Analysis
            </span>
            <span class="stTag">
                <span class="material-icons md-18">bar_chart</span> EDA
            </span>
            <span class="stTag">
                <span class="material-icons md-18">visibility</span> Visualization
            </span>
        ''', unsafe_allow_html=True)
        st.markdown("")
    st.markdown("---")