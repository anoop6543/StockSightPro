import streamlit as st
import time

def trigger_celebration(achievement_name: str, description: str):
    """
    Display an animated celebration when a user earns an achievement
    
    Args:
        achievement_name: Name of the achievement earned
        description: Description of the achievement
    """
    # Create a container for the celebration animation
    celebration_container = st.empty()
    
    # Display the celebration with CSS animation
    celebration_container.markdown(
        f"""
        <div class="celebration-wrapper" style="
            text-align: center;
            padding: 20px;
            animation: slideIn 1s ease-out, fadeOut 1s ease-out 4s;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin: 20px 0;
        ">
            <div style="
                font-size: 2em;
                margin-bottom: 10px;
                animation: bounce 1s infinite;
            ">
                🎉 Achievement Unlocked! 🎉
            </div>
            <div style="
                font-size: 1.5em;
                color: #444;
                margin-bottom: 10px;
                animation: fadeIn 1s ease-out;
            ">
                {achievement_name}
            </div>
            <div style="
                color: #666;
                animation: fadeIn 1s ease-out 0.5s;
            ">
                {description}
            </div>
        </div>
        <style>
            @keyframes slideIn {{
                from {{ transform: translateY(-100%); opacity: 0; }}
                to {{ transform: translateY(0); opacity: 1; }}
            }}
            @keyframes fadeOut {{
                from {{ opacity: 1; }}
                to {{ opacity: 0; }}
            }}
            @keyframes bounce {{
                0%, 100% {{ transform: translateY(0); }}
                50% {{ transform: translateY(-10px); }}
            }}
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
            .celebration-wrapper {{
                position: relative;
                z-index: 1000;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Remove the celebration after 5 seconds
    time.sleep(5)
    celebration_container.empty()

def display_milestone_animation(points: int, milestone: int):
    """
    Display an animated celebration for reaching point milestones
    
    Args:
        points: Current points
        milestone: Milestone point value reached
    """
    milestone_container = st.empty()
    
    milestone_container.markdown(
        f"""
        <div class="milestone-celebration" style="
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #6C5CE7, #a393eb);
            border-radius: 20px;
            color: white;
            margin: 20px 0;
            animation: scaleIn 0.5s ease-out, glow 2s infinite;
            box-shadow: 0 0 20px rgba(108,92,231,0.5);
        ">
            <div style="
                font-size: 2.5em;
                margin-bottom: 15px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">
                🌟 Milestone Reached! 🌟
            </div>
            <div style="
                font-size: 2em;
                margin-bottom: 10px;
                animation: pulse 1s infinite;
            ">
                {points} Points
            </div>
            <div style="font-size: 1.2em;">
                Congratulations on reaching {milestone} points!
            </div>
        </div>
        <style>
            @keyframes scaleIn {
                from { transform: scale(0); opacity: 0; }
                to { transform: scale(1); opacity: 1; }
            }
            @keyframes glow {
                0%, 100% { box-shadow: 0 0 20px rgba(108,92,231,0.5); }
                50% { box-shadow: 0 0 40px rgba(108,92,231,0.8); }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Remove the milestone celebration after 6 seconds
    time.sleep(6)
    milestone_container.empty()
