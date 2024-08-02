# customer_support/Dockerfile
FROM python:3.10.12-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Assuming additional installation steps for ollama (e.g., curl) if necessary
RUN apt-get update && apt-get install -y curl

COPY . .
RUN chmod +x wait-for-it.sh

ENV PYTHONPATH="${PYTHONPATH}:/app"

ENTRYPOINT ["./wait-for-it.sh", "kafka:9092", "--timeout=180", "--", "python", "customer_support_agent.py"]
