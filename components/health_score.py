import streamlit as st
import yfinance as yf
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@st.cache_data(ttl=3600)
def calculate_health_score(symbol: str) -> dict:
    """
    Calculate a financial health score using AI analysis of stock metrics.
    
    Args:
        symbol: Stock symbol
        
    Returns:
        Dictionary containing health score and analysis
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Prepare financial context for AI analysis
        context = {
            "symbol": symbol,
            "company_name": info.get("longName", symbol),
            "market_cap": info.get("marketCap", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "forward_pe": info.get("forwardPE", "N/A"),
            "price_to_book": info.get("priceToBook", "N/A"),
            "debt_to_equity": info.get("debtToEquity", "N/A"),
            "current_ratio": info.get("currentRatio", "N/A"),
            "return_on_equity": info.get("returnOnEquity", "N/A"),
            "profit_margins": info.get("profitMargins", "N/A"),
            "beta": info.get("beta", "N/A"),
            "dividend_yield": info.get("dividendYield", "N/A")
        }
        
        # Request AI analysis
        response = client.chat.completions.create(
            model="gpt-4",  # Using GPT-4 for reliable financial analysis
            messages=[
                {
                    "role": "system",
                    "content": """You are a financial analyst expert. Analyze the given metrics and provide:
                    1. A health score from 0-100
                    2. A brief analysis (max 100 words)
                    3. Key strengths (max 3)
                    4. Key risks (max 3)
                    
                    Respond in JSON format with these keys: score, analysis, strengths, risks"""
                },
                {
                    "role": "user",
                    "content": f"Analyze this company's financial health: {json.dumps(context)}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error calculating health score: {str(e)}")
        return None

def display_health_score(score_data: dict):
    """
    Display the financial health score and analysis in the Streamlit app.
    
    Args:
        score_data: Dictionary containing score and analysis
    """
    if not score_data:
        return
    
    # Create columns for layout
    score_col, analysis_col = st.columns([1, 2])
    
    # Display score with color coding
    with score_col:
        score = score_data.get('score', 0)
        color = (
            "🟢" if score >= 70 else
            "🟡" if score >= 50 else
            "🔴"
        )
        st.markdown(f"### Financial Health Score")
        st.markdown(f"# {color} {score}/100")
    
    # Display analysis
    with analysis_col:
        st.markdown("### Analysis")
        st.write(score_data.get('analysis', ''))
    
    # Display strengths and risks
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Key Strengths")
        for strength in score_data.get('strengths', []):
            st.markdown(f"✅ {strength}")
    
    with col2:
        st.markdown("### Key Risks")
        for risk in score_data.get('risks', []):
            st.markdown(f"⚠️ {risk}")
