import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

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

    def format_value(value):
        """Helper function to format values properly"""
        if pd.isna(value) or value == 'N/A':
            return np.nan
        try:
            return float(value)
        except (ValueError, TypeError):
            return np.nan

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
            format_value(info.get('trailingPE')),
            format_value(info.get('forwardPE')),
            format_value(info.get('pegRatio')),
            format_value(info.get('priceToBook')),
            format_value(info.get('priceToSalesTrailing12Months')),
            format_value(info.get('dividendYield')),
            format_value(info.get('beta')),
            format_value(info.get('fiftyTwoWeekHigh')),
            format_value(info.get('fiftyTwoWeekLow'))
        ]
    }

    df = pd.DataFrame(metrics)

    # Create a styled dataframe with proper formatting
    styled_df = df.copy()
    styled_df['Value'] = styled_df['Value'].apply(
        lambda x: 'N/A' if pd.isna(x) else f'{x:.2f}'
    )

    # Display the styled dataframe
    st.dataframe(styled_df, use_container_width=True)
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
    try:
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
                return pd.Series([np.nan] * len(statement.columns), index=statement.columns)
            except:
                return pd.Series([np.nan] * len(statement.columns), index=statement.columns)

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
        if metrics_data and metrics_index:
            df = pd.DataFrame(metrics_data, index=metrics_index)

            # Format the DataFrame, handling NaN values
            try:
                formatted_df = df.fillna('N/A')
                st.dataframe(
                    formatted_df.style.format(lambda x: 'N/A' if pd.isna(x) else f'${x:,.0f}'),
                    use_container_width=True
                )
            except Exception as e:
                st.warning(f"Some financial data might not be in the expected format: {str(e)}")
                st.dataframe(formatted_df, use_container_width=True)

            return df
        else:
            st.info("No financial statements data available for this stock.")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Error creating financial table: {str(e)}")
        return pd.DataFrame()