import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

def data_upload_page():
    st.title("📝 Data Upload and Analysis")
    
    # File upload section
    st.header("Upload Data File")
    uploaded_file = st.file_uploader(
        "Select a CSV or Excel file", 
        type=['csv', 'xlsx']
    )
    
    if uploaded_file is not None:
        # Read the file
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Store DataFrame in session
            st.session_state['uploaded_data'] = df
            
            # Analysis tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "Preview", 
                "Descriptive Analysis", 
                "Missing Values", 
                "Variable Conversion"
            ])
            
            with tab1:
                st.subheader("Data Preview")
                st.dataframe(df.head(10))
                
                # Basic dataset info
                st.subheader("Dataset Information")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Number of Rows", df.shape[0])
                with col2:
                    st.metric("Number of Columns", df.shape[1])
                with col3:
                    st.metric("Unique Data Types", len(df.dtypes.unique()))
            
            with tab2:
                st.subheader("Descriptive Analysis")
                # Descriptive statistics for numeric variables
                desc_stats = df.describe()
                st.dataframe(desc_stats)
                
                # Distribution plots
                st.subheader("Distribution of Numeric Variables")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                selected_col = st.selectbox("Select a variable", numeric_cols)
                
                fig = px.histogram(df, x=selected_col, 
                                   title=f'Distribution of {selected_col}')
                st.plotly_chart(fig)
            
            with tab3:
                st.subheader("Missing Values Analysis")
                # Missing values count
                missing_data = df.isnull().sum()
                missing_percent = 100 * df.isnull().sum() / len(df)
                
                missing
