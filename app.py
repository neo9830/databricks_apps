import streamlit as st
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import databricks_cli
import os

# Page configuration
st.set_page_config(
    page_title="Project Data Entry",
    page_icon="📊",
    layout="wide"
)

# Get Databricks client (uses OAuth automatically in Apps)
@st.cache_resource
def get_workspace_client():
    return WorkspaceClient()

# Database connection function using SQL Statement Execution API
def execute_sql(query, parameters=None):
    try:
        w = get_workspace_client()
        warehouse_id = "3b16ccf20d74f512"
        
        # Execute SQL using warehouse
        result = w.statement_execution.execute_statement(
            warehouse_id=warehouse_id,
            statement=query,
            wait_timeout="30s"
        )
        
        return True, "Success", result
    except Exception as e:
        return False, f"Error: {str(e)}", None

# Function to insert project summary
def insert_project_summary(project_id, project_name, division, 
                          project_manager, customer_name, customer_country):
    query = f"""
        INSERT INTO default.projects_summary 
        (project_id, project_name, division, project_manager_name, 
         customer_name, customer_country)
        VALUES ('{project_id}', '{project_name}', '{division}', '{project_manager}', 
                '{customer_name}', '{customer_country}')
    """
    
    success, message, _ = execute_sql(query)
    return success, message

# Function to insert project financials
def insert_project_financials(project_id, sales_volume, direct_cost, 
                              indirect_cost, provisions):
    query = f"""
        INSERT INTO default.project_financials 
        (project_id, sales_volume, direct_cost, indirect_cost, provisions)
        VALUES ('{project_id}', {sales_volume}, {direct_cost}, {indirect_cost}, {provisions})
    """
    
    success, message, _ = execute_sql(query)
    return success, message

# Main app
st.title("📊 Project Data Entry System")
st.markdown("---")

# Create two tabs for the two forms
tab1, tab2 = st.tabs(["📋 Project Summary", "💰 Project Financials"])

# Tab 1: Project Summary Form
with tab1:
    st.header("Project Summary Information")
    
    with st.form("project_summary_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            proj_id_1 = st.text_input("Project ID *", placeholder="e.g., PROJ001")
            division = st.text_input("Division *", placeholder="e.g., Engineering")
            customer_name = st.text_input("Customer Name *", placeholder="Customer name")
        
        with col2:
            proj_name = st.text_input("Project Name *", placeholder="Enter project name")
            proj_manager = st.text_input("Project Manager Name *", placeholder="Manager name")
            customer_country = st.text_input("Customer Country *", placeholder="e.g., USA")
        
        submit_summary = st.form_submit_button("Submit Project Summary", use_container_width=True)
        
        if submit_summary:
            if not all([proj_id_1, proj_name, division, proj_manager, customer_name, customer_country]):
                st.error("❌ Please fill in all required fields")
            else:
                success, message = insert_project_summary(
                    proj_id_1, proj_name, division, proj_manager, 
                    customer_name, customer_country
                )
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")

# Tab 2: Project Financials Form
with tab2:
    st.header("Project Financial Information")
    
    with st.form("project_financials_form"):
        proj_id_2 = st.text_input("Project ID *", placeholder="e.g., PROJ001")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sales_vol = st.number_input("Sales Volume *", min_value=0.0, format="%.2f")
            indirect_cost = st.number_input("Indirect Cost *", min_value=0.0, format="%.2f")
        
        with col2:
            direct_cost = st.number_input("Direct Cost *", min_value=0.0, format="%.2f")
            provisions = st.number_input("Provisions *", min_value=0.0, format="%.2f")
        
        submit_financials = st.form_submit_button("Submit Project Financials", use_container_width=True)
        
        if submit_financials:
            if not proj_id_2:
                st.error("❌ Please enter a Project ID")
            else:
                success, message = insert_project_financials(
                    proj_id_2, sales_vol, direct_cost, indirect_cost, provisions
                )
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")

# Footer
st.markdown("---")
st.caption("💡 Tip: Fill in all required fields marked with *")