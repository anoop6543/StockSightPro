import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

def create_stock_chart(data: pd.DataFrame, company_name: str) -> go.Figure:
    """
    Create an interactive stock chart using Plotly.
    
    Args:
        data: DataFrame containing stock price data
        company_name: Name of the company
    
    Returns:
        Plotly figure object
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, 
                        row_heights=[0.7, 0.3])

    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='OHLC'
        ),
        row=1, col=1
    )

    # Volume bar chart
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data['Volume'],
            name='Volume'
        ),
        row=2, col=1
    )

    # Update layout
    fig.update_layout(
        title=f"{company_name} Stock Price",
        yaxis_title="Price ($)",
        yaxis2_title="Volume",
        xaxis_rangeslider_visible=False,
        height=800,
        showlegend=False,
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

    return fig
