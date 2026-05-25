import streamlit as st
from databricks import sql
import os

# Page configuration
st.set_page_config(
    page_title="Project Data Entry",
    page_icon="📊",
    layout="wide"
)

# Database connection function - create connection only when needed
def get_connection():
    try:
        return sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN")
        )
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

# Function to insert project summary
def insert_project_summary(project_id, project_name, division, 
                          project_manager, customer_name, customer_country):
    try:
        connection = get_connection()
        if connection is None:
            return False, "Failed to connect to database"
            
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO default.projects_summary 
                    (project_id, project_name, division, project_manager_name, 
                     customer_name, customer_country)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (project_id, project_name, division, project_manager, 
                      customer_name, customer_country))
        return True, "Project Summary submitted successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Function to insert project financials
def insert_project_financials(project_id, sales_volume, direct_cost, 
                              indirect_cost, provisions):
    try:
        connection = get_connection()
        if connection is None:
            return False, "Failed to connect to database"
            
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO default.project_financials 
                    (project_id, sales_volume, direct_cost, indirect_cost, provisions)
                    VALUES (?, ?, ?, ?, ?)
                """, (project_id, float(sales_volume), float(direct_cost), 
                      float(indirect_cost), float(provisions)))
        return True, "Project Financials submitted successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"

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