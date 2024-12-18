import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def calculate_technical_indicators(data: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate technical indicators for the given stock data.
    
    Args:
        data: DataFrame with OHLCV data
        
    Returns:
        DataFrame with technical indicators
    """
    df = data.copy()
    
    # Simple Moving Averages
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # Exponential Moving Averages
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    df['BB_Upper'] = df['BB_Middle'] + 2 * df['Close'].rolling(window=20).std()
    df['BB_Lower'] = df['BB_Middle'] - 2 * df['Close'].rolling(window=20).std()
    
    return df

def create_stock_chart(data: pd.DataFrame, company_name: str, show_indicators: dict = None) -> go.Figure:
    """
    Create an interactive stock chart using Plotly with technical indicators.
    
    Args:
        data: DataFrame containing stock price data
        company_name: Name of the company
        show_indicators: Dictionary of indicators to show
        
    Returns:
        Plotly figure object
    """
    # Calculate indicators
    df = calculate_technical_indicators(data)
    
    # Create subplots - main chart, RSI, MACD, Volume
    fig = make_subplots(rows=4, cols=1, 
                       shared_xaxes=True,
                       vertical_spacing=0.05,
                       row_heights=[0.5, 0.15, 0.15, 0.2])

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )
    
    # Add technical indicators if enabled
    if show_indicators:
        if show_indicators.get('sma'):
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='blue')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50', line=dict(color='orange')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200', line=dict(color='red')), row=1, col=1)
        
        if show_indicators.get('bollinger'):
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dash')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dash')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Middle'], name='BB Middle', line=dict(color='gray')), row=1, col=1)
        
        if show_indicators.get('rsi'):
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2)
        
        if show_indicators.get('macd'):
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')), row=3, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], name='Signal Line', line=dict(color='orange')), row=3, col=1)
            fig.add_trace(go.Bar(x=df.index, y=df['MACD_Histogram'], name='MACD Histogram'), row=3, col=1)

    # Volume bar chart
    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df['Volume'],
            name='Volume'
        ),
        row=4, col=1
    )

    # Update layout
    fig.update_layout(
        title=f"{company_name} Stock Price",
        yaxis_title="Price ($)",
        yaxis2_title="RSI",
        yaxis3_title="MACD",
        yaxis4_title="Volume",
        xaxis_rangeslider_visible=False,
        height=1000,
        showlegend=True,
        template="plotly_white"
    )

    # Add range selector
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    # Update y-axis labels and ranges
    fig.update_yaxes(title_text="Price ($)", row=1, col=1)
    if show_indicators and show_indicators.get('rsi'):
        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
    if show_indicators and show_indicators.get('macd'):
        fig.update_yaxes(title_text="MACD", row=3, col=1)
    fig.update_yaxes(title_text="Volume", row=4, col=1)

    return fig

def create_dividend_chart(dividend_data: pd.DataFrame, company_name: str) -> go.Figure:
    """
    Create an interactive dividend history chart using Plotly.
    
    Args:
        dividend_data: DataFrame containing dividend history
        company_name: Name of the company
    
    Returns:
        Plotly figure object
    """
    if dividend_data is None or dividend_data.empty:
        return None
        
    fig = go.Figure()
    
    # Add dividend amount trace
    fig.add_trace(
        go.Scatter(
            x=dividend_data.index,
            y=dividend_data,
            mode='lines+markers',
            name='Dividend Amount',
            line=dict(color='green'),
            hovertemplate='Date: %{x}<br>Dividend: $%{y:.4f}<extra></extra>'
        )
    )
    
    # Update layout
    fig.update_layout(
        title=f"{company_name} Dividend History",
        yaxis_title="Dividend Amount ($)",
        xaxis_title="Date",
        height=400,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig