import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import logging
from datetime import datetime, timedelta
import os

class DatabaseExtractor:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        
    def extract_sales_data(self, start_date=None, end_date=None):
        """Extrai dados de vendas do banco operacional"""
        if not start_date:
            start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        query = """
        SELECT 
            s.sale_id,
            s.customer_id,
            s.product_id,
            s.quantity,
            s.unit_price,
            s.total_amount,
            s.sale_date,
            c.customer_name,
            c.email,
            c.city,
            c.country,
            p.product_name,
            p.category,
            p.brand
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        JOIN products p ON s.product_id = p.product_id
        WHERE s.sale_date BETWEEN %s AND %s
        ORDER BY s.sale_date
        """
        
        try:
            df = pd.read_sql_query(query, self.engine, params=[start_date, end_date])
            logging.info(f"Extracted {len(df)} sales records from {start_date} to {end_date}")
            return df
        except Exception as e:
            logging.error(f"Error extracting sales data: {str(e)}")
            raise
            
    def extract_customer_data(self):
        """Extrai dados de clientes"""
        query = """
        SELECT 
            customer_id,
            customer_name,
            email,
            phone,
            address,
            city,
            country,
            registration_date,
            last_purchase_date,
            total_purchases,
            customer_status
        FROM customers
        WHERE customer_status = 'active'
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logging.info(f"Extracted {len(df)} customer records")
            return df
        except Exception as e:
            logging.error(f"Error extracting customer data: {str(e)}")
            raise
            
    def extract_product_data(self):
        """Extrai dados de produtos"""
        query = """
        SELECT 
            product_id,
            product_name,
            category,
            brand,
            unit_price,
            cost_price,
            stock_quantity,
            supplier_id,
            product_status,
            created_date,
            last_updated
        FROM products
        WHERE product_status = 'active'
        """
        
        try:
            df = pd.read_sql_query(query, self.engine)
            logging.info(f"Extracted {len(df)} product records")
            return df
        except Exception as e:
            logging.error(f"Error extracting product data: {str(e)}")
            raise

def main():
    # Configuração do logging
    logging.basicConfig(level=logging.INFO)
    
    # String de conexão
    connection_string = os.getenv(
        'SOURCE_DB_CONNECTION', 
        'postgresql://dataops:dataops123@postgres-data:5432/dataops'
    )
    
    extractor = DatabaseExtractor(connection_string)
    
    # Extrair dados
    sales_df = extractor.extract_sales_data()
    customers_df = extractor.extract_customer_data()
    products_df = extractor.extract_product_data()
    
    # Salvar dados extraídos
    sales_df.to_csv('/opt/airflow/data/raw/sales_data.csv', index=False)
    customers_df.to_csv('/opt/airflow/data/raw/customers_data.csv', index=False)
    products_df.to_csv('/opt/airflow/data/raw/products_data.csv', index=False)
    
    logging.info("Data extraction completed successfully")

if __name__ == "__main__":
    main()