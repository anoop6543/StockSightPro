import streamlit as st
from components.games.progress_tracker import display_progress_dashboard

# Page configuration
st.set_page_config(
    page_title="Learning Progress",
    page_icon="📊",
    layout="wide"
)

# Display the progress dashboard
display_progress_dashboard()
