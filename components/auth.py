import os
import streamlit as st
import psycopg2
import bcrypt
from typing import Optional, Dict, Any
from datetime import datetime

# Database connection
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    """Create a database connection"""
    return psycopg2.connect(DATABASE_URL)

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a stored password against one provided by user"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(username: str, email: str, password: str) -> bool:
    """Register a new user"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                password_hash = hash_password(password)
                cur.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash)
                )
                conn.commit()
                return True
    except psycopg2.Error as e:
        st.error(f"Registration failed: {str(e)}")
        return False

def login_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate a user and return their data"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, password_hash FROM users WHERE username = %s",
                    (username,)
                )
                user_data = cur.fetchone()
                
                if user_data and verify_password(password, user_data[2]):
                    return {
                        'id': user_data[0],
                        'username': user_data[1]
                    }
        return None
    except psycopg2.Error as e:
        st.error(f"Login failed: {str(e)}")
        return None

def init_session_state():
    """Initialize session state for authentication"""
    if 'user' not in st.session_state:
        st.session_state.user = None

def login_required(func):
    """Decorator to require login for certain pages/functions"""
    def wrapper(*args, **kwargs):
        if st.session_state.user is None:
            st.warning("Please log in to access this feature")
            display_login_form()
            return
        return func(*args, **kwargs)
    return wrapper

def display_login_form():
    """Display login form and handle authentication"""
    init_session_state()
    
    if st.session_state.user:
        st.write(f"Welcome back, {st.session_state.user['username']}!")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
        return

    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                user = login_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            new_username = st.text_input("Choose Username")
            email = st.text_input("Email")
            new_password = st.text_input("Choose Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            
            if st.form_submit_button("Register"):
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif register_user(new_username, email, new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username or email already exists")
