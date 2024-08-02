CREATE TABLE technical_complaints (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    location VARCHAR(50),
    complaint_reason VARCHAR(50),
    time_received TIMESTAMP,
    status VARCHAR(20)
);

CREATE TABLE financial_complaints (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50),
    location VARCHAR(50),
    complaint_reason VARCHAR(50),
    time_received TIMESTAMP,
    status VARCHAR(20)
);
