import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def initialize_progress_state():
    """Initialize progress tracking in session state"""
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'achievements' not in st.session_state:
        st.session_state.achievements = set()
    if 'total_predictions' not in st.session_state:
        st.session_state.total_predictions = 0
    if 'correct_predictions' not in st.session_state:
        st.session_state.correct_predictions = 0
    if 'highest_streak' not in st.session_state:
        st.session_state.highest_streak = 0
    if 'total_points' not in st.session_state:
        st.session_state.total_points = 0

def update_progress(game_name: str, points: int, correct: bool = False):
    """Update user's progress with new game results"""
    initialize_progress_state()
    
    # Update game history
    st.session_state.game_history.append({
        'timestamp': datetime.now(),
        'game': game_name,
        'points': points,
        'correct': correct
    })
    
    # Update statistics
    st.session_state.total_predictions += 1
    if correct:
        st.session_state.correct_predictions += 1
    st.session_state.total_points += points
    
    # Update highest streak if current streak is higher
    if 'streak' in st.session_state:
        st.session_state.highest_streak = max(
            st.session_state.highest_streak,
            st.session_state.streak
        )
    
    # Check for new achievements
    check_achievements()

def check_achievements():
    """Check and award new achievements based on progress"""
    achievements = st.session_state.achievements
    
    # Point-based achievements
    if st.session_state.total_points >= 1000 and "🏆 Market Maven" not in achievements:
        achievements.add("🏆 Market Maven")
    elif st.session_state.total_points >= 500 and "📈 Trading Pro" not in achievements:
        achievements.add("📈 Trading Pro")
    elif st.session_state.total_points >= 100 and "🎯 Market Novice" not in achievements:
        achievements.add("🎯 Market Novice")
    
    # Accuracy-based achievements
    if (st.session_state.correct_predictions >= 50 and 
        st.session_state.correct_predictions / st.session_state.total_predictions >= 0.7 and
        "🎓 Prediction Master" not in achievements):
        achievements.add("🎓 Prediction Master")
    
    # Streak-based achievements
    if st.session_state.highest_streak >= 10 and "🔥 Hot Streak Master" not in achievements:
        achievements.add("🔥 Hot Streak Master")
    elif st.session_state.highest_streak >= 5 and "⚡ Momentum Builder" not in achievements:
        achievements.add("⚡ Momentum Builder")

def create_progress_charts():
    """Create visualizations for progress tracking"""
    if not st.session_state.game_history:
        return None, None
    
    # Convert game history to DataFrame
    history_df = pd.DataFrame(st.session_state.game_history)
    
    # Points over time chart
    points_fig = go.Figure()
    points_fig.add_trace(go.Scatter(
        x=history_df['timestamp'],
        y=history_df['points'].cumsum(),
        mode='lines+markers',
        name='Total Points',
        line=dict(color='#1f77b4')
    ))
    points_fig.update_layout(
        title='Points Progress Over Time',
        xaxis_title='Date',
        yaxis_title='Total Points',
        template='plotly_white'
    )
    
    # Accuracy chart
    accuracy = st.session_state.correct_predictions / st.session_state.total_predictions
    accuracy_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=accuracy * 100,
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
    
    return points_fig, accuracy_fig

def display_progress_dashboard():
    """Display the progress tracking dashboard"""
    initialize_progress_state()
    
    st.title("📊 Learning Progress Dashboard")
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Points", st.session_state.total_points)
    with col2:
        st.metric("Predictions Made", st.session_state.total_predictions)
    with col3:
        st.metric("Highest Streak", st.session_state.highest_streak)
    
    # Display charts
    points_fig, accuracy_fig = create_progress_charts()
    if points_fig and accuracy_fig:
        st.plotly_chart(points_fig, use_container_width=True)
        st.plotly_chart(accuracy_fig, use_container_width=True)
    else:
        st.info("Start playing games to see your progress charts!")
    
    # Display achievements
    st.subheader("🏆 Achievements Unlocked")
    if st.session_state.achievements:
        achievement_cols = st.columns(2)
        for i, achievement in enumerate(sorted(st.session_state.achievements)):
            with achievement_cols[i % 2]:
                st.markdown(f"### {achievement}")
    else:
        st.info("Keep playing to earn achievements!")
    
    # Display recent activity
    if st.session_state.game_history:
        st.subheader("📝 Recent Activity")
        recent_history = st.session_state.game_history[-5:]  # Show last 5 activities
        for entry in reversed(recent_history):
            st.markdown(
                f"**{entry['game']}** - "
                f"{'✅' if entry['correct'] else '❌'} "
                f"Points: {entry['points']} "
                f"({entry['timestamp'].strftime('%Y-%m-%d %H:%M')})"
            )
