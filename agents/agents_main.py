from customer_agent import CustomerAgent
from customer_support_agent import CustomerSupportAgent

def main():
    kafka_bootstrap_servers = 'kafka:9092'  # Use service name as per docker-compose
    neo4j_config = {
        "uri": "bolt://neo4j:7687",
        "user": "neo4j",
        "password": "password"
    }
    postgres_config = {
        "dbname": "complaints_db",
        "user": "user",
        "password": "password",
        "host": "postgres"
    }

    complaint_generator = CustomerAgent(kafka_bootstrap_servers)
    support_agent = CustomerSupportAgent(kafka_bootstrap_servers, neo4j_config, postgres_config)

    # Running agents in separate threads for simplicity
    import threading
    generator_thread = threading.Thread(target=complaint_generator.run)
    support_agent_thread = threading.Thread(target=support_agent.run)

    generator_thread.start()
    support_agent_thread.start()

    generator_thread.join()
    support_agent_thread.join()

if __name__ == "__main__":
    main()
