import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

class CheckSheet:
    def __init__(self):
        # Initialize session state variables
        if 'check_sheet' not in st.session_state:
            st.session_state.check_sheet = None
        if 'sheet_data' not in st.session_state:
            st.session_state.sheet_data = None

    def create_check_sheet(self):
        """
        Create a new check sheet with custom configuration
        """
        st.subheader("🛠 Create Check Sheet")
        
        # Types of check sheets
        sheet_types = [
            "Defect Count",
            "Event Log",
            "Process Control",
            "Frequency Analysis"
        ]
        
        # Sheet type selection
        sheet_type = st.selectbox("Select Sheet Type", sheet_types)
        
        # Field configuration
        num_fields = st.number_input("Number of Fields", min_value=1, max_value=10, value=3)
        
        fields = []
        for i in range(num_fields):
            col1, col2 = st.columns(2)
            with col1:
                field_name = st.text_input(f"Field Name {i+1}")
            with col2:
                field_type = st.selectbox(f"Field Type {i+1}", 
                                          ["Text", "Numeric", "Category", "Date"])
            
            fields.append({
                "name": field_name,
                "type": field_type
            })
        
        # Button to create the check sheet
        if st.button("Create Check Sheet"):
            st.session_state.check_sheet = {
                "type": sheet_type,
                "fields": fields
            }
            st.success("Check sheet created successfully")

    def input_data(self):
        """
        Interface to enter data into the check sheet
        """
        if st.session_state.check_sheet is None:
            st.warning("First, you must create a Check Sheet")
            return

        st.subheader("📝 Enter Data")
        
        # Prepare data structure
        data = {}
        for field in st.session_state.check_sheet['fields']:
            if field['type'] == 'Text':
                data[field['name']] = st.text_input(field['name'])
            elif field['type'] == 'Numeric':
                data[field['name']] = st.number_input(field['name'])
            elif field['type'] == 'Category':
                options = st.text_input(f"Options for {field['name']} (comma-separated)")
                data[field['name']] = st.selectbox(field['name'], options.split(','))
            elif field['type'] == 'Date':
                data[field['name']] = st.date_input(field['name'])
        
        # Button to save data
        if st.button("Save Data"):
            if st.session_state.sheet_data is None:
                st.session_state.sheet_data = pd.DataFrame(columns=[field['name'] for field in st.session_state.check_sheet['fields']])
            
            new_data = pd.DataFrame([data])
            st.session_state.sheet_data = pd.concat([st.session_state.sheet_data, new_data], ignore_index=True)
            st.success("Data saved successfully")

    def visualize_data(self):
        """
        Visualize and analyze check sheet data
        """
        st.subheader("📊 Data Visualization")
        
        if st.session_state.sheet_data is not None and not st.session_state.sheet_data.empty:
            # Show data
            st.dataframe(st.session_state.sheet_data)
            
            # Column selection for analysis
            column_analysis = st.selectbox("Select column for analysis", 
                                            st.session_state.sheet_data.columns)
            
            # Chart type based on data type
            if pd.api.types.is_numeric_dtype(st.session_state.sheet_data[column_analysis]):
                # Histogram for numeric data
                fig_hist = px.histogram(st.session_state.sheet_data, x=column_analysis, 
                                        title=f'Distribution of {column_analysis}')
                st.plotly_chart(fig_hist)
                
                # Descriptive statistics
                st.subheader("Descriptive Statistics")
                st.write(st.session_state.sheet_data[column_analysis].describe())
            
            elif pd.api.types.is_categorical_dtype(st.session_state.sheet_data[column_analysis]):
                # Pie chart for categorical data
                fig_pie = px.pie(st.session_state.sheet_data, names=column_analysis, 
                                 title=f'Distribution of {column_analysis}')
                st.plotly_chart(fig_pie)
            
            # Export options
            if st.button("Export Data to CSV"):
                csv = st.session_state.sheet_data.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name='check_sheet_data.csv',
                    mime='text/csv'
                )
        else:
            st.info("No data to visualize. Please enter data first.")

def check_sheet():
    """
    Main function for the Check Sheet module
    """
    st.title("📋 Check Sheet - Lean Six Sigma")
    
    # Instance of CheckSheet class
    cs = CheckSheet()
    
    # Action menu
    action = st.radio("Select an Action", [
        "Create Check Sheet", 
        "Enter Data", 
        "Visualize and Analyze Data"
    ])
    
    # Call the corresponding method based on selected action
    if action == "Create Check Sheet":
        cs.create_check_sheet()
    elif action == "Enter Data":
        cs.input_data()
    elif action == "Visualize and Analyze Data":
        cs.visualize_data()

# Entry point for direct testing
if __name__ == "__main__":
    st.set_page_config(page_title="Lean Six Sigma Check Sheet")
    check_sheet()
