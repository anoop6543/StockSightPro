import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data(ttl=3600)
def get_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """
    Fetch stock data from Yahoo Finance with caching.
    
    Args:
        symbol: Stock symbol
        period: Time period for historical data
    
    Returns:
        DataFrame with stock price data
    """
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period=period)
        return df if not df.empty else None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def download_csv(df: pd.DataFrame, filename: str):
    """
    Create a download button for CSV export.
    
    Args:
        df: DataFrame to export
        filename: Name for the downloaded file
    """
    csv = df.to_csv(index=True)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )
