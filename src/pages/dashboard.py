import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from io import BytesIO
import base64

from src.data_management.data_session import DataSession

class CustomDashboard:
    def __init__(self, df):
        self.df = df
        self.variables = list(df.columns)
        
        # Default values
        self.title = "Production Analysis Dashboard"
        self.description = "Detailed metrics analysis"
        self.selected_variables = self.variables[2:4]  # Select first 2 variables
    
    def configure_dashboard(self):
        """Modal for dashboard configuration"""
        with st.expander("🔧 Configure Dashboard"):
            self.title = st.text_input(
                "Dashboard Title", 
                value=self.title
            )
            self.description = st.text_area(
                "Description", 
                value=self.description
            )
    
    def select_variables(self):
        """Dynamic variable selector"""
        with st.sidebar.expander("📊 Variable Selection"):
            self.selected_variables = st.multiselect(
                "Select variables for analysis",
                self.variables,
                default=self.selected_variables
            )
    
    def generate_kpis(self):
        """Dynamic generation of KPIs"""
        st.header("🎯 Key Performance Indicators (KPIs)")
        
        kpi_cols = st.columns(len(self.selected_variables))
        
        for i, variable in enumerate(self.selected_variables):
            with kpi_cols[i]:
                mean_value = self.df[variable].mean()
                min_value = self.df[variable].min()
                max_value = self.df[variable].max()
                
                st.metric(
                    label=f"📈 {variable}", 
                    value=f"{mean_value:.2f}",
                    delta=f"Min: {min_value:.2f} | Max: {max_value:.2f}"
                )
    
    def control_plots(self):
        """Control charts for selected variables"""
        st.header("🔍 Control Charts")
        
        for variable in self.selected_variables:
            # Line chart with control limits
            fig = px.line(
                self.df, 
                y=variable, 
                title=f'Control Chart - {variable}',
                labels={'index': 'Observations', 'value': variable}
            )
            
            # Add control bands
            fig.add_hrect(
                y0=self.df[variable].mean() - self.df[variable].std(), 
                y1=self.df[variable].mean() + self.df[variable].std(), 
                fillcolor="green", 
                opacity=0.2,
                layer="below",
                line_width=0,
            )
            
            st.plotly_chart(fig)
    
    def distribution_plots(self):
        """Distribution charts"""
        st.header("📊 Variable Distribution")
        
        for variable in self.selected_variables:
            # Histogram with marginal boxplot
            fig = px.histogram(
                self.df, 
                x=variable, 
                title=f'Distribution of {variable}',
                marginal='box'
            )
            st.plotly_chart(fig)
    
    def export_to_pdf(self):
        """Export dashboard to PDF modal"""
        with st.expander("📄 Export Dashboard"):
            filename = st.text_input(
                "PDF File Name", 
                value="analysis_dashboard"
            )
            
            if st.button("Generate PDF"):
                # Basic PDF export implementation
                buffer = BytesIO()
                c = canvas.Canvas(buffer, pagesize=letter)
                width, height = letter
                
                # Title
                c.setFont("Helvetica-Bold", 16)
                c.drawString(inch, height - inch, self.title)
                
                # Description
                c.setFont("Helvetica", 12)
                c.drawString(inch, height - (inch * 1.5), self.description)
                
                c.save()
                
                pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                href = f'<a href="data:application/pdf;base64,{pdf_base64}" download="{filename}.pdf">Download PDF</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    def render(self):
        """Render complete dashboard"""
        st.title(self.title)
        st.write(self.description)
        
        self.generate_kpis()
        self.control_plots()
        self.distribution_plots()
        self.export_to_pdf()

def dashboard():
    """Main dashboard function"""
    # Retrieve DataFrame from session
    df = DataSession.get_dataframe()
    
    if df is not None:
        dashboard_instance = CustomDashboard(df)
        
        # Configuration
        dashboard_instance.configure_dashboard()
        dashboard_instance.select_variables()
        
        # Render dashboard
        dashboard_instance.render()
    else:
        st.warning("No dataset has been uploaded. Please upload data first.")
