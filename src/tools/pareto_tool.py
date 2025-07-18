import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
import io
import base64

class ParetoDiagram:
    def __init__(self, df):
        self.df = df
        self.possible_categories = list(df.columns)

    def prepare_pareto_data(self, category_column, value_column=None):
        """
        Prepare data for Pareto diagram with flexibility
        """
        if value_column:
            # Group by category and sum values
            grouped = self.df.groupby(category_column)[value_column].sum()
        else:
            # Count frequencies
            grouped = self.df[category_column].value_counts()
        
        # Calculate percentages
        total = grouped.sum()
        percentages = (grouped / total * 100).round(2)
        
        # Create Pareto DataFrame
        df_pareto = pd.DataFrame({
            'Category': grouped.index,
            'Value': grouped.values,
            'Individual Percentage': percentages.values
        })
        
        # Calculate cumulative percentage
        df_pareto['Cumulative Percentage'] = df_pareto['Individual Percentage'].cumsum()
        
        # Sort from highest to lowest
        df_pareto = df_pareto.sort_values('Value', ascending=False)
        
        return df_pareto

    def generate_pareto_chart(self, df_pareto):
        """
        Generate interactive Pareto chart
        """
        fig = go.Figure()
        
        # Bar chart for frequency
        fig.add_trace(go.Bar(
            x=df_pareto['Category'],
            y=df_pareto['Value'],
            name='Value',
            marker_color='rgba(58, 71, 80, 0.6)',
            yaxis='y1'
        ))
        
        # Line for cumulative percentage
        fig.add_trace(go.Scatter(
            x=df_pareto['Category'],
            y=df_pareto['Cumulative Percentage'],
            name='% Cumulative',
            marker_color='red',
            yaxis='y2'
        ))
        
        # Layout configuration
        fig.update_layout(
            title='Pareto Chart - Detailed Analysis',
            xaxis_title='Categories',
            yaxis_title='Value',
            yaxis2=dict(
                title='Cumulative Percentage',
                overlaying='y',
                side='right',
                range=[0, 110]
            )
        )
        
        return fig

    def interpret_pareto(self, df_pareto, category_column):
        """
        Generate contextualized interpretation of Pareto diagram
        """
        # Identify critical categories (80% of the problem)
        critical_categories = df_pareto[df_pareto['Cumulative Percentage'] <= 80]
        
        # Interpretations by analysis type
        interpretations = {
            'defects': [
                "Critical defects require immediate attention.",
                "Focus efforts on reducing the main causes of defects."
            ],
            'times': [
                "Stages with the longest processing times need optimization.",
                "Identify improvement opportunities in the slowest processes."
            ],
            'costs': [
                "Items with the highest economic impact demand strategic review.",
                "Prioritize actions to reduce the most significant costs."
            ],
            'default': [
                "Key categories in the analysis have been identified.",
                "Focus your efforts on areas with the greatest impact."
            ]
        }
        
        # Select interpretation
        if 'defect' in category_column.lower():
            context = 'defects'
        elif 'time' in category_column.lower():
            context = 'times'
        elif 'cost' in category_column.lower():
            context = 'costs'
        else:
            context = 'default'
        
        base_interpretation = interpretations[context]
        
        return base_interpretation

    def generate_critical_summary(self, df_pareto):
        """
        Generate summary of critical categories according to Pareto
        """
        # Categories representing 80% of the problem
        critical = df_pareto[df_pareto['Cumulative Percentage'] <= 80]
        
        summary = pd.DataFrame({
            'Category': critical['Category'],
            'Value': critical['Value'],
            '% Individual': critical['Individual Percentage'],
            '% Cumulative': critical['Cumulative Percentage']
        })
        
        return summary

def export_to_pdf(fig, df_pareto, interpretation):
    """
    Exports Pareto analysis to PDF
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Title
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Pareto Analysis", styles['Title']))
    
    # Save chart as image
    img_buffer = io.BytesIO()
    fig.write_image(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Convert image to base64
    img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
    
    # Add image to PDF
    img_path = f"data:image/png;base64,{img_base64}"
    elements.append(Image(img_path, width=500, height=300))
    
    # Table of data
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors
    
    table_data = [df_pareto.columns.tolist()] + df_pareto.values.tolist()
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    
    elements.append(table)
    
    # Interpretation
    elements.append(Paragraph("Interpretation", styles['Heading2']))
    elements.append(Paragraph(interpretation, styles['Normal']))
    
    doc.build(elements)
    
    return buffer.getvalue()

def lss_tool1_pareto_page():
    st.title("🔍 Pareto Chart Tool")
    
    # Check if data is loaded
    if 'uploaded_data' not in st.session_state:
        st.warning("Please load a dataset first.")
        return
    
    df = st.session_state['uploaded_data']
    
    # Numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Column selectors
    col1, col2 = st.columns(2)
    
    with col1:
        category_column = st.selectbox(
            "Select categorical column", 
            options=categorical_cols
        )
    
    with col2:
        value_column = st.selectbox(
            "Select value column (optional)", 
            options=['No value'] + numeric_cols
        )
    
    # Prepare Pareto data
    pareto = ParetoDiagram(df)
    
    # Conditional data preparation
    if value_column == 'No value':
        df_pareto = pareto.prepare_pareto_data(category_column)
    else:
        df_pareto = pareto.prepare_pareto_data(category_column, value_column)
    
    # Generate chart
    fig_pareto = pareto.generate_pareto_chart(df_pareto)
    
    # Display chart
    st.plotly_chart(fig_pareto)
    
    # Interpretation
    interpretation = pareto.interpret_pareto(df_pareto, category_column)
    st.info(" ".join(interpretation))
    
    # Critical summary
    st.subheader("Summary of Critical Categories")
    critical_summary = pareto.generate_critical_summary(df_pareto)
    st.dataframe(critical_summary)
    
    # Export to PDF button
    if st.button("Export Analysis to PDF"):
        pdf_data = export_to_pdf(fig_pareto, df_pareto, " ".join(interpretation))
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="pareto_analysis.pdf",
            mime="application/pdf"
        )

# Function to be called from main.py
def load_lss_tool1_pareto():
    lss_tool1_pareto_page()
