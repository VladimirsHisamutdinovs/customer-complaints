FROM python:3.10.12-bullseye

RUN pip install ollama kafka-python neo4j psycopg2

COPY scripts/wait-for-it.sh /wait-for-it.sh
COPY . /app

WORKDIR /app

ENV PYTHONPATH=/app

RUN chmod +x /wait-for-it.sh

ENTRYPOINT ["/wait-for-it.sh", "kafka:9092", "--timeout=180", "--", "python", "agents/agents_main.py"]
