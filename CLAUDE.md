# Pipeline DataOps - Guia do Projeto

## Visão Geral
Este projeto implementa um pipeline completo de DataOps usando Apache Airflow, PostgreSQL, Redis, Jupyter, Grafana, Prometheus e MinIO. O pipeline ETL processa dados de APIs externas e bases de dados, transformando e carregando em um data warehouse.

## Estrutura do Projeto

### Diretórios Principais

- **`airflow/`** - Configurações do Apache Airflow
  - `dags/etl_pipeline.py` - Pipeline principal de ETL
  - `logs/` - Logs do Airflow
  - `plugins/` - Plugins customizados

- **`etl/`** - Scripts do pipeline ETL
  - `extract/` - Extração de dados
    - `api_extractor.py` - Extrai dados de APIs externas
    - `db_extractor.py` - Extrai dados do banco
  - `transform/` - Transformação de dados
    - `data_transformer.py` - Limpeza e transformação
  - `load/` - Carregamento de dados
    - `data_loader.py` - Carrega dados no warehouse

- **`data/`** - Armazenamento de dados
  - `raw/` - Dados brutos extraídos
  - `processed/` - Dados transformados
  - `warehouse/` - Dados finais do warehouse

- **`monitoring/`** - Configurações de monitoramento
  - `grafana/` - Dashboards e datasources
  - `prometheus.yml` - Configuração de métricas

- **`sql/`** - Scripts SQL
  - `create_tables.sql` - Criação de tabelas
  - `sample_data.sql` - Dados de exemplo

- **`notebooks/`** - Análises exploratórias
  - `data_analysis.ipynb` - Notebook principal

## Como Executar o Projeto

### Pré-requisitos
- Docker e Docker Compose
- Make (opcional, mas recomendado)

### Configuração Inicial
```bash
# Configuração completa para desenvolvimento
make dev-setup
```

### Comandos Principais

#### Gerenciamento de Serviços
```bash
make up          # Inicia todos os serviços
make down        # Para todos os serviços
make restart     # Reinicia todos os serviços
make status      # Mostra status dos serviços
```

#### Monitoramento
```bash
make logs            # Logs de todos os serviços
make logs-airflow    # Logs específicos do Airflow
make check-health    # Verifica saúde dos serviços
make monitor         # Abre interfaces de monitoramento
```

#### Pipeline ETL
```bash
make trigger-dag     # Executa o pipeline ETL
make list-dags       # Lista todas as DAGs
make test-pipeline   # Testa o pipeline completo
```

#### Utilitários
```bash
make backup-data     # Backup dos dados
make clean          # Remove containers e volumes
make jupyter        # Abre Jupyter Notebook
```

## Serviços e Portas

### Interfaces Web
- **Airflow**: http://localhost:8080 (admin/admin)
- **Jupyter**: http://localhost:8888 (token: dataops123)
- **Grafana**: http://localhost:3000 (admin/admin)
- **Adminer**: http://localhost:8081
- **MinIO**: http://localhost:9001 (minioadmin/minioadmin123)
- **Prometheus**: http://localhost:9090

### Bancos de Dados
- **PostgreSQL Dados**: localhost:5432 (dataops/dataops123)
- **PostgreSQL Airflow**: localhost:5433 (airflow/airflow)
- **Redis**: localhost:6379

## Pipeline ETL

### Fluxo de Dados
1. **Extract**: Coleta dados de APIs externas e banco fonte
2. **Transform**: Limpa, valida e transforma os dados
3. **Load**: Carrega dados no data warehouse

### Fontes de Dados
- **APIs Externas**: JSONPlaceholder (usuários, posts)
- **Dados Simulados**: Clima, indicadores econômicos
- **Banco Fonte**: Dados transacionais

### Agendamento
- Pipeline executa automaticamente via Airflow
- Configurável para execução diária/horária
- Monitoramento via Grafana

## GitHub Actions

### Workflow `etl_now`
- **Trigger**: Push para main/master
- **Ações**: 
  - Configura ambiente Python
  - Instala dependências
  - Executa pipeline ETL completo
  - Verifica resultados

```bash
# Testar localmente com act
act
```

## Comandos de Desenvolvimento

### Teste Local
```bash
# Testar ETL manualmente
cd etl/extract && python api_extractor.py
cd etl/transform && python data_transformer.py
cd etl/load && python data_loader.py
```

### Análise de Dados
```bash
# Abrir Jupyter para análises
make jupyter
```

### Monitoramento
```bash
# Verificar métricas no Prometheus
curl http://localhost:9090/metrics

# Verificar logs do Airflow
make logs-airflow
```

## Troubleshooting

### Problemas Comuns
1. **Serviços não iniciam**: Verificar portas em uso
2. **ETL falha**: Verificar logs do Airflow
3. **Dados não aparecem**: Verificar conexões de banco

### Comandos de Diagnóstico
```bash
make status          # Status dos containers
make logs           # Logs completos
docker ps           # Containers ativos
docker system df    # Uso de espaço
```

### Reset Completo
```bash
make clean          # Remove tudo
make dev-setup      # Reconfigura ambiente
```

## Estrutura de Dados

### Tabelas Principais
- `users` - Dados de usuários
- `posts` - Posts/atividades
- `weather` - Dados meteorológicos
- `economic_indicators` - Indicadores econômicos
- `processed_metrics` - Métricas agregadas

### Formatos de Arquivo
- **CSV**: Dados brutos e processados
- **JSON**: Configurações e metadados
- **SQL**: Scripts de banco

## Segurança

### Credenciais Padrão
- Alterar senhas em produção
- Usar variáveis de ambiente
- Configurar SSL/TLS para produção

### Backup
```bash
make backup-data    # Backup automático com timestamp
```