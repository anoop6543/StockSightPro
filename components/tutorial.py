import streamlit as st
from typing import Optional
import psycopg2
from .auth import get_db_connection
from .celebrations import trigger_celebration

def get_tutorial_state(user_id: int) -> tuple[bool, int]:
    """Get the user's tutorial completion status and current step"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT tutorial_completed, tutorial_step FROM users WHERE id = %s",
                    (user_id,)
                )
                result = cur.fetchone()
                return result if result else (False, 0)
    except Exception as e:
        st.error(f"Error fetching tutorial state: {str(e)}")
        return False, 0

def update_tutorial_state(user_id: int, completed: bool, step: int):
    """Update the user's tutorial progress"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users 
                    SET tutorial_completed = %s, tutorial_step = %s 
                    WHERE id = %s
                    """,
                    (completed, step, user_id)
                )
                conn.commit()
    except Exception as e:
        st.error(f"Error updating tutorial state: {str(e)}")

def display_tutorial_step(step: int) -> Optional[str]:
    """Display the current tutorial step and return the next route if navigation is needed"""
    next_route = None
    
    if step == 0:
        st.markdown("""
        # 👋 Welcome to Your Financial Learning Journey!
        
        Let's take a quick tour of the platform to help you get started.
        
        **What you'll learn:**
        - 📊 How to analyze stocks in real-time
        - 🎮 Play interactive learning games
        - 🤖 Get AI-powered market insights
        - 📈 Track your learning progress
        """)
        
        if st.button("Begin Tour 🚀"):
            return 1
            
    elif step == 1:
        st.markdown("""
        ## 📊 Stock Analysis Dashboard
        
        This is your main workspace for analyzing stocks:
        1. Enter any stock symbol (e.g., AAPL, GOOGL)
        2. View real-time price data and charts
        3. Check key financial metrics
        4. Get AI-powered health scores
        
        Try it out by entering a stock symbol above! ☝️
        """)
        
        if st.button("Next: Games & Learning 🎮"):
            next_route = "Financial_Games"
            return 2
            
    elif step == 2:
        st.markdown("""
        ## 🎮 Financial Learning Games
        
        Test your market knowledge through interactive games:
        - Predict price movements
        - Earn points and achievements
        - Build your prediction streak
        - Track your progress
        
        Try making your first prediction! 🎯
        """)
        
        if st.button("Next: Market Mentor 🤖"):
            next_route = "Market_Mentor"
            return 3
            
    elif step == 3:
        st.markdown("""
        ## 🤖 Your AI Market Mentor
        
        Get personalized help with:
        - Understanding market concepts
        - Analyzing stocks and trends
        - Learning investment strategies
        - Answering your questions
        
        Try asking your first question! 💭
        """)
        
        if st.button("Next: Progress Tracking 📊"):
            next_route = "Progress_Dashboard"
            return 4
            
    elif step == 4:
        st.markdown("""
        ## 📊 Track Your Progress
        
        Monitor your learning journey:
        - View earned achievements
        - Check prediction accuracy
        - Track learning streaks
        - Set new goals
        
        Your progress is automatically saved! 🎯
        """)
        
        if st.button("Complete Tutorial 🎉"):
            trigger_celebration(
                "🎓 Tutorial Complete",
                "You're ready to start your financial learning journey!"
            )
            return 5
            
    return None

def check_and_display_tutorial():
    """Check if tutorial should be shown and display it"""
    if not st.session_state.user:
        return
        
    user_id = st.session_state.user['id']
    tutorial_completed, current_step = get_tutorial_state(user_id)
    
    if not tutorial_completed:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📚 Tutorial Progress")
        progress = min(current_step / 4 * 100, 100)
        st.sidebar.progress(progress)
        
        next_step = display_tutorial_step(current_step)
        
        if next_step is not None:
            if next_step == 5:  # Tutorial completion
                update_tutorial_state(user_id, True, next_step)
            else:
                update_tutorial_state(user_id, False, next_step)
            st.rerun()
