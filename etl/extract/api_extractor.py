import requests
import pandas as pd
import json
import logging
from datetime import datetime
import os
import time

class APIExtractor:
    def __init__(self, base_url=None, api_key=None):
        self.base_url = base_url or "https://jsonplaceholder.typicode.com"
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({'Authorization': f'Bearer {api_key}'})
    
    def extract_external_data(self):
        """Extrai dados externos de APIs simuladas"""
        try:
            # Simular dados de usuários externos
            users_response = self.session.get(f"{self.base_url}/users")
            users_data = users_response.json()
            
            # Simular dados de posts/atividades
            posts_response = self.session.get(f"{self.base_url}/posts")
            posts_data = posts_response.json()
            
            # Converter para DataFrames
            users_df = pd.DataFrame(users_data)
            posts_df = pd.DataFrame(posts_data)
            
            # Adicionar timestamp de extração
            extraction_time = datetime.now().isoformat()
            users_df['extraction_timestamp'] = extraction_time
            posts_df['extraction_timestamp'] = extraction_time
            
            logging.info(f"Extracted {len(users_df)} users and {len(posts_df)} posts from API")
            
            return users_df, posts_df
            
        except Exception as e:
            logging.error(f"Error extracting data from API: {str(e)}")
            raise
    
    def extract_weather_data(self):
        """Simula extração de dados meteorológicos"""
        # Dados simulados de clima para diferentes cidades
        weather_data = [
            {
                'city': 'São Paulo',
                'temperature': 23.5,
                'humidity': 68,
                'weather_condition': 'Cloudy',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'extraction_timestamp': datetime.now().isoformat()
            },
            {
                'city': 'Rio de Janeiro',
                'temperature': 28.2,
                'humidity': 75,
                'weather_condition': 'Sunny',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'extraction_timestamp': datetime.now().isoformat()
            },
            {
                'city': 'Belo Horizonte',
                'temperature': 25.1,
                'humidity': 62,
                'weather_condition': 'Partly Cloudy',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'extraction_timestamp': datetime.now().isoformat()
            }
        ]
        
        weather_df = pd.DataFrame(weather_data)
        logging.info(f"Generated {len(weather_df)} weather records")
        
        return weather_df
    
    def extract_economic_indicators(self):
        """Simula extração de indicadores econômicos"""
        # Dados simulados de indicadores econômicos
        economic_data = [
            {
                'indicator': 'USD_BRL',
                'value': 5.25,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Central Bank',
                'extraction_timestamp': datetime.now().isoformat()
            },
            {
                'indicator': 'SELIC',
                'value': 11.75,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Central Bank',
                'extraction_timestamp': datetime.now().isoformat()
            },
            {
                'indicator': 'IPCA',
                'value': 4.62,
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'IBGE',
                'extraction_timestamp': datetime.now().isoformat()
            }
        ]
        
        economic_df = pd.DataFrame(economic_data)
        logging.info(f"Generated {len(economic_df)} economic indicator records")
        
        return economic_df

def main():
    # Configuração do logging
    logging.basicConfig(level=logging.INFO)
    
    extractor = APIExtractor()
    
    try:
        # Extrair dados de APIs
        users_df, posts_df = extractor.extract_external_data()
        weather_df = extractor.extract_weather_data()
        economic_df = extractor.extract_economic_indicators()
        
        # Salvar dados extraídos
        users_df.to_csv('/opt/airflow/data/raw/external_users.csv', index=False)
        posts_df.to_csv('/opt/airflow/data/raw/external_posts.csv', index=False)
        weather_df.to_csv('/opt/airflow/data/raw/weather_data.csv', index=False)
        economic_df.to_csv('/opt/airflow/data/raw/economic_indicators.csv', index=False)
        
        logging.info("API data extraction completed successfully")
        
    except Exception as e:
        logging.error(f"API extraction failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()