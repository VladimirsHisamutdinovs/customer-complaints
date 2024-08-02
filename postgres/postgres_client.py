"""
PostgreSQL Client module to handle interactions with the PostgreSQL database.
"""
import psycopg2
from datetime import datetime

class PostgresClient:
    def __init__(self, dbname, user, password, host):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)

    def close(self):
        self.conn.close()

    def _store_complaint(self, table, complaint, complaint_reason):
        cur = self.conn.cursor()
        cur.execute(
            f"INSERT INTO {table} (customer_id, location, complaint_reason, time_received, status) VALUES (%s, %s, %s, %s, %s)",
            (complaint["customer_id"], complaint["location"], complaint_reason, datetime.now(), 'received')
        )
        self.conn.commit()
        cur.close()

    def store_technical_complaint(self, complaint):
        self._store_complaint('technical_complaints', complaint, 'technical')

    def store_financial_complaint(self, complaint):
        self._store_complaint('financial_complaints', complaint, 'financial')
