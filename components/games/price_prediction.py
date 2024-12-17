import streamlit as st
import yfinance as yf
import pandas as pd
import random
from datetime import datetime, timedelta

def run_price_prediction_game(symbol: str):
    """
    Run a stock price prediction mini-game where users guess if the stock price
    will go up or down in the next period.
    
    Args:
        symbol: Stock symbol to use for the game
    """
    st.subheader("🎮 Stock Price Prediction Game")
    st.markdown("""
    Test your market intuition! Look at the historical price chart and predict 
    whether the stock price will go UP ⬆️ or DOWN ⬇️ in the next period.
    
    **Rules:**
    - Correct prediction: +10 points
    - Wrong prediction: -5 points
    - Streak bonus: +5 points for each correct prediction in a row
    """)
    
    # Initialize session state for tracking scores and streaks
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
    
    # Get historical data
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period='1mo', interval='1d')
        
        if not hist.empty:
            # Display current score and streak
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Score", st.session_state.game_score)
            with col2:
                st.metric("Current Streak", st.session_state.streak)
            
            # Show historical price chart
            st.line_chart(hist['Close'])
            
            # Get prediction from user
            col1, col2 = st.columns(2)
            with col1:
                if st.button("⬆️ Price Will Go Up"):
                    make_prediction(True, hist)
            with col2:
                if st.button("⬇️ Price Will Go Down"):
                    make_prediction(False, hist)
            
            # Display achievement badges
            display_achievements()
            
        else:
            st.error("Unable to fetch stock data for the game.")
            
    except Exception as e:
        st.error(f"Error running the game: {str(e)}")

def make_prediction(prediction_up: bool, hist: pd.DataFrame):
    """Process the user's prediction and update score"""
    if len(hist) < 2:
        return
    
    # Compare last two closing prices
    actual_up = hist['Close'].iloc[-1] > hist['Close'].iloc[-2]
    
    # Update score based on prediction
    if prediction_up == actual_up:
        # Correct prediction
        st.session_state.streak += 1
        points = 10 + (5 * (st.session_state.streak - 1))  # Base points + streak bonus
        st.session_state.game_score += points
        st.success(f"🎯 Correct! You earned {points} points! Streak: {st.session_state.streak}")
    else:
        # Wrong prediction
        st.session_state.streak = 0
        st.session_state.game_score = max(0, st.session_state.game_score - 5)
        st.error("❌ Wrong prediction. Lost 5 points. Streak reset.")
    
    st.session_state.last_prediction = prediction_up

def display_achievements():
    """Display achievement badges based on score and streak"""
    st.markdown("---")
    st.subheader("🏆 Achievements")
    
    achievements = []
    
    # Score-based achievements
    if st.session_state.game_score >= 100:
        achievements.append("🌟 Market Master")
    elif st.session_state.game_score >= 50:
        achievements.append("📈 Rising Star")
    elif st.session_state.game_score >= 25:
        achievements.append("🎯 Market Novice")
    
    # Streak-based achievements
    if st.session_state.streak >= 5:
        achievements.append("🔥 Hot Streak")
    elif st.session_state.streak >= 3:
        achievements.append("⚡ Momentum Builder")
    
    if achievements:
        for achievement in achievements:
            st.markdown(f"### {achievement}")
    else:
        st.info("Keep playing to earn achievements!")
