import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.connector import SnowflakeConnector, get_cached_query

st.set_page_config(page_title="Analisys", page_icon="📈", layout="wide")

st.title("📈 Advanced Análisys")
st.markdown("---")
snowflake_conn = SnowflakeConnector()

if not snowflake_conn.connect():
    st.error("⚠️ Configure credentials first")
    st.stop()

# Análise de vendas por região
st.header("💰 Sales by Region")

sales_query = """
SELECT 
    n.N_NAME as REGION,
    COUNT(o.O_ORDERKEY) as total_orders,
    SUM(o.O_TOTALPRICE) as TOTAL_SALES,
    AVG(o.O_TOTALPRICE) as avg_order_value
FROM ORDERS o
JOIN CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
JOIN NATION n ON c.C_NATIONKEY = n.N_NATIONKEY
GROUP BY n.N_NAME
ORDER BY TOTAL_SALES DESC
"""

sales_df = get_cached_query(snowflake_conn, sales_query)

if sales_df is not None:
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de barras
        fig1 = px.bar(sales_df, x='REGION', y='TOTAL_SALES',
                    title='Total Sales by Region',
                    labels={'REGION': 'Region', 'TOTAL_SALES': 'Total Sales'})
        st.plotly_chart(fig1, width=True)
    
    with col2:
        # Gráfico de pizza
        fig2 = px.pie(sales_df, values='TOTAL_SALES', names='REGION',
                     title='Sales Distribution by Region')
        st.plotly_chart(fig2, width=True)

# Análise temporal
st.header("📅 Temporal Trend")

time_query = """
SELECT 
    DATE_TRUNC('month', O_ORDERDATE) as ORDER_MONTH,
    COUNT(O_ORDERKEY) as order_count,
    SUM(O_TOTALPRICE) as MONTHLY_SALES
FROM ORDERS
GROUP BY ORDER_MONTH
ORDER BY ORDER_MONTH
"""

time_df = get_cached_query(snowflake_conn, time_query)

if time_df is not None:
    fig3 = px.line(time_df, x='ORDER_MONTH', y='MONTHLY_SALES',
                  title='Monthly Sales Evolution',
                  labels={'ORDER_MONTH': 'Month', 'MONTHLY_SALES': 'Sales'})
    st.plotly_chart(fig3, width=True)

# Análise de correlação
st.header("🔗 Correlations")

correlation_query = """
SELECT 
    c.C_ACCTBAL as CUSTOMER_BALANCE,
    AVG(o.O_TOTALPRICE) as AVG_ORDER_VALUE,
    COUNT(o.O_ORDERKEY) as ORDER_COUNT
FROM CUSTOMER c
JOIN ORDERS o ON c.C_CUSTKEY = o.O_CUSTKEY
GROUP BY c.C_ACCTBAL
HAVING COUNT(o.O_ORDERKEY) > 1
"""

correlation_df = get_cached_query(snowflake_conn, correlation_query)

if correlation_df is not None:
    fig4 = px.scatter(correlation_df, x='CUSTOMER_BALANCE', y='AVG_ORDER_VALUE',
                     size='ORDER_COUNT', hover_data=['ORDER_COUNT'],
                     title='Relationship: Balance vs Average Order Value',
                     labels={'CUSTOMER_BALANCE': 'Customer Balance', 
                            'AVG_ORDER_VALUE': 'Average Order Value'})
    st.plotly_chart(fig4, width='stretch')

# Painel de métricas avançadas
st.header("📊 Advanced KPIs")

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

kpi_query = """
SELECT 
    COUNT(DISTINCT C_CUSTKEY) as total_customers,
    COUNT(DISTINCT O_ORDERKEY) as total_orders,
    SUM(O_TOTALPRICE) as total_revenue,
    AVG(O_TOTALPRICE) as AVG_ORDER_VALUE
FROM ORDERS o
JOIN CUSTOMER c ON o.O_CUSTKEY = c.C_CUSTKEY
"""

kpi_df = get_cached_query(snowflake_conn, kpi_query)

if kpi_df is not None:
    kpi_col1.metric("Unique Clients", f"{kpi_df['TOTAL_CUSTOMERS'].iloc[0]:,}")
    kpi_col2.metric("Total Orders", f"{kpi_df['TOTAL_ORDERS'].iloc[0]:,}")
    kpi_col3.metric("Total Revenue", f"${kpi_df['TOTAL_REVENUE'].iloc[0]:,.2f}")
    kpi_col4.metric("Medium Ticket", f"${kpi_df['AVG_ORDER_VALUE'].iloc[0]:,.2f}")