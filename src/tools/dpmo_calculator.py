import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def dpmo_calculator_page():
    # Sigma level reference table
    sigma_table = pd.DataFrame({
        "Sigma Level": ["2σ", "3σ", "4σ", "5σ", "6σ"],
        "DPMO": [308537, 66807, 6210, 233, 3.4],
        "Performance": ["69.2%", "93.3%", "99.38%", "99.977%", "99.9997%"]
    })

    # DPMO calculation function
    def calculate_dpmo(defects, units, opportunities):
        if units <= 0 or opportunities <= 0:
            st.error("Units and opportunities must be greater than zero")
            return None, None, None
        
        if defects > (units * opportunities):
            st.error("Defects cannot exceed total opportunities")
            return None, None, None

        dpmo = (defects * 1_000_000) / (units * opportunities)
        performance = 1 - (dpmo / 1_000_000)
        sigma_level = norm.ppf(performance) + 1.5
        return dpmo, sigma_level, performance

    # Function to create visualizations
    def create_visualizations(dpmo, sigma_table):
        col1, col2 = st.columns(2)
        
        # Chart 1: DPMO comparison
        with col1:
            st.subheader("DPMO Comparison")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            sns.barplot(x=sigma_table["Sigma Level"], y=sigma_table["DPMO"], palette="Blues", ax=ax1)
            ax1.axhline(dpmo, color="red", linestyle="--", label=f"Calculated DPMO ({dpmo:.2f})")
            ax1.set_ylabel("DPMO")
            ax1.set_title("DPMO by Sigma Level")
            ax1.legend()
            st.pyplot(fig1)

        # Chart 2: Performance by Sigma Level
        with col2:
            st.subheader("Performance by Sigma Level")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sigma_table['Performance_Num'] = sigma_table['Performance'].str.rstrip('%').astype('float')
            sns.barplot(x=sigma_table["Sigma Level"], y=sigma_table["Performance_Num"], palette="Greens", ax=ax2)
            ax2.set_ylabel("Performance (%)")
            ax2.set_title("Performance by Sigma Level")
            st.pyplot(fig2)

    # Function to interpret result
    def interpret_result(sigma_level):
        if sigma_level is None:
            return None
        
        interpretations = {
            (0, 2): "Critical Level: High variability and many defects",
            (2, 3): "Poor Level: Significant improvements needed",
            (3, 4): "Acceptable Level: Medium quality process",
            (4, 5): "Good Level: High-quality process",
            (5, 6): "Excellent Level: World-class process",
            (6, float('inf')): "Six Sigma Level: Near-perfect process"
        }
        
        for (min_val, max_val), interpretation in interpretations.items():
            if min_val <= sigma_level < max_val:
                return interpretation
        
        return "Result out of range"

    # Main interface
    st.title("🔢 DPMO Calculator")
    st.markdown("Calculate Defects Per Million Opportunities (DPMO)")

    # Input form
    with st.form("dpmo_calculator"):
        defects = st.number_input("Total Defects", min_value=0, step=1, format="%d")
        units = st.number_input("Total Units", min_value=1, step=1, format="%d")
        opportunities = st.number_input("Opportunities per Unit", min_value=1, step=1, format="%d")
        submit_button = st.form_submit_button(label="Calculate 📊")

    # Process results
    if submit_button:
        result = calculate_dpmo(defects, units, opportunities)
        
        if result[0] is not None:
            dpmo, sigma_level, performance = result

            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Calculated DPMO", value=f"{dpmo:.2f}")
            col2.metric(label="Sigma Level", value=f"{sigma_level:.2f}")
            col3.metric(label="Performance", value=f"{performance * 100:.2f}%")

            # Interpretation
            interpretation = interpret_result(sigma_level)
            st.subheader("Result Interpretation")
            st.info(interpretation)

            # Visualizations
            create_visualizations(dpmo, sigma_table)

            # Export results
            results = pd.DataFrame({
                'Metric': ['DPMO', 'Sigma Level', 'Performance'],
                'Value': [dpmo, sigma_level, performance * 100]
            })
            st.download_button(
                label="Download Results", 
                data=results.to_csv(index=False).encode('utf-8'),
                file_name='dpmo_results.csv',
                mime='text/csv'
            )

# Entry point
def main():
    dpmo_calculator_page()

if __name__ == "__main__":
    main()
