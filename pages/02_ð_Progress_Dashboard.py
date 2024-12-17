import streamlit as st
from components.games.progress_tracker import display_progress_dashboard
from components.auth import init_session_state, display_login_form

# Page configuration
st.set_page_config(
    page_title="Learning Progress",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
init_session_state()

# Display the progress dashboard
display_progress_dashboard()
