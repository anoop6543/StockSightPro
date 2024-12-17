import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import psycopg2
from ..auth import get_db_connection, login_required

def get_user_progress(user_id: int):
    """Get user's game progress from database"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT game_name, points, correct_predictions, 
                           total_predictions, highest_streak
                    FROM game_progress 
                    WHERE user_id = %s
                """, (user_id,))
                return cur.fetchone() or (0, 0, 0, 0, 0)
    except psycopg2.Error as e:
        st.error(f"Error fetching progress: {str(e)}")
        return (0, 0, 0, 0, 0)

def update_progress(user_id: int, game_name: str, points: int, correct: bool = False):
    """Update user's progress in the database"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get current progress
                cur.execute("""
                    SELECT correct_predictions, total_predictions, highest_streak
                    FROM game_progress 
                    WHERE user_id = %s AND game_name = %s
                """, (user_id, game_name))
                result = cur.fetchone()
                
                if result:
                    correct_predictions, total_predictions, highest_streak = result
                    # Update existing record
                    cur.execute("""
                        UPDATE game_progress 
                        SET points = points + %s,
                            correct_predictions = correct_predictions + %s,
                            total_predictions = total_predictions + 1,
                            highest_streak = GREATEST(highest_streak, %s),
                            updated_at = CURRENT_TIMESTAMP
                        WHERE user_id = %s AND game_name = %s
                    """, (points, int(correct), st.session_state.get('streak', 0), user_id, game_name))
                else:
                    # Create new record
                    cur.execute("""
                        INSERT INTO game_progress 
                        (user_id, game_name, points, correct_predictions, 
                         total_predictions, highest_streak)
                        VALUES (%s, %s, %s, %s, 1, %s)
                    """, (user_id, game_name, points, int(correct), st.session_state.get('streak', 0)))
                
                conn.commit()
                check_achievements(user_id)
    except psycopg2.Error as e:
        st.error(f"Error updating progress: {str(e)}")

def get_user_achievements(user_id: int):
    """Get user's achievements from database"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT achievement_name, achieved_at
                    FROM achievements
                    WHERE user_id = %s
                    ORDER BY achieved_at DESC
                """, (user_id,))
                return cur.fetchall()
    except psycopg2.Error as e:
        st.error(f"Error fetching achievements: {str(e)}")
        return []

def check_achievements(user_id: int):
    """Check and award new achievements based on progress"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Get current progress
                cur.execute("""
                    SELECT SUM(points) as total_points,
                           SUM(correct_predictions) as total_correct,
                           SUM(total_predictions) as total_predictions,
                           MAX(highest_streak) as max_streak
                    FROM game_progress
                    WHERE user_id = %s
                """, (user_id,))
                progress = cur.fetchone()
                
                if not progress:
                    return
                
                total_points, total_correct, total_predictions, max_streak = progress
                
                # Define achievements criteria
                achievements = []
                if total_points >= 1000:
                    achievements.append("🏆 Market Maven")
                elif total_points >= 500:
                    achievements.append("📈 Trading Pro")
                elif total_points >= 100:
                    achievements.append("🎯 Market Novice")
                
                if total_correct >= 50 and total_correct/total_predictions >= 0.7:
                    achievements.append("🎓 Prediction Master")
                
                if max_streak >= 10:
                    achievements.append("🔥 Hot Streak Master")
                elif max_streak >= 5:
                    achievements.append("⚡ Momentum Builder")
                
                # Award new achievements
                for achievement in achievements:
                    cur.execute("""
                        INSERT INTO achievements (user_id, achievement_name)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id, achievement_name) DO NOTHING
                    """, (user_id, achievement))
                
                conn.commit()
    except psycopg2.Error as e:
        st.error(f"Error checking achievements: {str(e)}")

@login_required
def display_progress_dashboard():
    """Display the progress tracking dashboard"""
    if not st.session_state.user:
        return
    
    user_id = st.session_state.user['id']
    progress = get_user_progress(user_id)
    achievements = get_user_achievements(user_id)
    
    st.title("📊 Learning Progress Dashboard")
    st.subheader(f"Welcome, {st.session_state.user['username']}!")
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Points", progress[1])
    with col2:
        st.metric("Predictions Made", progress[3])
    with col3:
        st.metric("Highest Streak", progress[4])
    
    # Display achievements
    st.subheader("🏆 Achievements Unlocked")
    if achievements:
        achievement_cols = st.columns(2)
        for i, (achievement, achieved_at) in enumerate(achievements):
            with achievement_cols[i % 2]:
                st.markdown(f"### {achievement}")
                st.caption(f"Achieved on {achieved_at.strftime('%Y-%m-%d')}")
    else:
        st.info("Keep playing to earn achievements!")
    
    # Display accuracy metrics if available
    if progress[3] > 0:  # If there are predictions made
        accuracy = progress[2] / progress[3] * 100
        st.subheader("📈 Performance Metrics")
        
        accuracy_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=accuracy,
            title={'text': "Prediction Accuracy"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "gray"},
                    {'range': [75, 100], 'color': "darkgray"}
                ],
            }
        ))
        accuracy_fig.update_layout(height=300)
        st.plotly_chart(accuracy_fig, use_container_width=True)
