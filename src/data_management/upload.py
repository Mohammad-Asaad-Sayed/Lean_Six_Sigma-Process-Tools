import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def data_upload_page():
    st.title("📝 Data Upload and Analysis")

    # File upload section
    st.header("Upload Data File")
    uploaded_file = st.file_uploader("Select a CSV or Excel file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        try:
            # Read the file
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

                fig = px.histogram(df, x=selected_col, title=f'Distribution of {selected_col}')
                st.plotly_chart(fig)

            with tab3:
                st.subheader("Missing Values Analysis")
                # Missing values count
                missing_data = df.isnull().sum()
                missing_percent = 100 * df.isnull().sum() / len(df)

                missing_df = pd.DataFrame({
                    'Missing Values': missing_data,
                    'Percentage (%)': missing_percent
                })

                st.dataframe(missing_df)

                # Missing values visualization
                if missing_data.sum() > 0:
                    st.warning("Missing values found in some columns.")

                    # Missing values handling options
                    handle_method = st.radio(
                        "Select method to handle missing values:", 
                        ['Delete Rows', 'Fill with Mean', 'Fill with Median']
                    )

                    if st.button("Apply Handling Method"):
                        if handle_method == 'Delete Rows':
                            df_cleaned = df.dropna()
                        elif handle_method == 'Fill with Mean':
                            df_cleaned = df.fillna(df.mean())
                        else:
                            df_cleaned = df.fillna(df.median())

                        st.success("Data processed successfully.")
                        st.dataframe(df_cleaned)
                else:
                    st.success("No missing values found in the dataset.")

            with tab4:
                st.subheader("Variable Conversion")

                # Column selection for conversion
                col_to_convert = st.selectbox("Select column to convert", df.columns)

                # Conversion type
                conversion_type = st.radio("Conversion Type", ['Numeric', 'Categorical', 'One-Hot Encoding'])

                if st.button("Convert Variable"):
                    if conversion_type == 'Numeric':
                        try:
                            df[col_to_convert] = pd.to_numeric(df[col_to_convert], errors='coerce')
                            st.success(f"Column {col_to_convert} converted to numeric")
                        except Exception as e:
                            st.error(f"Conversion error: {e}")

                    elif conversion_type == 'Categorical':
                        df[col_to_convert] = df[col_to_convert].astype('category')
                        st.success(f"Column {col_to_convert} converted to categorical")

                    elif conversion_type == 'One-Hot Encoding':
                        df_encoded = pd.get_dummies(df, columns=[col_to_convert])
                        st.success(f"One-Hot Encoding applied to {col_to_convert}")
                        st.dataframe(df_encoded)

        except Exception as e:
            st.error(f"Error loading file: {e}")

# Function to be called from main.py
def upload_data_page():
    data_upload_page()
