import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

class ScatterPlot:
    def __init__(self):
        # Load data from session
        self.df = st.session_state.get('uploaded_data')
        
        # Module settings
        self.settings = {
            'max_columns': 20,
            'max_rows': 10000,
            'valid_data_types': [np.number]
        }

    def validate_data(self) -> bool:
        """
        Comprehensive data validation before analysis
        """
        if self.df is None:
            st.error("⚠️ No data loaded")
            return False
        
        try:
            # Safety checks
            if len(self.df.columns) > self.settings['max_columns']:
                st.warning(f"Too many columns. Max {self.settings['max_columns']}")
                return False
            
            if len(self.df) > self.settings['max_rows']:
                st.warning(f"Too many rows. Max {self.settings['max_rows']}")
                return False
            
            return True
        
        except Exception as e:
            st.error(f"Error in data validation: {e}")
            return False

    def prepare_columns(self) -> list:
        """
        Prepare numeric columns for analysis
        """
        try:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
            if not numeric_columns:
                st.warning("⚠️ No numeric columns found")
                return []
            
            return numeric_columns
        
        except Exception as e:
            st.error(f"Error preparing columns: {e}")
            return []

    def generate_scatter_plot(self):
        """
        Generate a professional scatter plot with analysis
        """
        st.title("🔍 Scatter Plot Analysis")
        
        # Preliminary validations
        if not self.validate_data():
            return
        
        # Prepare numeric columns
        numeric_columns = self.prepare_columns()
        
        if len(numeric_columns) < 2:
            st.warning("At least two numeric columns are required for analysis")
            return
        
        # Title and description
        title = st.text_input("Analysis Title", "Scatter Plot")
        description = st.text_area("Description", "Analyzing relationship between variables")

        # Variable selection
        col1, col2 = st.columns(2)
        
        with col1:
            var_x = st.selectbox("X-axis Variable", numeric_columns)
        
        with col2:
            var_y = st.selectbox("Y-axis Variable", 
                [col for col in numeric_columns if col != var_x])
        
        # Advanced options
        with st.expander("Advanced Options"):
            color_by = st.selectbox("Color by", 
                ['None'] + [col for col in self.df.columns if col not in [var_x, var_y]])
            
            size = st.selectbox("Point Size", 
                ['Fixed', 'Variable'], index=0)
        
        # Generate plot
        try:
            fig = self._create_scatter_plot(
                var_x, 
                var_y, 
                color_by if color_by != 'None' else None,
                size
            )
            
            # Display plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistical analysis
            self._generate_statistical_analysis(var_x, var_y)
            
            # Export button
            self._export_analysis(
                fig, 
                title, 
                description, 
                var_x, 
                var_y
            )
            
        except Exception as e:
            st.error(f"Error generating scatter plot: {e}")

    def _create_scatter_plot(self, x, y, color=None, size='Fixed'):
        """
        Create an interactive scatter plot
        """
        # Prepare data
        data = self.df[[x, y]]
        if color:
            data[color] = self.df[color]
        
        # Size configuration
        if size == 'Fixed':
            point_size = 8
        else:
            # Normalize size based on another numeric variable
            point_size = self.df[x] / self.df[x].max() * 20
        
        # Create figure
        if color:
            fig = px.scatter(
                data, 
                x=x, 
                y=y, 
                color=color,
                title=f'Scatter Plot: {x} vs {y}',
                labels={x: x, y: y},
                hover_data=data.columns
            )
        else:
            fig = px.scatter(
                data, 
                x=x, 
                y=y, 
                title=f'Scatter Plot: {x} vs {y}',
                labels={x: x, y: y}
            )
        
        # Customization
        fig.update_traces(marker=dict(size=point_size))
        fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Rockwell"
            )
        )
        
        return fig

    def _generate_statistical_analysis(self, x, y):
        """
        Generate statistical analysis of the scatter plot
        """
        # Correlation calculation
        correlation = self.df[x].corr(self.df[y])
        
        # Metrics table
        st.subheader("📊 Statistical Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Correlation", f"{correlation:.2f}")
        
        with col2:
            st.metric("Mean X", f"{self.df[x].mean():.2f}")
        
        with col3:
            st.metric("Mean Y", f"{self.df[y].mean():.2f}")
        
        # Correlation interpretation
        interpretation = self._interpret_correlation(correlation)
        st.info(interpretation)

    def _interpret_correlation(self, correlation):
        """
        Interpret the correlation value
        """
        if abs(correlation) < 0.3:
            return f"Weak correlation ({correlation:.2f}): No strong linear relationship."
        elif abs(correlation) < 0.7:
            return f"Moderate correlation ({correlation:.2f}): Partial linear relationship."
        else:
            return f"Strong correlation ({correlation:.2f}): Significant linear relationship."

    def _export_analysis(self, fig, title, description, x, y):
        """
        Export analysis results
        """
        st.subheader("📥 Export Analysis")
        
        # Export as PDF
        if st.button("Export Analysis"):
            # Create PDF buffer
            pdf_buffer = BytesIO()
            
            # Convert Plotly figure to image
            img_bytes = fig.to_image(format='png')
            
            # Create PDF using matplotlib
            plt.figure(figsize=(10, 6))
            plt.title(title)
            plt.imshow(plt.imread(BytesIO(img_bytes)))
            plt.axis('off')
            
            # Save PDF
            plt.savefig(pdf_buffer, format='pdf', bbox_inches='tight')
            pdf_buffer.seek(0)
            
            # Generate download link
            b64 = base64.b64encode(pdf_buffer.getvalue()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="scatter_analysis.pdf">Download Analysis</a>'
            st.markdown(href, unsafe_allow_html=True)

def scatter_plot():
    """Main function for the Scatter Plot module"""
    scatter = ScatterPlot()
    scatter.generate_scatter_plot()

# Page configuration
if __name__ == "__main__":
    st.set_page_config(page_title="Scatter Plot", layout="wide")
    scatter_plot()
