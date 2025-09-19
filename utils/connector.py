import os
import snowflake.connector
from dotenv import load_dotenv
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

class SnowflakeConnector:
    def __init__(self):
        self.conn = None
        
    def connect(self):
        """Estabelece conexão com Snowflake"""
        try:
            self.conn = snowflake.connector.connect(
                user=os.getenv('SNOWFLAKE_USER'),
                password=os.getenv('SNOWFLAKE_PASSWORD'),
                account=os.getenv('SNOWFLAKE_ACCOUNT'),
                warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
                database=os.getenv('SNOWFLAKE_DATABASE'),
                schema=os.getenv('SNOWFLAKE_SCHEMA')
            )
            return True
        except Exception as e:
            st.error(f"Connection error {str(e)}")
            return False
    
    def execute_query(self, query):
        """Executa query e retorna DataFrame"""
        try:
            if self.conn is None:
                self.connect()
            
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            import pandas as pd
            df = pd.DataFrame(result, columns=columns)
            return df
            
        except Exception as e:
            st.error(f"Error in query: {str(e)}")
            return None
    
    def close(self):
        """Fecha a conexão"""
        if self.conn:
            self.conn.close()

# Função de utilidade para usar com st.cache
@st.cache_data(ttl=3600)
def get_cached_query(_connector, query):
    """Executa query com cache de 1 hora"""
    return _connector.execute_query(query)


