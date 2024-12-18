import streamlit as st
import yfinance as yf
import pandas as pd
from openai import OpenAI
import os
from typing import List, Dict

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_recommendation(symbol: str) -> str:
    """
    Get AI-powered recommendation for a stock using OpenAI.
    
    Args:
        symbol: Stock symbol to analyze
    
    Returns:
        AI-generated recommendation
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Prepare context for AI
        context = (
            f"Stock: {info.get('longName', symbol)} ({symbol})\n"
            f"Current Price: ${info.get('currentPrice', 'N/A')}\n"
            f"52 Week Range: ${info.get('fiftyTwoWeekLow', 'N/A')} - ${info.get('fiftyTwoWeekHigh', 'N/A')}\n"
            f"P/E Ratio: {info.get('trailingPE', 'N/A')}\n"
            f"Market Cap: ${info.get('marketCap', 'N/A')}\n"
        )
        
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for better analysis
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional stock analyst. Provide a brief, actionable recommendation based on the given financial data. Focus on key metrics and current market position. Keep it under 100 words."
                },
                {
                    "role": "user",
                    "content": f"Analyze this stock and provide a recommendation:\n{context}"
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Unable to generate recommendation: {str(e)}"

def initialize_watchlist():
    """Initialize watchlist in session state if it doesn't exist"""
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
        st.session_state.recommendations = {}

def add_to_watchlist(symbol: str):
    """Add a stock to the watchlist and get its recommendation"""
    if symbol not in st.session_state.watchlist:
        st.session_state.watchlist.append(symbol)
        st.session_state.recommendations[symbol] = get_ai_recommendation(symbol)

def remove_from_watchlist(symbol: str):
    """Remove a stock from the watchlist"""
    if symbol in st.session_state.watchlist:
        st.session_state.watchlist.remove(symbol)
        st.session_state.recommendations.pop(symbol, None)

def display_watchlist():
    """Display the watchlist with AI recommendations"""
    initialize_watchlist()
    
    st.subheader("📋 Your Watchlist")
    
    # Add stock to watchlist with responsive layout
    if st.session_state.get('mobile_view', False):
        # Mobile: Stack vertically
        new_symbol = st.text_input(
            "Add Stock to Watchlist",
            key="new_watchlist_symbol",
            help="Enter a stock symbol to add to your watchlist"
        ).upper()
        if st.button("➕ Add to Watchlist", use_container_width=True) and new_symbol:
            add_to_watchlist(new_symbol)
    else:
        # Desktop: Side by side
        col1, col2 = st.columns([3, 1])
        with col1:
            new_symbol = st.text_input(
                "Add Stock to Watchlist",
                key="new_watchlist_symbol",
                help="Enter a stock symbol to add to your watchlist"
            ).upper()
        with col2:
            if st.button("Add to Watchlist") and new_symbol:
                add_to_watchlist(new_symbol)
    
    # Display watchlist
    if st.session_state.watchlist:
        for symbol in st.session_state.watchlist:
            try:
                stock = yf.Ticker(symbol)
                info = stock.info
                
                with st.expander(f"{info.get('longName', symbol)} ({symbol})"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.metric(
                            "Current Price",
                            f"${info.get('currentPrice', 'N/A')}",
                            f"{info.get('regularMarketChangePercent', 0):.2f}%"
                        )
                    with col2:
                        if st.button("Remove", key=f"remove_{symbol}"):
                            remove_from_watchlist(symbol)
                            st.rerun()
                    
                    st.markdown("### AI Recommendation")
                    if symbol in st.session_state.recommendations:
                        st.write(st.session_state.recommendations[symbol])
                    else:
                        st.session_state.recommendations[symbol] = get_ai_recommendation(symbol)
                        st.write(st.session_state.recommendations[symbol])
                    
            except Exception as e:
                st.error(f"Error loading data for {symbol}: {str(e)}")
    else:
        st.info("Your watchlist is empty. Add stocks to get AI-powered recommendations!")
