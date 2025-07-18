import streamlit as st
import graphviz
import pandas as pd

def initialize_session_state():
    """Initializes session state if not present."""
    if 'causes_data' not in st.session_state:
        st.session_state.causes_data = {
            "Methods": [],
            "Machines": [],
            "People": [],
            "Materials": [],
            "Environment": []
        }
    if 'effect' not in st.session_state:
        st.session_state.effect = ""

def add_cause_to_category(category, cause, whys):
    """Adds a cause to the specified category."""
    if cause:
        st.session_state.causes_data[category].append({
            "cause": cause,
            "whys": whys
        })

def create_summary_table():
    """Creates a summary table of causes and effects."""
    data = []
    for category, items in st.session_state.causes_data.items():
        for item in items:
            data.append({
                "Category": category,
                "Cause": item["cause"],
                "Whys": " → ".join(item["whys"])
            })
    return pd.DataFrame(data)

def create_styled_graph(effect, categories):
    """Creates a styled Ishikawa diagram graph."""
    graph = graphviz.Digraph(
        graph_attr={
            'rankdir': 'LR',
            'splines': 'ortho',
            'nodesep': '0.5',
            'ranksep': '2',
            'fontname': 'Arial',
            'bgcolor': 'white'
        }
    )
    
    colors = {
        "Methods": "#FF9999",
        "Machines": "#99FF99",
        "People": "#9999FF",
        "Materials": "#FFFF99",
        "Environment": "#FF99FF"
    }
    
    # Main effect node
    graph.node('effect', 
        effect, 
        shape='box',
        style='filled',
        fillcolor='#E6E6E6',
        fontname='Arial Bold',
        fontsize='14'
    )
    
    # Add categories and causes
    for category, causes in categories.items():
        if causes:
            cat_id = f"cat_{category}"
            graph.node(cat_id, 
                category,
                shape='box',
                style='filled',
                fillcolor=colors[category],
                fontname='Arial',
                fontsize='12'
            )
            graph.edge(cat_id, 'effect',
                penwidth='2.0',
                color=colors[category]
            )
            
            for i, cause_data in enumerate(causes):
                cause_id = f"{category}cause{i}"
                graph.node(cause_id,
                    cause_data['cause'],
                    shape='oval',
                    style='filled',
                    fillcolor=f"{colors[category]}80",
                    fontname='Arial',
                    fontsize='10'
                )
                graph.edge(cause_id, cat_id,
                    penwidth='1.5',
                    color=f"{colors[category]}80"
                )
                
                for j, why in enumerate(cause_data['whys']):
                    why_id = f"{cause_id}why{j}"
                    graph.node(why_id,
                        why,
                        shape='oval',
                        style='filled',
                        fillcolor=f"{colors[category]}40",
                        fontname='Arial',
                        fontsize='9'
                    )
                    graph.edge(why_id, cause_id,
                        penwidth='1.0',
                        color=f"{colors[category]}60"
                    )
    return graph

def ishikawa_page():
    """Main function for the Ishikawa diagram page."""
    st.title("Ishikawa Diagram (Cause and Effect)")
    st.write("### Ishikawa Diagram Features")
    st.write("""
    - *Cause Identification*: Helps identify various causes contributing to a specific problem.
    - *Visualization*: Provides a clear graphical representation of the relationship between the effect and its causes.
    - *Problem Analysis*: Allows analysis of root causes of a problem.
    - *Idea Organization*: Facilitates brainstorming and group discussion.
    - *Continuous Improvement*: Identifies areas for improvement in products, services, or processes.
    """)
    
    st.write("### Components of the Ishikawa Diagram")
    st.write("""
    - *Effect (Problem)*: Represents the problem being analyzed.
    - *Cause Categories*: Grouped into categories such as Methods, Machines, People, Materials, and Environment.
    """)

    initialize_session_state()
    
    input_tab, diagram_tab, summary_tab = st.tabs(["📝 Input", "📊 Diagram", "📋 Summary"])
    
    with input_tab:
        st.session_state.effect = st.text_input("Main Problem or Effect:", 
                                              value=st.session_state.effect)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            selected_category = st.selectbox("Select Category:", 
                list(st.session_state.causes_data.keys()))
        
        with col2:
            new_cause = st.text_input(f"New cause for {selected_category}:")
            if new_cause:
                whys = []
                st.write("5 Whys:")
                for i in range(5):
                    why = st.text_input(f"Why? {i+1}", key=f"why_{i}")
                    if why:  
                        whys.append(why)
                if st.button("Add Cause"):
                    add_cause_to_category(selected_category, new_cause, whys)
                    st.success(f"Cause added to {selected_category}")
    
    with diagram_tab:
        if st.button("Generate Diagram"):
            if st.session_state.effect:
                try:
                    graph = create_styled_graph(st.session_state.effect, 
                                             st.session_state.causes_data)
                    st.graphviz_chart(graph)
                except Exception as e:
                    st.error(f"Error generating diagram: {str(e)}")
            else:
                st.warning("Please enter the main problem or effect")
    
    with summary_tab:
        df = create_summary_table()
        if not df.empty:
            st.write("Summary of Causes and Effects")
            category_filter = st.multiselect(
                "Filter by Category:",
                options=st.session_state.causes_data.keys()
            )
            
            if category_filter:
                filtered_df = df[df['Category'].isin(category_filter)]
            else:
                filtered_df = df
                
            st.dataframe(filtered_df)
            
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Summary (CSV)",
                csv,
                "ishikawa_summary.csv",
                "text/csv",
                key='download-csv'
            )
        else:
            st.info("No data to display in the summary")

# Entry point
if __name__ == "__main__":
    st.set_page_config(page_title="Ishikawa Diagram", layout="wide")
    ishikawa_page()
