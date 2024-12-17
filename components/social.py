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
        linkedin_url = f"https://www.linkedin.com/sharing/share-offsite/?url=https://stock-analysis.com&summary={encoded_content}"
        st.link_button("Share on LinkedIn", linkedin_url)
    
    with col3:
        # Copy to clipboard button
        st.button("📋 Copy Analysis", help="Copy analysis to clipboard",
                 on_click=lambda: st.write(share_content))
