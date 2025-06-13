import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import os
import json

class DataLoader:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(connection_string)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_warehouse_tables(self):
        """Cria tabelas do data warehouse se não existirem"""
        self.logger.info("Creating warehouse tables")
        
        create_tables_sql = """
        -- Tabela de dimensão tempo
        CREATE TABLE IF NOT EXISTS dim_time (
            date_key INTEGER PRIMARY KEY,
            full_date DATE,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            quarter INTEGER,
            day_of_week INTEGER,
            month_name VARCHAR(20),
            day_name VARCHAR(20),
            is_weekend BOOLEAN
        );
        
        -- Tabela de dimensão produto
        CREATE TABLE IF NOT EXISTS dim_product (
            product_key SERIAL PRIMARY KEY,
            product_id INTEGER,
            product_name VARCHAR(255),
            category VARCHAR(100),
            brand VARCHAR(100),
            unit_price DECIMAL(10,2),
            cost_price DECIMAL(10,2),
            profit_margin DECIMAL(5,2),
            margin_category VARCHAR(20),
            price_category VARCHAR(20),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Tabela de dimensão cliente
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_key SERIAL PRIMARY KEY,
            customer_id INTEGER,
            customer_name VARCHAR(255),
            email VARCHAR(255),
            city VARCHAR(100),
            country VARCHAR(100),
            customer_segment VARCHAR(50),
            registration_date DATE,
            is_valid_email BOOLEAN,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Tabela fato de vendas
        CREATE TABLE IF NOT EXISTS fact_sales (
            sale_key SERIAL PRIMARY KEY,
            sale_id INTEGER,
            customer_key INTEGER REFERENCES dim_customer(customer_key),
            product_key INTEGER REFERENCES dim_product(product_key),
            date_key INTEGER REFERENCES dim_time(date_key),
            quantity INTEGER,
            unit_price DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            is_discounted BOOLEAN,
            sale_category VARCHAR(20),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Tabela de métricas agregadas
        CREATE TABLE IF NOT EXISTS agg_daily_sales (
            date_key INTEGER,
            total_revenue DECIMAL(12,2),
            total_orders INTEGER,
            avg_order_value DECIMAL(10,2),
            unique_customers INTEGER,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (date_key)
        );
        
        -- Tabela de métricas de produto
        CREATE TABLE IF NOT EXISTS agg_product_metrics (
            product_key INTEGER,
            period_start DATE,
            period_end DATE,
            total_quantity INTEGER,
            total_revenue DECIMAL(12,2),
            total_sales INTEGER,
            avg_sale_value DECIMAL(10,2),
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (product_key, period_start)
        );
        
        -- Tabela de auditoria
        CREATE TABLE IF NOT EXISTS etl_audit_log (
            log_id SERIAL PRIMARY KEY,
            process_name VARCHAR(100),
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            status VARCHAR(20),
            records_processed INTEGER,
            error_message TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text(create_tables_sql))
                conn.commit()
            self.logger.info("Warehouse tables created successfully")
        except Exception as e:
            self.logger.error(f"Error creating warehouse tables: {str(e)}")
            raise
    
    def log_etl_process(self, process_name, start_time, end_time, status, records_processed, error_message=None):
        """Registra log do processo ETL"""
        log_data = {
            'process_name': process_name,
            'start_time': start_time,
            'end_time': end_time,
            'status': status,
            'records_processed': records_processed,
            'error_message': error_message
        }
        
        log_df = pd.DataFrame([log_data])
        log_df.to_sql('etl_audit_log', self.engine, if_exists='append', index=False)
    
    def load_dimension_tables(self):
        """Carrega tabelas de dimensão"""
        start_time = datetime.now()
        
        try:
            # Carregar dados limpos
            customers_df = pd.read_csv('/opt/airflow/data/processed/customers_clean.csv')
            products_df = pd.read_csv('/opt/airflow/data/processed/products_clean.csv')
            
            # Preparar dimensão cliente
            dim_customer = customers_df[[
                'customer_id', 'customer_name', 'email', 'city', 'country',
                'customer_segment', 'registration_date', 'is_valid_email'
            ]].copy()
            
            # Preparar dimensão produto
            dim_product = products_df[[
                'product_id', 'product_name', 'category', 'brand',
                'unit_price', 'cost_price', 'profit_margin',
                'margin_category', 'price_category'
            ]].copy()
            
            # Carregar dimensões (usando upsert para evitar duplicatas)
            with self.engine.connect() as conn:
                # Limpar tabelas de dimensão
                conn.execute(text("TRUNCATE TABLE dim_customer RESTART IDENTITY CASCADE"))
                conn.execute(text("TRUNCATE TABLE dim_product RESTART IDENTITY CASCADE"))
                conn.commit()
            
            # Inserir dados
            records_customer = len(dim_customer)
            records_product = len(dim_product)
            
            dim_customer.to_sql('dim_customer', self.engine, if_exists='append', index=False)
            dim_product.to_sql('dim_product', self.engine, if_exists='append', index=False)
            
            end_time = datetime.now()
            total_records = records_customer + records_product
            
            self.log_etl_process('load_dimensions', start_time, end_time, 'SUCCESS', total_records)
            self.logger.info(f"Dimension tables loaded: {records_customer} customers, {records_product} products")
            
        except Exception as e:
            end_time = datetime.now()
            self.log_etl_process('load_dimensions', start_time, end_time, 'FAILED', 0, str(e))
            self.logger.error(f"Error loading dimension tables: {str(e)}")
            raise
    
    def generate_time_dimension(self, start_date, end_date):
        """Gera dimensão tempo"""
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        time_data = []
        for date in date_range:
            time_record = {
                'date_key': int(date.strftime('%Y%m%d')),
                'full_date': date.date(),
                'year': date.year,
                'month': date.month,
                'day': date.day,
                'quarter': date.quarter,
                'day_of_week': date.dayofweek,
                'month_name': date.strftime('%B'),
                'day_name': date.strftime('%A'),
                'is_weekend': date.dayofweek >= 5
            }
            time_data.append(time_record)
        
        dim_time = pd.DataFrame(time_data)
        
        # Carregar dimensão tempo
        with self.engine.connect() as conn:
            conn.execute(text("DELETE FROM dim_time WHERE date_key IN ({})".format(
                ','.join([str(key) for key in dim_time['date_key']])
            )))
            conn.commit()
        
        dim_time.to_sql('dim_time', self.engine, if_exists='append', index=False)
        self.logger.info(f"Time dimension loaded: {len(dim_time)} records")
    
    def load_fact_table(self):
        """Carrega tabela fato de vendas"""
        start_time = datetime.now()
        
        try:
            # Carregar dados de vendas limpos
            sales_df = pd.read_csv('/opt/airflow/data/processed/sales_clean.csv')
            
            # Converter date para date_key
            sales_df['sale_date'] = pd.to_datetime(sales_df['sale_date'])
            sales_df['date_key'] = sales_df['sale_date'].dt.strftime('%Y%m%d').astype(int)
            
            # Buscar chaves das dimensões
            with self.engine.connect() as conn:
                customer_keys = pd.read_sql(
                    "SELECT customer_key, customer_id FROM dim_customer", conn
                )
                product_keys = pd.read_sql(
                    "SELECT product_key, product_id FROM dim_product", conn
                )
            
            # Fazer joins para obter as chaves
            sales_with_keys = sales_df.merge(customer_keys, on='customer_id', how='left')
            sales_with_keys = sales_with_keys.merge(product_keys, on='product_id', how='left')
            
            # Preparar dados para a tabela fato
            fact_sales = sales_with_keys[[
                'sale_id', 'customer_key', 'product_key', 'date_key',
                'quantity', 'unit_price', 'total_amount', 'is_discounted', 'sale_category'
            ]].copy()
            
            # Remover registros sem chaves válidas
            fact_sales = fact_sales.dropna(subset=['customer_key', 'product_key'])
            
            # Carregar tabela fato
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE fact_sales RESTART IDENTITY"))
                conn.commit()
            
            records_processed = len(fact_sales)
            fact_sales.to_sql('fact_sales', self.engine, if_exists='append', index=False)
            
            end_time = datetime.now()
            self.log_etl_process('load_fact_sales', start_time, end_time, 'SUCCESS', records_processed)
            self.logger.info(f"Fact table loaded: {records_processed} records")
            
        except Exception as e:
            end_time = datetime.now()
            self.log_etl_process('load_fact_sales', start_time, end_time, 'FAILED', 0, str(e))
            self.logger.error(f"Error loading fact table: {str(e)}")
            raise
    
    def load_aggregated_tables(self):
        """Carrega tabelas agregadas"""
        start_time = datetime.now()
        
        try:
            # Carregar resumos
            daily_summary = pd.read_csv('/opt/airflow/data/processed/daily_summary.csv')
            product_summary = pd.read_csv('/opt/airflow/data/processed/product_summary.csv')
            
            # Preparar agregação diária
            daily_summary['sale_date'] = pd.to_datetime(daily_summary['sale_date'])
            daily_summary['date_key'] = daily_summary['sale_date'].dt.strftime('%Y%m%d').astype(int)
            
            agg_daily = daily_summary[['date_key', 'daily_revenue', 'daily_orders']].copy()
            agg_daily.columns = ['date_key', 'total_revenue', 'total_orders']
            agg_daily['avg_order_value'] = (agg_daily['total_revenue'] / agg_daily['total_orders']).round(2)
            agg_daily['unique_customers'] = agg_daily['total_orders']  # Simplificado
            
            # Carregar agregações
            with self.engine.connect() as conn:
                conn.execute(text("TRUNCATE TABLE agg_daily_sales"))
                conn.commit()
            
            agg_daily.to_sql('agg_daily_sales', self.engine, if_exists='append', index=False)
            
            end_time = datetime.now()
            records_processed = len(agg_daily)
            self.log_etl_process('load_aggregations', start_time, end_time, 'SUCCESS', records_processed)
            self.logger.info(f"Aggregated tables loaded: {records_processed} daily records")
            
        except Exception as e:
            end_time = datetime.now()
            self.log_etl_process('load_aggregations', start_time, end_time, 'FAILED', 0, str(e))
            self.logger.error(f"Error loading aggregated tables: {str(e)}")
            raise

def main():
    # Configuração da conexão
    connection_string = os.getenv(
        'WAREHOUSE_DB_CONNECTION',
        'postgresql://dataops:dataops123@postgres-data:5432/dataops'
    )
    
    loader = DataLoader(connection_string)
    
    try:
        # Criar estrutura do warehouse
        loader.create_warehouse_tables()
        
        # Gerar dimensão tempo
        loader.generate_time_dimension('2024-01-01', '2025-12-31')
        
        # Carregar dimensões
        loader.load_dimension_tables()
        
        # Carregar fatos
        loader.load_fact_table()
        
        # Carregar agregações
        loader.load_aggregated_tables()
        
        loader.logger.info("Data loading completed successfully")
        
    except Exception as e:
        loader.logger.error(f"Data loading failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()