import streamlit as st
from typing import Dict, Any
import urllib.parse

def create_share_content(stock_info: Dict[str, Any], ai_recommendation: str = None) -> str:
    """
    Create formatted content for social sharing.
    
    Args:
        stock_info: Dictionary containing stock information
        ai_recommendation: Optional AI recommendation text
    
    Returns:
        Formatted text for sharing
    """
    content = f"""
📈 Stock Analysis: {stock_info.get('longName', '')} (${stock_info.get('symbol', '')})

Current Price: ${stock_info.get('currentPrice', 'N/A')}
Change: {stock_info.get('regularMarketChangePercent', 0):.2f}%
Market Cap: ${stock_info.get('marketCap', 0):,.0f}

Key Metrics:
• P/E Ratio: {stock_info.get('trailingPE', 'N/A')}
• 52W Range: ${stock_info.get('fiftyTwoWeekLow', 'N/A')} - ${stock_info.get('fiftyTwoWeekHigh', 'N/A')}
"""
    if ai_recommendation:
        content += f"\n🤖 AI Recommendation:\n{ai_recommendation}"
    
    return content

def display_share_buttons(stock_info: Dict[str, Any], ai_recommendation: str = None):
    """
    Display social sharing buttons for stock insights.
    
    Args:
        stock_info: Dictionary containing stock information
        ai_recommendation: Optional AI recommendation text
    """
    share_content = create_share_content(stock_info, ai_recommendation)
    encoded_content = urllib.parse.quote(share_content)
    
    st.subheader("📱 Share this Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        twitter_url = f"https://twitter.com/intent/tweet?text={encoded_content}"
        st.link_button("Share on Twitter", twitter_url)
    
    with col2:
        # Structure LinkedIn URL with required parameters
        linkedin_title = urllib.parse.quote(f"Stock Analysis: {stock_info.get('symbol', '')}")
        linkedin_url = (
            "https://www.linkedin.com/shareArticle?"
            f"mini=true&"
            f"url={urllib.parse.quote('https://stock-analysis.com')}&"
            f"title={linkedin_title}&"
            f"summary={encoded_content}"
        )
        st.link_button("Share on LinkedIn", linkedin_url)
    
    with col3:
        # Create a container for the copy button and success message
        copy_container = st.container()
        with copy_container:
            if st.button("📋 Copy Analysis", help="Copy analysis to clipboard"):
                # Use JavaScript to copy to clipboard
                js_code = f"""
                    <script>
                    navigator.clipboard.writeText(`{share_content.replace('`', '\\`')}`);
                    </script>
                """
                st.markdown(js_code, unsafe_allow_html=True)
                st.success("Analysis copied to clipboard!")
