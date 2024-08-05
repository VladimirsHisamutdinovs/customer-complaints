CREATE DATABASE customer_complaints_db;

\c customer_complaints_db

CREATE TABLE customer_complaints (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    location VARCHAR(50),
    complaint_reason VARCHAR(50),
    time_received TIMESTAMP,
    status VARCHAR(20)
);
