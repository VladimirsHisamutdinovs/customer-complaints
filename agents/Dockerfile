FROM python:3.9

# Install required packages
RUN pip install ollama kafka-python neo4j psycopg2

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Run the application
CMD ["python", "main.py"]
