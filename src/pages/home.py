import streamlit as st

def render_home_page():
    # st.title("Welcome to Toritos de Pucara Analytics")
    
    # Description section
    st.markdown("""
    ## Statistical Analysis Tools for Process Improvement
    
    ### Our Mission
    Provide advanced statistical analysis tools to optimize processes 
    and enhance operational efficiency.
    
    ### Key Features
    - 📊 DPMO Calculator
    - 🧩 Lean Six Sigma Tools
    - 📈 Process Analysis
    - 📉 Control Charts
    - 🔍 Capability Analysis
    """)
    
    # Feature columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("DPMO Calculator")
        st.write("Measure your process efficiency using our Defects Per Million Opportunities (DPMO) calculator.")
    
    with col2:
        st.subheader("LSS Tools")
        st.write("Access Lean Six Sigma tools for analysis and continuous improvement.")
    
    with col3:
        st.subheader("Statistical Analysis")
        st.write("Perform advanced statistical analysis using our built-in tools.")
    
    # Call-to-action section
    st.markdown("---")
    st.markdown("### Ready to Optimize Your Processes?")
    
    # Show login/register buttons only if not logged in
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.markdown("""
        Sign up or log in to access all our tools.
        
        [🔐 Login](#) [📝 Register](#)
        """)

# Run directly for testing
if __name__ == "__main__":
    render_home_page()
