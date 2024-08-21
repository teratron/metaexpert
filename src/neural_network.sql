-- Database: neuralnetwork

CREATE DATABASE neuralnetwork
    WITH
    OWNER = postgres
    ENCODING = 'UTF8';

-- Table: network

-- CREATE TABLE IF NOT EXISTS network
-- (
--     symbol character varying(16) NOT NULL,
--     value  real NOT NULL DEFAULT 0.0,
--     CONSTRAINT price_pkey PRIMARY KEY (symbol)
-- );

-- Table: cell

CREATE TABLE IF NOT EXISTS cell
(
    value  real NOT NULL DEFAULT 0.0,
    missing real NOT NULL DEFAULT 0.0
);