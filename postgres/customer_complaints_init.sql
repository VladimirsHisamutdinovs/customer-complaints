CREATE EXTENSION IF NOT EXISTS dblink;

DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 
        FROM pg_database 
        WHERE datname = 'customer_complaints_db'
    ) THEN
        PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE customer_complaints_db');
    END IF;
END $$;

\c customer_complaints_db

CREATE TABLE IF NOT EXISTS customer_complaints (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    location VARCHAR(50),
    complaint_reason VARCHAR(50),
    time_received TIMESTAMP,
    status VARCHAR(20)
);
