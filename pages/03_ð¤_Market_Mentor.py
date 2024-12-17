import streamlit as st
from components.chatbot import display_chatbot, suggest_topics
from components.auth import init_session_state, display_login_form, login_required

# Page configuration
st.set_page_config(
    page_title="Stock Market Mentor",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
init_session_state()

# Title and description
st.title("🤖 Stock Market Mentor")
st.markdown("""
Welcome to your personal AI Stock Market Mentor! Get instant answers to your questions
about investing, trading, and financial markets. Whether you're a beginner or an
experienced investor, I'm here to help you learn and grow.
""")

# Display login form or chatbot based on authentication
if st.session_state.user:
    suggested_query = suggest_topics()
    if suggested_query:
        st.session_state.chat_history = []  # Reset chat for new topic
    display_chatbot()
else:
    st.info("Please log in to chat with your Stock Market Mentor!")
    display_login_form()
