-- 1. Banco para a etapa de Extração (Dados Crus)
CREATE DATABASE IF NOT EXISTS datasus_raw;
USE datasus_raw;

CREATE TABLE IF NOT EXISTS raw_sim (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conteudo_linha TEXT,
    data_carga TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Banco para o Data Warehouse (Dados Transformados)
CREATE DATABASE IF NOT EXISTS datasus_dw;
USE datasus_dw;

-- Tabela Dimensão: Tempo
CREATE TABLE IF NOT EXISTS dim_tempo (
    id_tempo INT PRIMARY KEY,
    ano INT,
    mes INT,
    dia INT
);

-- Tabela Dimensão: Localidade (Municípios)
CREATE TABLE IF NOT EXISTS dim_localidade (
    id_municipio INT PRIMARY KEY,
    nome_municipio VARCHAR(100),
    estado VARCHAR(2)
);

-- Tabela Fato: Mortalidade (SIM) ou Internações (SIH)
CREATE TABLE IF NOT EXISTS fato_saude_publica (
    id_fato INT AUTO_INCREMENT PRIMARY KEY,
    id_tempo INT,
    id_municipio INT,
    cid_causa VARCHAR(10),
    quantidade INT,
    FOREIGN KEY (id_tempo) REFERENCES dim_tempo(id_tempo),
    FOREIGN KEY (id_municipio) REFERENCES dim_localidade(id_municipio)
);
