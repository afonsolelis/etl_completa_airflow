-- Inicialização do banco de dados
-- Este script cria a database dataops caso ela não exista

-- Conectar ao banco padrão postgres para criar a database
SELECT 'CREATE DATABASE dataops'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'dataops')\gexec

-- Criar usuário se não existir
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'dataops_user') THEN

      CREATE ROLE dataops_user LOGIN PASSWORD 'dataops123';
   END IF;
END
$do$;

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE dataops TO dataops_user;
GRANT ALL PRIVILEGES ON DATABASE datawarehouse TO dataops;