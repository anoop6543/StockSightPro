import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import logging
import sys
from components.chart import create_stock_chart, create_dividend_chart
from components.metrics import display_metrics, create_financials_table
from components.watchlist import display_watchlist, get_ai_recommendation
from components.social import display_share_buttons
from components.health_score import calculate_health_score, display_health_score
from components.tutorial import check_and_display_tutorial
from components.auth import init_session_state, display_login_form
from components.theme import display_theme_toggle
from utils import get_stock_data, get_dividend_data, download_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set page config with proper base URL handling
try:
    st.set_page_config(
        page_title="Stock Data Dashboard",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    logger.info("Page configuration set successfully")
except Exception as e:
    logger.error(f"Error setting page config: {str(e)}")
    st.error("Error initializing page. Please refresh.")

# Initialize session state for user and theme
try:
    init_session_state()
    logger.info("Session state initialized successfully")
except Exception as e:
    logger.error(f"Error initializing session state: {str(e)}")
    st.error("Error initializing session. Please refresh.")
    st.stop()

# Title and description
st.title("📈 Stock Data Dashboard")
st.markdown("""
    Enter a stock symbol to view real-time data, financial metrics, and interactive charts.
    Data provided by Yahoo Finance.
""")

# Display login form if user is not authenticated
try:
    if not st.session_state.user:
        display_login_form()
    else:
        check_and_display_tutorial()
except Exception as e:
    logger.error(f"Error in authentication flow: {str(e)}")
    st.error("Authentication error. Please try again.")
    st.stop()

# Input section with responsive layout
try:
    if st.session_state.get('mobile_view', False):
        # Mobile layout: Stack inputs vertically
        symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL").upper()
        period = st.selectbox(
            "Select Time Period",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=2
        )
    else:
        # Desktop layout: Side by side
        col1, col2 = st.columns([2, 1])
        with col1:
            symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL").upper()
        with col2:
            period = st.selectbox(
                "Select Time Period",
                ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
                index=2
            )

    logger.info(f"User input received - Symbol: {symbol}, Period: {period}")
except Exception as e:
    logger.error(f"Error in input section: {str(e)}")
    st.error("Error processing inputs. Please try again.")
    st.stop()

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
        logger.info(f"Successfully fetched stock data for {symbol}")
        # Get stock info
        info = yf.Ticker(symbol).info
        company_name = info.get('longName', symbol)

        # Display metrics based on layout
        if st.session_state.get('mobile_view', False):
            st.metric(
                "Current Price",
                f"${stock_data['Close'].iloc[-1]:.2f}",
                f"{((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[-2]) / stock_data['Close'].iloc[-2] * 100):.2f}%"
            )
            st.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,.0f}")
            st.metric("Market Cap", f"${info.get('marketCap', 0):,.0f}")
        else:
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

        # Technical Indicators
        st.subheader("Technical Indicators")
        indicator_col1, indicator_col2 = st.columns(2)
        with indicator_col1:
            show_sma = st.checkbox("Moving Averages", value=True)
            show_bollinger = st.checkbox("Bollinger Bands")
        with indicator_col2:
            show_rsi = st.checkbox("RSI")
            show_macd = st.checkbox("MACD")

        show_indicators = {
            'sma': show_sma,
            'bollinger': show_bollinger,
            'rsi': show_rsi,
            'macd': show_macd
        }

        # Create and display charts
        fig = create_stock_chart(stock_data, company_name, show_indicators)
        st.plotly_chart(fig, use_container_width=True)

        # Display other components only if basic data loaded successfully
        dividend_data = get_dividend_data(symbol)
        if dividend_data is not None:
            dividend_fig = create_dividend_chart(dividend_data, company_name)
            if dividend_fig:
                st.subheader("Dividend History")
                st.plotly_chart(dividend_fig, use_container_width=True)

        # Financial metrics and statements
        metrics_df = display_metrics(symbol)
        st.subheader("Financial Statements")
        financials_df = create_financials_table(symbol)

        if not financials_df.empty:
            st.dataframe(financials_df.style.format("${:,.0f}"), use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                download_csv(stock_data, f"{symbol}_price_data")
            with col2:
                download_csv(financials_df, f"{symbol}_financials")

        # Additional components
        st.markdown("---")
        st.subheader("AI-Powered Financial Health Assessment")
        health_score_data = calculate_health_score(symbol)
        display_health_score(health_score_data)

        st.markdown("---")
        ai_rec = get_ai_recommendation(symbol)
        display_share_buttons(info, ai_rec)

        st.markdown("---")
        display_watchlist()

        if st.session_state.user:
            st.markdown("---")
            display_deployment_assistant()

    else:
        logger.warning(f"No data available for symbol: {symbol}")
        st.warning("Unable to fetch data for the specified symbol. Please check the symbol and try again.")

except Exception as e:
    logger.error(f"Error in main app execution: {str(e)}")
    st.error(f"An error occurred while loading the dashboard. Please try again.")
    st.stop()