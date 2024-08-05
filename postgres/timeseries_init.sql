CREATE EXTENSION IF NOT EXISTS dblink;

DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 
        FROM pg_database 
        WHERE datname = 'timeseries_db'
    ) THEN
        PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE timeseries_db');
    END IF;
END $$;

\c timeseries_db

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE IF NOT EXISTS timeseries_data (
    time TIMESTAMPTZ NOT NULL,
    network_load DOUBLE PRECISION,
    throughput DOUBLE PRECISION,
    latency DOUBLE PRECISION,
    user_count INTEGER,
    PRIMARY KEY (time)
);

SELECT create_hypertable('timeseries_data', 'time');

CREATE TABLE IF NOT EXISTS predictions (
    time TIMESTAMPTZ NOT NULL,
    network_load DOUBLE PRECISION,
    throughput DOUBLE PRECISION,
    latency DOUBLE PRECISION,
    user_count INTEGER,
    PRIMARY KEY (time)
);
