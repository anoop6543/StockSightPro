import streamlit as st
from components.games.price_prediction import run_price_prediction_game
from components.auth import display_login_form, login_required

# Page configuration
st.set_page_config(
    page_title="Financial Learning Games",
    page_icon="🎮",
    layout="wide"
)

# Title and description
st.title("🎮 Financial Learning Games")
st.markdown("""
Test your market knowledge and intuition with our interactive financial games!
Each game helps you learn different aspects of stock market trading and investing.
""")

# Display login/register form
display_login_form()

# Only show games if user is logged in
if st.session_state.user:
    # Input section for stock symbol
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL").upper()
    
    # Run the price prediction game
    run_price_prediction_game(symbol)
    
    # Future games section
    st.markdown("---")
    st.subheader("🔜 Coming Soon")
    st.markdown("""
    - 📊 Technical Analysis Quiz
    - 💼 Portfolio Management Simulator
    - 📈 Market Trend Analyzer
    """)
else:
    st.info("Please log in to play the financial learning games and track your progress!")
