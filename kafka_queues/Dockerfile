# kafka_queues/Dockerfile
FROM python:3.10.12-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x wait-for-it.sh
ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["./wait-for-it.sh", "kafka:9092", "--timeout=180","python", "kafka_consumer.py", "kafka_consumer.py"]  