import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
from components.chart import create_stock_chart
from components.metrics import display_metrics, create_financials_table
from utils import get_stock_data, download_csv

# Page configuration
st.set_page_config(
    page_title="Stock Data Dashboard",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("📈 Stock Data Dashboard")
st.markdown("""
    Enter a stock symbol to view real-time data, financial metrics, and interactive charts.
    Data provided by Yahoo Finance.
""")

# Input section
col1, col2 = st.columns([2, 1])
with col1:
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL").upper()
with col2:
    period = st.selectbox(
        "Select Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2
    )

try:
    # Fetch stock data
    stock_data = get_stock_data(symbol, period)
    
    if stock_data is not None:
        # Display current price and basic info
        info = yf.Ticker(symbol).info
        company_name = info.get('longName', symbol)
        
        # Header metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Current Price",
                f"${stock_data['Close'].iloc[-1]:.2f}",
                f"{((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]) / stock_data['Close'].iloc[-2] * 100):.2f}%"
            )
        with col2:
            st.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,.0f}")
        with col3:
            st.metric("Market Cap", f"${info.get('marketCap', 0):,.0f}")

        # Create and display stock price chart
        fig = create_stock_chart(stock_data, company_name)
        st.plotly_chart(fig, use_container_width=True)
        
        # Get and display dividend history
        dividend_data = get_dividend_data(symbol)
        if dividend_data is not None:
            dividend_fig = create_dividend_chart(dividend_data, company_name)
            if dividend_fig:
                st.subheader("Dividend History")
                st.plotly_chart(dividend_fig, use_container_width=True)
        else:
            st.info("No dividend history available for this stock.")

        # Financial metrics
        st.subheader("Financial Metrics")
        metrics_df = display_metrics(symbol)
        
        # Financial statements
        st.subheader("Financial Statements")
        financials_df = create_financials_table(symbol)
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            download_csv(stock_data, f"{symbol}_price_data")
        with col2:
            download_csv(financials_df, f"{symbol}_financials")

    else:
        st.error("Unable to fetch data for the specified symbol.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check the stock symbol and try again.")
