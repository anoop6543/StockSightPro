import streamlit as st
from typing import Literal

def initialize_theme_state():
    """Initialize the theme state in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'

def inject_theme_transition_css():
    """Inject CSS for smooth theme transitions"""
    st.markdown(
        """
        <style>
        /* Smooth transition for all theme-affected elements */
        * {
            transition: background-color 0.3s ease, color 0.3s ease !important;
        }
        
        /* Dark mode specific styles */
        [data-theme="dark"] {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Light mode specific styles */
        [data-theme="light"] {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Custom toggle button styles */
        .theme-toggle {
            display: inline-flex;
            align-items: center;
            padding: 0.5rem 1rem;
            border-radius: 2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(128, 128, 128, 0.3);
        }
        
        .theme-toggle:hover {
            border-color: rgba(128, 128, 128, 0.5);
        }
        
        /* Smooth transition for charts and plots */
        .js-plotly-plot {
            transition: background-color 0.3s ease;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_theme_toggle():
    """Display the theme toggle button in the sidebar"""
    initialize_theme_state()
    inject_theme_transition_css()
    
    # Add theme toggle to sidebar
    with st.sidebar:
        st.markdown("### 🌓 Theme Settings")
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
        
        if st.button(f"{theme_icon} Switch to {theme_label}", key="theme_toggle"):
            toggle_theme()
            st.rerun()  # Rerun to apply theme changes
