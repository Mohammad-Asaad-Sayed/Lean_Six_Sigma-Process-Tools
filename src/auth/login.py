import streamlit as st
import pandas as pd
import bcrypt
from datetime import datetime
import os

def validate_login(username, password):
    users_file = 'data/users.csv'
    
    # Check if the file exists
    if not os.path.exists(users_file):
        return False, "Users file not found"
    
    # Read user data
    df = pd.read_csv(users_file)
    
    # Find user
    user = df[df['username'] == username]
    
    if user.empty:
        return False, "User not found"
    
    # Verify password
    stored_password = user['password_hash'].values[0]
    
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
        # Update last login timestamp
        df.loc[df['username'] == username, 'last_login'] = datetime.now().isoformat()
        df.to_csv(users_file, index=False)
        return True, "Login successful"
    
    return False, "Incorrect password"

def login_page():
    st.title("Login")
    
    # Check if user is already logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            # Validate non-empty fields
            if not username or not password:
                st.error("Please fill in all fields")
                return
            
            # Attempt login
            login_successful, message = validate_login(username, password)
            
            if login_successful:
                # Set session state
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                
                # Show success message
                st.success(message)
                
                # Use rerun() instead of experimental_rerun()
                st.rerun()
            else:
                # Show login error
                st.error(message)
    
    # Registration option
    st.markdown("Don't have an account? [Register here](/register)")

# Run directly
if __name__ == "__main__":
    login_page()
