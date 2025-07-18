import streamlit as st
import pandas as pd
import bcrypt
from datetime import datetime
import os

def validate_username(username):
    # Username validations
    if len(username) < 4:
        return False, "Username must be at least 4 characters long"
    if not username.isalnum():
        return False, "Username can only contain letters and numbers"
    return True, ""

def validate_email(email):
    # Basic email validation
    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return False, "Invalid email address"
    return True, ""

def validate_password(password):
    # Password validations
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    return True, ""

def user_exists(username, email):
    # Check if username or email already exist
    users_file = 'data/users.csv'
    if not os.path.exists(users_file):
        return False
    
    df = pd.read_csv(users_file)
    return (
        username in df['username'].values or 
        email in df['email'].values
    )

def register_user(username, email, password):
    # Hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Prepare user data
    user_data = pd.DataFrame({
        'username': [username],
        'email': [email],
        'password_hash': [hashed_password.decode('utf-8')],
        'created_at': [datetime.now().isoformat()],
        'last_login': [None]
    })
    
    # Save to CSV
    users_file = 'data/users.csv'
    
    # Create file if it doesn't exist
    if not os.path.exists(users_file):
        df = pd.DataFrame(columns=['username', 'email', 'password_hash', 'created_at', 'last_login'])
        df.to_csv(users_file, index=False)
    
    # Read and add new user
    df = pd.read_csv(users_file)
    
    # Use concat instead of append
    df = pd.concat([df, user_data], ignore_index=True)
    
    df.to_csv(users_file, index=False)

def register_page():
    st.title("User Registration")
    
    # Registration form
    with st.form("registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            # Validations
            username_valid, username_error = validate_username(username)
            email_valid, email_error = validate_email(email)
            password_valid, password_error = validate_password(password)
            
            # Check if passwords match
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            # Run field validations
            if not (username_valid and email_valid and password_valid):
                if not username_valid:
                    st.error(username_error)
                if not email_valid:
                    st.error(email_error)
                if not password_valid:
                    st.error(password_error)
                return
            
            # Check if user or email already exists
            if user_exists(username, email):
                st.error("Username or email already exists")
                return
            
            # Successful registration
            try:
                register_user(username, email, password)
                st.success("Registration successful! You can now log in.")
            except Exception as e:
                st.error(f"Registration error: {e}")

# Run directly
if __name__ == "__main__":
    register_page()
