import streamlit as st
import sys
import os  # Import os module for file handling
import traceback  # Import traceback or sys to show errors

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# System functions
from src.auth.login import login_page
from src.auth.register import register_page
from src.pages.home import render_home_page

# Import DPMO calculator function
from src.tools.dpmo_calculator import dpmo_calculator_page

# Import upload data function
from src.data_management.upload import upload_data_page

# Import dashboard
from src.pages.dashboard import dashboard
from src.tools.pareto_tool import load_lss_tool1_pareto  # Pareto tool
from src.tools.control_chart_tool import load_lss_tool3_control_chart  # Control chart tool
from src.tools.check_sheet import check_sheet  # Check sheet module
from src.tools.ishikawa_diagram import ishikawa_page  # Ishikawa diagram
from src.tools.histogram_analysis import histogram  # Histogram analysis
from src.tools.scatter_plot import scatter_plot  # Scatter plot analysis
from src.tools.stratification_analysis import stratification_analysis  # Stratification analysis


# Page configuration
st.set_page_config(
    # page_title="Analytics", 
    page_icon=":bar_chart:", 
    layout="wide"
)

def main():
    # Initialize session state if it doesn't exist
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Sidebar navigation
    if not st.session_state['logged_in']:
        # Menu for unauthenticated users
        menu = st.sidebar.radio("Navigation", 
            ["🏠 Home", "🔐 Login", "📝 Register"]
        )
        
        # Render pages based on selection
        if menu == "🏠 Home":
            render_home_page()
        elif menu == "🔐 Login":
            login_page()
        elif menu == "📝 Register":
            register_page()
    
    else:
        # Menu for authenticated users
        menu = st.sidebar.radio("Main Menu", [
            "🏠 Home",
            "📝 Upload Data",
            "📊 Dashboard",
            "🧮 DPMO Calculator",
            "📋 Checklist",
            "📊 Pareto Chart",
            "🐟 Ishikawa Diagram",
            "📈 Histogram",
            "🔍 Scatter Plot",
            "🎛️ Control Charts",
            "🔬 Stratification",  # pending
            # "🛠️ Additional LSS Tools",
            "🚪 Logout"
        ])

        # Navigation logic for authenticated users
        if menu == "🏠 Home":
            st.title(f"Welcome, {st.session_state['username']}")
            render_home_page()
        elif menu == "📝 Upload Data":
            st.title("Upload Data")
            upload_data_page()
        elif menu == "📊 Dashboard":
            dashboard()
        elif menu == "🧮 DPMO Calculator":
            try:
                st.write("Attempting to load DPMO calculator...")
                dpmo_calculator_page()  # Calls the dp function from dpmo_calculator.py
            except Exception as e:
                st.error(f"Error loading DPMO calculator: {e}")
                st.write(f"Error details: {traceback.format_exc()}")
        elif menu == "📋 Checklist":
            check_sheet()
        elif menu == "📊 Pareto Chart":
            load_lss_tool1_pareto()
        elif menu == "🐟 Ishikawa Diagram":
            ishikawa_page()
        elif menu == "📈 Histogram":
            histogram()
        elif menu == "🔍 Scatter Plot":
            scatter_plot()
        elif menu == "🔬 Stratification":
            stratification_analysis()
        elif menu == ".panelControl Charts":
            load_lss_tool3_control_chart()
        elif menu == "🚪 Logout":
            # Logout
            st.session_state['logged_in'] = False
            st.session_state['username'] = None
            st.experimental_rerun()


# Custom styles
def load_css():
    with open("static/css/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main entry point
if __name__ == "__main__":
    load_css()  # Load custom styles
    main()
