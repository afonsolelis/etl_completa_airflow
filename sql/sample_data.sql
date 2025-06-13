-- Inserção de dados de exemplo

-- Inserir clientes
INSERT INTO customers (customer_name, email, phone, address, city, country, registration_date, last_purchase_date, total_purchases) VALUES
('João Silva', 'joao.silva@email.com', '11999999999', 'Rua das Flores, 123', 'São Paulo', 'BR', '2023-01-15', '2024-12-01', 5),
('Maria Santos', 'maria.santos@email.com', '11888888888', 'Av. Paulista, 456', 'São Paulo', 'BR', '2023-02-20', '2024-11-28', 8),
('Pedro Oliveira', 'pedro.oliveira@email.com', '21777777777', 'Rua Copacabana, 789', 'Rio de Janeiro', 'BR', '2023-03-10', '2024-12-02', 3),
('Ana Costa', 'ana.costa@email.com', '31666666666', 'Rua da Liberdade, 321', 'Belo Horizonte', 'BR', '2023-04-05', '2024-11-30', 12),
('Carlos Ferreira', 'carlos.ferreira@email.com', '41555555555', 'Av. Beira Mar, 654', 'Curitiba', 'BR', '2023-05-12', '2024-12-01', 6),
('Luciana Rodrigues', 'luciana.rodrigues@email.com', '51444444444', 'Rua Gaúcha, 987', 'Porto Alegre', 'BR', '2023-06-18', '2024-11-29', 9),
('Roberto Lima', 'roberto.lima@email.com', '85333333333', 'Av. Beira Mar, 147', 'Fortaleza', 'BR', '2023-07-22', '2024-12-02', 4),
('Fernanda Alves', 'fernanda.alves@email.com', '62222222222', 'Rua Central, 258', 'Goiânia', 'BR', '2023-08-30', '2024-11-27', 7),
('Marcos Pereira', 'marcos.pereira@email.com', '11111111111', 'Rua Augusta, 369', 'São Paulo', 'BR', '2023-09-14', '2024-12-01', 11),
('Patrícia Souza', 'patricia.souza@email.com', '47999999999', 'Av. Atlântica, 741', 'Florianópolis', 'BR', '2023-10-25', '2024-11-30', 5);

-- Inserir produtos
INSERT INTO products (product_name, category, brand, unit_price, cost_price, stock_quantity) VALUES
('Smartphone Galaxy S24', 'Eletrônicos', 'Samsung', 1299.99, 800.00, 50),
('iPhone 15 Pro', 'Eletrônicos', 'Apple', 1899.99, 1200.00, 30),
('Notebook Dell Inspiron', 'Informática', 'Dell', 2499.99, 1800.00, 25),
('Smart TV 55"', 'Eletrônicos', 'LG', 1799.99, 1200.00, 40),
('Fone Bluetooth', 'Acessórios', 'Sony', 299.99, 150.00, 100),
('Tablet iPad Air', 'Eletrônicos', 'Apple', 999.99, 700.00, 35),
('Mouse Gamer', 'Informática', 'Logitech', 199.99, 80.00, 80),
('Teclado Mecânico', 'Informática', 'Corsair', 399.99, 200.00, 60),
('Monitor 27"', 'Informática', 'ASUS', 899.99, 600.00, 45),
('Câmera Digital', 'Eletrônicos', 'Canon', 1599.99, 1000.00, 20),
('Smartwatch', 'Acessórios', 'Garmin', 799.99, 400.00, 55),
('Caixa de Som', 'Áudio', 'JBL', 399.99, 200.00, 70),
('Carregador Portátil', 'Acessórios', 'Anker', 149.99, 60.00, 120),
('Webcam HD', 'Informática', 'Logitech', 249.99, 120.00, 90),
('SSD 1TB', 'Informática', 'Kingston', 499.99, 300.00, 65);

-- Inserir vendas (últimos 30 dias)
INSERT INTO sales (customer_id, product_id, quantity, unit_price, total_amount, sale_date) VALUES
-- Vendas de João Silva
(1, 1, 1, 1299.99, 1299.99, '2024-11-15 10:30:00'),
(1, 5, 2, 299.99, 599.98, '2024-11-20 14:15:00'),
(1, 13, 1, 149.99, 149.99, '2024-12-01 09:45:00'),

-- Vendas de Maria Santos
(2, 2, 1, 1899.99, 1899.99, '2024-11-18 16:20:00'),
(2, 6, 1, 999.99, 999.99, '2024-11-25 11:30:00'),
(2, 8, 1, 399.99, 399.99, '2024-11-28 13:45:00'),

-- Vendas de Pedro Oliveira
(3, 3, 1, 2499.99, 2499.99, '2024-11-22 15:10:00'),
(3, 9, 1, 899.99, 899.99, '2024-12-02 10:20:00'),

-- Vendas de Ana Costa
(4, 4, 1, 1799.99, 1799.99, '2024-11-19 12:00:00'),
(4, 7, 2, 199.99, 399.98, '2024-11-26 14:30:00'),
(4, 12, 1, 399.99, 399.99, '2024-11-30 16:45:00'),

-- Vendas de Carlos Ferreira
(5, 10, 1, 1599.99, 1599.99, '2024-11-21 09:15:00'),
(5, 11, 1, 799.99, 799.99, '2024-12-01 11:20:00'),

-- Vendas de Luciana Rodrigues
(6, 1, 1, 1299.99, 1299.99, '2024-11-17 13:25:00'),
(6, 14, 1, 249.99, 249.99, '2024-11-24 15:40:00'),
(6, 15, 1, 499.99, 499.99, '2024-11-29 10:55:00'),

-- Vendas de Roberto Lima
(7, 5, 1, 299.99, 299.99, '2024-11-23 14:10:00'),
(7, 12, 1, 399.99, 399.99, '2024-12-02 16:30:00'),

-- Vendas de Fernanda Alves
(8, 6, 1, 999.99, 999.99, '2024-11-16 11:45:00'),
(8, 8, 1, 399.99, 399.99, '2024-11-27 13:20:00'),

-- Vendas de Marcos Pereira
(9, 2, 1, 1899.99, 1899.99, '2024-11-20 15:30:00'),
(9, 7, 1, 199.99, 199.99, '2024-11-28 09:40:00'),
(9, 13, 2, 149.99, 299.98, '2024-12-01 12:15:00'),

-- Vendas de Patrícia Souza
(10, 3, 1, 2499.99, 2499.99, '2024-11-19 10:25:00'),
(10, 9, 1, 899.99, 899.99, '2024-11-30 14:50:00');

-- Atualizar last_purchase_date dos clientes
UPDATE customers SET last_purchase_date = (
    SELECT MAX(sale_date)::date 
    FROM sales 
    WHERE sales.customer_id = customers.customer_id
);

-- Atualizar total_purchases dos clientes
UPDATE customers SET total_purchases = (
    SELECT COUNT(*) 
    FROM sales 
    WHERE sales.customer_id = customers.customer_id
);