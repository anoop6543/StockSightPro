import streamlit as st
from openai import OpenAI
import os
from typing import List, Dict, Any

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_mentor_response(user_message: str, chat_history: List[Dict[str, str]] = None) -> str:
    """
    Get AI mentor response using OpenAI's API.
    
    Args:
        user_message: User's question or message
        chat_history: Optional list of previous messages
    
    Returns:
        AI mentor's response
    """
    try:
        # Prepare the conversation context
        messages = [
            {
                "role": "system",
                "content": """You are a knowledgeable Stock Market Mentor, an expert in financial markets 
                and investing. Your role is to:
                1. Explain complex financial concepts in simple terms
                2. Provide practical investing advice and best practices
                3. Help users understand market analysis
                4. Guide users in developing their investment strategy
                
                Keep responses concise (max 3-4 sentences) unless asked for detailed explanations.
                Always maintain a supportive, educational tone."""
            }
        ]
        
        # Add chat history if provided
        if chat_history:
            messages.extend(chat_history[-5:])  # Keep last 5 messages for context
        
        # Add user's current message
        messages.append({"role": "user", "content": user_message})
        
        # Get response from OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error getting mentor response: {str(e)}")
        return "I apologize, but I'm having trouble responding right now. Please try again."

def display_chatbot():
    """Display the Stock Market Mentor chatbot interface"""
    st.subheader("🤖 Stock Market Mentor")
    st.markdown("""
    Ask me anything about stock markets, investing, or trading! I'm here to help you learn
    and understand financial concepts better.
    """)
    
    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write("You: " + message["content"])
        else:
            st.write("🤖 Mentor: " + message["content"])
    
    # Chat input
    user_message = st.chat_input("Ask your question here...")
    
    if user_message:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        
        # Get and display AI response
        mentor_response = get_mentor_response(user_message, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": mentor_response})
        
        # Force a rerun to update the chat display
        st.rerun()

def suggest_topics():
    """Suggest learning topics based on user's progress"""
    suggested_topics = {
        "📈 Technical Analysis Basics": "Technical Analysis Basics",
        "💼 Portfolio Diversification": "Portfolio Diversification",
        "📊 Understanding Financial Ratios": "Understanding Financial Ratios",
        "🏢 Fundamental Analysis": "Fundamental Analysis",
        "📉 Risk Management": "Risk Management",
        "💰 Value Investing Principles": "Value Investing Principles"
    }
    
    st.sidebar.markdown("### 📚 Suggested Topics")
    for display_text, topic_name in suggested_topics.items():
        if st.sidebar.button(display_text):
            query = f"Can you explain {topic_name} in simple terms?"
            return query
    return None