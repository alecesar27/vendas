import streamlit as st
import pandas as pd
import plotly.express as px
from utils.connector import SnowflakeConnector, get_cached_query
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
st.title("📊 Dashboard Interativo")
st.markdown("---")
snowflake_conn = SnowflakeConnector()
# Verificar conexão
if not snowflake_conn.connect():
    st.error("⚠️ Configure primeiro as credenciais na página de Configuração")
    st.stop()
# Filtros na sidebar
st.sidebar.header("🔍 Filtros")

# Filtro de região
region_query = "SELECT DISTINCT C_NATIONKEY FROM CUSTOMER"
regions_df = get_cached_query(snowflake_conn, region_query)
regions = regions_df['C_NATIONKEY'].tolist() if regions_df is not None else []
selected_region = st.sidebar.selectbox("Selecione a região:", options=regions)

# Filtro de valor mínimo
min_balance = st.sidebar.slider("Saldo Mínimo:", min_value=0, max_value=10000, value=1000)


# Layout principal
col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("📈 Métricas Principais")
    
    # Métricas em cards
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    total_customers_query = "SELECT COUNT(*) as total FROM CUSTOMER"
    total_customers_df = get_cached_query(snowflake_conn, total_customers_query)
    
    if total_customers_df is not None:
        total_customers = total_customers_df['TOTAL'].iloc[0]
        metric_col1.metric("Total Clientes", f"{total_customers:,}")

        avg_balance_query = "SELECT AVG(C_ACCTBAL) as avg_balance FROM CUSTOMER"
    avg_balance_df = get_cached_query(snowflake_conn, avg_balance_query)
    
    if avg_balance_df is not None:
        avg_balance = avg_balance_df['AVG_BALANCE'].iloc[0]
        metric_col2.metric("Saldo Médio", f"${avg_balance:,.2f}")
    
    total_balance_query = "SELECT SUM(C_ACCTBAL) as total_balance FROM CUSTOMER"
    total_balance_df = get_cached_query(snowflake_conn, total_balance_query)
    
    if total_balance_df is not None:
        total_balance = total_balance_df['TOTAL_BALANCE'].iloc[0]
        metric_col3.metric("Saldo Total", f"${total_balance:,.2f}")

with col2:
    st.subheader("💡 Informações")
    st.info("""
    Dados provenientes do dataset 
    **TPCH_SF1** do Snowflake.
    Use os filtros para explorar os dados.
    """)

# Gráficos
st.markdown("---")
st.subheader("📊 Visualizações")

tab1, tab2, tab3 = st.tabs(["Distribuição", "Top Clientes", "Análise Detalhada"])

with tab1:
    # Gráfico de distribuição de saldos
    balance_query = """
    SELECT C_ACCTBAL, COUNT(*) as count 
    FROM CUSTOMER 
    GROUP BY C_ACCTBAL 
    ORDER BY C_ACCTBAL
    """
    balance_df = get_cached_query(snowflake_conn, balance_query)
    
    if balance_df is not None:
        fig = px.histogram(balance_df, x='C_ACCTBAL', y='COUNT', 
                         title="Balance Distribution",
                         labels={'C_ACCTBAL': 'Balance', 'COUNT': 'Frequency'},)
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Top clientes
    top_customers_query = """
    SELECT C_NAME, C_ACCTBAL, C_NATIONKEY 
    FROM CUSTOMER 
    ORDER BY C_ACCTBAL DESC 
    LIMIT 15
    """
    top_customers_df = get_cached_query(snowflake_conn, top_customers_query)
    
    if top_customers_df is not None:
        fig = px.bar(top_customers_df, x='C_NAME', y='C_ACCTBAL',
                   color='C_NATIONKEY',
                   title="Top 15 Customers by Balance",
                   labels={'C_NAME': 'CCustomer', 'C_ACCTBAL': 'Balance', 'C_NATIONKEY': 'Region'})
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Tabela detalhada
    detailed_query = """
    SELECT C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, 
           C_PHONE, C_ACCTBAL, C_MKTSEGMENT
    FROM CUSTOMER
    WHERE C_ACCTBAL >= %s
    """ % min_balance
    
    detailed_df = get_cached_query(snowflake_conn, detailed_query)
    
    if detailed_df is not None:
        st.dataframe(detailed_df, use_container_width=True)
        
        # Opção de download
        csv = detailed_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="clientes_filtrados.csv",
            mime="text/csv"
        )

# Query builder interativo
st.markdown("---")
st.subheader("🔧 Query Builder")

query_input = st.text_area(    "Enter your SQL query",
    value="SELECT * FROM CUSTOMER LIMIT 10",
    height=100
)

if st.button("Run Custom Query"):
    if query_input.strip():
        custom_df = snowflake_conn.execute_query(query_input)
        if custom_df is not None:
            st.dataframe(custom_df, use_container_width=True)
    else:
        st.warning("Enter a valid query.")