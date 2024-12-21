import streamlit as st
from components.games.price_prediction import run_price_prediction_game

# Page configuration
st.set_page_config(page_title="Financial Learning Games",
                   page_icon="🎮",
                   layout="wide")

# Title and description
st.title("🎮 Financial Learning Games")
st.markdown("""
Test your market knowledge and intuition with our interactive financial games!
Each game helps you learn different aspects of stock market trading and investing.
""")

# Input section for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL").upper()

# Run the price prediction game
run_price_prediction_game(symbol)

# Future games can be added here
st.markdown("---")
st.subheader("🔜 Coming Soon")
st.markdown("""
- 📊 Technical Analysis Quiz
- 💼 Portfolio Management Simulator
- 📈 Market Trend Analyzer
""")
