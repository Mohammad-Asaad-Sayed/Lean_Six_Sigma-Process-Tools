import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import seaborn as sns

def stratification_analysis():
    """
    Main Stratification Analysis function that handles the full analysis
    """
    st.title("🔬 Stratification Analysis")
    
    # Load data from session
    df = st.session_state.get('uploaded_data')
    
    # Data validations
    if df is None:
        st.error("⚠️ No data loaded")
        return
    
    # Module settings
    max_columns = 20
    max_rows = 10000
    
    # Safety checks
    if len(df.columns) > max_columns:
        st.warning(f"Too many columns. Maximum {max_columns}")
        return
    
    if len(df) > max_rows:
        st.warning(f"Too many rows. Maximum {max_rows}")
        return
    
    # Prepare columns
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Title and description input
    title = st.text_input("Analysis Title", "Stratification Analysis")
    description = st.text_area("Description", "Detailed stratification analysis of data")
    
    # Variable selection
    col1, col2 = st.columns(2)
    
    with col1:
        categorical_var = st.selectbox("Categorical Variable", 
            categorical_columns if categorical_columns else ['No categorical variables'])
    
    with col2:
        numeric_var = st.selectbox("Numeric Variable", 
            numeric_columns if numeric_columns else ['No numeric variables'])
    
    # Validate variable selection
    if categorical_var == 'No categorical variables' or numeric_var == 'No numeric variables':
        st.warning("Please select valid variables for analysis")
        return
    
    # Generate visualizations
    try:
        # Boxplot
        fig1 = px.box(
            df, 
            x=categorical_var, 
            y=numeric_var,
            title=f'Distribution of {numeric_var} by {categorical_var}'
        )
        
        # Bar chart with aggregation
        aggregated_data = df.groupby(categorical_var)[numeric_var].agg(['mean', 'count']).reset_index()
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=aggregated_data[categorical_var],
            y=aggregated_data['mean'],
            name='Mean',
            marker_color='blue'
        ))
        fig2.add_trace(go.Scatter(
            x=aggregated_data[categorical_var],
            y=aggregated_data['count'],
            name='Count',
            yaxis='y2',
            mode='lines+markers',
            marker_color='red'
        ))
        fig2.update_layout(
            title=f'Analysis of {numeric_var} by {categorical_var}',
            xaxis_title=categorical_var,
            yaxis_title=f'Mean of {numeric_var}',
            yaxis2=dict(
                title='Count',
                overlaying='y',
                side='right'
            )
        )
        
        # Display charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.plotly_chart(fig2, use_container_width=True)
        
        # Summary table
        st.subheader("📊 Summary Table")
        summary = df.groupby(categorical_var)[numeric_var].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        st.dataframe(summary)
        
        # Interpretation of results
        st.subheader("🔍 Results Interpretation")
        interpretation = f"""
        Stratification Analysis of {numeric_var} by {categorical_var}:
        
        - Identified Categories: {len(summary)} 
        - Distribution:
        {summary.to_string()}
        
        Key Observations:
        - Highest concentration: {summary['count'].idxmax()} 
        - Highest average: {summary['mean'].idxmax()}
        """
        st.info(interpretation)
        
        # Export results
        st.subheader("📥 Export Analysis")
        if st.button("Export Analysis"):
            # Export logic similar to previous versions
            plt.figure(figsize=(15, 10))
            plt.suptitle(title, fontsize=16)
            
            # Add charts to PDF
            plt.subplot(1, 2, 1)
            img_bytes1 = fig1.to_image(format='png')
            plt.imshow(plt.imread(BytesIO(img_bytes1)))
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            img_bytes2 = fig2.to_image(format='png')
            plt.imshow(plt.imread(BytesIO(img_bytes2)))
            plt.axis('off')
            
            # Save and generate download link
            pdf_buffer = BytesIO()
            plt.savefig(pdf_buffer, format='pdf', bbox_inches='tight')
            pdf_buffer.seek(0)
            
            b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
            href = f'<a href="application/pdf;base64,{b64}" download="stratification_analysis.pdf">Download Analysis</a>'
            st.markdown(href, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error generating stratification analysis: {e}")

# Page configuration
if __name__ == "__main__":
    st.set_page_config(page_title="Stratification Analysis", layout="wide")
    stratification_analysis()
