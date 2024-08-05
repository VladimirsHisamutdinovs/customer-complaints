CREATE DATABASE timeseries_db;

\c timeseries_db

CREATE EXTENSION IF NOT EXISTS timescaledb;

CREATE TABLE timeseries_data (
    time TIMESTAMPTZ NOT NULL,
    network_load DOUBLE PRECISION,
    throughput DOUBLE PRECISION,
    latency DOUBLE PRECISION,
    user_count INTEGER,
    PRIMARY KEY (time)
);

SELECT create_hypertable('timeseries_data', 'time');

CREATE TABLE predictions (
    time TIMESTAMPTZ NOT NULL,
    network_load DOUBLE PRECISION,
    throughput DOUBLE PRECISION,
    latency DOUBLE PRECISION,
    user_count INTEGER,
    PRIMARY KEY (time)
);
