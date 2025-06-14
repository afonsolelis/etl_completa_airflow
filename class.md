# ROTEIRO DE AULA: DataOps e DevOps - Pipeline Completo com Observabilidade

## **MÓDULO 1: Conceitos Fundamentais (30 min)**

### 1.1 DevOps vs DataOps
**DevOps**: Cultura e práticas que unificam desenvolvimento e operações
- **Objetivo**: Acelerar entrega de software com qualidade
- **Foco**: Aplicações, código, infraestrutura

**DataOps**: Extensão do DevOps para dados
- **Objetivo**: Acelerar entrega de dados confiáveis e insights de valor
- **Foco**: Pipelines de dados, qualidade, governança

### 1.2 Business Drive e Qualidade - ISO 27001
**ISO 27001** como framework para DataOps:
- **Governança de Dados**: Controles de segurança e acesso
- **Gestão de Riscos**: Avaliação contínua de dados sensíveis
- **Conformidade**: Atendimento a regulamentações (LGPD, GDPR)
- **Melhoria Contínua**: Auditorias e revisões regulares

**Business Drive**:
- Dados como ativo estratégico
- Decisões baseadas em dados (Data-Driven)
- ROI mensurável em projetos de dados

---

## **MÓDULO 2: Arquitetura do Pipeline DataOps (45 min)**

### 2.1 Visão Geral da Arquitetura
```
APIs/Fontes → Extract → Transform → Load → Warehouse → Analytics
     ↓           ↓         ↓         ↓        ↓         ↓
  Monitoramento ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### 2.2 Ferramentas e Suas Funções

#### **Apache Airflow** - Orquestração
- **Função**: Scheduler e executor de workflows
- **DataOps**: Automatização, versionamento de DAGs
- **Observabilidade**: UI visual, logs detalhados, alertas
- **Business Value**: Redução de erros manuais, consistência

#### **PostgreSQL** - Armazenamento
- **Função**: Data Warehouse e metadados do Airflow
- **DataOps**: ACID compliance, backup/restore
- **Observabilidade**: Query performance, conexões ativas
- **Business Value**: Dados íntegros, histórico confiável

#### **Redis** - Cache e Messaging
- **Função**: Cache de resultados, broker de mensagens
- **DataOps**: Performance, desacoplamento de sistemas
- **Observabilidade**: Métricas de hit/miss, latência
- **Business Value**: Respostas mais rápidas, escalabilidade

#### **MinIO** - Object Storage
- **Função**: Armazenamento de arquivos grandes (S3 compatible)
- **DataOps**: Versionamento de datasets, backup distribuído
- **Observabilidade**: Storage utilizado, operações I/O
- **Business Value**: Custos reduzidos vs cloud, controle total

#### **Prometheus** - Métricas
- **Função**: Coleta e armazenamento de métricas
- **DataOps**: Alertas proativos, SLAs de dados
- **Observabilidade**: Séries temporais, alerting
- **Business Value**: Prevenção de problemas, uptime

#### **Grafana** - Visualização
- **Função**: Dashboards e alertas visuais
- **DataOps**: Monitoramento em tempo real
- **Observabilidade**: Painéis customizáveis, relatórios
- **Business Value**: Visibilidade executiva, tomada de decisão

#### **Jupyter** - Exploração
- **Função**: Análise exploratória e prototipagem
- **DataOps**: Data science colaborativo, documentação
- **Observabilidade**: Notebooks versionados
- **Business Value**: Insights rápidos, experimentação

---

## **MÓDULO 3: Observabilidade e Mantenabilidade (40 min)**

### 3.1 Os 3 Pilares da Observabilidade

#### **Logs** (Airflow + Aplicações)
```bash
make logs-airflow    # Logs específicos do Airflow
make logs           # Logs de todos os serviços
```
- **DataOps**: Rastreabilidade de transformações
- **Business**: Auditoria e compliance

#### **Métricas** (Prometheus + Grafana)
- **Infraestrutura**: CPU, RAM, Disk, Network
- **Aplicação**: Task success rate, duration, throughput
- **Negócio**: Data quality, SLA compliance

#### **Traces** (Distributed Tracing)
- **Pipeline**: Tempo de execução end-to-end
- **Dependencies**: Mapeamento de dependências

### 3.2 Estratégias de Mantenabilidade

#### **Health Checks Automatizados**
```bash
make check-health    # Verifica saúde dos serviços
make status         # Status dos containers
```

#### **Testes Automatizados**
```bash
make test-pipeline   # Testa o pipeline completo
```

#### **Backup e Recovery**
```bash
make backup-data     # Backup automático com timestamp
```

#### **Deployment Seguro**
- **Blue-Green**: Zero downtime
- **Canary**: Rollout gradual
- **Rollback**: Reversão rápida

---

## **MÓDULO 4: Business Drive e ROI (25 min)**

### 4.1 Métricas de Negócio

#### **Operational Excellence**
- **MTTR** (Mean Time to Recovery): < 15 min
- **MTBF** (Mean Time Between Failures): > 30 dias
- **Data Quality Score**: > 95%
- **SLA Compliance**: > 99.5%

#### **Business Impact**
- **Tempo de Insight**: De semanas para horas
- **Confiabilidade de Dados**: Redução de 90% em erros
- **Custo Operacional**: Redução de 60% com automação
- **Time-to-Market**: Aceleração de 80% em novos produtos

### 4.2 Governança ISO 27001

#### **Controles de Segurança**
- **A.12.6.1**: Gestão de vulnerabilidades técnicas
- **A.18.1.4**: Proteção de dados e privacidade

#### **Gestão de Riscos**
- **Asset Inventory**: Catalogação de dados sensíveis
- **Risk Assessment**: Avaliação contínua
- **Incident Response**: Plano de resposta a incidentes

#### **Auditoria e Compliance**
- **Logs Imutáveis**: Trilha de auditoria completa
- **Access Control**: Princípio do menor privilégio
- **Data Lineage**: Rastreabilidade completa

---

## **MÓDULO 5: Hands-On Demo (30 min)**

### 5.1 Execução do Pipeline
```bash
make dev-setup      # Configuração inicial
make up            # Inicia todos os serviços
make trigger-dag   # Executa pipeline ETL
```

### 5.2 Monitoramento em Tempo Real
- **Airflow UI**: http://localhost:8080 (admin/admin)
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Jupyter**: http://localhost:8888 (token: dataops123)
- **Adminer**: http://localhost:8081
- **MinIO**: http://localhost:9001 (minioadmin/minioadmin123)

### 5.3 Análise de Resultados
- **Jupyter**: Análise exploratória dos dados
- **Database**: Verificação dos dados carregados no warehouse
- **Grafana**: Dashboards de monitoramento

---

## **EXERCÍCIOS PRÁTICOS**

### Exercício 1: Configuração do Ambiente
1. Clone o repositório do projeto
2. Execute `make dev-setup` para configuração inicial
3. Inicie os serviços com `make up`
4. Verifique o status com `make status`

### Exercício 2: Execução do Pipeline
1. Acesse o Airflow UI em http://localhost:8080
2. Execute a DAG `etl_pipeline` manualmente
3. Monitore a execução através dos logs
4. Verifique os dados no PostgreSQL via Adminer

### Exercício 3: Monitoramento e Alertas
1. Configure um dashboard no Grafana
2. Crie alertas para falhas no pipeline
3. Simule uma falha e observe os alertas
4. Analise as métricas no Prometheus

### Exercício 4: Análise de Dados
1. Abra o Jupyter Notebook
2. Carregue os dados processados
3. Crie visualizações dos dados
4. Documente insights encontrados

---

## **CHECKLIST DE QUALIDADE ISO 27001**

### Controles de Segurança Implementados
- [ ] **A.9.1.1**: Política de controle de acesso
- [ ] **A.9.2.1**: Registro e cancelamento de usuários
- [ ] **A.12.1.2**: Controle de software malicioso
- [ ] **A.12.3.1**: Backup de informações
- [ ] **A.12.4.1**: Registro de eventos (logging)
- [ ] **A.12.6.1**: Gestão de vulnerabilidades técnicas
- [ ] **A.18.1.4**: Proteção de dados e privacidade

### Métricas de Compliance
- [ ] Backup automatizado diário: ✅
- [ ] Logs imutáveis por 1 ano: ✅
- [ ] Controle de acesso por RBAC: ✅
- [ ] Criptografia em trânsito: ✅
- [ ] Monitoramento 24/7: ✅
- [ ] Plano de resposta a incidentes: ✅

---

## **GLOSSÁRIO**

**DataOps**: Metodologia colaborativa focada na melhoria da comunicação, integração e automação dos fluxos de dados entre gestores de dados e consumidores de dados.

**ETL**: Extract, Transform, Load - processo de extração, transformação e carregamento de dados.

**SLA**: Service Level Agreement - acordo de nível de serviço que define métricas de qualidade.

**MTTR**: Mean Time to Recovery - tempo médio para recuperação após uma falha.

**MTBF**: Mean Time Between Failures - tempo médio entre falhas.

**Data Lineage**: Rastreabilidade completa dos dados desde a origem até o destino.

**RBAC**: Role-Based Access Control - controle de acesso baseado em funções.

---

## **RECURSOS ADICIONAIS**

### Documentação Oficial
- [Apache Airflow](https://airflow.apache.org/docs/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)
- [ISO 27001](https://www.iso.org/isoiec-27001-information-security.html)

### Ferramentas de Apoio
- [DataOps Manifesto](https://www.dataopsmanifesto.org/)
- [Twelve-Factor App](https://12factor.net/)
- [Site Reliability Engineering](https://sre.google/)

### Certificações Recomendadas
- **AWS Certified Data Analytics**
- **Google Cloud Professional Data Engineer**
- **Microsoft Azure Data Engineer Associate**
- **Certified Information Security Manager (CISM)**

---

## **CONCLUSÃO E PRÓXIMOS PASSOS**

### Principais Takeaways:
1. **DataOps ≠ DevOps**: Foco específico em dados e qualidade
2. **Observabilidade**: Essencial para pipelines confiáveis
3. **Business Drive**: Dados como vantagem competitiva
4. **ISO 27001**: Framework de governança e segurança
5. **Automação**: Chave para escalabilidade e redução de custos

### Implementação em Produção:
1. **Segurança**: Alterar credenciais padrão
2. **Monitoramento**: Configurar alertas proativos
3. **Backup**: Estratégia de disaster recovery
4. **Documentação**: Manter atualizada e versionada
5. **Treinamento**: Capacitar equipe em DataOps

### Próximos Passos:
- [ ] Implementar CI/CD para DAGs
- [ ] Expandir testes automatizados
- [ ] Configurar monitoramento avançado
- [ ] Documentar procedimentos operacionais
- [ ] Planejar certificação ISO 27001

---

**Instrutor**: [Nome do Instrutor]  
**Data**: [Data da Aula]  
**Duração**: 3 horas  
**Pré-requisitos**: Docker, conhecimentos básicos de SQL e Python