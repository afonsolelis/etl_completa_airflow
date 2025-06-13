import pandas as pd
import numpy as np
import logging
from datetime import datetime
import os
import re

class DataTransformer:
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def clean_sales_data(self, sales_df):
        """Limpa e transforma dados de vendas"""
        self.logger.info("Starting sales data cleaning")
        
        # Fazer cópia para não modificar o original
        df = sales_df.copy()
        
        # Remover registros com valores nulos críticos
        initial_count = len(df)
        df = df.dropna(subset=['sale_id', 'customer_id', 'product_id', 'total_amount'])
        self.logger.info(f"Removed {initial_count - len(df)} records with null critical values")
        
        # Converter tipos de dados
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        df['total_amount'] = pd.to_numeric(df['total_amount'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        
        # Validar valores lógicos
        df = df[df['total_amount'] > 0]
        df = df[df['quantity'] > 0]
        df = df[df['unit_price'] > 0]
        
        # Calcular métricas derivadas
        df['calculated_total'] = df['quantity'] * df['unit_price']
        df['price_variance'] = abs(df['total_amount'] - df['calculated_total'])
        df['is_discounted'] = df['price_variance'] > 0.01
        
        # Adicionar categorias de valor
        df['sale_category'] = pd.cut(df['total_amount'], 
                                   bins=[0, 100, 500, 1000, float('inf')],
                                   labels=['Low', 'Medium', 'High', 'Premium'])
        
        # Adicionar informações temporais
        df['year'] = df['sale_date'].dt.year
        df['month'] = df['sale_date'].dt.month
        df['day_of_week'] = df['sale_date'].dt.dayofweek
        df['quarter'] = df['sale_date'].dt.quarter
        
        self.logger.info(f"Sales data cleaning completed. Final count: {len(df)}")
        return df
    
    def clean_customer_data(self, customers_df):
        """Limpa e transforma dados de clientes"""
        self.logger.info("Starting customer data cleaning")
        
        df = customers_df.copy()
        
        # Limpeza de email
        df['email'] = df['email'].str.lower().str.strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        df['is_valid_email'] = df['email'].str.match(email_pattern, na=False)
        
        # Limpeza de telefone
        df['phone'] = df['phone'].astype(str).str.replace(r'[^\d]', '', regex=True)
        
        # Padronização de nomes
        df['customer_name'] = df['customer_name'].str.title().str.strip()
        df['city'] = df['city'].str.title().str.strip()
        df['country'] = df['country'].str.upper().str.strip()
        
        # Converter datas
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df['last_purchase_date'] = pd.to_datetime(df['last_purchase_date'])
        
        # Calcular métricas de engajamento
        current_date = datetime.now()
        df['days_since_registration'] = (current_date - df['registration_date']).dt.days
        df['days_since_last_purchase'] = (current_date - df['last_purchase_date']).dt.days
        
        # Categorizar clientes por recência
        df['customer_segment'] = 'Inactive'
        df.loc[df['days_since_last_purchase'] <= 30, 'customer_segment'] = 'Active'
        df.loc[df['days_since_last_purchase'] <= 7, 'customer_segment'] = 'Highly Active'
        df.loc[df['days_since_last_purchase'] > 365, 'customer_segment'] = 'Churned'
        
        self.logger.info(f"Customer data cleaning completed. Final count: {len(df)}")
        return df
    
    def clean_product_data(self, products_df):
        """Limpa e transforma dados de produtos"""
        self.logger.info("Starting product data cleaning")
        
        df = products_df.copy()
        
        # Padronização de texto
        df['product_name'] = df['product_name'].str.title().str.strip()
        df['category'] = df['category'].str.title().str.strip()
        df['brand'] = df['brand'].str.title().str.strip()
        
        # Converter preços
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
        df['cost_price'] = pd.to_numeric(df['cost_price'], errors='coerce')
        
        # Calcular margem de lucro
        df['profit_margin'] = ((df['unit_price'] - df['cost_price']) / df['unit_price'] * 100).round(2)
        
        # Categorizar por margem
        df['margin_category'] = 'Low'
        df.loc[df['profit_margin'] >= 20, 'margin_category'] = 'Medium'
        df.loc[df['profit_margin'] >= 40, 'margin_category'] = 'High'
        
        # Categorizar por preço
        df['price_category'] = pd.cut(df['unit_price'], 
                                    bins=[0, 50, 200, 500, float('inf')],
                                    labels=['Budget', 'Mid-Range', 'Premium', 'Luxury'])
        
        self.logger.info(f"Product data cleaning completed. Final count: {len(df)}")
        return df
    
    def create_sales_summary(self, sales_df):
        """Cria resumo agregado de vendas"""
        self.logger.info("Creating sales summary")
        
        # Resumo por produto
        product_summary = sales_df.groupby(['product_id', 'product_name', 'category']).agg({
            'quantity': 'sum',
            'total_amount': ['sum', 'mean', 'count'],
            'sale_date': ['min', 'max']
        }).round(2)
        
        product_summary.columns = ['total_quantity', 'total_revenue', 'avg_sale_value', 
                                 'total_sales', 'first_sale', 'last_sale']
        product_summary = product_summary.reset_index()
        
        # Resumo por cliente
        customer_summary = sales_df.groupby(['customer_id', 'customer_name']).agg({
            'total_amount': ['sum', 'mean', 'count'],
            'sale_date': ['min', 'max']
        }).round(2)
        
        customer_summary.columns = ['total_spent', 'avg_order_value', 'total_orders',
                                   'first_purchase', 'last_purchase']
        customer_summary = customer_summary.reset_index()
        
        # Resumo temporal
        daily_summary = sales_df.groupby(sales_df['sale_date'].dt.date).agg({
            'total_amount': 'sum',
            'sale_id': 'count'
        }).round(2)
        
        daily_summary.columns = ['daily_revenue', 'daily_orders']
        daily_summary = daily_summary.reset_index()
        
        self.logger.info("Sales summary creation completed")
        return product_summary, customer_summary, daily_summary
    
    def validate_data_quality(self, df, dataset_name):
        """Valida qualidade dos dados"""
        self.logger.info(f"Validating data quality for {dataset_name}")
        
        quality_report = {
            'dataset': dataset_name,
            'total_records': len(df),
            'total_columns': len(df.columns),
            'null_values': df.isnull().sum().sum(),
            'duplicate_records': df.duplicated().sum(),
            'validation_timestamp': datetime.now().isoformat()
        }
        
        # Calcular porcentagem de completude por coluna
        completeness = ((len(df) - df.isnull().sum()) / len(df) * 100).round(2)
        quality_report['column_completeness'] = completeness.to_dict()
        
        self.logger.info(f"Data quality validation completed for {dataset_name}")
        return quality_report

def main():
    transformer = DataTransformer()
    
    try:
        # Carregar dados brutos
        sales_df = pd.read_csv('/opt/airflow/data/raw/sales_data.csv')
        customers_df = pd.read_csv('/opt/airflow/data/raw/customers_data.csv')
        products_df = pd.read_csv('/opt/airflow/data/raw/products_data.csv')
        
        # Transformar dados
        clean_sales = transformer.clean_sales_data(sales_df)
        clean_customers = transformer.clean_customer_data(customers_df)
        clean_products = transformer.clean_product_data(products_df)
        
        # Criar resumos
        product_summary, customer_summary, daily_summary = transformer.create_sales_summary(clean_sales)
        
        # Validar qualidade
        sales_quality = transformer.validate_data_quality(clean_sales, 'sales')
        customers_quality = transformer.validate_data_quality(clean_customers, 'customers')
        products_quality = transformer.validate_data_quality(clean_products, 'products')
        
        # Salvar dados transformados
        clean_sales.to_csv('/opt/airflow/data/processed/sales_clean.csv', index=False)
        clean_customers.to_csv('/opt/airflow/data/processed/customers_clean.csv', index=False)
        clean_products.to_csv('/opt/airflow/data/processed/products_clean.csv', index=False)
        
        # Salvar resumos
        product_summary.to_csv('/opt/airflow/data/processed/product_summary.csv', index=False)
        customer_summary.to_csv('/opt/airflow/data/processed/customer_summary.csv', index=False)
        daily_summary.to_csv('/opt/airflow/data/processed/daily_summary.csv', index=False)
        
        # Salvar relatórios de qualidade
        import json
        with open('/opt/airflow/data/processed/data_quality_report.json', 'w') as f:
            json.dump([sales_quality, customers_quality, products_quality], f, indent=2)
        
        transformer.logger.info("Data transformation completed successfully")
        
    except Exception as e:
        transformer.logger.error(f"Data transformation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()