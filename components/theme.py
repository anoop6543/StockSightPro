import streamlit as st
from typing import Literal

def initialize_theme_state():
    """Initialize the theme state in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Apply theme-specific styles
    if st.session_state.theme == 'dark':
        st.markdown("""
            <style>
                :root {
                    --background-color: #0E1117;
                    --secondary-background-color: #1B1F27;
                    --text-color: #FAFAFA;
                }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                :root {
                    --background-color: #FFFFFF;
                    --secondary-background-color: #F0F2F6;
                    --text-color: #262730;
                }
            </style>
            """, unsafe_allow_html=True)

def toggle_theme():
    """Toggle between light and dark theme"""
    if st.session_state.theme == 'light':
        st.session_state.theme = 'dark'
    else:
        st.session_state.theme = 'light'
    st.query_params['theme'] = st.session_state.theme

def inject_theme_transition_css():
    """Inject CSS for smooth theme transitions"""
    st.markdown(
        """
        <style>
        /* Base theme transition */
        * {
            transition: all 0.3s ease-in-out !important;
        }
        
        /* Theme-specific styles */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        .stSidebar {
            background-color: var(--secondary-background-color);
        }
        
        /* Dark mode adjustments */
        [data-theme="dark"] .stButton>button {
            background-color: #262730;
            color: #FAFAFA;
            border-color: #4A4A4A;
        }
        
        [data-theme="dark"] .stTextInput>div>div>input {
            background-color: #262730;
            color: #FAFAFA;
        }
        
        /* Light mode adjustments */
        [data-theme="light"] .stButton>button {
            background-color: #FFFFFF;
            color: #262730;
            border-color: #E0E0E0;
        }
        
        /* Chart transitions */
        .js-plotly-plot {
            transition: background-color 0.3s ease-in-out;
        }
        
        /* Custom toggle button */
        .theme-toggle {
            padding: 0.5rem;
            border-radius: 2rem;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 1px solid rgba(128, 128, 128, 0.3);
            margin: 0.5rem 0;
        }
        
        .theme-toggle:hover {
            border-color: rgba(128, 128, 128, 0.5);
            transform: scale(1.02);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def display_theme_toggle():
    """Display the theme toggle button in the sidebar"""
    # Initialize theme state
    initialize_theme_state()
    
    # Get theme from URL parameters if available
    if 'theme' in st.query_params:
        st.session_state.theme = st.query_params['theme']
    
    # Inject CSS for theme transitions
    inject_theme_transition_css()
    
    # Add theme toggle to sidebar
    with st.sidebar:
        st.markdown("### 🌓 Theme Settings")
        theme_icon = "🌙" if st.session_state.theme == 'light' else "☀️"
        theme_label = "Dark Mode" if st.session_state.theme == 'light' else "Light Mode"
        
        if st.button(f"{theme_icon} Switch to {theme_label}", key="theme_toggle", 
                    help="Toggle between light and dark mode"):
            toggle_theme()
            st.rerun()  # Rerun to apply theme changes
