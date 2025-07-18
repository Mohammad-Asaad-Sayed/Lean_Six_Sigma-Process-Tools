import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import base64

class ControlChartAnalyzer:
    def __init__(self, dataframe):
        self.df = dataframe
        self.numeric_columns = dataframe.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_columns = dataframe.select_dtypes(include=['object']).columns.tolist()

    def calculate_xbar_control_limits(self, variable):
        """
        Calculates control limits for X-bar control chart
        """
        data = self.df[variable]
        mean = data.mean()
        std_dev = data.std()
        
        # Classic 3-sigma control limits
        upper_limit = mean + 3 * (std_dev / np.sqrt(len(data)))
        lower_limit = mean - 3 * (std_dev / np.sqrt(len(data)))
        
        return {
            'mean': mean,
            'upper_limit': upper_limit,
            'lower_limit': lower_limit
        }

    def generate_xbar_control_chart(self, variable):
        """
        Generates interactive X-bar control chart
        """
        limits = self.calculate_xbar_control_limits(variable)
        
        fig = go.Figure()
        
        # Data points
        fig.add_trace(go.Scatter(
            x=self.df.index, 
            y=self.df[variable],
            mode='markers+lines',
            name=f'{variable}',
            marker=dict(
                color=self.df[variable].apply(
                    lambda x: 'red' if x > limits['upper_limit'] or x < limits['lower_limit'] else 'blue'
                )
            )
        ))
        
        # Mean line
        fig.add_trace(go.Scatter(
            x=self.df.index, 
            y=[limits['mean']] * len(self.df),
            mode='lines',
            name='Mean',
            line=dict(color='green', dash='dash')
        ))
        
        # Control limits
        fig.add_trace(go.Scatter(
            x=self.df.index, 
            y=[limits['upper_limit']] * len(self.df),
            mode='lines',
            name='Upper Limit',
            line=dict(color='red', dash='dot')
        ))
        
        fig.add_trace(go.Scatter(
            x=self.df.index, 
            y=[limits['lower_limit']] * len(self.df),
            mode='lines',
            name='Lower Limit',
            line=dict(color='red', dash='dot')
        ))
        
        fig.update_layout(
            title=f'X-bar Control Chart for {variable}',
            xaxis_title='Sample',
            yaxis_title='Value'
        )
        
        return fig, limits

    def interpret_control_chart(self, variable, limits):
        """
        Generates contextualized interpretation of the control chart
        """
        out_of_control = self.df[
            (self.df[variable] > limits['upper_limit']) | 
            (self.df[variable] < limits['lower_limit'])
        ]
        
        interpretation = [
            f"Quality Control Analysis for {variable}:",
            f"Mean: {limits['mean']:.2f}",
            f"Upper Control Limit: {limits['upper_limit']:.2f}",
            f"Lower Control Limit: {limits['lower_limit']:.2f}",
            f"Number of out-of-control samples: {len(out_of_control)}"
        ]
        
        if len(out_of_control) > 0:
            interpretation.append("ALERT: There are samples outside the control limits")
        
        return interpretation

    def export_to_pdf(self, fig, variable, limits, interpretation):
        """
        Exports the analysis to PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph(f"Quality Control Analysis - {variable}", styles['Title']))
        
        # Save chart as image
        img_buffer = io.BytesIO()
        fig.write_image(img_buffer, format='png')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        # Image
        img_path = f"data:image/png;base64,{img_base64}"
        from reportlab.platypus import Image
        elements.append(Image(img_path, width=500, height=300))
        
        # Interpretation
        elements.append(Paragraph("Interpretation", styles['Heading2']))
        for line in interpretation:
            elements.append(Paragraph(line, styles['Normal']))
        
        # Limits Table
        table_data = [
            ['Metric', 'Value'],
            ['Mean', f"{limits['mean']:.2f}"],
            ['Upper Limit', f"{limits['upper_limit']:.2f}"],
            ['Lower Limit', f"{limits['lower_limit']:.2f}"]
        ]
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        return buffer.getvalue()


def lss_tool3_control_chart_page():
    st.title("🔍 Quality Control Charts")
    
    # Check if data is loaded
    if 'uploaded_data' not in st.session_state:
        st.warning("Please load a dataset first.")
        return
    
    df = st.session_state['uploaded_data']
    
    # Instantiate analyzer
    analyzer = ControlChartAnalyzer(df)
    
    # Variable selection
    variable = st.selectbox(
        "Select Variable for Control Analysis",
        options=analyzer.numeric_columns
    )
    
    # Generate chart
    fig, limits = analyzer.generate_xbar_control_chart(variable)
    
    # Display chart
    st.plotly_chart(fig)
    
    # Interpretation
    interpretation = analyzer.interpret_control_chart(variable, limits)
    st.info("\n".join(interpretation))
    
    # Export button
    if st.button("Export Analysis to PDF"):
        pdf_data = analyzer.export_to_pdf(fig, variable, limits, interpretation)
        st.download_button(
            label="Download PDF Report",
            data=pdf_data,
            file_name=f"quality_control_{variable}.pdf",
            mime="application/pdf"
        )

def load_lss_tool3_control_chart():
    lss_tool3_control_chart_page()


if __name__ == "__main__":
    st.set_page_config(page_title="Quality Control Chart", layout="wide")
    load_lss_tool3_control_chart()
