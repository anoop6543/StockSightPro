import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
from components.chart import create_stock_chart, create_dividend_chart
from components.metrics import display_metrics, create_financials_table
from components.watchlist import display_watchlist, get_ai_recommendation
from components.social import display_share_buttons
from components.health_score import calculate_health_score, display_health_score
from components.tutorial import check_and_display_tutorial
from components.auth import init_session_state, display_login_form
from components.theme import display_theme_toggle
from utils import get_stock_data, get_dividend_data, download_csv
from components.deployment_assistant import display_deployment_assistant

# Set page config with proper base URL handling
st.set_page_config(
    page_title="Stock Data Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Initialize session state for user and theme
init_session_state()

# Display login form if user is not authenticated
if not st.session_state.user:
    display_login_form()
else:
    check_and_display_tutorial()

# Title and description
st.title("📈 Stock Data Dashboard")
st.markdown("""
    Enter a stock symbol to view real-time data, financial metrics, and interactive charts.
    Data provided by Yahoo Finance.
""")

# Input section with responsive layout
if st.session_state.get('mobile_view', False):
    # Mobile layout: Stack inputs vertically
    symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL", 
                          help="Enter a valid stock symbol").upper()
    period = st.selectbox(
        "Select Time Period",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2,
        help="Choose the time period for analysis"
    )
else:
    # Desktop layout: Side by side
    col1, col2 = st.columns([2, 1])
    with col1:
        symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL",
                              help="Enter a valid stock symbol").upper()
    with col2:
        period = st.selectbox(
            "Select Time Period",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=2,
            help="Choose the time period for analysis"
        )

# Add responsive layout and theme toggles in sidebar
with st.sidebar:
    st.session_state.mobile_view = st.checkbox("📱 Mobile View", 
                                             value=st.session_state.get('mobile_view', False))
    st.markdown("---")
    display_theme_toggle()

try:
    # Fetch stock data
    stock_data = get_stock_data(symbol, period)

    if stock_data is not None:
        # Display current price and basic info
        info = yf.Ticker(symbol).info
        company_name = info.get('longName', symbol)

        # Header metrics with responsive layout
        if st.session_state.get('mobile_view', False):
            # Mobile: Stack metrics vertically with larger touch targets
            st.metric(
                "Current Price",
                f"${stock_data['Close'].iloc[-1]:.2f}",
                f"{((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]) / stock_data['Close'].iloc[-2] * 100):.2f}%",
                help="Latest stock price and daily change"
            )
            st.metric(
                "Volume",
                f"{stock_data['Volume'].iloc[-1]:,.0f}",
                help="Trading volume"
            )
            st.metric(
                "Market Cap",
                f"${info.get('marketCap', 0):,.0f}",
                help="Total market capitalization"
            )
        else:
            # Desktop: Show metrics in columns
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Current Price",
                    f"${stock_data['Close'].iloc[-1]:.2f}",
                    f"{((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]) / stock_data['Close'].iloc[-2] * 100):.2f}%",
                    help="Latest stock price and daily change"
                )
            with col2:
                st.metric(
                    "Volume",
                    f"{stock_data['Volume'].iloc[-1]:,.0f}",
                    help="Trading volume"
                )
            with col3:
                st.metric(
                    "Market Cap", 
                    f"${info.get('marketCap', 0):,.0f}",
                    help="Total market capitalization"
                )

        # Technical Indicators Selection
        st.subheader("Technical Indicators")
        indicator_col1, indicator_col2 = st.columns(2)

        with indicator_col1:
            show_sma = st.checkbox("Moving Averages", value=True, help="Show 20, 50, and 200-day Simple Moving Averages")
            show_bollinger = st.checkbox("Bollinger Bands", help="Show Bollinger Bands (20-day, 2 standard deviations)")

        with indicator_col2:
            show_rsi = st.checkbox("RSI", help="Show Relative Strength Index")
            show_macd = st.checkbox("MACD", help="Show Moving Average Convergence Divergence")

        # Create and display stock price chart with selected indicators
        show_indicators = {
            'sma': show_sma,
            'bollinger': show_bollinger,
            'rsi': show_rsi,
            'macd': show_macd
        }

        fig = create_stock_chart(stock_data, company_name, show_indicators)
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

        if not financials_df.empty:
            st.dataframe(financials_df.style.format("${:,.0f}"), use_container_width=True)

            # Download buttons
            col1, col2 = st.columns(2)
            with col1:
                download_csv(stock_data, f"{symbol}_price_data")
            with col2:
                download_csv(financials_df, f"{symbol}_financials")
        else:
            st.info("Financial statements are not available for this stock.")

        # Financial Health Score
        st.markdown("---")
        st.subheader("AI-Powered Financial Health Assessment")
        health_score_data = calculate_health_score(symbol)
        display_health_score(health_score_data)

        # Social sharing section
        st.markdown("---")
        ai_rec = get_ai_recommendation(symbol)
        display_share_buttons(info, ai_rec)

        # Display watchlist with AI recommendations
        st.markdown("---")
        display_watchlist()
        if st.session_state.user:  # Only show to logged-in users
            st.markdown("---")
            display_deployment_assistant()
    else:
        st.error("Unable to fetch data for the specified symbol.")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check the stock symbol and try again.")