import streamlit as st
import os
from dotenv import load_dotenv
from utils.connector import SnowflakeConnector

st.set_page_config(page_title="Configuração", page_icon="⚙️")

st.title("⚙️ Configuração do Snowflake")
snowflake_conn = SnowflakeConnector()

# Formulário de configuração
with st.form("config_form"):
    st.subheader("Credenciais do Snowflake")
    
    account = st.text_input("Account", value=os.getenv('SNOWFLAKE_ACCOUNT', ''))
    user = st.text_input("User", value=os.getenv('SNOWFLAKE_USER', ''))
    password = st.text_input("Password", type="password", value=os.getenv('SNOWFLAKE_PASSWORD', ''))
    warehouse = st.text_input("Warehouse", value=os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'))
    database = st.text_input("Database", value=os.getenv('SNOWFLAKE_DATABASE', 'SNOWFLAKE_SAMPLE_DATA'))
    schema = st.text_input("Schema", value=os.getenv('SNOWFLAKE_SCHEMA', 'TPCH_SF1'))
    
    submitted = st.form_submit_button("Save and Test Connection")
    
    if submitted:
        # Atualizar variáveis de ambiente
        os.environ['SNOWFLAKE_ACCOUNT'] = account
        os.environ['SNOWFLAKE_USER'] = user
        os.environ['SNOWFLAKE_PASSWORD'] = password
        os.environ['SNOWFLAKE_WAREHOUSE'] = warehouse
        os.environ['SNOWFLAKE_DATABASE'] = database
        os.environ['SNOWFLAKE_SCHEMA'] = schema
        
        # Testar conexão
        if snowflake_conn.connect():
            st.success("✅ Connection successful!")
            
            # Salvar no .env
            with open('.env', 'w') as f:
                f.write(f"SNOWFLAKE_ACCOUNT={account}\n")
                f.write(f"SNOWFLAKE_USER={user}\n")
                f.write(f"SNOWFLAKE_PASSWORD={password}\n")
                f.write(f"SNOWFLAKE_WAREHOUSE={warehouse}\n")
                f.write(f"SNOWFLAKE_DATABASE={database}\n")
                f.write(f"SNOWFLAKE_SCHEMA={schema}\n")
        else:
            st.error("❌ Connection failed. Please check your credentials.")

    # Exemplo de queries
if st.button("Test Example Queries"):
    if snowflake_conn.connect():
        st.subheader("📋 Query Examples")
        
        # Query 1: Tabelas disponíveis
        tables_query = """
        SELECT TABLE_NAME, ROW_COUNT, BYTES 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = 'TPCH_SF1'
        LIMIT 10
        """
        
        tables_df = snowflake_conn.execute_query(tables_query)
        if tables_df is not None:
            st.write("**Tables in the schema:**")
            st.dataframe(tables_df)
        
        # Query 2: Dados de clientes
        customers_query = "SELECT * FROM CUSTOMER LIMIT 10"
        customers_df = snowflake_conn.execute_query(customers_query)
        if customers_df is not None:
            st.write("**Customer data:**")
            st.dataframe(customers_df)