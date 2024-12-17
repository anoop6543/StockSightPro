import streamlit as st
import yfinance as yf
import pandas as pd

@st.cache_data(ttl=3600)
def display_metrics(symbol: str) -> pd.DataFrame:
    """
    Display key financial metrics for the stock.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        DataFrame containing financial metrics
    """
    stock = yf.Ticker(symbol)
    info = stock.info
    
    metrics = {
        'Metric': [
            'P/E Ratio',
            'Forward P/E',
            'PEG Ratio',
            'Price to Book',
            'Price to Sales',
            'Dividend Yield (%)',
            'Beta',
            '52 Week High',
            '52 Week Low'
        ],
        'Value': [
            info.get('trailingPE', 'N/A'),
            info.get('forwardPE', 'N/A'),
            info.get('pegRatio', 'N/A'),
            info.get('priceToBook', 'N/A'),
            info.get('priceToSalesTrailing12Months', 'N/A'),
            info.get('dividendYield', 'N/A'),
            info.get('beta', 'N/A'),
            info.get('fiftyTwoWeekHigh', 'N/A'),
            info.get('fiftyTwoWeekLow', 'N/A')
        ]
    }
    
    df = pd.DataFrame(metrics)
    st.dataframe(df, use_container_width=True)
    return df

@st.cache_data(ttl=3600)
def create_financials_table(symbol: str) -> pd.DataFrame:
    """
    Create a table of financial statements data.
    
    Args:
        symbol: Stock symbol
    
    Returns:
        DataFrame containing financial statements
    """
    stock = yf.Ticker(symbol)
    
    # Get financial statements
    income_stmt = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    # Combine key metrics
    key_metrics = pd.concat([
        income_stmt.loc['Total Revenue'],
        income_stmt.loc['Net Income'],
        balance_sheet.loc['Total Assets'],
        balance_sheet.loc['Total Liabilities'],
        cash_flow.loc['Operating Cash Flow'],
        cash_flow.loc['Free Cash Flow']
    ])
    
    # Create and format DataFrame
    df = pd.DataFrame(key_metrics)
    df.index = ['Revenue', 'Net Income', 'Total Assets', 'Total Liabilities',
                'Operating Cash Flow', 'Free Cash Flow']
    
    st.dataframe(df.style.format("${:,.0f}"), use_container_width=True)
    return df