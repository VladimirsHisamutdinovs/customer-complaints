FROM python:3.10.12-bullseye

WORKDIR /app/postgres

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "postgres_client.py"]
