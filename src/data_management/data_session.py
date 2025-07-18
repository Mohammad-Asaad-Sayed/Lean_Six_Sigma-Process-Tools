import streamlit as st
import pandas as pd

class DataSession:
    @staticmethod
    def set_dataframe(df):
        """Store DataFrame in Streamlit session state"""
        st.session_state['shared_dataframe'] = df

    @staticmethod
    def get_dataframe():
        """Retrieve DataFrame from Streamlit session state"""
        return st.session_state.get('uploaded_data', None)
    
    # @staticmethod
    # def get_dataframe():
    #     """Retrieve DataFrame from Streamlit session state"""
    #     return st.session_state.get('shared_dataframe', None)
    
    @staticmethod
    def clear_dataframe():
        """Clear DataFrame from session state"""
        if 'shared_dataframe' in st.session_state:
            del st.session_state['shared_dataframe']
