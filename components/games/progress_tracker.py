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
                
                # Points-based achievements
                point_achievements = [
                    (5000, "🌟 Market Legend", "Earned 5,000+ points"),
                    (2500, "🏆 Market Maven", "Earned 2,500+ points"),
                    (1000, "📈 Trading Pro", "Earned 1,000+ points"),
                    (500, "🎯 Market Expert", "Earned 500+ points"),
                    (100, "🌱 Market Novice", "First 100 points")
                ]
                
                for points, badge, description in point_achievements:
                    if total_points >= points:
                        achievements.append((badge, description))
                        break
                
                # Accuracy-based achievements
                if total_predictions >= 20:  # Minimum predictions required
                    accuracy = total_correct / total_predictions
                    accuracy_achievements = [
                        (0.9, "🎓 Prediction Master", "90%+ prediction accuracy"),
                        (0.8, "🔮 Market Oracle", "80%+ prediction accuracy"),
                        (0.7, "📊 Analysis Expert", "70%+ prediction accuracy")
                    ]
                    
                    for acc, badge, description in accuracy_achievements:
                        if accuracy >= acc:
                            achievements.append((badge, description))
                            break
                
                # Streak-based achievements
                streak_achievements = [
                    (20, "🔥 Legendary Streak", "20+ correct predictions in a row"),
                    (10, "⚡ Hot Streak Master", "10+ correct predictions in a row"),
                    (5, "🎯 Momentum Builder", "5+ correct predictions in a row")
                ]
                
                for streak, badge, description in streak_achievements:
                    if max_streak >= streak:
                        achievements.append((badge, description))
                        break
                
                # Activity-based achievements
                if total_predictions >= 100:
                    achievements.append(("🌟 Market Veteran", "Made 100+ predictions"))
                elif total_predictions >= 50:
                    achievements.append(("📊 Market Analyst", "Made 50+ predictions"))
                elif total_predictions >= 10:
                    achievements.append(("🎮 Market Player", "Made 10+ predictions"))
                
                # Award new achievements
                for badge, description in achievements:
                    # Check if achievement already exists
                    cur.execute("""
                        INSERT INTO achievements (user_id, achievement_name)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id, achievement_name) DO NOTHING
                        RETURNING id
                    """, (user_id, badge))
                    
                    # If new achievement was inserted (not existing), trigger celebration
                    if cur.fetchone() is not None:
                        from ..celebrations import trigger_celebration
                        trigger_celebration(badge, description)
                
                conn.commit()
                
                # Check for point milestones
                if total_points >= 100 and total_points % 100 == 0:
                    from ..celebrations import display_milestone_animation
                    display_milestone_animation(total_points, total_points)
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
    st.subheader("🏆 Achievements Gallery")
    if achievements:
        # Create a grid layout for achievements
        achievement_cols = st.columns(3)
        for i, (achievement, achieved_at) in enumerate(achievements):
            with achievement_cols[i % 3]:
                # Create an achievement card with CSS styling
                st.markdown("""
                    <div style="
                        padding: 1rem;
                        border-radius: 10px;
                        background: linear-gradient(145deg, #f0f2f6, #ffffff);
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        margin-bottom: 1rem;
                        text-align: center;
                    ">
                        <h3 style="margin: 0; color: #1f77b4;">{}</h3>
                        <p style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">
                            Achieved on {}</p>
                    </div>
                """.format(
                    achievement,
                    achieved_at.strftime('%B %d, %Y')
                ), unsafe_allow_html=True)
        
        # Add a progress section
        st.markdown("---")
        st.subheader("🎯 Next Achievements")
        next_achievement_cols = st.columns(2)
        with next_achievement_cols[0]:
            points_to_next = 100
            for points, badge, desc in point_achievements:
                if progress[1] < points:
                    points_to_next = points - progress[1]
                    st.info(f"📈 {points_to_next} points to unlock: {badge}\n\n{desc}")
                    break
        
        with next_achievement_cols[1]:
            if progress[3] > 0:
                current_accuracy = (progress[2] / progress[3]) * 100
                st.info(f"Current Accuracy: {current_accuracy:.1f}%\n\nKeep improving to unlock more badges!")
            else:
                st.info("Make your first prediction to start earning accuracy badges!")
    else:
        st.info("""
        🎮 Start playing to earn achievements!
        
        Available badges include:
        • 🌱 Market Novice - Get started with your first 100 points
        • 📈 Trading Pro - Show your expertise
        • 🏆 Market Maven - Become a market master
        • 🔥 Hot Streak Master - Build impressive prediction streaks
        """)
    
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
