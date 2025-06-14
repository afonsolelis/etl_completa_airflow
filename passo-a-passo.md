# Passo-a-Passo: Como Executar e Monitorar o Pipeline DataOps

## 🚀 **CONFIGURAÇÃO INICIAL**

### Passo 1: Preparar o Ambiente
```bash
# 1. Configuração completa (primeira vez)
make dev-setup

# OU se já tem o ambiente:
make up
```

**O que acontece:**
- ✅ Cria diretórios necessários
- ✅ Copia arquivo .env
- ✅ Constrói imagens Docker
- ✅ Inicia todos os serviços
- ✅ Aguarda 30 segundos para inicialização

### Passo 2: Verificar se Tudo Está Funcionando
```bash
make status
```

**Você deve ver algo assim:**
```
       Name                     Command               State           Ports         
-----------------------------------------------------------------------------------
adminer              entrypoint.sh docker-php-e...   Up      0.0.0.0:8081->8080/tcp
airflow-scheduler    /usr/bin/dumb-init -- /ent...   Up      8080/tcp              
airflow-webserver    /usr/bin/dumb-init -- /ent...   Up      0.0.0.0:8080->8080/tcp
grafana              /run.sh                          Up      0.0.0.0:3000->3000/tcp
jupyter              tini -g -- start-notebook.sh    Up      0.0.0.0:8888->8888/tcp
minio                /usr/bin/docker-entrypoint ...   Up      0.0.0.0:9001->9001/tcp
postgres-airflow     docker-entrypoint.sh postgres   Up      0.0.0.0:5433->5432/tcp
postgres-data        docker-entrypoint.sh postgres   Up      0.0.0.0:5432->5432/tcp
prometheus           /bin/prometheus --config.f...   Up      0.0.0.0:9090->9090/tcp
redis                docker-entrypoint.sh redis ...   Up      0.0.0.0:6379->6379/tcp
```

---

## 📊 **EXECUTANDO O PIPELINE**

### Passo 3: Executar o Pipeline ETL
```bash
make test-pipeline
```

**Saída esperada:**
```
Testando pipeline ETL...
Triggering DAG with dag_id: etl_pipeline
Pipeline triggerado. Verifique o status no Airflow UI.
```

### Passo 4: Monitorar a Execução (3 Opções)

#### **OPÇÃO A: Airflow UI (Visual - Recomendado)**
1. **Abra o navegador:** http://localhost:8080
2. **Login:** `admin` / `admin`
3. **Clique em:** "DAGs" → "etl_pipeline"
4. **Veja a execução:** Clique na execução mais recente

**O que você verá:**
- 🔵 **Azul**: Task em execução
- 🟢 **Verde**: Task concluída com sucesso
- 🔴 **Vermelho**: Task falhou
- ⚪ **Branco**: Task aguardando

#### **OPÇÃO B: Logs em Tempo Real (Terminal)**
```bash
# Terminal 1: Logs do Airflow
make logs-airflow

# Terminal 2: Logs de todos os serviços
make logs
```

#### **OPÇÃO C: Status dos Containers**
```bash
# Verificar se containers estão rodando
make status

# Verificar saúde dos serviços
make check-health
```

---

## 🔍 **VERIFICANDO OS RESULTADOS**

### Passo 5: Verificar Dados no Banco
1. **Abra:** http://localhost:8081 (Adminer)
2. **Conecte:**
   - **Server:** `postgres-data`
   - **Username:** `dataops`
   - **Password:** `dataops123`
   - **Database:** `datawarehouse`
3. **Execute queries:**
```sql
-- Ver tabelas criadas
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Ver dados de usuários
SELECT * FROM users LIMIT 10;

-- Ver dados de posts
SELECT * FROM posts LIMIT 10;

-- Ver métricas processadas
SELECT * FROM processed_metrics;
```

### Passo 6: Análise no Jupyter
1. **Abra:** http://localhost:8888
2. **Token:** `dataops123`
3. **Abra o notebook:** `data_analysis.ipynb`
4. **Execute as células** para ver análises

### Passo 7: Dashboards no Grafana
1. **Abra:** http://localhost:3000
2. **Login:** `admin` / `admin`
3. **Vá para:** Dashboards → Browse
4. **Veja métricas:** Sistema, Airflow, Pipeline

---

## 🔧 **COMANDOS ÚTEIS DURANTE EXECUÇÃO**

### Monitoramento Contínuo
```bash
# Ver logs específicos do Airflow (recomendado)
make logs-airflow

# Ver logs de todos os serviços
make logs

# Ver apenas logs do PostgreSQL
make logs-postgres

# Status dos containers
make status
```

### Controle do Pipeline
```bash
# Listar todas as DAGs
make list-dags

# Triggerar novamente o pipeline
make trigger-dag

# Reiniciar todos os serviços
make restart
```

---

## 📈 **INTERFACES DE MONITORAMENTO**

### Todas as URLs de Acesso:
| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Airflow** | http://localhost:8080 | admin/admin |
| **Jupyter** | http://localhost:8888 | token: dataops123 |
| **Grafana** | http://localhost:3000 | admin/admin |
| **Adminer** | http://localhost:8081 | dataops/dataops123 |
| **MinIO** | http://localhost:9001 | minioadmin/minioadmin123 |
| **Prometheus** | http://localhost:9090 | - |

### Comando Rápido para Abrir Tudo:
```bash
make monitor    # Abre Grafana, Prometheus e Airflow
make jupyter    # Abre Jupyter
```

---

## 🔄 **FLUXO COMPLETO DO PIPELINE**

### O que acontece quando você executa `make test-pipeline`:

1. **Extract (Extração)**
   - 📡 Busca dados da API JSONPlaceholder
   - 💾 Salva dados brutos em `/data/raw/`
   - 🗄️ Extrai dados do banco fonte

2. **Transform (Transformação)**
   - 🧹 Limpa e valida dados
   - 🔄 Aplica transformações de negócio
   - 📊 Calcula métricas agregadas
   - 💾 Salva dados processados em `/data/processed/`

3. **Load (Carregamento)**
   - 🗄️ Carrega dados no Data Warehouse
   - 📋 Atualiza tabelas de dimensão e fato
   - ✅ Valida integridade dos dados

### Arquivos Gerados:
```
data/
├── raw/
│   ├── users.csv
│   ├── posts.csv
│   └── weather.csv
├── processed/
│   ├── users_cleaned.csv
│   ├── posts_processed.csv
│   └── metrics.csv
└── warehouse/
    └── final_dataset.csv
```

---

## 🚨 **TROUBLESHOOTING**

### Problema: Serviços não iniciam
```bash
# Verificar portas em uso
netstat -tlnp | grep -E ':(8080|8888|3000|5432|6379)'

# Reiniciar tudo
make down
make up
```

### Problema: Pipeline falha
```bash
# Ver logs detalhados
make logs-airflow

# Verificar no Airflow UI
# http://localhost:8080 → DAGs → etl_pipeline → Clique na execução falhada
```

### Problema: Dados não aparecem
```bash
# Verificar conexões no Airflow UI
# Admin → Connections → Verificar postgres_default

# Testar conexão com banco
docker-compose exec postgres-data psql -U dataops -d datawarehouse -c "SELECT NOW();"
```

### Reset Completo:
```bash
make clean      # Remove tudo
make dev-setup  # Reconfigura ambiente
```

---

## 📊 **VALIDANDO O SUCESSO**

### ✅ Checklist de Validação:

#### 1. **Airflow UI**
- [ ] DAG `etl_pipeline` aparece na lista
- [ ] Execução mostra todas as tasks verdes
- [ ] Logs não mostram erros críticos

#### 2. **Banco de Dados**
- [ ] Tabelas `users`, `posts`, `weather` existem
- [ ] Dados foram inseridos (contagem > 0)
- [ ] Tabela `processed_metrics` tem métricas

#### 3. **Arquivos**
- [ ] Diretório `data/raw/` tem arquivos CSV
- [ ] Diretório `data/processed/` tem dados limpos
- [ ] Logs em `airflow/logs/` são gerados

#### 4. **Monitoramento**
- [ ] Grafana mostra métricas do sistema
- [ ] Prometheus coleta métricas
- [ ] Jupyter abre notebooks corretamente

### Comandos de Validação:
```bash
# 1. Verificar execução da DAG
make list-dags

# 2. Contar registros no banco
docker-compose exec postgres-data psql -U dataops -d datawarehouse -c "
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'posts' as table_name, COUNT(*) as count FROM posts;"

# 3. Verificar arquivos gerados
ls -la data/raw/
ls -la data/processed/

# 4. Status final
make status
```

---

## 🎯 **PRÓXIMOS PASSOS**

### Depois que tudo funcionar:
1. **Explore o Jupyter:** Faça análises dos dados
2. **Configure Alertas:** No Grafana, crie alertas personalizados
3. **Teste Falhas:** Simule erros para ver como o sistema reage
4. **Customize:** Modifique o pipeline para seus dados

### Para Produção:
```bash
make prod-setup  # Configuração otimizada para produção
```

---

## 📞 **SUPORTE**

### Em caso de problemas:
1. **Verificar logs:** `make logs-airflow`
2. **Status dos serviços:** `make status`
3. **Reset completo:** `make clean && make dev-setup`
4. **Documentação:** Consulte `CLAUDE.md` e `class.md`

### Comandos de Diagnóstico:
```bash
docker ps -a              # Todos os containers
docker system df          # Uso de espaço
docker-compose logs -f    # Logs detalhados
```

**🎉 Sucesso!** Agora você tem um pipeline DataOps completo funcionando!