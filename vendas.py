import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Dashboard E-commerce",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📦 Dashboard de Vendas E-commerce")
st.markdown("---")

# Sidebar para upload ou seleção de arquivos
st.sidebar.title("Navegação")
st.sidebar.info("Explore os dados de vendas e clientes")

# Carregar dados
@st.cache_data
def load_data():
    vendas = pd.read_csv("vendas_ecommerce_2023_completo.csv", parse_dates=["order_date"])
    customers = pd.read_csv("customers.csv")
    return vendas, customers

vendas, customers = load_data()

# Filtros interativos
st.sidebar.header("Filtros")
region = st.sidebar.multiselect(
    "Região do Cliente",
    options=customers["customer_region"].unique(),
    default=customers["customer_region"].unique()
)

category = st.sidebar.multiselect(
    "Categoria do Produto",
    options=vendas["category"].unique(),
    default=vendas["category"].unique()
)

# Filtrar dados
filtered_vendas = vendas[
    (vendas["category"].isin(category)) &
    (vendas["customer_region"].isin(region))
]

# KPIs
st.subheader("📊 Indicadores")
col1, col2, col3 = st.columns(3)
col1.metric("Total de Vendas", f"R$ {filtered_vendas['total_price'].sum():,.2f}")
col2.metric("Pedidos", f"{filtered_vendas['order_id'].nunique()}")
col3.metric("Clientes", f"{filtered_vendas['customer_id'].nunique()}")

st.markdown("---")

# Tabela de vendas filtrada
st.header("📝 Tabela de Vendas")
st.dataframe(filtered_vendas.head(50))

# Gráfico de vendas por categoria
st.header("📈 Vendas por Categoria")
vendas_categoria = filtered_vendas.groupby("category")["total_price"].sum().sort_values(ascending=False)
st.bar_chart(vendas_categoria)

# Gráfico de vendas por região
st.header("🌎 Vendas por Região")
vendas_regiao = filtered_vendas.groupby("customer_region")["total_price"].sum().sort_values(ascending=False)
st.bar_chart(vendas_regiao)

# Exibir tabela de clientes
with st.expander("👥 Ver tabela de clientes"):
    st.dataframe(customers)