import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Dashboard E-commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📦 Sales Dashboard ")
st.markdown("---")

# Sidebar para upload ou seleção de arquivos
st.sidebar.title("Navigation")
st.sidebar.info("Explore sales and customer data")

# Carregar dados
@st.cache_data
def load_data():
    vendas = pd.read_csv("vendas_ecommerce_2023_completo.csv", parse_dates=["order_date"])
    customers = pd.read_csv("customers.csv")
    return vendas, customers

vendas, customers = load_data()

# Filtros interativos
st.sidebar.header("Filters")
region = st.sidebar.multiselect(
    "Customer Region",
    options=customers["customer_region"].unique(),
    default=customers["customer_region"].unique()
)

category = st.sidebar.multiselect(
    "Category by Product",
    options=vendas["category"].unique(),
    default=vendas["category"].unique()
)

# Filtrar dados
filtered_vendas = vendas[
    (vendas["category"].isin(category)) &
    (vendas["customer_region"].isin(region))
]

# KPIs
st.subheader("📊 Indicadtors")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"R$ {filtered_vendas['total_price'].sum():,.2f}")
col2.metric("Orders", f"{filtered_vendas['order_id'].nunique()}")
col3.metric("Customers", f"{filtered_vendas['customer_id'].nunique()}")

st.markdown("---")

# Tabela de vendas filtrada
st.header("📝 Sales Table")
st.dataframe(filtered_vendas.head(50))

# Gráfico de vendas por categoria
st.header("📈 Sales by Category")
vendas_categoria = filtered_vendas.groupby("category")["total_price"].sum().sort_values(ascending=False)
st.bar_chart(vendas_categoria)

# Gráfico de vendas por região
st.header("🌎 Region Sales")
vendas_regiao = filtered_vendas.groupby("customer_region")["total_price"].sum().sort_values(ascending=False)
st.bar_chart(vendas_regiao)

# Exibir tabela de clientes
with st.expander("👥 Expand clients table"):
    st.dataframe(customers)