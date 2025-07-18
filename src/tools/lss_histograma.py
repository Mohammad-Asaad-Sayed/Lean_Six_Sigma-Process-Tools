import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import matplotlib.pyplot as plt
from typing import List, Optional

class StatisticalHistogram:
    def __init__(self):
        self.df = st.session_state.get('uploaded_data')
        
        # Safety and validation settings
        self.settings = {
            'max_columns': 20,
            'max_rows': 10000,
            'valid_data_types': [np.number, 'object', 'category']
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

    def prepare_columns(self) -> tuple:
        """
        Prepare columns for analysis with exception handling
        """
        try:
            numeric_columns = self.df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            if not numeric_columns:
                st.warning("⚠️ No numeric columns found")
                return [], []
            
            return numeric_columns, categorical_columns
        
        except Exception as e:
            st.error(f"Error preparing columns: {e}")
            return [], []

    def generate_professional_histogram(self):
        """
        Generate histogram with validations and professional analysis
        """
        st.title("📊 Professional Statistical Analysis")
        
        # Preliminary validations
        if not self.validate_data():
            return
        
        # Prepare columns
        numeric_columns, categorical_columns = self.prepare_columns()
        
        if not numeric_columns:
            st.warning("No numeric data available for analysis")
            return
        
        # Variable selector
        variable = st.selectbox("Select Variable for Analysis", numeric_columns)
        
        try:
            # Generate histogram
            fig = self._create_detailed_histogram(variable)
            
            # Display chart
            st.plotly_chart(fig)
            
            # Summary table and analysis
            self._generate_summary_table(variable)
            
        except Exception as e:
            st.error(f"Error generating histogram: {e}")

    def _create_detailed_histogram(self, variable: str):
        """
        Create detailed histogram with professional annotations
        """
        data = self.df[variable]
        
        # Statistical calculations
        mean = data.mean()
        median = data.median()
        std_dev = data.std()
        
        # Histogram with distribution
        fig = go.Figure()
        
        # Base histogram
        fig.add_trace(go.Histogram(
            x=data, 
            name='Distribution',
            marker_color='blue',
            opacity=0.7
        ))
        
        # Mean line
        fig.add_shape(
            type='line', 
            x0=mean, 
            x1=mean, 
            y0=0, 
            y1=1, 
            yref='paper',
            line=dict(color='red', width=2, dash='dash')
        )
        
        # Additional settings
        fig.update_layout(
            title=f'Detailed Analysis of {variable}',
            xaxis_title=variable,
            yaxis_title='Frequency',
            annotations=[
                dict(
                    x=mean, 
                    y=1.1, 
                    xref='x', 
                    yref='paper',
                    text=f'Mean: {mean:.2f}',
                    showarrow=True
                )
            ]
        )
        
        return fig

    def _generate_summary_table(self, variable: str):
        """
        Generate summary table with interpretations
        """
        data = self.df[variable]
        
        # Statistical metrics
        metrics = {
            'Mean': data.mean(),
            'Median': data.median(),
            'Standard Deviation': data.std(),
            'Minimum': data.min(),
            'Maximum': data.max(),
            'Range': data.max() - data.min(),
            'Variance': data.var()
        }
        
        # Summary table
        st.subheader("📋 Summary Statistics")
        summary_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
        st.dataframe(summary_df)
        
        # Interpretations
        st.subheader("🔍 Interpretation")
        
        # Basic interpretation
        interpretation = f"""
        Analysis of {variable}:
        - Central Value: The mean of {metrics['Mean']:.2f} indicates the central tendency of the distribution.
        - Variability: A standard deviation of {metrics['Standard Deviation']:.2f} suggests the spread of data.
        - Range: It varies between {metrics['Minimum']:.2f} and {metrics['Maximum']:.2f}.
        """
        
        st.info(interpretation)

def histogram():
    """Main function for the Histogram module"""
    hist = StatisticalHistogram()
    hist.generate_professional_histogram()

# Page configuration
if __name__ == "__main__":
    st.set_page_config(page_title="Statistical Analysis", layout="wide")
    histogram()
