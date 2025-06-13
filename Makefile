.PHONY: help build up down restart logs clean status check-health

# Configurações
COMPOSE_FILE = docker-compose.yml
PROJECT_NAME = dataops-pipeline

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Constrói as imagens Docker
	docker-compose -f $(COMPOSE_FILE) build

up: ## Inicia todos os serviços
	@echo "Iniciando pipeline DataOps..."
	docker-compose -f $(COMPOSE_FILE) up -d
	@echo "Aguardando inicialização dos serviços..."
	@sleep 30
	@make check-health

down: ## Para todos os serviços
	docker-compose -f $(COMPOSE_FILE) down

restart: ## Reinicia todos os serviços
	@make down
	@make up

logs: ## Mostra logs de todos os serviços
	docker-compose -f $(COMPOSE_FILE) logs -f

logs-airflow: ## Mostra logs específicos do Airflow
	docker-compose -f $(COMPOSE_FILE) logs -f airflow-webserver airflow-scheduler

logs-postgres: ## Mostra logs do PostgreSQL
	docker-compose -f $(COMPOSE_FILE) logs -f postgres-data

status: ## Mostra status dos serviços
	docker-compose -f $(COMPOSE_FILE) ps

check-health: ## Verifica saúde dos serviços
	@echo "Verificando saúde dos serviços..."
	@echo "Airflow: http://localhost:8080 (admin/admin)"
	@echo "Jupyter: http://localhost:8888 (token: dataops123)"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Adminer: http://localhost:8081"
	@echo "MinIO: http://localhost:9001 (minioadmin/minioadmin123)"
	@echo "Prometheus: http://localhost:9090"

clean: ## Remove containers, volumes e imagens
	docker-compose -f $(COMPOSE_FILE) down -v --rmi all
	docker system prune -f

install-deps: ## Instala dependências locais
	pip install pandas sqlalchemy psycopg2-binary requests matplotlib seaborn jupyter

setup: ## Configuração inicial completa
	@echo "Configurando ambiente DataOps..."
	@cp .env.example .env
	@mkdir -p data/raw data/processed data/warehouse
	@mkdir -p airflow/logs
	@chmod 777 airflow/logs data
	@echo "Setup concluído!"

init-airflow: ## Inicializa banco do Airflow
	docker-compose -f $(COMPOSE_FILE) exec airflow-webserver airflow db init

reset-airflow: ## Reseta banco do Airflow
	docker-compose -f $(COMPOSE_FILE) exec airflow-webserver airflow db reset

trigger-dag: ## Triggera a DAG do pipeline ETL
	docker-compose -f $(COMPOSE_FILE) exec airflow-webserver airflow dags trigger etl_pipeline

list-dags: ## Lista todas as DAGs
	docker-compose -f $(COMPOSE_FILE) exec airflow-webserver airflow dags list

backup-data: ## Faz backup dos dados
	@echo "Fazendo backup dos dados..."
	@mkdir -p backup/$(shell date +%Y%m%d_%H%M%S)
	@docker-compose -f $(COMPOSE_FILE) exec postgres-data pg_dump -U dataops datawarehouse > backup/$(shell date +%Y%m%d_%H%M%S)/database_backup.sql
	@cp -r data backup/$(shell date +%Y%m%d_%H%M%S)/
	@echo "Backup concluído em backup/$(shell date +%Y%m%d_%H%M%S)/"

test-pipeline: ## Testa o pipeline ETL
	@echo "Testando pipeline ETL..."
	@make trigger-dag
	@echo "Pipeline triggerado. Verifique o status no Airflow UI."

dev-setup: setup build up ## Configuração completa para desenvolvimento
	@echo "Ambiente de desenvolvimento pronto!"
	@make check-health

prod-setup: ## Configuração para produção
	@echo "Configurando para produção..."
	@docker-compose -f $(COMPOSE_FILE) up -d --scale airflow-triggerer=2
	@make check-health

monitor: ## Abre interfaces de monitoramento
	@echo "Abrindo interfaces de monitoramento..."
	@open http://localhost:3000 2>/dev/null || echo "Grafana: http://localhost:3000"
	@open http://localhost:9090 2>/dev/null || echo "Prometheus: http://localhost:9090"
	@open http://localhost:8080 2>/dev/null || echo "Airflow: http://localhost:8080"

jupyter: ## Abre Jupyter Notebook
	@open http://localhost:8888 2>/dev/null || echo "Jupyter: http://localhost:8888 (token: dataops123)"