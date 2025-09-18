import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime

fake = Faker()

# Configurações
num_products = 1000
num_customers = 500
num_orders = 10000  # 10 mil vendas
start_date = '2023-01-01'
end_date = '2023-12-31'
# Converta as datas para datetime.date
start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

# Categorias e regiões
categories = ['Eletrônicos', 'Roupas', 'Casa', 'Beleza', 'Esportes', 'Brinquedos', 'Livros', 'Alimentos', 'Automotivo', 'Jardinagem']
regions = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']



# Gerar produtos
product_names_by_category = {
    'Eletrônicos': ['Smartphone', 'Notebook', 'Fone de Ouvido', 'Tablet', 'Monitor', 'Mouse', 'Teclado', 'Câmera', 'Smartwatch', 'Caixa de Som'],
    'Roupas': ['Camiseta', 'Calça Jeans', 'Vestido', 'Jaqueta', 'Bermuda', 'Blusa', 'Saia', 'Camisa Polo', 'Shorts', 'Casaco'],
    'Casa': ['Sofá', 'Mesa de Jantar', 'Cadeira', 'Cama Box', 'Armário', 'Estante', 'Poltrona', 'Rack', 'Tapete', 'Luminária'],
    'Beleza': ['Perfume', 'Shampoo', 'Condicionador', 'Creme Facial', 'Batom', 'Base', 'Esmalte', 'Sabonete', 'Protetor Solar', 'Desodorante'],
    'Esportes': ['Tênis de Corrida', 'Bicicleta', 'Bola de Futebol', 'Halter', 'Camiseta Esportiva', 'Luvas', 'Raquete', 'Boné', 'Short Esportivo', 'Squeeze'],
    'Brinquedos': ['Quebra-cabeça', 'Boneca', 'Carrinho', 'Jogo de Tabuleiro', 'Lego', 'Pelúcia', 'Pião', 'Bola', 'Blocos de Montar', 'Patinete'],
    'Livros': ['Romance', 'Biografia', 'Livro Infantil', 'Ficção Científica', 'Autoajuda', 'História', 'Fantasia', 'HQ', 'Didático', 'Suspense'],
    'Alimentos': ['Arroz', 'Feijão', 'Macarrão', 'Azeite', 'Chocolate', 'Café', 'Biscoito', 'Leite', 'Suco', 'Queijo'],
    'Automotivo': ['Pneu', 'Óleo de Motor', 'Bateria', 'Lâmpada', 'Filtro de Ar', 'Tapete Automotivo', 'Capa de Banco', 'Calota', 'Kit Ferramentas', 'GPS'],
    'Jardinagem': ['Vaso de Planta', 'Terra Adubada', 'Tesoura de Poda', 'Regador', 'Sementes', 'Adubo', 'Mangueira', 'Luvas de Jardim', 'Pá', 'Cortador de Grama']
}

# Gerar produtos
products = []
for i in range(1, num_products + 1):
    category = random.choice(categories)
    product_base = random.choice(product_names_by_category[category])
    product = {
        'product_id': i,
        'product_name': f"{product_base} {i}",
        'category': category,
        'price': round(random.uniform(5, 500), 2)
    }
    products.append(product)
products_df = pd.DataFrame(products)

# Gerar clientes
customers = []
for i in range(1, num_customers + 1):
    customer = {
        'customer_id': i,
        'customer_region': random.choice(regions)
    }
    customers.append(customer)
customers_df = pd.DataFrame(customers)

# Gerar vendas
orders = []
for order_id in range(1, num_orders + 1):
    order_date = fake.date_between(start_date=start_date, end_date=end_date)
    product = products_df.sample(1).iloc[0]
    customer = customers_df.sample(1).iloc[0]
    quantity = random.randint(1, 5)
    total_price = round(quantity * product['price'], 2)
    
    order = {
        'order_id': order_id,
        'order_date': order_date,
        'product_id': product['product_id'],
        'product_name': product['product_name'],
        'category': product['category'],
        'quantity': quantity,
        'price': product['price'],
        'total_price': total_price,
        'customer_id': customer['customer_id'],
        'customer_region': customer['customer_region']
    }
    orders.append(order)
# Salvar CSV de customers
customers_df.to_csv('customers.csv', index=False)

# Salvar CSV de regions (apenas regiões únicas)
regions_df = pd.DataFrame({'region': regions})
regions_df.to_csv('regions.csv', index=False)    

orders_df = pd.DataFrame(orders)

# Salvar CSV
orders_df.to_csv('vendas_ecommerce_2023_completo.csv', index=False)

print("Arquivos 'vendas_ecommerce_2023_completo.csv', 'customers.csv' e 'regions.csv' criados com sucesso!")