import streamlit as st
from typing import Literal

def initialize_theme_state():
    """Initialize the theme state in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Apply theme-specific styles with enhanced color palette
    if st.session_state.theme == 'dark':
        st.markdown("""
            <style>
                :root {
                    /* Base colors */
                    --background-color: #0E1117;
                    --secondary-background-color: #1B1F27;
                    --text-color: #E6E9EF;
                    
                    /* UI Elements */
                    --card-background: #262730;
                    --input-background: #2C303A;
                    --border-color: #3B4252;
                    
                    /* Interactive Elements */
                    --primary-color: #6C8EEF;
                    --primary-hover: #7B9BF8;
                    --success-color: #4CAF50;
                    --warning-color: #FFA726;
                    --error-color: #EF5350;
                    
                    /* Data Visualization */
                    --chart-background: #1B1F27;
                    --grid-color: #3B4252;
                    --axis-color: #A0AEC0;
                    
                    /* Text Hierarchy */
                    --text-primary: #E6E9EF;
                    --text-secondary: #A0AEC0;
                    --text-disabled: #666B7A;
                }
            </style>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                :root {
                    /* Base colors */
                    --background-color: #FFFFFF;
                    --secondary-background-color: #F0F2F6;
                    --text-color: #262730;
                    
                    /* UI Elements */
                    --card-background: #FFFFFF;
                    --input-background: #FFFFFF;
                    --border-color: #E2E8F0;
                    
                    /* Interactive Elements */
                    --primary-color: #1F77B4;
                    --primary-hover: #2D87C4;
                    --success-color: #4CAF50;
                    --warning-color: #FF9800;
                    --error-color: #F44336;
                    
                    /* Data Visualization */
                    --chart-background: #FFFFFF;
                    --grid-color: #E2E8F0;
                    --axis-color: #718096;
                    
                    /* Text Hierarchy */
                    --text-primary: #262730;
                    --text-secondary: #4A5568;
                    --text-disabled: #A0AEC0;
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
        [data-theme="dark"] {
            /* Buttons */
            .stButton > button {
                background-color: var(--input-background);
                color: var(--text-primary);
                border: 1px solid var(--border-color);
                transition: all 0.2s ease;
            }
            .stButton > button:hover {
                background-color: var(--primary-color);
                color: var(--text-primary);
                border-color: var(--primary-color);
            }
            
            /* Inputs and Selects */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stTextArea > div > div > textarea {
                background-color: var(--input-background) !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border-color) !important;
            }
            
            /* DataFrames and Tables */
            .stDataFrame {
                background-color: var(--card-background);
                color: var(--text-primary);
            }
            .stDataFrame td {
                background-color: var(--secondary-background-color);
                color: var(--text-primary);
                border-color: var(--border-color);
            }
            
            /* Expanders */
            .streamlit-expanderHeader {
                background-color: var(--card-background) !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border-color);
            }
            .streamlit-expanderContent {
                background-color: var(--secondary-background-color) !important;
                color: var(--text-primary) !important;
                border: 1px solid var(--border-color);
            }
            
            /* Links */
            .stMarkdown a {
                color: var(--primary-color);
                text-decoration: none;
            }
            .stMarkdown a:hover {
                color: var(--primary-hover);
                text-decoration: underline;
            }
            
            /* Tooltips */
            .stTooltipIcon {
                color: var(--text-secondary) !important;
            }
            
            /* Progress Bars */
            .stProgress > div > div > div {
                background-color: var(--primary-color);
            }
            
            /* Metrics */
            .stMetric {
                background-color: var(--card-background);
                padding: 1rem;
                border-radius: 8px;
                border: 1px solid var(--border-color);
            }
            .stMetric label {
                color: var(--text-secondary) !important;
            }
            .stMetric .metric-value {
                color: var(--text-primary) !important;
            }
        }
        
        /* Light mode adjustments */
        [data-theme="light"] {
            /* Buttons */
            .stButton > button {
                background-color: var(--input-background);
                color: var(--text-primary);
                border: 1px solid var(--border-color);
                transition: all 0.2s ease;
            }
            .stButton > button:hover {
                background-color: var(--primary-color);
                color: white;
            }
            
            /* Inputs and Selects */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > select,
            .stTextArea > div > div > textarea {
                background-color: var(--input-background);
                color: var(--text-primary);
                border: 1px solid var(--border-color);
            }
        }
        
        /* Chart transitions */
        .js-plotly-plot {
            transition: background-color 0.3s ease-in-out;
        }
        
        [data-theme="dark"] .js-plotly-plot .plot-container {
            background-color: #1B1F27 !important;
        }
        
        [data-theme="dark"] .js-plotly-plot .main-svg {
            background-color: #1B1F27 !important;
        }
        
        /* Metrics styling */
        [data-theme="dark"] .stMetric {
            background-color: #262730;
            border-radius: 5px;
            padding: 10px;
        }
        
        [data-theme="dark"] .stMetric label {
            color: #FAFAFA !important;
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
