"""
Neo4j Client module to handle interactions with the Neo4j database.
"""
from neo4j import GraphDatabase

class Neo4jClient:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def store_complaint(self, complaint):
        with self.driver.session() as session:
            print("Storing complaint:", complaint) 
            session.run(
                "CREATE (c:Complaint {customer_id: $customer_id, location: $location, text: $text})",
                customer_id=complaint["customer_id"],
                location=complaint["location"],
                text=complaint["complaint_text"]
            )

