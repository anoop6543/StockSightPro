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
    
    # Initialize empty lists for metrics
    metrics_data = []
    metrics_index = []
    
    # Helper function to safely get financial data
    def safe_get_metric(statement, metric_name):
        try:
            if metric_name in statement.index:
                return statement.loc[metric_name]
            return pd.Series([None] * len(statement.columns), index=statement.columns)
        except:
            return pd.Series([None] * len(statement.columns), index=statement.columns)
    
    # Safely get each metric
    metrics = [
        ('Revenue', income_stmt, 'Total Revenue'),
        ('Net Income', income_stmt, 'Net Income'),
        ('Total Assets', balance_sheet, 'Total Assets'),
        ('Total Liabilities', balance_sheet, 'Total Liabilities Net Minority Interest'),
        ('Operating Cash Flow', cash_flow, 'Operating Cash Flow'),
        ('Free Cash Flow', cash_flow, 'Free Cash Flow')
    ]
    
    for display_name, statement, metric_name in metrics:
        metric_data = safe_get_metric(statement, metric_name)
        if not metric_data.empty and not all(pd.isna(metric_data)):
            metrics_data.append(metric_data)
            metrics_index.append(display_name)
    
    # Create DataFrame only if we have data
    if metrics_data:
        key_metrics = pd.concat(metrics_data, axis=0)
        key_metrics.index = metrics_index
    else:
        # Create empty DataFrame with same structure
        key_metrics = pd.DataFrame(columns=income_stmt.columns)
    
    # Create and format DataFrame
    df = pd.DataFrame(key_metrics)
    df.index = ['Revenue', 'Net Income', 'Total Assets', 'Total Liabilities',
                'Operating Cash Flow', 'Free Cash Flow']
    
    st.dataframe(df.style.format("${:,.0f}"), use_container_width=True)
    return df
